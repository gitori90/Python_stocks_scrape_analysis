##############################################################
#
#
#   call the functions of stocks_backend_API from here
# this is just a script used to play with those functions
#
#
##############################################################

from backend import stocks_backend_API as backend_API


dataframe_of_top_by_column = backend_API.StocksSectionAdvanced().\
    top_x_companies_by_column_with_specific_word_dataframe('corp',
                                                           'Percent-Change', 20, 'bottom')

print(dataframe_of_top_by_column)
