import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
from collections import Counter
import re


def all_exchanges_dataframes():
    exchange_names = stocks_API.viable_exchange_names()
    all_dataframe = pd.DataFrame()
    for exchange in exchange_names:
        exchange_dataframe = stocks_API.AllDataAnalysisToday(exchange).all_daily_dataframe
        all_dataframe = all_dataframe.append(exchange_dataframe)

    return all_dataframe


def remove_all_nonalphabetic_from_string(str):
    regex = re.compile('[^a-zA-Z]')
    clean_str = regex.sub('', str)
    return clean_str


def name_to_alphabetic_words_list(company_name):
    alphabet_words_list = []
    replace_a_char = company_name.replace(".", " ")
    space_split = replace_a_char.split()
    for word in space_split:
        cleaned_word = remove_all_nonalphabetic_from_string(word)
        alphabet_words_list.append(cleaned_word)

    return alphabet_words_list


def all_words_in_all_company_names_dataframe_counter():
    all_frames = all_exchanges_dataframes()
    all_words = []
    name_list = all_frames['Name'].tolist()

    for company_name in name_list:
        try:
            words_in_company = name_to_alphabetic_words_list(company_name)
            for i in range(len(words_in_company)):
                try:
                    words_in_company.remove('')
                except ValueError:
                    break
            all_words.extend(words_in_company)
        except TypeError:
            continue
        except AttributeError:
            continue

    counts = Counter(all_words)
    return counts


def top_x_in_count_dictionary(counter_dict, top_number):
    sorted_dict = sorted(counter_dict, key=counter_dict.get, reverse=True)
    top_dict = {}
    for i in range(top_number):
        key = sorted_dict[i]
        top_dict[key] = counter_dict[key]

    return top_dict


def top_x_words_in_all_dataframes_dict(top_number):
    count_dict = all_words_in_all_company_names_dataframe_counter()
    top_dict = top_x_in_count_dictionary(count_dict, top_number)
    return top_dict


def analyse_method_on_all_dataframes_partial_name(partial_names_list, method_name, column_name):
    all_frames = all_exchanges_dataframes()
    filtered_companies_dataframe = stocks_analysis.\
        filter_companies_dataframe_by_partial_name(all_frames, partial_names_list)
    method_result = stocks_analysis.\
        pandas_analysis_functions_dict(method_name, filtered_companies_dataframe, column_name)

    return method_result



