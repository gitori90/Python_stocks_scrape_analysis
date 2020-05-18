import pandas as pd
import re
import threading
import backend.scripts.data_scrape.path_finding_functions as path_functions

DEFAULT_NAN = 'nan'


def get_symbols(page):
    symbols_list = []
    symbol_filter = page.find_all("a", {'title': re.compile(r'^Display Quote & Chart')})
    for matched in symbol_filter:
        symbols_list.append(matched.get_text())
    return symbols_list


def fix_sector_name_error(sector_name):
    if sector_name == 'Healthcare':
        sector_name = 'Health Care'

    return sector_name


def get_name_and_sector_and_industry(root_url, symbols_list):
    company_names_list = []
    sector_names_list = []
    industry_names_list = []

    for company_symbol in symbols_list:
        company_url = root_url + company_symbol.upper() + ".htm"
        company_url = company_url.replace("stocklist", "stockquote")
        page = path_functions.use_requests_get(company_url)
        sector = DEFAULT_NAN
        industry = DEFAULT_NAN
        first_filter = page.find_all("div", class_="cb")
        x = page.find_all("title")[0].get_text()
        name = x[x.find("[") + 1: x.find("]")]
        company_names_list.append(name)

        for i in range(len(first_filter)):
            temp_filter = first_filter[i].find_all("td")
            try:
                if temp_filter[0].get_text() == "Sector:":

                    sector = temp_filter[1].get_text()
                    sector = fix_sector_name_error(sector)

                    industry = temp_filter[3].get_text()
                    break
            except:
                pass

        sector_names_list.append(sector)
        industry_names_list.append(industry)
    return company_names_list, sector_names_list, industry_names_list


def scrape_data_from_url(full_url_of_letter, root_url):

    web_page = path_functions.use_requests_get(full_url_of_letter)

    symbols_list = get_symbols(web_page)
    name_of_symbols, sector_of_symbols, industry_of_symbols = get_name_and_sector_and_industry(root_url, symbols_list)

    return symbols_list, name_of_symbols, sector_of_symbols, industry_of_symbols


class ReadPartialSymbolsData(threading.Thread):
    def __init__(self, letter, section_root_list_url, closing_url):
        threading.Thread.__init__(self)
        self.letter = letter
        self.closing_url = closing_url
        self.section_root_list_url = section_root_list_url
        self.loaded_partial_frame_list = []

        self.next_symbol_list = 0
        self.next_names_list = 0
        self.next_sector_list = 0
        self.next_industry_list = 0

    def run(self):
        full_url_of_letter = self.section_root_list_url + self.letter + self.closing_url
        self.next_symbol_list, self.next_names_list, self.next_sector_list, self.next_industry_list = \
            scrape_data_from_url(full_url_of_letter, self.section_root_list_url)
        print("finished reading letter ", self.letter)


# the main function:
def symbols_and_names_to_excel(section_root_list_url, exchange_title, letter_list):

    closing_url = ".htm"
    all_symbols = []
    corresponding_names = []
    corresponding_sectors = []
    corresponding_industry = []

    page_read_classes = []
    for letter in letter_list:
        page = ReadPartialSymbolsData(letter, section_root_list_url, closing_url)
        page_read_classes.append(page)

    # threading:
    for read_class in page_read_classes:
        read_class.start()

    for read_class in page_read_classes:
        read_class.join()

    for read_class in page_read_classes:
        all_symbols.append(read_class.next_symbol_list)
        corresponding_names.append(read_class.next_names_list)
        corresponding_sectors.append(read_class.next_sector_list)
        corresponding_industry.append(read_class.next_industry_list)

    data_file_name = path_functions.set_symbols_file_name(exchange_title)

    writer = pd.ExcelWriter(data_file_name, engine='xlsxwriter')
    for letter_index in range(len(all_symbols)):
        data_dict = {"Symbol": all_symbols[letter_index],
                     "Name": corresponding_names[letter_index],
                     "Sector": corresponding_sectors[letter_index],
                     "Industry": corresponding_industry[letter_index]}

        symbols_sheet_dataframe = pd.DataFrame(data_dict)

        symbols_sheet_dataframe.to_excel(writer, sheet_name=letter_list[letter_index])
    writer.save()
