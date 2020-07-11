import pandas as pd
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.analysis.advanced_utils as advanced_utils
import backend.scripts.analysis.stocks_analysis as stocks_analysis


def load_last_predictions(market_name):
    last_predictions_path = path_finding_functions.get_last_operations_file_path(market_name)
    print("Last predictions file's path: ", last_predictions_path)
    sheet1_name = 'Growth'
    sheet2_name = 'Shrink'
    growth_dataframe = pd.read_excel(last_predictions_path, sheet_name=sheet1_name)
    shrink_datafre = pd.read_excel(last_predictions_path, sheet_name=sheet2_name)

    return growth_dataframe, shrink_datafre


def get_last_daily_dataframe(market_name):
    last_daily_path = path_finding_functions.get_last_daily_data_file_path(market_name)
    print("Last daily file's path: ", last_daily_path)
    last_daily_dataframe = stocks_analysis.all_companies_data_frame(last_daily_path)
    return last_daily_dataframe


def get_today_percent_values_dataframe(last_daily_dataframe, predictions_dataframe):
    columns = ['Symbol', 'Percent-Change']
    today_values_dataframe = pd.DataFrame(columns=columns)
    predictions_symbols_list = predictions_dataframe['Symbol'].tolist()
    for symbol in predictions_symbols_list:
        today_symbol_serie = last_daily_dataframe[last_daily_dataframe['Symbol'] == symbol]
        today_symbol_serie = today_symbol_serie.drop(columns=[x for x in today_symbol_serie.columns if x not in columns])
        today_values_dataframe = today_values_dataframe.append(today_symbol_serie, ignore_index=True)

    return today_values_dataframe


def write_results_dataframes_today_to_excel(exchange_name, growth_dataframe, shrink_dataframe):
    file_path = path_finding_functions.set_operations_results_file_path(exchange_name)
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    growth_dataframe.to_excel(writer, sheet_name='Growth')
    shrink_dataframe.to_excel(writer, sheet_name='Shrink')
    writer.save()


def evaluate_predictions_datframe(market_name):
    print("Evaluating predictions for {}...".format(market_name))
    last_daily_dataframe = get_last_daily_dataframe(market_name)
    growth_dataframe, shrink_dataframe = load_last_predictions(market_name)

    today_growth_values_dataframe = get_today_percent_values_dataframe(last_daily_dataframe, growth_dataframe)
    today_shrink_values_dataframe = get_today_percent_values_dataframe(last_daily_dataframe, shrink_dataframe)

    growth_dataframe["Real-Percent-Change"] = today_growth_values_dataframe['Percent-Change']
    shrink_dataframe["Real-Percent-Change"] = today_shrink_values_dataframe['Percent-Change']
    growth_dataframe.drop(columns=['Unnamed: 0'], inplace=True)
    shrink_dataframe.drop(columns=['Unnamed: 0'], inplace=True)

    write_results_dataframes_today_to_excel(market_name, growth_dataframe, shrink_dataframe)






