import backend.scripts.analysis.advanced_analysis as advanced_analysis


class GlobalConnections:
    def __init__(self):
        pass

    def top_x_words_in_all_dataframes_dict(self, top_number):
        top_dict = advanced_analysis.top_x_words_in_all_dataframes_dict(top_number)
        return top_dict

    def analyse_method_on_all_dataframes_partial_name(self, partial_name, method_name, column_name):
        method_result = advanced_analysis.\
            analyse_method_on_all_dataframes_partial_name(partial_name, method_name, column_name)
        return method_result
