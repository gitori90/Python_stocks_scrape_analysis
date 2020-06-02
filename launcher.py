##############################################################
#
#
#   call the functions of stocks_backend_API from here
# this is just a script used to play with those functions
#
#
##############################################################
import re
from backend import stocks_backend_API as backend_API
import backend.scripts.analysis.advanced_analysis as advanced_analysis
import backend.scripts.data_scrape.path_finding_functions as path_finding_functions

import threading
import concurrent.futures





"""funny_global = 0

def printer(something):
    global funny_global
    funny_global += 1
    j = 0
    for i in range(100000):
        j += 1
    print(funny_global)
    return something + 100

with concurrent.futures.ThreadPoolExecutor() as executor:
    x = executor.map(printer, [99,98,97,96,95,94,93,92])
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


"""testdict = advanced_analysis.top_x_influenced_by_selected_company_dict('nasdaq',
                                                                       'AMZN', 'Percent-Change', 1, 'rise', 150, 40)
print(testdict)"""


testdict2 = advanced_analysis.\
    selected_companies_percent_connection_strength_dict('nasdaq',
                                                        'AMZN', ["ALEC",'AMRS', 'BEAM', 'MEIP', 'CNTY'],
                                                        1, 'Percent-Change')

print(testdict2)


# EXECUTE TO SCRAPE ALL DAILY DATA:

"""dataframe_of_top_by_column = backend_API.StocksSectionAdvanced().\
    top_x_companies_by_column_with_specific_word_dataframe('corp',
                                                           'Percent-Change', 20, 'bottom')

print(dataframe_of_top_by_column)"""



