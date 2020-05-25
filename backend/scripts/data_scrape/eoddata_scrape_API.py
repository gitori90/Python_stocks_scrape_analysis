import backend.scripts.data_scrape.path_finding_functions as path_finding_functions
import backend.scripts.data_scrape.eodatta_scrape_symbols as symbols_scrape
import backend.scripts.data_scrape.eoddata_scrape_daily as daily_scrape


class Eoddata:
    def __init__(self):
        sheet_letters_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sheet_letters_london = "03456789" + sheet_letters_alphabet
        sheet_letters_singapore = "13456789" + sheet_letters_alphabet
        self.stocklist = r"http://eoddata.com/stocklist/"

        self.tab_dict = {'nasdaq': "NASDAQ/",
                         'currencies': 'FOREX/',
                         'london': 'LSE/',
                         'american': 'AMEX/',
                         'singapore': 'SGX/'}

        self.tab_sheet_letters = {'nasdaq': sheet_letters_alphabet,
                                  'currencies': sheet_letters_alphabet,
                                  'london': sheet_letters_london,
                                  'american': sheet_letters_alphabet,
                                  'singapore': sheet_letters_singapore}


class EoddataExchange(Eoddata):

    def __init__(self, exchange_tab):
        Eoddata.__init__(self)
        self.exchange_title = exchange_tab
        self.section_root_list_url = self.stocklist + self.tab_dict[exchange_tab]

    def set_daily_data_file_name(self):
        file_path = path_finding_functions.set_daily_data_file_path(self.exchange_title)
        return file_path

    def create_symbols_file(self):
        sheet_letter_list = self.tab_sheet_letters[self.exchange_title]
        symbols_scrape.symbols_and_names_to_excel(self.section_root_list_url, self.exchange_title, sheet_letter_list)

    def create_daily_data(self):
        sheet_letter_list = self.tab_sheet_letters[self.exchange_title]
        daily_scrape.create_daily_data(self.section_root_list_url, self.exchange_title, sheet_letter_list)

