import pandas as pd
import threading
import backend.scripts.data_scrape.path_finding_functions as path_functions
from backend.scripts.df_utils.data_frame_utilities import replace_all_nan


def load_sheet_to_dataframe(sheet_name, title):
    try:
        symbols_file_name = path_functions.get_symbols_file_path(title)
    except:
        exit("No symbols file found.")
    sheet_dataframe = pd.read_excel(symbols_file_name, sheet_name=sheet_name)
    return sheet_dataframe


def get_company_daily_data(filtered_web_page, symbol):
    company_data_row = ['nan'] * 6
    for i in range(len(filtered_web_page)):
        if filtered_web_page[i].get_text() == symbol:

            high = filtered_web_page[i + 2].get_text()
            low = filtered_web_page[i + 3].get_text()
            close = filtered_web_page[i + 4].get_text()
            volume = filtered_web_page[i + 5].get_text()
            value_change = filtered_web_page[i + 6].get_text()
            percent_change = filtered_web_page[i + 8].get_text()

            try:
                percent_change = str(float(percent_change) * float(value_change)/abs(float(value_change)))
            except:
                pass

            company_data_row = [high, low, close, volume, value_change, percent_change]
            break

    return company_data_row


def build_data_frame_from_rows(list_of_daily_data_rows):
    columns = []
    for row_element in range(len(list_of_daily_data_rows[0])):
        new_column = []
        for column_element in range(len(list_of_daily_data_rows)):
            new_column.append(list_of_daily_data_rows[column_element][row_element])

        columns.append(new_column)

    new_page_data_dict = {}
    headers = ["High", "Low", "Close", "Volume", "Value-Change", "Percent-Change"]
    for i in range(len(headers)):
        new_page_data_dict[headers[i]] = columns[i]

    page_data_frame = pd.DataFrame(new_page_data_dict)
    return page_data_frame


class ReadPartialDailyData(threading.Thread):
    def __init__(self, sheet_name, target_url, closing_url, title):
        threading.Thread.__init__(self)
        self.sheet_name = sheet_name
        self.closing_url = closing_url
        self.target_url = target_url
        self.title = title
        self.loaded_partial_frame_list = []

    def run(self):
        partial_daily_data_frames_list = []

        full_url = self.target_url + self.sheet_name + self.closing_url
        page = path_functions.use_requests_get(full_url)
        first_filter = page.find_all("table", class_="quotes")
        second_filter = first_filter[0].find_all("td")

        sheet_dataframe = load_sheet_to_dataframe(self.sheet_name, self.title)
        daily_data_rows = []
        for symbol in sheet_dataframe['Symbol']:
            daily_company_data_row = get_company_daily_data(second_filter, symbol)
            daily_data_rows.append(daily_company_data_row)

        new_daily_letter_frame = build_data_frame_from_rows(daily_data_rows)
        add_to_sheet_dataframe = sheet_dataframe.join(new_daily_letter_frame, how='outer')
        remove_redundant_column_dataframe = add_to_sheet_dataframe.drop(columns=["Unnamed: 0"])
        replaced_nan_dataframe = replace_all_nan(remove_redundant_column_dataframe)

        partial_daily_data_frames_list.append(replaced_nan_dataframe)

        self.loaded_partial_frame_list = partial_daily_data_frames_list


def read_daily_data(target_url, title, sheet_letter_list):

    closing_url = ".htm"

    page_read_classes = []
    for letter in sheet_letter_list:
        page = ReadPartialDailyData(letter, target_url, closing_url, title)
        page_read_classes.append(page)

    # threading:
    for read_class in page_read_classes:
        read_class.start()

    for read_class in page_read_classes:
        read_class.join()

    daily_data_frames_list = []
    for read_class in page_read_classes:
        daily_data_frames_list.extend(read_class.loaded_partial_frame_list)

    return daily_data_frames_list


def write_daily_data_to_excel(today_site_data_list, site_title, sheet_letter_list):
    file_path = path_functions.set_daily_data_file_name(site_title)

    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    for i in range(len(sheet_letter_list)):
        sheet_dataframe = today_site_data_list[i]
        sheet_dataframe.to_excel(writer, sheet_name=sheet_letter_list[i], index=False)
    writer.save()


def create_daily_data(section_root_list_url, site_title, sheet_letter_list):
    today_site_data_list = read_daily_data(section_root_list_url, site_title, sheet_letter_list)
    write_daily_data_to_excel(today_site_data_list, site_title, sheet_letter_list)

