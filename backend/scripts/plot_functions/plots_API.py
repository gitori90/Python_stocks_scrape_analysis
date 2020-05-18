import backend.scripts.plot_functions.plot_functions as plots


# input: self explanatory.
#        file_name_addition is another string to add to the graph image's file name.
def bar_plot(data_frame, x_col_name, y_col_name, title, plot_file_name, show_or_save):
    plots.bar_plot(data_frame, x_col_name, y_col_name, title, plot_file_name, show_or_save)


# input: 1. data frame of the resulted method applied to the sectors (sector names are the columns).
#        2. name of the method applied to the data.
#        3. the name of the data column the method acted on.
# return value: none. calls for bar_plot to show or save the graph.
def plot_sectors_analysis_today(analysis_df, method_name, column_name):
    plots.plot_sectors_analysis_today(analysis_df, method_name, column_name)
