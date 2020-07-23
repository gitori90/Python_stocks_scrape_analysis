import backend.scripts.analysis.advanced_analysis as advanced_analysis
import backend.scripts.analysis.stocks_analysis as stocks_analysis


class GlobalConnections:
    def __init__(self):
        pass

    def top_x_words_in_dataframe_dict(self, dataframe, top_number):
        top_dict = advanced_analysis.top_x_words_in_dataframe_dict(dataframe, top_number)
        return top_dict

    def top_x_words_in_all_dataframes_dict(self, top_number):
        all_dataframes = advanced_analysis.all_exchanges_dataframes()
        top_dict = self.top_x_words_in_dataframe_dict(all_dataframes, top_number)
        return top_dict

    def top_x_companies_by_column_with_specific_name_dataframe\
                    (self, specific_name, column_name, number_of_companies, bottom_or_top=False):

        all_dataframes = advanced_analysis.all_exchanges_dataframes()

        names_filtered_dataframe = stocks_analysis.\
            filter_companies_dataframe_by_partial_name(all_dataframes, specific_name)

        dataframe_of_top_by_column = stocks_analysis.\
            top_x_companies_by_column(names_filtered_dataframe, column_name, number_of_companies, bottom_or_top)

        return dataframe_of_top_by_column

    def analyse_method_on_all_dataframes_partial_name(self, partial_name, method_name, column_name):
        method_result = advanced_analysis.\
            analyse_method_on_all_dataframes_partial_name(partial_name, method_name, column_name)
        return method_result


    def create_ascending_points_dataframe(self, market_name, delay_days,
                                          volume_percent_filter=0, sign_or_value='value',
                                          column_name='Percent-Change', number_of_iterations=1):
        advanced_analysis.create_points_dataframe(market_name, delay_days,
                            volume_percent_filter, 'ascend', column_name, sign_or_value, number_of_iterations)

    def create_descending_points_dataframe(self, market_name, delay_days,
                                           volume_percent_filter=0, sign_or_value='value',
                                           column_name='Percent-Change', number_of_iterations=1):
        advanced_analysis.create_points_dataframe(market_name, delay_days,
                            volume_percent_filter, 'descend', column_name, sign_or_value, number_of_iterations)
