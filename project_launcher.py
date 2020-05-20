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


df = backend_API.StocksSectionAdvanced().top_x_companies_by_column_with_specific_word_dataframe('group', 'Value-Change', 10)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)


result = backend_API.StocksSectionAdvanced().analyse_method_on_all_dataframes_partial_name('group', 'describe', 'Value-Change')
print(result)
