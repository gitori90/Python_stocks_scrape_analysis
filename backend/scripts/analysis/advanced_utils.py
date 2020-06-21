import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
from collections import Counter
from datetime import date
import threading
import re
import inspect


def create_daily_signs_dict(symbols_list, column_values_list):
    today_signs_dict = {}
    for i in range(len(symbols_list)):
        try:
            sign_value = column_values_list[i] / abs(column_values_list[i])
        except ZeroDivisionError:
            sign_value = 0

        today_signs_dict[symbols_list[i]] = sign_value
    return today_signs_dict


def build_counter_dict(symbols_list, today_signs_dict, company_value_sign, daily_dict_counter, ascend_or_descend):

    if ascend_or_descend == 'both':
        for key in symbols_list:
            try:
                company_value_of_dict = today_signs_dict[key] * company_value_sign
                daily_dict_counter[key] += company_value_of_dict
            except KeyError:
                pass

    elif ascend_or_descend == 'ascend':
        for key in symbols_list:
            try:
                if today_signs_dict[key] > 0 and company_value_sign > 0:
                    daily_dict_counter[key] += company_value_sign
            except KeyError:
                pass

    elif ascend_or_descend == 'descend':
        for key in symbols_list:
            try:
                if today_signs_dict[key] < 0 and company_value_sign < 0:
                    daily_dict_counter[key] += -company_value_sign
            except KeyError:
                pass
    else:
        line_number = inspect.getframeinfo(inspect.currentframe()).lineno
        exit("advanced_utils, line {}: Invalid input for ascend_or_descend: ".format(line_number) + ascend_or_descend)

    return daily_dict_counter


def add_day_to_counter_dict(daily_dataframe, company_value_sign, col_name,
                            daily_dict_counter, ascend_or_descend='both'):
    symbols_list = daily_dataframe['Symbol'].tolist()
    column_values_list = daily_dataframe[col_name].tolist()
    today_signs_dict = create_daily_signs_dict(symbols_list, column_values_list)

    daily_dict_counter = build_counter_dict(symbols_list, today_signs_dict,
                                            company_value_sign, daily_dict_counter, ascend_or_descend)
    return daily_dict_counter


def get_company_value_sign_from_daily_dataframe(today_dataframe, company_symbol, col_name):
    try:
        today_chosen_company = today_dataframe[today_dataframe['Symbol'] == company_symbol]
    except:
        # print(company_symbol, " advanced utils 71")
        return 0
    try:
        today_chosen_company_value = float(today_chosen_company[col_name])
    except:
        # print("Error in today_chosen_company_value. Company: ", company_symbol)
        return 0
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


def volume_filtered_market_dataframe(market_dataframe, volume_percent_filter=0):
    if volume_percent_filter not in range(0, 101):
        exit("Invalid input for volume_percent_filter.")

    volume_sorted_dataframe = market_dataframe.sort_values(by=['Volume'], ascending=False)
    if volume_percent_filter == 0:
        return volume_sorted_dataframe

    volume_list = volume_sorted_dataframe['Volume'].tolist()

    number_of_rows = len(volume_list)
    chosen_percent_to_rows_to_remove = int(number_of_rows * volume_percent_filter / 100)

    #print("volume filter threshold: " + str(volume_list[chosen_percent_to_rows_to_remove]))

    volume_filtered_dataframe = volume_sorted_dataframe[:-chosen_percent_to_rows_to_remove]
    return volume_filtered_dataframe


def create_companies_zero_dict(market_name, volume_percent_filter=0):
    daily_dataframe = stocks_analysis.get_market_today_dataframe(market_name)
    filtered_daily_dataframe = volume_filtered_market_dataframe(daily_dataframe, volume_percent_filter)
    symbols_list = filtered_daily_dataframe['Symbol'].tolist()
    dict_of_zeros = {symbols_list[i]: 0 for i in range(len(symbols_list))}
    return dict_of_zeros


def get_company_selected_column_value(today_dataframe, company_symbol, col_name):
    selected_company_dataframe = today_dataframe[today_dataframe['Symbol'] == company_symbol]
    selected_column_value = float(selected_company_dataframe[col_name])
    return selected_column_value


def normalize_daily_dict_counter(tendency, updated_daily_dict_counter, ascend_count,
                                 descent_count, number_of_counted_days):
    tendency_count = number_of_counted_days
    if tendency == 'ascend':
        tendency_count = ascend_count
    elif tendency == 'descend':
        tendency_count = descent_count
    elif tendency == 'both':
        pass
    else:
        line_number = inspect.getframeinfo(inspect.currentframe()).lineno
        exit("advanced_utils, line {}: Invalid input for ascend_or_descend: ".format(line_number) + ascend_or_descend)

    for key in updated_daily_dict_counter:
        try:
            updated_daily_dict_counter[key] /= tendency_count
        except ZeroDivisionError:
            # print(key, " advanced utils 145")
            updated_daily_dict_counter[key] = 0
            continue
        updated_daily_dict_counter[key] = round(updated_daily_dict_counter[key], 3)

    return updated_daily_dict_counter


def initiate_square_dataframe_zeros(symbols_list):
    zeros_dataframe = pd.DataFrame(index=symbols_list, columns=symbols_list)
    for col in zeros_dataframe.columns:
        zeros_dataframe[col].values[:] = 0

    return zeros_dataframe


def splitted_symbols_list(symbols_list, number_of_sublists):
    total_symbols = len(symbols_list)
    numb_in_each_sublist = int(total_symbols/number_of_sublists)
    splitted_list = []
    i = 0
    while i < total_symbols:
        splitted_list.append(symbols_list[i:i+numb_in_each_sublist])
        i += numb_in_each_sublist

    return splitted_list
