import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
from collections import Counter
from datetime import date
import threading
import re

LETTERS_LIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def all_exchanges_dataframes():
    exchange_names = stocks_API.viable_exchange_names()
    all_dataframe = pd.DataFrame()
    for exchange in exchange_names:
        exchange_dataframe = stocks_API.AllDataAnalysisToday(exchange).all_daily_dataframe
        all_dataframe = all_dataframe.append(exchange_dataframe)

    return all_dataframe


def remove_all_nonalphabetic_from_string(str):
    regex = re.compile('[^a-zA-Z]')
    clean_str = regex.sub('', str)
    return clean_str


def name_to_alphabetic_words_list(company_name):
    alphabet_words_list = []
    replace_a_char = company_name.replace(".", " ")
    space_split = replace_a_char.split()
    for word in space_split:
        cleaned_word = remove_all_nonalphabetic_from_string(word)
        alphabet_words_list.append(cleaned_word)

    return alphabet_words_list


def all_words_in_company_names_dataframe_counter(companies_dataframe):
    all_words = []
    name_list = companies_dataframe['Name'].tolist()

    for company_name in name_list:
        try:
            words_in_company = name_to_alphabetic_words_list(company_name)
            for i in range(len(words_in_company)):
                try:
                    words_in_company.remove('')
                except ValueError:
                    break
            all_words.extend(words_in_company)
        except TypeError:
            continue
        except AttributeError:
            continue

    counts = Counter(all_words)
    return counts


def top_x_in_count_dictionary(counter_dict, top_number):
    sorted_dict = sorted(counter_dict, key=counter_dict.get, reverse=True)
    top_dict = {}
    for i in range(top_number):
        key = sorted_dict[i]
        top_dict[key] = counter_dict[key]

    return top_dict


def top_x_words_in_dataframe_dict(dataframe, top_number):
    count_dict = all_words_in_company_names_dataframe_counter(dataframe)
    top_dict = top_x_in_count_dictionary(count_dict, top_number)
    return top_dict


def analyse_method_on_all_dataframes_partial_name(partial_name, method_name, column_name):
    all_frames = all_exchanges_dataframes()

    filtered_companies_dataframe = stocks_analysis.\
        filter_companies_dataframe_by_partial_name(all_frames, partial_name)

    method_result = stocks_analysis.\
        pandas_analysis_functions_dict(method_name, filtered_companies_dataframe, column_name)

    return method_result


# the plan, for each company:
# 1. build a dictionary, the keys are the nasdaq companies (ALL of them),
#    the values are set to 0.
# 2. start at the first day (the earliest day recorded), get the sign of the
#    mentioned company's value change (just the same for percent change).
# 3. look at the sign of the change of all companies on the following day.
#    add +1 to the values in the dictionary only to the companies with
#    the same sign as the mentioned company of the day before,
#    and add -1 (subtract!) to the companies with the opposite sign.
# 4. repeat this for every day, adding to the SAME dictionary every time.
#
# for enough days recorded, the companies affected by the original company will
# (should) have the highest/lowest value.
# the unrelated companies should have values close to 0.
#
# normalize by the number of days recorded, so the values will range
# from -1 to 1.

def create_companies_zero_dict(market_name):
    daily_dataframe = stocks_analysis.get_market_today_dataframe(market_name)
    symbols_list = daily_dataframe['Symbol'].tolist()
    dict_of_zeros = {symbols_list[i]: 0 for i in range(len(symbols_list))}
    return dict_of_zeros

"""
# WORKS ONLY IF COMPANY SYMBOLS START WITH LETTERS ONLY
def split_symbols_list(symbols_list):
    splitted_list_by_letters = []
    letter_count = 0

    temp_letter_list = []
    for symbol in symbols_list:
        if symbol[0] == LETTERS_LIST[letter_count]:
            temp_letter_list.append(symbol)
        else:
            splitted_list_by_letters.append(temp_letter_list)
            temp_letter_list = []
            letter_count += 1

    return splitted_list_by_letters





class ReadPartialDataFrame(threading.Thread):
    def __init__(self, partial_symbols_list):
        threading.Thread.__init__(self)
        self.partial_symbols_list = partial_symbols_list

    def run(self):
        pass

    def daily_sign_dict(self):
        for i in range(len(self.partial_symbols_list)):
            try:
                sign_value = column_values_list[i] / abs(column_values_list[i])
            except ZeroDivisionError:
                sign_value = 0

            today_signs_dict[symbols_list[i]] = sign_value




def build_daily_signs_dict(partial_symbols_list):
    # threading:
    for sub_symbols_list in partial_symbols_list:
        page = ReadPartialDataFrame(letter, target_url, closing_url, title)
        page_read_classes.append(page)

    for read_class in page_read_classes:
        read_class.start()

    for read_class in page_read_classes:
        read_class.join()

    daily_data_frames_list = []
    for read_class in page_read_classes:
        daily_data_frames_list.extend(read_class.loaded_partial_frame_list)

"""


def add_day_to_counter_dict(daily_dict_counter, daily_dataframe, company_value_sign, col_name, number_of_days):
    symbols_list = daily_dataframe['Symbol'].tolist()
    #splitted_symbols_list = split_symbols_list(symbols_list)
    column_values_list = daily_dataframe[col_name].tolist()

    today_signs_dict = {}
    for i in range(len(symbols_list)):
        try:
            sign_value = column_values_list[i] / abs(column_values_list[i])
        except ZeroDivisionError:
            sign_value = 0

        today_signs_dict[symbols_list[i]] = sign_value

    for key in symbols_list:
        company_value_of_dict = today_signs_dict[key] * company_value_sign / number_of_days
        daily_dict_counter[key] += round(company_value_of_dict, 3)

    return daily_dict_counter


def get_company_value_sign_from_daily_dataframe(today_dataframe, company_symbol, col_name):
    today_chosen_company = today_dataframe[today_dataframe['Symbol'] == company_symbol]
    try:
        today_chosen_company_value = float(today_chosen_company[col_name])
    except:
        raise
    try:
        value_sign = today_chosen_company_value / abs(today_chosen_company_value)
    except ZeroDivisionError:
        return 0

    return value_sign


def check_for_daily_gaps(daily_files_paths_list):
    for i in range(len(daily_files_paths_list) - 1):
        date_as_list1 = re.findall(r'\d+', daily_files_paths_list[i])
        date_as_list2 = re.findall(r'\d+', daily_files_paths_list[i + 1])
        d1 = date(int(date_as_list1[0]), int(date_as_list1[1]), int(date_as_list1[2]))
        d2 = date(int(date_as_list2[0]), int(date_as_list2[1]), int(date_as_list2[2]))
        dates_delta = d2 - d1
        dates_delta = dates_delta.days

        if dates_delta > 1:
            print("Warning: missing {0} data file(s) between {1} and {2}."
                  .format(dates_delta - 1, str(d1), str(d2)))



def build_companies_counter_dict_for_specific_company(market_name, company_symbol, col_name, delay_days):
    daily_files_paths_list = path_finding_functions.get_all_daily_files_paths_in_specific_market(market_name)
    number_of_files = len(daily_files_paths_list)
    check_for_daily_gaps(daily_files_paths_list)  # put this where it displays only once (another function).

    updated_daily_dict_counter = create_companies_zero_dict(market_name)

    for i in range(number_of_files - delay_days):
        today_dataframe = stocks_analysis.all_companies_data_frame(daily_files_paths_list[i])
        company_value_sign = get_company_value_sign_from_daily_dataframe(today_dataframe, company_symbol, col_name)

        delayed_daily_dataframe = \
            stocks_analysis.all_companies_data_frame(daily_files_paths_list[i + delay_days])

        updated_daily_dict_counter = \
            add_day_to_counter_dict(updated_daily_dict_counter,
                                    delayed_daily_dataframe, company_value_sign,
                                    col_name, number_of_files)

    return updated_daily_dict_counter



