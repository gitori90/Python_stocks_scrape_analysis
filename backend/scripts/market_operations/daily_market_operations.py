import pandas as pd
import backend.scripts.analysis.stocks_analysis as stocks_analysis
import backend.scripts.analysis.stocks_analysis_API as stocks_API
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.analysis.advanced_utils as advanced_utils
import statistics


def company_points_giving_by_filter(requested_points_dataframe, exiled_filtered_points_dataframe,
                                    all_symbols_list, company_symbol, percent_filter=0.8, today_company_value=0):
    # pd.at[] doesnt work here, so i had to take the dataframe apart and recreate it at the end.
    requested_points_dataframe_symbols = list(requested_points_dataframe)
    requested_points_dataframe_points = requested_points_dataframe.iloc[0].tolist()
    requested_points_dataframe_count = requested_points_dataframe.iloc[1].tolist()

    giving_companies_pass_filter = []
    try:
        company_points_giving_serie = exiled_filtered_points_dataframe.loc[[company_symbol]]
    except KeyError:
        print("Captured KeyError, company not in giving points companies list: ", company_symbol)
        print("today_company_value: ", today_company_value)
        return requested_points_dataframe, False

    for symbol_runner in all_symbols_list:
        # ALL THE DIFFERENCE BETWEEN THE CHANCE POINTS AND THE VALUE POINTS IS HERE!

        points = company_points_giving_serie.at[company_symbol, symbol_runner]
        if today_company_value > 0:  # this occurs only when i plug in a different value for it
                                     # in the if statement of the value/sign in the function that calls this1.
            points *= today_company_value

        if points >= percent_filter:
            index = requested_points_dataframe_symbols.index(symbol_runner)

            requested_points_dataframe_points[index] += points
            requested_points_dataframe_count[index] += 1

            if today_company_value == 0:  # THIS IS BUILT DURING THE SIGN POINTS GIVING,
                                          # AND SHOULD BE RETURNED AT THE END OF THE FUNCTION.
                                          # AT THE VALUE ASSIGNMENTS, PASS THIS RETURNED LIST IN
                                          # AS 'all_symbols_list'
                giving_companies_pass_filter.append(symbol_runner)

    updated_requested_points_dict = \
        {requested_points_dataframe_symbols[i]: [requested_points_dataframe_points[i],
                                                 requested_points_dataframe_count[i]]
         for i in range(len(requested_points_dataframe_symbols))}

    updated_requested_points_dataframe = pd.DataFrame(data=updated_requested_points_dict)

    return updated_requested_points_dataframe, giving_companies_pass_filter



def assign_today_points(exchange_dataframe_today, exchange_name, delay_days,
                        col_name, ascend_or_descend, sign_or_value, percent_filter=0.8,
                        values_filtered_symbols_list=['nan']):
    exiled_filtered_points_dataframe = \
        advanced_utils.get_filtered_selected_points_dataframe(exchange_name, ascend_or_descend, sign_or_value, delay_days)

    if sign_or_value == 'value':
        all_symbols_list = values_filtered_symbols_list
        # black_list = advanced_utils.get_companies_black_list(exchange_name)
        # all_symbols_list = [x for x in all_symbols_list if x not in black_list]

    elif sign_or_value == 'sign':
        all_symbols_list = list(exiled_filtered_points_dataframe)

    init_dict_for_dataframe = {symbol: [0, 0] for symbol in all_symbols_list}
    requested_points_dataframe = pd.DataFrame(data=init_dict_for_dataframe)
    giving_companies_pass_filter_total_list = []

    for symbol in all_symbols_list:
        # make sure the indexes are indeed the symbols

        today_company_value = float(exchange_dataframe_today.at[symbol, col_name])

        try:
            today_company_sign = today_company_value/abs(today_company_value)
            if ((today_company_sign > 0 and ascend_or_descend == 'ascend')
                or (today_company_sign < 0 and ascend_or_descend == 'descend')):

                if sign_or_value == 'sign':
                    requested_points_dataframe, giving_companies_pass_filter = \
                        company_points_giving_by_filter(requested_points_dataframe,
                                                        exiled_filtered_points_dataframe,
                                                        all_symbols_list, symbol, percent_filter)
                    if giving_companies_pass_filter is False:
                        print("got false1")
                        continue
                        # for some reason this occurs for companies
                        # that were removed by the volume filtering.
                        # they might appear in the columns but not in the rows.

                    giving_companies_pass_filter_total_list.extend(giving_companies_pass_filter)

                elif sign_or_value == 'value':
                    requested_points_dataframe, giving_companies_pass_filter = \
                        company_points_giving_by_filter(requested_points_dataframe,
                                                        exiled_filtered_points_dataframe,
                                                        all_symbols_list, symbol, 0, today_company_value)
                    if giving_companies_pass_filter is False:
                        print("got false2")
                        continue
                        # for some reason this occurs for companies
                        # that were removed by the volume filtering.
                        # they might appear in the columns but not in the rows.


                else:
                    print("Error input sign_or_value: ", sign_or_value)
                    exit(1)



            else:
                continue

        except ZeroDivisionError:
            continue

    giving_companies_pass_filter_total_list = list(set(giving_companies_pass_filter_total_list))
    requested_points_dataframe = requested_points_dataframe.rename(index={0: 'points', 1: 'companies_count'}).T
    return requested_points_dataframe, giving_companies_pass_filter_total_list


def create_sign_and_value_top_companies_dataframes(exchange_dataframe_today_filtered, exchange_name,
                                                   delay_days, ascend_or_descend, sign_percent_filter,
                                                   top_companies_number):
    today_points_ascend_sign_dataframe, giving_companies_pass_filter = \
        assign_today_points(exchange_dataframe_today_filtered, exchange_name, delay_days,
                            'Percent-Change', ascend_or_descend, 'sign', sign_percent_filter)

    today_points_ascend_sign_dataframe.sort_values(by=['points'], ascending=False, inplace=True)

    top_chance_companies_symbols = today_points_ascend_sign_dataframe.head(top_companies_number).index

    today_points_ascend_value_dataframe, null_list = \
        assign_today_points(exchange_dataframe_today_filtered, exchange_name, delay_days,
                            'Percent-Change', ascend_or_descend, 'value', sign_percent_filter,
                            giving_companies_pass_filter)

    today_points_ascend_value_dataframe.sort_values(by=['points'], ascending=False, inplace=True)

    return today_points_ascend_sign_dataframe, today_points_ascend_value_dataframe, top_chance_companies_symbols


def top_chance_power_dataframe_today(exchange_dataframe_today_filtered, exchange_name,
                                     delay_days, ascend_or_descend, sign_percent_filter, top_companies_number):

    today_points_ascend_sign_dataframe, today_points_ascend_value_dataframe, top_chance_companies_symbols = \
        create_sign_and_value_top_companies_dataframes(exchange_dataframe_today_filtered, exchange_name,
                                                       delay_days, ascend_or_descend, sign_percent_filter,
                                                       top_companies_number)

    probability_col = []
    growth_value_col = []
    companies_voting_number_col = []
    for symbol_in_tops in top_chance_companies_symbols:
        sum_probability = today_points_ascend_sign_dataframe.at[symbol_in_tops, 'points']
        number_of_voting_companies = today_points_ascend_sign_dataframe.at[symbol_in_tops, 'companies_count']
        expected_growth_percent = today_points_ascend_value_dataframe.at[symbol_in_tops, 'points']

        probability_col.append(sum_probability / number_of_voting_companies)
        companies_voting_number_col.append(number_of_voting_companies)
        growth_value_col.append(expected_growth_percent / number_of_voting_companies)

    if ascend_or_descend == 'descend':
        growth_or_shrink = 'Shrink'
    else:
        growth_or_shrink = 'Growth'

    top_chance_power_dataframe = pd.DataFrame(data=
                                              {'Symbol': top_chance_companies_symbols,
                                               'Mean-' + growth_or_shrink + '-Probability(%)': probability_col,
                                               'Mean-Expected-' + growth_or_shrink + '(%)': growth_value_col,
                                               '# Voting-Companies': companies_voting_number_col})

    top_chance_power_dataframe.sort_values(by=['Mean-' + growth_or_shrink + '-Probability(%)'],
                                           ascending=False, inplace=True)

    return top_chance_power_dataframe


def write_top_dataframes_today_to_excel(top_chance_power_dataframe_ascend, top_chance_power_dataframe_descend):
    file_path = path_finding_functions.set_operations_file_path()
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    top_chance_power_dataframe_ascend.to_excel(writer, sheet_name='Growth')
    top_chance_power_dataframe_descend.to_excel(writer, sheet_name='Shrink')
    writer.save()


def top_stocks_today(exchange_name, delay_days, top_companies_number=10, sign_percent_filter=0.8):
    print("Initializing analysis of top_stocks_today.")
    exchange_dataframe_today = stocks_API.AllDataAnalysisToday(exchange_name).all_daily_dataframe

    """exchange_dataframe_today_filtered = \
        advanced_utils.remove_companies_black_list_from_dataframe(exchange_dataframe_today)"""
    exchange_dataframe_today = exchange_dataframe_today.set_index('Symbol')

    top_chance_power_dataframe_ascend = \
        top_chance_power_dataframe_today(exchange_dataframe_today, exchange_name,
                                         delay_days, 'ascend', sign_percent_filter, top_companies_number)

    top_chance_power_dataframe_descend = \
        top_chance_power_dataframe_today(exchange_dataframe_today, exchange_name,
                                         delay_days, 'descend', sign_percent_filter, top_companies_number)

    write_top_dataframes_today_to_excel(top_chance_power_dataframe_ascend, top_chance_power_dataframe_descend)

