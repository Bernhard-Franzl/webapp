from matplotlib import pyplot as plt

class Visualizer():
    def __init__(self):
        # maybe some general settings like style and window size
        pass
        
    def plot_line(self,dataframes:list, legend:list, x_column, y_column, save_path, extrema):
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        for dataframe in dataframes:
            dataframe.plot(x=x_column, y=y_column, kind="line", ax=ax)
            
        plt.scatter(extrema.time, extrema["min"], c="r")
        plt.scatter(extrema.time, extrema["max"], c="g")

        plt.legend(legend)
        plt.grid()
        fig.savefig(f"plots/{save_path}.png")
        
        