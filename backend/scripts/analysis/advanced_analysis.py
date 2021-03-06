import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.analysis.advanced_utils as advanced_utils
from collections import Counter
from datetime import date
import concurrent.futures
import re

LETTERS_LIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER_OF_SUBLISTS = 200


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


# when the print is no more needed - REMOVE the last 3 inputs:
def check_equal_days_values(today_dataframe, delayed_daily_dataframe, col_name,
                            next_company_values, previous_company_values):

    # check if the focused day and the delayed day contain the exact same data (if so - skip):
    day1_col = today_dataframe[col_name]
    day2_col = delayed_daily_dataframe[col_name]
    check_equals = day1_col.equals(day2_col)
    if check_equals is True:
        return True

    # check if following days of the focused company hold the exact same values
    # (aka no change at all -> skip):
    check_value_equals = next_company_values.equals(previous_company_values)
    if check_value_equals is True:
        return True

    return False


def build_count_dict_from_daily_files(number_of_counted_days, daily_files_paths_list,
                                      company_symbol, col_name, delay_days, updated_daily_dict_counter,
                                      ascend_or_descend, volume_percent_filter_to_remove=0, sign_or_value='sign'):
    ascend_count = 0
    descend_count = 0
    company_value_sign = 0
    previous_company_values = 0

    print(company_symbol, ascend_or_descend, sign_or_value)

    # run over each daily file, focusing on a specific company (company_symbol):
    for i in range(number_of_counted_days):

        # focused_day_dataframe
        today_dataframe = stocks_analysis.all_companies_data_frame(daily_files_paths_list[i])
        # today_dataframe = advanced_utils.remove_companies_black_list_from_dataframe(today_dataframe)

        volume_filtered_dataframe = advanced_utils.\
            volume_filtered_market_dataframe(today_dataframe, volume_percent_filter_to_remove)

        if sign_or_value == 'sign':     # take its percent-change sign (+ or -)
            company_value_sign = advanced_utils.\
                get_company_value_sign_from_daily_dataframe(volume_filtered_dataframe,
                                                            company_symbol, col_name)
        elif sign_or_value == 'value':  # take its percent-change value.
            try:
                company_value_sign = \
                    volume_filtered_dataframe[volume_filtered_dataframe['Symbol'] ==
                                              company_symbol]['Percent-Change'].tolist()[0]
            except IndexError:
                print("Index out of range. Company is not in volume_filtered_dataframe: ", company_symbol)
                company_value_sign = 0

        delayed_daily_dataframe = \
            stocks_analysis.all_companies_data_frame(daily_files_paths_list[i + delay_days])
        # delayed_daily_dataframe = advanced_utils.remove_companies_black_list_from_dataframe(delayed_daily_dataframe)

        next_company_values = volume_filtered_dataframe[volume_filtered_dataframe['Symbol'] == company_symbol]

        check_equals = check_equal_days_values(today_dataframe, delayed_daily_dataframe,
                                               col_name, next_company_values, previous_company_values)

        previous_company_values = next_company_values
        if check_equals is True:
            continue

        if company_value_sign > 0:
            ascend_count += 1
            if ascend_or_descend == 'descend':
                continue
        elif company_value_sign < 0:
            descend_count += 1
            if ascend_or_descend == 'ascend':
                continue
        else:
            continue

        volume_filtered_delayed_dataframe = \
            advanced_utils.volume_filtered_market_dataframe(delayed_daily_dataframe, volume_percent_filter_to_remove)

        updated_daily_dict_counter = \
            advanced_utils.add_day_to_counter_dict(volume_filtered_delayed_dataframe,
                                                   company_value_sign, col_name,
                                                   updated_daily_dict_counter, ascend_or_descend, sign_or_value)

    return updated_daily_dict_counter, ascend_count, descend_count


def build_companies_counter_dict_for_specific_company(market_name, company_symbol, col_name,
                                                      delay_days, ascend_or_descend='ascend',
                                                      volume_percent_filter=100, sign_or_value='sign'):

    daily_files_paths_list = path_finding_functions.get_all_daily_files_paths_in_specific_market(market_name)
    number_of_files = len(daily_files_paths_list)

    number_of_counted_days = number_of_files - delay_days

    initialized_daily_dict_counter = advanced_utils.create_companies_zero_dict(market_name, volume_percent_filter)

    updated_daily_dict_counter, ascend_count, descent_count = \
        build_count_dict_from_daily_files(number_of_counted_days, daily_files_paths_list,
                                          company_symbol, col_name, delay_days,
                                          initialized_daily_dict_counter, ascend_or_descend,
                                          volume_percent_filter, sign_or_value)

    normalized_dict_counter = \
        advanced_utils.normalize_daily_dict_counter(ascend_or_descend, updated_daily_dict_counter,
                                                    ascend_count, descent_count, number_of_counted_days)

    return normalized_dict_counter


company_count = 0


def companies_influenced_by_selected_company_dict(args_list):

    market_name = args_list[0]
    company_symbol = args_list[1]
    col_name = args_list[2]
    delay_days = args_list[3]
    ascend_or_descend = args_list[4]
    volume_percent_filter = args_list[5]
    sign_or_value = args_list[6]

    updated_daily_dict_counter = \
        build_companies_counter_dict_for_specific_company(market_name, company_symbol,
                                                          col_name, delay_days, ascend_or_descend,
                                                          volume_percent_filter, sign_or_value)

    result_dataframe = pd.DataFrame.from_dict(updated_daily_dict_counter, orient='index')
    result_dataframe = result_dataframe.T
    result_dict = {company_symbol: result_dataframe}

    # print for development stage (maybe even for later):
    global company_count
    company_count += 1
    print("number of companies finished: ", company_count)

    return result_dict


def build_companies_squared_dataframe(symbols_list, splitted_list_of_symbols,
                                      column_name, market_name, delay_days,
                                      volume_percent_filter, ascend_or_descend='ascend',
                                      sign_or_value='sign', number_of_iterations=1):

    try:
        companies_squared_dataframe = advanced_utils. \
            get_filtered_selected_points_dataframe(market_name, ascend_or_descend, sign_or_value, delay_days)
    except:
        print("Failed loading existing points_dataframe. Initializing a new one.")
        companies_squared_dataframe = advanced_utils.initiate_square_dataframe_zeros(symbols_list)

    current_position = advanced_utils.\
        get_and_increment_symbols_sublist_position(market_name, NUMBER_OF_SUBLISTS,
                                                   number_of_iterations, ascend_or_descend,
                                                   sign_or_value, delay_days)

    j = 0
    for partial_company_symbols_list in splitted_list_of_symbols:

        # makes sure we start from the intended position and stop after the intended number of iterations
        if j < current_position:
            j += 1
            continue
        elif j >= current_position + number_of_iterations:
            break
        j += 1

        args_list = [[market_name, company_symbol, column_name, delay_days,
                      ascend_or_descend, volume_percent_filter, sign_or_value]
                     for company_symbol in partial_company_symbols_list]

        print("Companies giving points now:")
        print(partial_company_symbols_list)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            company_points_dataframe_dicts = executor.map(companies_influenced_by_selected_company_dict, args_list)
            for points_dicts in company_points_dataframe_dicts:
                points_giving_company_symbol = list(points_dicts.keys())[0]
                points_giving_company_dataframe = list(points_dicts.values())[0]
                for symbol in symbols_list:
                    try:
                        companies_squared_dataframe.at[points_giving_company_symbol, symbol] = \
                            points_giving_company_dataframe.at[0, symbol]
                    except KeyError:
                        points_dataframe_symbols_list = list(companies_squared_dataframe.index)
                        if points_giving_company_symbol not in points_dataframe_symbols_list:
                            missing_symbol = points_giving_company_symbol
                            print("points_giving_company_symbol not in points_dataframe_symbols_list: ", missing_symbol)
                            print("Adding it to the dataframe. Check it specifically.")
                        elif symbol not in points_dataframe_symbols_list:
                            missing_symbol = symbol
                            print("symbol not in points_dataframe_symbols_list: ", missing_symbol)
                            print("Adding it to the dataframe. Check it specifically.")
                        else:
                            raise
                        companies_squared_dataframe[missing_symbol] = 0  # this might cause an error
                        companies_squared_dataframe.append(pandas.Series(name=missing_symbol))

                        companies_squared_dataframe.at[points_giving_company_symbol, symbol] = \
                            points_giving_company_dataframe.at[0, symbol]

    return companies_squared_dataframe


def create_points_dataframe(market_name, delay_days,
                            volume_percent_filter=0, ascend_or_descend='ascend',
                            column_name='Percent-Change', sign_or_value='value', number_of_iterations=1):

    daily_files_paths_list = path_finding_functions.get_all_daily_files_paths_in_specific_market(market_name)
    advanced_utils.check_for_daily_gaps(daily_files_paths_list)

    sample_daily_dataframe = stocks_analysis.all_companies_data_frame(daily_files_paths_list[-1])

    initial_volume_filtered_dataframe = \
        advanced_utils.volume_filtered_market_dataframe(sample_daily_dataframe, volume_percent_filter)

    symbols_list = initial_volume_filtered_dataframe['Symbol'].tolist()

    # split the symbols list, so each thread takes a sub-list to work on.
    splitted_list_of_symbols = advanced_utils.splitted_symbols_list(symbols_list, NUMBER_OF_SUBLISTS)

    companies_squared_dataframe = \
        build_companies_squared_dataframe(symbols_list, splitted_list_of_symbols,
                                          column_name, market_name, delay_days,
                                          volume_percent_filter, ascend_or_descend,
                                          sign_or_value, number_of_iterations)

    sort_by_companies = ['TOPS', 'CSCO', 'SRNE']  # just to make sure i see all companies that were-
                                                  # included in the count, and not spreaded all over the sheet.
    companies_squared_dataframe.sort_values(by=sort_by_companies, ascending=False, inplace=True)

    file_path = path_finding_functions.\
        set_points_file_path(market_name + "_" + ascend_or_descend + "_"
                             + sign_or_value + "_" + "delay" + str(delay_days))
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    companies_squared_dataframe.to_excel(writer)
    writer.save()
