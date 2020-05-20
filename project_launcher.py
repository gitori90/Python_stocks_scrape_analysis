##############################################################
#
#
#   call the functions of stocks_backend_API from here
#
#
##############################################################

import pandas as pd
from backend import stocks_backend_API as backend_API

WORDS_OF_INTEREST = ['corp', 'inc', 'group', 'us', 'china', 'plc']

"""omg_dict = backend_API.StocksSectionAdvanced().top_x_words_in_all_dataframes_dict(40)
print(omg_dict)"""


df = backend_API.StocksSectionAdvanced().top_x_companies_by_column_with_specific_word_dataframe('corp', 'Value-Change', 50)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

"""
exchange_names_list = backend_API.StocksSectionBasic().get_exchange_names_list()
valid_column_names_list = backend_API.StocksSectionBasic().valid_column_names_list()
methods_list = backend_API.StocksSectionBasic().analysis_methods_viable_names_list()
sectors_list = backend_API.StocksSectionBasic().get_sector_names_list(exchange_names_list[0])


sector_name = 'All'
col_name = valid_column_names_list[0]
numb_of_companies = 9
top_or_bottom = 'top'
method = methods_list[0]

print(sectors_list)

print('#############################################################')

print(sector_name)
print(col_name)
print(numb_of_companies)
print(top_or_bottom)
print(method)
print('#############################################################')

for exchange_name in exchange_names_list:
    print('EXCHANGE: ', exchange_name)
    top1 = backend_API.StocksSectionBasic().\
        top_companies_dataframe(sector_name, col_name, numb_of_companies, top_or_bottom, exchange_name)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ "TOP" RESULTS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(top1)

    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ "METHOD" RESULTS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    analyse = backend_API.StocksSectionBasic().analyse_column_of_sectors_dataframe(col_name, method, exchange_name)
    print(analyse)

    #count, division = np.histogram(top1['Name'])
    # print(count)


    division = top1.hist(column='Name')

    print(division)
    break
"""