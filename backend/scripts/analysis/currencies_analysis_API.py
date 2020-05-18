import os
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.data_scrape.eoddata_scrape_API as scrape_API
import backend.scripts.analysis.stocks_analysis_API as stocks_API


class AllDataAnalysisToday:
    def __init__(self):
        self.daily_data_file_path_currencies = scrape_API.EoddataExchange('currencies').set_daily_data_file_name()

        if os.path.isfile(self.daily_data_file_path_currencies) is False:
            try:
                scrape_API.EoddataExchange('currencies').create_daily_data()
            except:
                print("no currency symbols data file found.\n initiating symbols data file creation.")
                scrape_API.EoddataExchange('currencies').create_symbols_file()

        self.all_currencies_dataframe = stocks_analysis.all_companies_data_frame(self.daily_data_file_path_currencies)

    def viable_data_column_names(self):
        return stocks_API.viable_data_column_names()

    # input: list of strings where each is supposedly part of the required currency's name.
    # output: list of strings containing exchange symbols that have the input strings in them.
    def get_exchange_rates_symbols_with_partial_name(self, partial_text_list):
        return stocks_analysis.get_company_symbol_with_partial_name(partial_text_list, self.all_currencies_dataframe)

    # input:  exchange_rates_symbols (a list of symbols)
    #         and/or list of strings where each is supposedly part of the required currency's name.
    # output: data frame (with the daily data) of the exchange rates.
    def get_specific_exchange_rates(self, exchange_rates_symbols):
        from_partial_strings = self.get_exchange_rates_symbols_with_partial_name(exchange_rates_symbols)
        exchange_rates_symbols.extend(from_partial_strings)
        return stocks_analysis.get_specific_companies(self.all_currencies_dataframe, exchange_rates_symbols)

    """# input: company_symbols (a list of symbols)
    # output: a dictionary (with the daily data) of the requested_companies.
    def get_specific_companies_dict_list(self, company_symbols):
        return stocks_analysis.get_specific_companies_dict_list(self.all_companies_df, company_symbols)"""

    # input: column_name, number_of_rates.
    #        number_of_rates to be retrieved from the daily data.
    # output: a data frame of the top number_of_rates in the data frame sorted by column_name.
    #         if bottom=True, returns the bottom rates in the data frame.
    def top_x_exchange_rates_by_column(self, column_name, number_of_rates, bottom=False):
        return stocks_analysis.\
            top_x_companies_by_column(self.all_currencies_dataframe, column_name, number_of_rates, bottom)

