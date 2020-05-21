import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use('Agg')


IMAGES_DIR_PATH = r".\backend\project_files\plots"


#   file_name_addition is another string to add to the graph image's file name.
def bar_plot(data_frame, x_col_name, y_col_name, title, file_name_addition="default", show_or_save='save'):
    data_frame.plot(kind='bar', x=x_col_name, y=y_col_name)
    plt.title(title)
    plt.ylabel(y_col_name)
    plt.tight_layout()
    if show_or_save == 'show':
        plt.show()
    elif show_or_save == 'save':
        dir_path = IMAGES_DIR_PATH
        image_name = r"\{}.jpg".format(file_name_addition)

        plt.savefig(dir_path + image_name)
    plt.close('all')


def plot_sectors_analysis_today(analysis_dataframe, method_name, column_name):
    method_name = method_name.capitalize()
    sectors = list(analysis_df.columns)
    values = analysis_dataframe.values.tolist()

    modified_df = pd.DataFrame()
    modified_df['Sectors'] = sectors
    modified_df[method_name] = values[0]
    bar_plot(modified_df, 'Sectors', method_name,
             method_name.capitalize() + "/" + column_name + " of sectors", 'sectors_analysis', 'save')
