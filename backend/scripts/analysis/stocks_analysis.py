import pandas as pd
import backend.scripts.df_utils.data_frame_utilities as dataframe_utils
import backend.scripts.analysis.stocks_analysis_utils as stocks_utils
import re


def all_companies_data_frame(data_file_address):
    data_file = pd.ExcelFile(data_file_address)
    full_daily_list = []
    text_columns = ["Symbol", "Name", "Sector", "Industry"]
    hybrid_columns = ["Volume"]
    for sheet in data_file.sheet_names:
        stripped_dataframe = dataframe_utils.trim_data_frame(data_file.parse(sheet))
        dataframe_with_floats = dataframe_utils.\
            convert_data_frame_numbers_to_float(stripped_dataframe, text_columns, hybrid_columns)
        data_frame_without_nan = dataframe_utils.replace_all_nan(dataframe_with_floats)
        full_daily_list.append(data_frame_without_nan)
    all_companies_dataframe = pd.concat(full_daily_list)
    return all_companies_dataframe


def split_data_frame_by_sectors(data_frame, sector_or_industry):
    sectors_set = set(data_frame[sector_or_industry].to_list())
    data_frame_without_null = {x for x in sectors_set if pd.notna(x)}
    requested_section_dataframes_list = []
    for sector in data_frame_without_null:
        requested_section_dataframes_list.append(data_frame.loc[data_frame[sector_or_industry] == sector])

    return requested_section_dataframes_list


def sectors_data_from_daily_file(all_companies_dataframe):
    all_companies_dataframe.dropna(subset=['Sector'], inplace=True)
    only_sectors_dataframe = all_companies_dataframe.sort_values(by=['Sector', 'Industry'])
    return only_sectors_dataframe


def volume_weighted_mean(data_frame, column_name):
    total_volume = data_frame['Volume'].sum()
    volume_list = data_frame['Volume'].tolist()
    value_list = data_frame[column_name].tolist()
    mean_weighted_by_volume = 0
    for i in range(len(value_list)):
        try:
            mean_weighted_by_volume += value_list[i] * volume_list[i] / total_volume
        except ZeroDivisionError as err:
            print(err)

    return mean_weighted_by_volume


class FunctionsOnDataframe:
    def __init__(self, dataframe, column_name):
        self.dataframe = dataframe
        self.column_name = column_name

    def mean(self):
        return self.dataframe.mean()

    def max(self):
        return self.dataframe.max()

    def min(self):
        return self.dataframe.min()

    def sum(self):
        return self.dataframe.sum()

    def median(self):
        return self.dataframe.median()

    def mad(self):
        return self.dataframe.mad()

    def describe(self):
        return self.dataframe.describe()

    def vol_weighted_mean(self):
        return volume_weighted_mean(self.dataframe, self.column_name)


def pandas_analysis_functions_dict(analysis_function, dataframe, column_name):
    pandas_functions_object = FunctionsOnDataframe(dataframe, column_name)
    usable_functions = {
        'mean': pandas_functions_object.mean,
        'describe': pandas_functions_object.describe,
        'max': pandas_functions_object.max,
        'min': pandas_functions_object.min,
        'sum': pandas_functions_object.sum,
        'median': pandas_functions_object.median,
        'mad': pandas_functions_object.mad,
        'volume_weighted_mean': pandas_functions_object.vol_weighted_mean
    }

    chosen_function = usable_functions[analysis_function]

    requested_result_value = chosen_function()
    return requested_result_value


def analysis_functions_for_sectors_list(column_name, method, sectors_splitted_dataframe):
    method_result_dictionary = {}
    method = method.lower()
    drop_nan_rows_in_columns = ['Volume', column_name]

    for dataframe in sectors_splitted_dataframe:
        no_null_dataframe = dataframe.dropna(subset=drop_nan_rows_in_columns)
        method_result_dictionary[no_null_dataframe['Sector'].tolist()[0]] = \
            pandas_analysis_functions_dict(method, no_null_dataframe[column_name], column_name)

    return method_result_dictionary


"""def analysis_functions_for_sectors_list(column_name, method, sectors_splitted_dataframe):
    method_result_dictionary = stocks_utils.DEFAULT_NAN
    if method.lower() == 'mean':
        mean_value = {}
        for df in sectors_splitted_dataframe:
            no_null_df = df.dropna(subset=[column_name])
            mean_value[no_null_df['Sector'].tolist()[0]] = no_null_df[column_name].mean()
        method_result_dictionary = mean_value

    elif method.lower() == 'volume weighted mean':
        mean_value = {}
        for df in sectors_splitted_dataframe:
            no_null_df = df.dropna(subset=['Volume', column_name])
            mean_value[no_null_df['Sector'].tolist()[0]] = volume_weighted_mean(no_null_df, column_name)
        method_result_dictionary = mean_value

    elif method.lower() == 'describe':
        description = {}
        for df in sectors_splitted_dataframe:
            description[df['Sector'].tolist()[0]] = df[column_name].describe()
        method_result_dictionary = description

    elif method.lower() == 'max':
        max = {}
        for df in sectors_splitted_dataframe:
            max[df['Sector'].tolist()[0]] = df[column_name].max()
        method_result_dictionary = max

    elif method.lower() == 'min':
        min = {}
        for df in sectors_splitted_dataframe:
            min[df['Sector'].tolist()[0]] = df[column_name].min()
        method_result_dictionary = min

    elif method.lower() == 'sum':
        sum = {}
        for df in sectors_splitted_dataframe:
            sum[df['Sector'].tolist()[0]] = df[column_name].sum()
        method_result_dictionary = sum

    elif method.lower() == 'median':
        median = {}
        for df in sectors_splitted_dataframe:
            median[df['Sector'].tolist()[0]] = df[column_name].median()
        method_result_dictionary = median

    elif method.lower() == 'mad':
        mad = {}
        for df in sectors_splitted_dataframe:
            mad[df['Sector'].tolist()[0]] = df[column_name].mad()
        method_result_dictionary = mad

    return method_result_dictionary"""


def analyse_column_of_sectors(sector_data_frame, column_name, method):
    authenticated_column_name = stocks_utils.authenticate_column_name(column_name)
    if authenticated_column_name == stocks_utils.DEFAULT_NAN:
        return stocks_utils.DEFAULT_NAN

    sectors_splitted_dataframe = split_data_frame_by_sectors(sector_data_frame, 'Sector')

    dictionary_of_method_analysis_results = \
        analysis_functions_for_sectors_list(authenticated_column_name, method, sectors_splitted_dataframe)
    dataframe_of_method_analysis_results = dataframe_utils.dict_to_data_frame(dictionary_of_method_analysis_results)

    return dataframe_of_method_analysis_results


def analyse_column_of_sectors_strings_list(sectors_method_dataframe):
    column_string_list = []
    for column_name in sectors_method_dataframe.columns:
        column_string = str(column_name) + "\n" + \
                     str(round(sectors_method_dataframe[column_name].tolist()[0], 2))
        column_string_list.append(column_string)
    return column_string_list


def top_x_companies_by_column(daily_dataframe, column_name, number_of_companies, bottom=False):
    column_name = stocks_utils.authenticate_column_name(column_name)
    dataframe_without_nan = daily_dataframe.dropna(subset=[column_name])
    column_sorted_dataframe = stocks_utils.sort_all_daily_data_by_column(dataframe_without_nan, column_name)
    if bottom is False:
        try:
            requested_sorted_dataframe = column_sorted_dataframe.head(int(number_of_companies))
        except:
            return 0
    else:
        try:
            requested_sorted_dataframe = column_sorted_dataframe.tail(int(number_of_companies))
        except:
            return 0

    return requested_sorted_dataframe


def top_x_companies_in_sector_by_column(all_companies_dataframe, sector_name,
                                        column_name, number_of_companies, bottom=False):
    authenticated_column_name = stocks_utils.authenticate_column_name(column_name)
    sector_name = stocks_utils.authenticate_sector_name(sector_name, all_companies_dataframe['Sector'].tolist())
    if sector_name == stocks_utils.DEFAULT_NAN:
        return stocks_utils.DEFAULT_NAN

    only_sectors_dataframe = sectors_data_from_daily_file(all_companies_dataframe)
    sector_dataframe = only_sectors_dataframe[only_sectors_dataframe['Sector'] == sector_name]
    top_companies = top_x_companies_by_column(sector_dataframe, authenticated_column_name, number_of_companies, bottom)

    return top_companies


def get_specific_companies(all_daily_data, company_symbols_list):
    requested_companies_dataframe = pd.DataFrame()
    for company_symbol in company_symbols_list:
        company_symbol = company_symbol.upper()
        requested_company = all_daily_data[all_daily_data['Symbol'] == company_symbol]
        requested_companies_dataframe = requested_companies_dataframe.append(requested_company)
    return requested_companies_dataframe


def get_company_symbol_with_partial_name(partial_names_list, all_companies_dataframe):
    name_list = all_companies_dataframe['Name'].tolist()
    matched_symbols_list = []
    for partial_text in partial_names_list:
        match_list = stocks_utils.matched_strings_list(name_list, partial_text)
        symbols_list = []
        for matched_name in match_list:
            symbol_string = all_companies_dataframe[all_companies_dataframe['Name'] == matched_name]['Symbol'].to_string()
            regex = re.compile('[^a-zA-Z]')
            symbol_string = regex.sub('', symbol_string)
            symbols_list.append(symbol_string)
        matched_symbols_list.extend(symbols_list)

    return matched_symbols_list


def get_specific_companies_dict_list(all_daily_data_dataframe, company_symbols):
    requested_companies_dict_list = []
    requested_companies_dataframe = get_specific_companies(all_daily_data_dataframe, company_symbols)
    replaced_nan_dataframe = requested_companies_dataframe.fillna(value='--')

    index_list = [i for i in range(len(replaced_nan_dataframe['Symbol'].tolist()))]
    replaced_nan_dataframe.index = index_list  # otherwise there may be duplicate indexes.
    requested_dict = replaced_nan_dataframe.to_dict('index')
    for i in requested_dict:
        requested_companies_dict_list.append(requested_dict[i])

    return requested_companies_dict_list


