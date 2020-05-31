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
def run_dict_test(company_symbol):
    print(company_symbol)
    print("delay = 1:")
    testdict = advanced_analysis.build_companies_counter_dict_for_specific_company('nasdaq',
                                                                                        company_symbol,
                                                                                       'Value-Change', 1)
    sort_testdict = sorted(testdict.items(), key=lambda x: x[1], reverse=True)
    j = 0
    for i in sort_testdict:
        j += 1
        print(i[0], i[1])
        if j > 20:
            break

    print("################################")

    print("delay = 0:")
    testdict2 = advanced_analysis.build_companies_counter_dict_for_specific_company('nasdaq',
                                                                                        company_symbol,
                                                                                       'Value-Change', 0)

    sort_testdict2 = sorted(testdict2.items(), key=lambda x: x[1], reverse=True)
    j = 0
    for i in sort_testdict2:
        j += 1
        print(i[0], i[1])
        if j > 20:
            break
    print("################################")


with concurrent.futures.ThreadPoolExecutor() as executor:
    x = executor.map(run_dict_test, ['AMZN', 'SEDG'])












"""dict = advanced_analysis.create_companies_zero_dict('nasdaq')
print(dict)"""




"""dataframe_of_top_by_column = backend_API.StocksSectionAdvanced().\
    top_x_companies_by_column_with_specific_word_dataframe('corp',
                                                           'Percent-Change', 20, 'bottom')

print(dataframe_of_top_by_column)"""



