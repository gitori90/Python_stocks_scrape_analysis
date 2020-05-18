from backend import stocks_backend_API as backend_API


exchange_names_list = backend_API.StocksSection().get_exchange_names_list()
valid_column_names_list = backend_API.StocksSection().valid_column_names_list()
methods_list = backend_API.StocksSection().analysis_methods_viable_names_list()
sectors_list = backend_API.StocksSection().get_sector_names_list(exchange_names_list[0])


sector_name = sectors_list[0]
col_name = valid_column_names_list[0]
numb_of_companies = 9
top_or_bottom = 'top'



print('#############################################################')

print('All')
print(col_name)
print(numb_of_companies)
print(top_or_bottom)
print('#############################################################')

for exchange_name in exchange_names_list:
    print(exchange_name)
    top1 = backend_API.StocksSection().\
        top_companies_dataframe(sector_name, col_name, numb_of_companies, top_or_bottom, exchange_name)

    print(top1)
