import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.analysis.advanced_utils as advanced_utils
import statistics

COMPANIES_BLACK_LIST = ['TRNX']


def remove_companies_black_list_from_dataframe(dataframe):
    for company_symbol in COMPANIES_BLACK_LIST:
        dataframe = dataframe[dataframe['Symbol'] != company_symbol]

    return dataframe


# filtered by COMPANIES_BLACK_LIST
def get_filtered_selected_points_dataframe(exchange_name, ascend_or_descend, sign_or_value, delay_days):
    points_dataframe_file_path = path_finding_functions. \
        get_points_file_path(exchange_name, ascend_or_descend, sign_or_value, delay_days)
    points_dataframe = pd.read_excel(points_dataframe_file_path)
    points_dataframe = points_dataframe.set_index('Unnamed: 0')

    filtered_points_dataframe = points_dataframe.drop(columns=COMPANIES_BLACK_LIST,
                                                      index=COMPANIES_BLACK_LIST,
                                                      errors='ignore')
    return filtered_points_dataframe



def company_points_giving_by_filter(requested_points_dataframe, filtered_points_dataframe,
                                    all_symbols_list, company_symbol, percent_filter=0.8):
    # pd.at[] doesnt work here, so i had to take the dataframe apart and recreate it at the end.
    requested_points_dataframe_symbols = list(requested_points_dataframe)
    requested_points_dataframe_points = requested_points_dataframe.iloc[0].tolist()
    requested_points_dataframe_count = requested_points_dataframe.iloc[1].tolist()

    company_points_giving_serie = filtered_points_dataframe.loc[[company_symbol]]
    for symbol_runner in all_symbols_list:
        # ALL THE DIFFERENCE BETWEEN THE CHANCE POINTS AND THE VALUE POINTS IS HERE!
        # TO CALCULATE THE POINTS FOR THE VALUE CASE, TAKE THE POINTS VAR CREATED JUST BELOW
        # AND MULTIPLY IT BY TODAY'S PERCENT-CHANGE VALUE OF 1 OF THE COMPANIES (decide tomorrow which of them)
        # THEN ADD THAT TO THE 'requested_points_dataframe_points'
        points = company_points_giving_serie.at[company_symbol, symbol_runner]
        if points >= percent_filter:
            index = requested_points_dataframe_symbols.index(symbol_runner)

            requested_points_dataframe_points[index] += points
            requested_points_dataframe_count[index] += 1

    updated_requested_points_dict = \
        {requested_points_dataframe_symbols[i]: [requested_points_dataframe_points[i],
                                                 requested_points_dataframe_count[i]]
         for i in range(len(requested_points_dataframe_symbols))}

    updated_requested_points_dataframe = pd.DataFrame(data=updated_requested_points_dict)

    return updated_requested_points_dataframe
    #return requested_points_dataframe



def assign_today_points(exchange_dataframe_today, exchange_name, delay_days,
                        col_name, ascend_or_descend, sign_or_value, percent_filter=0.8):
    filtered_points_dataframe = \
        get_filtered_selected_points_dataframe(exchange_name, ascend_or_descend, sign_or_value, delay_days)

    all_symbols_list = list(filtered_points_dataframe)

    init_dict_for_dataframe = {symbol: [0, 0] for symbol in all_symbols_list}
    requested_points_dataframe = pd.DataFrame(data=init_dict_for_dataframe)

    for symbol in all_symbols_list:
        # make sure the indexes are indeed the symbols
        today_company_value = float(exchange_dataframe_today.at[symbol, col_name])

        try:
            today_company_sign = today_company_value/abs(today_company_value)
            if ((today_company_sign > 0 and ascend_or_descend == 'ascend')
                or (today_company_sign < 0 and ascend_or_descend == 'descend')):

                if sign_or_value == 'sign':
                    requested_points_dataframe = \
                        company_points_giving_by_filter(requested_points_dataframe,
                                                        filtered_points_dataframe,
                                                        all_symbols_list, symbol, percent_filter)

                elif sign_or_value == 'value':
                    requested_points_dataframe = \
                        company_points_giving_by_filter(requested_points_dataframe,
                                                        filtered_points_dataframe,
                                                        all_symbols_list, symbol, 0)

                else:
                    print("Error input sign_or_value: ", sign_or_value)
                    exit(1)

            else:
                continue

        except ZeroDivisionError:
            continue

    requested_points_dataframe = requested_points_dataframe.rename(index={0: 'points', 1: 'companies_count'}).T
    return requested_points_dataframe


def top_stocks_today(exchange_name, delay_days, sign_percent_filter=0.8, top_companies_number=10):
    exchange_dataframe_today = stocks_API.AllDataAnalysisToday(exchange_name).all_daily_dataframe
    exchange_dataframe_today_filtered = remove_companies_black_list_from_dataframe(exchange_dataframe_today)
    exchange_dataframe_today_filtered = exchange_dataframe_today_filtered.set_index('Symbol')

    today_points_ascend_sign_dataframe = assign_today_points(exchange_dataframe_today_filtered, exchange_name, delay_days,
                                                 'Percent-Change', 'ascend', 'sign', sign_percent_filter)

    # that dataframe should be saved in its own xlsx file:
    today_points_ascend_sign_dataframe.sort_values(by=['points'], ascending=False, inplace=True)

    # thats for later use:
    top_chance_companies_symbols = today_points_ascend_sign_dataframe.head(top_companies_number).index



    today_points_ascend_value_dataframe = \
        assign_today_points(exchange_dataframe_today_filtered, exchange_name, delay_days,
                            'Percent-Change', 'ascend', 'value', sign_percent_filter)

    print(today_points_ascend_value_dataframe)



# ['VTIQW', 'VTIQ', 'NIU', 'FMB', 'NEBU', 'VTIQU', 'TUES', 'CSFL', 'BCLI', 'VRIG']

