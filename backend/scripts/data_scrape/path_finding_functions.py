import datetime
import glob
import requests
from bs4 import BeautifulSoup


def get_splitted_list_of_symbols_position_path(market_name, ascend_or_descend, sign_or_value, delay_days):
    file_path = r"backend\project_files\analysis_results\\" + market_name \
                + "_" + ascend_or_descend + "_" + sign_or_value + "_" \
                + "delay" + str(delay_days) + "_splitted_list_of_symbols_position.txt"
    return file_path


def set_operations_file_path():
    today = str(datetime.date.today())
    file_path = r"backend\project_files\daily_predictions\predictions_" + today + ".xlsx"
    return file_path


def set_points_file_path(title):
    today = str(datetime.date.today())
    file_path = r"backend\project_files\analysis_results\companies_points_" + title + "_" + today + ".xlsx"
    return file_path


def get_points_file_path(exchange_name, ascend_or_descend, sign_or_value, delay_days):
    path_string = r"backend\project_files\analysis_results\companies_points_"\
                  + exchange_name + "_" + ascend_or_descend + "_" + sign_or_value +\
                  "_" + "delay" + str(delay_days) + "*.xlsx"
    requested_points_dataframe_file_path = glob.glob(path_string)[-1]

    return requested_points_dataframe_file_path


def set_daily_data_file_path(title):
    today = str(datetime.date.today())
    file_path = r"backend\project_files" + r"\daily_data_excels_" + title + r"\{}".format(title) + today + ".xlsx"
    return file_path


def get_last_daily_data_file_path(market_name):
    partial_file_path = r"backend\project_files" + r"\daily_data_excels_" + market_name + "\*.xlsx"
    last_daily_data_file_path = glob.glob(partial_file_path)[-1]
    return last_daily_data_file_path


def set_symbols_file_name(title):
    today = str(datetime.date.today())
    file_path = r"backend\project_files\symbols_excel_files\companies_symbols_" + title + today + ".xlsx"
    return file_path


def get_symbols_file_path(title):
    basic_data_file = glob.glob(r"backend\project_files\symbols_excel_files\companies_symbols_" + str(title) + "*.xlsx")
    last_file_matched = basic_data_file[-1]
    return last_file_matched


def use_requests_get(url):
    try:
        page = requests.get(url).content
        parsed_page = BeautifulSoup(page, 'html.parser')
    except:
        exit("error loading page at " + url)

    return parsed_page


def get_all_daily_files_paths_in_specific_market(market_name):
    root_path = r"backend\project_files\daily_data_excels_{}".format(market_name)
    excel_files_path_list = glob.glob(root_path + r"\*.xlsx")
    return excel_files_path_list



