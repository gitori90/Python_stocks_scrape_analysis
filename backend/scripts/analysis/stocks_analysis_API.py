import os
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.data_scrape.eoddata_scrape_API as scrape_API


class AllDataAnalysisToday:
    def __init__(self, exchange_name):
        self.daily_data_file_path = scrape_API.EoddataExchange(exchange_name).set_daily_data_file_name()

        if os.path.isfile(self.daily_data_file_path) is False:
            scrape_API.EoddataExchange(exchange_name).create_daily_data()
        try:
            self.all_daily_dataframe = stocks_analysis.all_companies_data_frame(self.daily_data_file_path)
        except:
            print("no " + exchange_name + " symbols data file found.\n initiating symbols data file creation.")
            scrape_API.EoddataExchange(exchange_name).create_symbols_file()

    def viable_data_column_names(self):
        return ['High', 'Low', 'Close', 'Volume', 'Value-Change', 'Percent-Change']

    def viable_exchange_names(self):
        exchange_names = list(scrape_API.Eoddata().tab_dict.keys())
        exchange_names.remove('currencies')
        return exchange_names

    # input: list of strings where each is supposedly part of the required company name.
    # output: list of strings containing company symbols that have the input strings in them.
    def get_company_symbol_with_partial_name(self, partial_text_list):
        return stocks_analysis.get_company_symbol_with_partial_name(partial_text_list, self.all_daily_dataframe)

    # input: company_symbols (a list of symbols).
    #        and/or list of strings where each is supposedly part of the required company's name.
    # output: data frame (with the daily data) of the requested_companies.
    def get_specific_companies_df(self, company_symbols):
        from_partial_strings = self.get_company_symbol_with_partial_name(company_symbols)
        company_symbols.extend(from_partial_strings)
        return stocks_analysis.get_specific_companies(self.all_daily_dataframe, company_symbols)

    # input: company_symbols (a list of symbols)
    # output: a dictionary (with the daily data) of the requested_companies.
    def get_specific_companies_dict_list(self, company_symbols):
        return stocks_analysis.get_specific_companies_dict_list(self.all_daily_dataframe, company_symbols)

    # input: column_name, number_of_companies.
    #        number_of_companies to be retrieved from the daily data.
    # output: a data frame of the top number_of_companies in the data frame sorted by column_name.
    #         if bottom=True, returns the bottom companies in the data frame.
    def top_x_companies_by_column(self, column_name, number_of_companies, bottom=False):
        return stocks_analysis.\
            top_x_companies_by_column(self.all_daily_dataframe, column_name, number_of_companies, bottom)


class SectorsDataAnalysisToday(AllDataAnalysisToday):
    def __init__(self, exchange_name):
        AllDataAnalysisToday.__init__(self, exchange_name)
        self.sectors_sorted_df = stocks_analysis.sectors_data_from_daily_file(self.all_daily_dataframe)

    # returns a list of the sectors analysis methods available in stocks_analysis.py
    def analysis_methods_viable_names(self):
        return ['mean', 'volume weighted mean', 'describe', 'max',
                'min', 'sum', 'median', 'mad']

    def get_sector_names_list(self):
        sectors = self.sectors_sorted_df['Sector'].tolist()
        return sorted(list(set(sectors)))

    # input: self explanatory.
    # output: a data frame of the method result values of the chosen column for each sector.
    def analyse_column_of_sectors(self, column_name, method):
        return stocks_analysis.analyse_column_of_sectors(self.sectors_sorted_df, column_name, method)

    # takes the output of analyse_column_of_sectors and converts it to list of strings.
    # was useful in tkinter gui, but probably useless in any other way.
    def analyse_column_of_sectors_strings_list(self, column_name, method):
        df = self.analyse_column_of_sectors(column_name, method)
        return stocks_analysis.analyse_column_of_sectors_strings_list(df)

    # input: sector_name, column_name, number_of_companies, bottom.
    #        number_of_companies to be retrieved from the daily data.
    # output: a data frame of the top number_of_companies in
    #               the requested sector data frame sorted by column_name.
    #               if bottom=True, returns the bottom companies in the data frame.
    def top_x_companies_in_sector_by_column(self, sector_name, column_name, number_of_companies, bottom=False):
        return stocks_analysis.\
            top_x_companies_in_sector_by_column(self.all_daily_dataframe,
                                                sector_name, column_name, number_of_companies, bottom)

