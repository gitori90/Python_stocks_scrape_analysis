import datetime
import glob
import requests
from bs4 import BeautifulSoup


def set_points_file_path(title):
    today = str(datetime.date.today())
    file_path = r"backend\project_files" + r"\analysis_results" \
                + r"\companies_points_" + title + "_" + today + ".xlsx"
    return file_path


def set_daily_data_file_path(title):
    today = str(datetime.date.today())
    file_path = r"backend\project_files" + r"\daily_data_excels_" + title + r"\{}".format(title) + today + ".xlsx"
    return file_path


def set_symbols_file_name(title):
    today = str(datetime.date.today())
    file_path = r"backend\project_files\symbols_excel_files" + r"\companies_symbols_" + title + today + ".xlsx"
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



