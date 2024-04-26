from matplotlib import pyplot as plt
import pandas as pd
class Visualizer():
    def __init__(self):
        # maybe some general settings like style and window size
        # also the path where the plots are saved
        pass
        
    def merge_participant_dfs(self, dataframes:list):
        
        if len(dataframes) != 3:
            raise ValueError("Expected 3 dataframes, got: ", len(dataframes))
        else:
            
            def correct_dataframes(dataframes, cur_last):
                # if dataframes is list
                df_list = []
                if type(dataframes) == list:
                    for df, info in dataframes:
                        pos, col = info.split("_")
                        
                        if col == "out":
                            df["people_out"] = df["people_out"] - df.iloc[0]["people_out"]
                            df["people_inside"] =  (-df["people_out"]) + cur_last
                            cur_last = cur_last + df.iloc[-1]["people_inside"]
                            df_list.append(df)
                            
                            
                        elif col == "in":
                            if cur_last != 0:
                                raise ValueError("First dataframe should start with 0 people inside")
                            
                            df["people_inside"] = df["people_in"] + cur_last
                            cur_last =  df.iloc[-1]["people_inside"]
                            df_list.append(df)

                            
                        else:
                            if pos == "before":
                                df["people_inside"] = df["people_inside"] - df.iloc[0]["people_inside"] + cur_last
                                cur_last = df.iloc[-1]["people_inside"]
                                df_list.append(df)
                                
                            if pos == "after":
                                df["people_inside"] = df["people_inside"] + cur_last
                                cur_last = df.iloc[-1]["people_inside"]
                                df_list.append(df)
            
                    return df_list, cur_last
                                
                else:
                    dataframes["people_inside"] = dataframes["people_inside"] + cur_last
                    cur_last = dataframes.iloc[-1]["people_inside"]
                    return [dataframes], cur_last
            
            df_list = []
            cur_last = 0
            for x in dataframes:        
                dfs, cur_last = correct_dataframes(x, cur_last)
                df_list += dfs

        return pd.concat(df_list).reset_index(drop=True)
    
    def plot_participants(self, save_path, participants=None, 
                        df_list=None, control=None, 
                        extrema=None, horizontal_lines=[]):
        
        if (participants is None) and (df_list is None) and (control is None):
            raise ValueError("Either participants, df_list or control must be provided")
        
        else:
            legend = []
            fig, ax = plt.subplots(figsize=(10, 5))
            
            if participants is not None:
                participants.plot(x="time", y="people_inside", kind="line", ax=ax)
                legend.append("participants")
            
            if df_list is not None:
                for df in df_list:
                    df.plot(x="time", y="people_inside", kind="line", ax=ax)
                    legend.append("control")
            
            if control is not None:
                control.plot(x="time", y="people_inside", kind="line", ax=ax)
                legend.append("simple")
                
            if extrema is not None:
                extrema.plot(x="time", y="min", kind="scatter", ax=ax, c="r")
                legend.append("min")
                extrema.plot(x="time", y="max", kind="scatter", ax=ax, c="g")
                legend.append("max")
            
            
            if len(horizontal_lines) > 0:
                for x, c, l in horizontal_lines:
                    plt.axhline(y = x, c=c, linestyle = '-')
                    legend.append(f"{l}")
                    
            plt.legend(legend)
            plt.grid()
            fig.savefig(save_path)