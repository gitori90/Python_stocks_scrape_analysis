#!/usr/bin/env python3

import backend.scripts.data_scrape.eoddata_scrape_API as scrape_API
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.analysis.currencies_analysis_API as currencies_API
import backend.scripts.plot_functions.plots_API as plots_API


DEFAULT_EXCHANGE_NAME = 'nasdaq'

# returns a list of the exchanges names as written in Eoddata class in eoddata_scrape_API.
def get_exchange_names_list():
    requested_names_list = stocks_API.viable_exchange_names()
    return requested_names_list


def refresh_daily_data():
    exchanges_dict = scrape_API.Eoddata().tab_dict
    for exchange in exchanges_dict:
        scrape_API.EoddataExchange(exchanges_dict[exchange]).create_daily_data()


def create_symbols_file(exchange_name):
    scrape_API.EoddataExchange(exchange_name).create_symbols_file()


# input: self explanatory.
#        file_name_addition is another string to add to the graph image's file name.
def bar_plot(data_frame, x_col_name, y_col_name, title, plot_file_name, show_or_save):
    plots_API.bar_plot(data_frame, x_col_name, y_col_name, title, plot_file_name, show_or_save)


# input: 1. data frame of the resulted method applied to the sectors (sector names are the columns).
#        2. name of the method applied to the data.
#        3. the name of the data column the method acted on.
# return value: none. calls for bar_plot to show or save the graph.
def plot_sectors_analysis_today(analysis_df, method_name, column_name):
    plots_API.plot_sectors_analysis_today(analysis_df, method_name, column_name)


# input:  column_name, number_of_companies.
#         number_of_companies to be retrieved from the daily data.
# output: a data frame of the top number_of_companies in the data frame sorted by column_name.
#         if bottom=True, returns the bottom companies in the data frame.
def top_companies(col_name, numb_of_companies, top_or_bottom, exchange_name):
    tops = stocks_API.AllDataAnalysisToday(exchange_name).\
        top_x_companies_by_column(col_name, numb_of_companies, top_or_bottom)
    return tops


# input:  1 long string containing the names/symbols.
# output: the data frame containing the requested companies.
def specific_companies(company_symbols_or_names, exchange_name):
    stripped_string = company_symbols_or_names.replace(" ", "")
    string_list = stripped_string.split(",")
    companies_df = stocks_API.AllDataAnalysisToday(exchange_name).get_specific_companies_df(string_list)
    return companies_df


# returns a list of the valid column names in the data frame.
def valid_column_names():
    return stocks_API.AllDataAnalysisToday(DEFAULT_EXCHANGE_NAME).viable_data_column_names()


# returns a list of the sectors analysis methods available in stocks_analysis.py
def analysis_methods_viable_names():
    return stocks_API.SectorsDataAnalysisToday(DEFAULT_EXCHANGE_NAME).analysis_methods_viable_names()


def get_sector_names_list(exchange_name):
    return stocks_API.SectorsDataAnalysisToday(exchange_name).get_sector_names_list()


# input:  self explanatory.
#         the method variable is to be taken from the list returned by analysis_methods_viable_names()
# output: a data frame of the method result values of the chosen column for each sector.
def analyse_column_of_sectors(column_name, method, exchange_name):
    return stocks_API.SectorsDataAnalysisToday(exchange_name).analyse_column_of_sectors(column_name, method)


# input:  sector_name, column_name, number_of_companies, bottom.
#         number_of_companies to be retrieved from the daily data.
# output: a data frame of the top number_of_companies in
#         the requested sector data frame sorted by column_name.
#         if bottom=True, returns the bottom companies in the data frame.
def top_x_companies_in_sector_by_column(sector_name, column_name, number_of_companies, top_or_bottom, exchange_name):
    return stocks_API.SectorsDataAnalysisToday(exchange_name).\
        top_x_companies_in_sector_by_column(sector_name, column_name, number_of_companies, top_or_bottom)


############################## CURRENCIES ##############################

def top_x_exchange_rates_by_column(column_name, number_of_rates, top_or_bottom):
    return currencies_API.AllDataAnalysisToday().\
        top_x_exchange_rates_by_column(column_name, number_of_rates, top_or_bottom)


def get_specific_exchange_rates(exchange_rates_symbols):
    return currencies_API.AllDataAnalysisToday().get_specific_exchange_rates(exchange_rates_symbols)
