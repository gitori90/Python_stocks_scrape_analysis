#!/usr/bin/env python3

import backend.scripts.data_scrape.eoddata_scrape_API as scrape_API
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.analysis.currencies_analysis_API as currencies_API
import backend.scripts.plot_functions.plots_API as plots_API
import backend.scripts.analysis.advanced_analysis_API as advanced_API

DEFAULT_EXCHANGE_NAME = 'nasdaq'


class StocksSectionBasic:

    def __init__(self):
        pass

    def get_exchange_names_list(self):
        requested_names_list = stocks_API.viable_exchange_names()
        return requested_names_list

    def refresh_daily_data(self):
        exchanges_dict = scrape_API.Eoddata().tab_dict
        for exchange in exchanges_dict:
            scrape_API.EoddataExchange(exchanges_dict[exchange]).create_daily_data()

    def create_symbols_file(self, exchange_name):
        scrape_API.EoddataExchange(exchange_name).create_symbols_file()

    def bar_plot(self, data_frame, x_col_name, y_col_name, title, plot_file_name, show_or_save):
        plots_API.bar_plot(data_frame, x_col_name, y_col_name, title, plot_file_name, show_or_save)

    def plot_sectors_analysis_today(self, analysis_df, method_name, column_name):
        plots_API.plot_sectors_analysis_today(analysis_df, method_name, column_name)

    def specific_companies_dataframe(self, company_symbols_or_names, exchange_name):
        stripped_string = company_symbols_or_names.replace(" ", "")
        string_list = stripped_string.split(",")
        companies_dataframe = stocks_API.AllDataAnalysisToday(exchange_name).get_specific_companies_df(string_list)
        return companies_dataframe

    def valid_column_names_list(self):
        return stocks_API.VIABLE_DATA_COLUMN_NAMES

    def analysis_methods_viable_names_list(self):
        return stocks_API.ANALYSIS_METHODS_VIABLE_NAMES

    def get_sector_names_list(self, exchange_name):
        return stocks_API.SectorsDataAnalysisToday(exchange_name).get_sector_names_list()

    def analyse_column_of_sectors_dataframe(self, column_name, method, exchange_name):
        return stocks_API.SectorsDataAnalysisToday(exchange_name).analyse_column_of_sectors(column_name, method)

    def top_companies_dataframe(self, sector_name, column_name, number_of_companies, top_or_bottom, exchange_name):
        if sector_name == 'All':
            tops = stocks_API.AllDataAnalysisToday(exchange_name).\
                top_x_companies_by_column(column_name, number_of_companies, top_or_bottom)
        else:
            tops = stocks_API.SectorsDataAnalysisToday(exchange_name).\
                top_x_companies_in_sector_by_column(sector_name, column_name, number_of_companies, top_or_bottom)
        return tops


class StocksSectionAdvanced:
    def __init__(self):
        pass

    def top_x_words_in_all_dataframes_dict(self, top_number):
        top_dict = advanced_API.GlobalConnections().top_x_words_in_dataframe_dict(top_number)
        return top_dict

    def top_x_companies_by_column_with_specific_word_dataframe\
        (self, specific_name, column_name, number_of_companies, bottom_or_top=False):

        dataframe_of_top_by_column = advanced_API.GlobalConnections().\
            top_x_companies_by_column_with_specific_name_dataframe\
            (specific_name, column_name, number_of_companies, bottom_or_top)

        return dataframe_of_top_by_column

    def analyse_method_on_all_dataframes_partial_name(self, partial_name, method_name, column_name):
        method_result = advanced_API.GlobalConnections().\
            analyse_method_on_all_dataframes_partial_name(partial_name, method_name, column_name)

        return method_result


class CurrenciesSection:
    def __init__(self):
        pass

    def top_x_exchange_rates_by_column_dataframe(self, column_name, number_of_rates, top_or_bottom):
        return currencies_API.AllDataAnalysisToday().\
            top_x_exchange_rates_by_column(column_name, number_of_rates, top_or_bottom)

    def get_specific_exchange_rates_dataframe(self, exchange_rates_symbols):
        return currencies_API.AllDataAnalysisToday().get_specific_exchange_rates(exchange_rates_symbols)
