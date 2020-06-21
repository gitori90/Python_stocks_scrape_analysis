import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.analysis.advanced_utils as advanced_utils
from collections import Counter
from datetime import date
import threading
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


def build_count_dict_from_daily_files(number_of_counted_days, daily_files_paths_list,
                                      company_symbol, col_name, delay_days, updated_daily_dict_counter,
                                      ascend_or_descend, volume_percent_filter_to_remove=0):
    ascend_count = 0
    descent_count = 0

    for i in range(number_of_counted_days):
        today_dataframe = stocks_analysis.all_companies_data_frame(daily_files_paths_list[i])
        volume_filtered_dataframe = advanced_utils.\
            volume_filtered_market_dataframe(today_dataframe, volume_percent_filter_to_remove)

        company_value_sign = advanced_utils.\
            get_company_value_sign_from_daily_dataframe(volume_filtered_dataframe,
                                                        company_symbol, col_name)

        if company_value_sign > 0:
            ascend_count += 1
            if ascend_or_descend == 'descend':
                continue
        elif company_value_sign < 0:
            descent_count += 1
            if ascend_or_descend == 'ascend':
                continue
        else:
            continue

        delayed_daily_dataframe = \
            stocks_analysis.all_companies_data_frame(daily_files_paths_list[i + delay_days])
        volume_filtered_delayed_dataframe = \
            advanced_utils.volume_filtered_market_dataframe(delayed_daily_dataframe, volume_percent_filter_to_remove)

        """check_for_identical_consecutive_company_values = advanced_utils.\
            is_identical_consecutive_company_values(volume_filtered_dataframe,
                                                    volume_filtered_delayed_dataframe, company_symbol)
        if check_for_identical_consecutive_company_values is True:
            continue"""
        day1_col = volume_filtered_dataframe[col_name]
        day2_col = volume_filtered_delayed_dataframe[col_name]
        check_equals = day1_col.equals(day2_col)
        if check_equals is True:
            print("identical files:\n" + daily_files_paths_list[i] + "\n" + daily_files_paths_list[i + delay_days])
            continue

        updated_daily_dict_counter = \
            advanced_utils.add_day_to_counter_dict(volume_filtered_delayed_dataframe,
                                                   company_value_sign, col_name,
                                                   updated_daily_dict_counter, ascend_or_descend)

    return updated_daily_dict_counter, ascend_count, descent_count


def build_companies_counter_dict_for_specific_company(market_name, company_symbol, col_name,
                                                      delay_days, ascend_or_descend='ascend', volume_percent_filter=100):

    daily_files_paths_list = path_finding_functions.get_all_daily_files_paths_in_specific_market(market_name)
    number_of_files = len(daily_files_paths_list)

    number_of_counted_days = number_of_files - delay_days

    initialized_daily_dict_counter = advanced_utils.create_companies_zero_dict(market_name, volume_percent_filter)
    # print("TRNX" in initialized_daily_dict_counter.keys())
    updated_daily_dict_counter, ascend_count, descent_count = \
        build_count_dict_from_daily_files(number_of_counted_days, daily_files_paths_list,
                                          company_symbol, col_name, delay_days,
                                          initialized_daily_dict_counter, ascend_or_descend, volume_percent_filter)

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
    """try:
        direct_or_reverse = args_list[6]
    except IndexError:
        direct_or_reverse = 'direct'"""

    updated_daily_dict_counter = \
        build_companies_counter_dict_for_specific_company(market_name, company_symbol,
                                                          col_name, delay_days, ascend_or_descend, volume_percent_filter)

    result_dataframe = pd.DataFrame.from_dict(updated_daily_dict_counter, orient='index')
    result_dataframe = result_dataframe.T
    result_dict = {company_symbol: result_dataframe}

    # print for development stage (maybe even for later):
    global company_count
    company_count += 1
    print("number of companies finished: ", company_count)

    return result_dict



# for API:
# variable 'related_companies_list' is (should be) a list of companies
# extracted from the dictionary returned by top_x_influenced_by_selected_company_dict
def selected_companies_percent_connection_strength_dict(market_name, company_symbol, related_companies_list,
                                                        delay_days, col_name, tendency='ascend'):

    daily_files_paths_list = path_finding_functions.get_all_daily_files_paths_in_specific_market(market_name)
    number_of_files = len(daily_files_paths_list)
    number_of_counted_days = number_of_files - delay_days

    delayed_companies_selected_values_dict = {company: 0 for company in related_companies_list}

    # run over each daily file, exclude those that have no correspondent delayed daily file:
    ascend_count = 0
    descent_count = 0
    for i in range(number_of_counted_days):
        today_dataframe = stocks_analysis.all_companies_data_frame(daily_files_paths_list[i])

        focused_company_selected_value = \
            advanced_utils.get_company_selected_column_value(today_dataframe, company_symbol, col_name)
        try:
            focused_company_value_sign = focused_company_selected_value / abs(focused_company_selected_value)
        except ZeroDivisionError:
            print("focused_company_selected_value = 0 for: ", company_symbol)
            continue

        if focused_company_value_sign > 0:
            ascend_count += 1
        elif focused_company_value_sign < 0:
            descent_count += 1

        delayed_daily_dataframe = \
            stocks_analysis.all_companies_data_frame(daily_files_paths_list[i + delay_days])

        # run over the related companies and get its relative change
        # (compared to the company in the focus) and add to the dict:
        for company_symbol in related_companies_list:
            related_selected_value = \
                advanced_utils.get_company_selected_column_value(delayed_daily_dataframe, company_symbol, col_name)
            try:
                related_company_value_sign = related_selected_value / abs(related_selected_value)
            except ZeroDivisionError:
                continue

            if ((tendency == 'ascend' and focused_company_value_sign == related_company_value_sign > 0)
                or (tendency == 'descent' and focused_company_value_sign == related_company_value_sign < 0)):

                relative_value = related_selected_value / focused_company_selected_value

                delayed_companies_selected_values_dict[company_symbol] += relative_value

    normalized_dict_counter = \
        advanced_utils.normalize_daily_dict_counter(tendency, delayed_companies_selected_values_dict,
                                                    ascend_count, descent_count, number_of_counted_days)

    return normalized_dict_counter


def build_companies_squared_dataframe(symbols_list, splitted_list_of_symbols,
                                      column_name, market_name, delay_days,
                                      volume_percent_filter, ascend_or_descend='ascend'):

    companies_squared_dataframe = advanced_utils.initiate_square_dataframe_zeros(symbols_list)
    for partial_company_symbols_list in splitted_list_of_symbols:
        args_list = [[market_name, company_symbol, column_name, delay_days, ascend_or_descend, volume_percent_filter]
                     for company_symbol in partial_company_symbols_list]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            company_points_dataframe_dicts = executor.map(companies_influenced_by_selected_company_dict, args_list)
            for points_dicts in company_points_dataframe_dicts:
                points_giving_company_symbol = list(points_dicts.keys())[0]
                points_giving_company_dataframe = list(points_dicts.values())[0]
                for symbol in symbols_list:
                    try:
                        """
                        that line (which executes after the comment):
                        companies_squared_dataframe.at[points_giving_company_symbol, symbol]
                        shows the structure of the final dataframe.
                        the ROWS are the points GIVEN to the companies 
                        in the COLUMNS.
                        
                        that company which gives the points on each iteration
                        to all the other companies, gives the normalized amount
                        of the -
                        
                        <times this company's price ascended / descended
                        and so did the other company at the delayed day>
                        
                        divided by the (thus normalized) - 
                        
                        <number of days that company's price ascended / descended>
                        
                        thus, each company will give to every other company,
                        a number in the range 0-1 (in the respective slot
                        in the dataframe).
                        """
                        companies_squared_dataframe.at[points_giving_company_symbol, symbol] += \
                            points_giving_company_dataframe.at[0, symbol]
                    except KeyError:
                        pass
        # this break is here so we can test things on 1 iteration instead of a ton of them.
        break

    return companies_squared_dataframe


def create_points_dataframe(market_name, delay_days,
                            volume_percent_filter=0, ascend_or_descend='ascend', column_name='Percent-Change'):

    daily_files_paths_list = path_finding_functions.get_all_daily_files_paths_in_specific_market(market_name)
    advanced_utils.check_for_daily_gaps(daily_files_paths_list)
    sample_daily_dataframe = stocks_analysis.all_companies_data_frame(daily_files_paths_list[0])

    initial_volume_filtered_dataframe = \
        advanced_utils.volume_filtered_market_dataframe(sample_daily_dataframe, volume_percent_filter)

    symbols_list = initial_volume_filtered_dataframe['Symbol'].tolist()

    # split the symbols list, so each thread takes a sub-list to work on.
    splitted_list_of_symbols = advanced_utils.splitted_symbols_list(symbols_list, NUMBER_OF_SUBLISTS)

    companies_squared_dataframe = \
        build_companies_squared_dataframe(symbols_list, splitted_list_of_symbols,
                                          column_name, market_name, delay_days,
                                          volume_percent_filter, ascend_or_descend)

    file_path = path_finding_functions.set_points_file_path(market_name + "_" + ascend_or_descend)
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    companies_squared_dataframe.to_excel(writer)
    writer.save()


