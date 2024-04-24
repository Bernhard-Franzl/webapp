from matplotlib import pyplot as plt

class Visualizer():
    def __init__(self):
        # maybe some general settings like style and window size
        pass
        
    def plot_line(self,dataframes:list, legend:list, x_column, y_column, save_path, extrema=None, horizontal_lines=[]):
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        for dataframe in dataframes:
            dataframe.plot(x=x_column, y=y_column, kind="line", ax=ax)

        if extrema is not None:
            extrema.plot(x="time", y="min", kind="scatter", ax=ax, c="r")
            extrema.plot(x="time", y="max", kind="scatter", ax=ax, c="g")
        
        if len(horizontal_lines) > 0:
            for x, c in horizontal_lines:
                plt.axhline(y = x, c=c, linestyle = '-')
                

        plt.legend(legend)
        plt.grid()
        fig.savefig(f"plots/{save_path}.png")
        
        