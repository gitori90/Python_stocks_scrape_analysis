##############################################################
#
#
#           CALL FUNCTIONS FROM stocks_backend_API
#
#
##############################################################

from backend import stocks_backend_API as backend_API

# EXECUTE TO SCRAPE ALL DAILY DATA:
backend_API.StocksSectionAdvanced().scrape_all_daily_markets_data()

