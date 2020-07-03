##############################################################
#
#
#
#
##############################################################
import re
from backend import stocks_backend_API as backend_API
import backend.scripts.analysis.advanced_analysis as advanced_analysis
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.market_operations.daily_market_operations as daily_operations

import threading
import concurrent.futures
import inspect







"""def printer(something):


    j = 0
    for i in range(100000):
        j += 1
    return something[0] + something[1]

args = [[1,2], [3,4], [5,6]]

with concurrent.futures.ThreadPoolExecutor() as executor:
    x = executor.map(printer, args)
    for i in x:
        print(i)
        print(type(i))"""

"""for i in range(50):
    thread = threading.Thread(target=printer, args=(i,))
    
    thread.start()
    print(funny_global)
    for thread in threads:
        thread.join()
    print(funny_global)"""


# print(path_finding_functions.get_all_daily_files_paths_in_specific_market('nasdaq'))


"""with concurrent.futures.ThreadPoolExecutor() as executor:
    x = executor.map(run_dict_test, ['AMZN'])"""
# run_dict_test is a function


"""testdict = advanced_analysis.top_x_influenced_by_selected_company_dataframe(['nasdaq',
                                                                       'AMZN', 'Percent-Change', 1, 'ascend', 40])
print(testdict)"""



"""testdict2 = advanced_analysis.\
    selected_companies_percent_connection_strength_dict('nasdaq',
                                                        'AMZN', ["ALEC",'AMRS', 'BEAM', 'MEIP', 'CNTY'],
                                                        1, 'Percent-Change')

print(testdict2)"""




#print(inspect.getframeinfo(inspect.currentframe()).lineno)


"""backend_API.StocksSectionAdvanced().create_ascending_points_dataframe('nasdaq', 1, 20, 'sign')
backend_API.StocksSectionAdvanced().create_descending_points_dataframe('nasdaq', 1, 20, 'sign')

backend_API.StocksSectionAdvanced().create_ascending_points_dataframe('nasdaq', 1, 20, 'value')
backend_API.StocksSectionAdvanced().create_descending_points_dataframe('nasdaq', 1, 20, 'value')"""

# EXECUTE TO SCRAPE ALL DAILY DATA:

"""dataframe_of_top_by_column = backend_API.StocksSectionAdvanced().\
    top_x_companies_by_column_with_specific_word_dataframe('corp',
                                                           'Percent-Change', 20, 'bottom')

print(dataframe_of_top_by_column)"""


daily_operations.top_stocks_today('nasdaq', 1)


