import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.analysis.advanced_utils as advanced_utils
import statistics

COMPANIES_BLACK_LIST = ['TRNX']


def remove_companies_black_list_from_dataframe(dataframe):
    for company_symbol in COMPANIES_BLACK_LIST:
        dataframe = dataframe[dataframe['Symbol'] != company_symbol]

    return dataframe


def get_filtered_selected_points_dataframe(exchange_name, ascend_or_descend, sign_or_value, delay_days):
    points_dataframe_file_path = path_finding_functions. \
        get_points_file_path(exchange_name, ascend_or_descend, sign_or_value, delay_days)
    points_dataframe = pd.read_excel(points_dataframe_file_path)
    points_dataframe = points_dataframe.set_index('Unnamed: 0')

    filtered_points_dataframe = points_dataframe.drop(columns=COMPANIES_BLACK_LIST,
                                                      index=COMPANIES_BLACK_LIST,
                                                      errors='ignore')
    return filtered_points_dataframe



def top_stocks_today(exchange_name, delay_days, sign_percent_filter=0.8, minimum_eligible_companies=3):
    exchange_dataframe_today = stocks_API.AllDataAnalysisToday(exchange_name).all_daily_dataframe
    exchange_dataframe_today_filtered = remove_companies_black_list_from_dataframe(exchange_dataframe_today)

    filtered_ascend_sign_points_dataframe = \
        get_filtered_selected_points_dataframe(exchange_name, 'ascend', 'sign', delay_days)

    all_symbols_list = list(filtered_ascend_sign_points_dataframe)

    # thats not what im supposed to do. i need to gather the points according to
    # the values in exchange_dataframe_today_filtered
    """top_points_dict = {}
    for symbol in all_symbols_list:
        sorted_list_all_points_of_company = filtered_ascend_sign_points_dataframe[symbol].tolist()
        top_points_of_company = [i for i in sorted_list_all_points_of_company if i >= sign_percent_filter]

        if len(top_points_of_company) < minimum_eligible_companies:
            continue

        company_temp_dict = {}
        company_temp_dict['mean_points'] = round(statistics.mean(top_points_of_company), 3)
        company_temp_dict['total_companies_included'] = len(top_points_of_company)

        top_points_dict[symbol] = company_temp_dict

    j = 0
    for i in top_points_dict:
        print(i)
        print(top_points_dict[i])
        print("###############################")
        j += 1
        if j > 10:
            break"""
