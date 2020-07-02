import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.analysis.advanced_utils as advanced_utils

COMPANIES_BLACK_LIST = ['Unnamed: 0', 'TRNX']


def remove_companies_black_list_from_dataframe(dataframe):
    for company_symbol in COMPANIES_BLACK_LIST:
        dataframe = dataframe[dataframe['Symbol'] != company_symbol]

    return dataframe


def get_filtered_selected_points_dataframe(exchange_name, ascend_or_descend, sign_or_value, delay_days):
    points_dataframe_file_path = path_finding_functions. \
        get_points_file_path(exchange_name, ascend_or_descend, sign_or_value, delay_days)
    points_dataframe = pd.read_excel(points_dataframe_file_path)
    filtered_points_dataframe = points_dataframe.drop(columns=COMPANIES_BLACK_LIST)
    return filtered_points_dataframe



def top_stocks_today(exchange_name, delay_days):
    exchange_dataframe_today = stocks_API.AllDataAnalysisToday(exchange_name).all_daily_dataframe
    exchange_dataframe_today_filtered = remove_companies_black_list_from_dataframe(exchange_dataframe_today)

    filtered_ascend_sign_points_dataframe = \
        get_filtered_selected_points_dataframe(exchange_name, 'ascend', 'sign', delay_days)

    all_symbols_list = list(filtered_ascend_sign_points_dataframe)
    print(all_symbols_list[:10])
    print(len(all_symbols_list))
