import pandas as pd
import re


def string_strip(string):
    return string.strip()


def strip_coma(string):
    return string.replace(",", "")


def remove_non_numerics(string):
    string = str(string)
    pure_numeric = re.sub('[^0-9]', '', string)
    return pure_numeric


# use .strip() on all strings in the data frame.
# uses string_strip function in the pandas's .apply() method.
def trim_data_frame(data_frame):
    for col in data_frame.columns:
        stripped_col = col.strip()
        data_frame.rename(columns={col: stripped_col}, inplace=True)
        try:
            data_frame[stripped_col] = data_frame[stripped_col].apply(string_strip)
        except:
            pass
    return data_frame


# removes non-numeric characters from numeric strings.
# input: data frame and list of some of its column names.
# return value: none. the modifications are in-place.
def hybrid_col_to_number(data_frame, column_name):
    data_frame[column_name] = data_frame[column_name].apply(remove_non_numerics)


# input: the raw data frame, column names lists which contain plain text and shouldnt be modified,
#        and hybrid column names which contain numbers with a letter or sign to be removed.
# return value: the modified data frame.
def convert_data_frame_numbers_to_float(data_frame, text_columns='nan', hybrid_columns='nan'):

    if text_columns != 'nan':
        saved_columns = {}
        # save description columns to re-insert after the pd.to_numeric() deletes them:
        for name in text_columns:
            saved_columns[name] = data_frame[name]

    if hybrid_columns != 'nan':
        for column in hybrid_columns:
            hybrid_col_to_number(data_frame, column)

    for header in data_frame.columns:
        try:
            data_frame[header] = data_frame[header].apply(strip_coma)
        except:
            pass
        data_frame[header] = pd.to_numeric(data_frame[header], errors='coerce')

    if text_columns != 'nan':
        for name in saved_columns.keys():
            data_frame[name] = saved_columns[name]

    return data_frame


def dict_to_data_frame(dictionary):
    data_frame = pd.DataFrame()
    for key in dictionary.keys():
        data_frame[key] = [dictionary[key]]
    return data_frame


def replace_all_nan(sheet_df):
    #sheet_df = sheet_df.fillna(value='--')
    for col in sheet_df.columns:
        sheet_df[col].replace('nan', '--', inplace=True)
    return sheet_df

"""
def set_user_data_excel_path():
    dir_path = r".\project_files"
    file_name = r"\saved_user_data.xlsx"
    return dir_path + file_name


def write_user_data_to_excel(sheet_name, data_frame):
    file_path = set_user_data_excel_path()
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    data_frame.to_excel(writer, sheet_name=sheet_name)
    writer.save()


def read_user_data_sheet(sheet_name):
    file_path = set_user_data_excel_path()
    data_sheet = pd.ExcelFile(file_path).parse(sheet_name)
    return data_sheet
"""