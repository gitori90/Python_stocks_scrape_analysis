import pandas as pd
from ...df_utils import data_frame_utilities as utils
import backend.scripts.analysis.stocks_analysis as stocks_analysis


def all_currencies_data_frame(data_file_path):
    all_currencies_dataframe = stocks_analysis.all_companies_data_frame(data_file_path)
    return all_currencies_dataframe


