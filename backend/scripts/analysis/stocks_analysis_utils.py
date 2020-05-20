
SITE_COLUMN_NAMES = ['volume', 'high', 'low', 'close', 'value-change', 'percent-change']
DEFAULT_NAN = 'nan'


def authenticate_column_name(column_name):
    space_char = ' '
    minus_char = "-"
    if space_char in column_name:
        column_name = column_name.replace(space_char, minus_char)

    if column_name.lower() not in SITE_COLUMN_NAMES:
        return DEFAULT_NAN
    elif minus_char in column_name:
        column_name = column_name.split(minus_char)
        column_name = column_name[0].lower().capitalize() + minus_char + column_name[1].lower().capitalize()
    else:
        column_name = column_name.lower().capitalize()
    return column_name


def sort_all_daily_data_by_column(daily_dataframe, column_name):
    column_names_sorted_dataframe = daily_dataframe.sort_values(by=[column_name], ascending=False)
    return column_names_sorted_dataframe


def authenticate_sector_name(sector_name, sector_names_list):
    lower_list = [name.lower() for name in sector_names_list]
    try:
        index = lower_list.index(sector_name.lower())
    except:
        return DEFAULT_NAN

    valid_sector_name = sector_names_list[index]
    return valid_sector_name


def matched_strings_list(name_list, partial_text):
    match_list = []

    for name in name_list:
        try:
            if partial_text.lower() in name.lower():
                match_list.append(name)
        except AttributeError:
            continue
    return match_list

