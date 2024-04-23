from preprocessing import Preprocessor
from analysis import Analyzer
from datetime import datetime as dt
from visulization import Visualizer

#########  Constants #########
room_to_id ={"HS18":0, "HS19":1}
door_to_id = {"door1":0, "door2":1}
data_path = "/home/berni/data_04_23"

#########  Data Preprocessing #########
worker = Preprocessor(data_path, room_to_id, door_to_id)
listy_dirs = worker.get_list_of_data_dirs()
data = worker.accumulate_raw_data(listy_dirs)
cleaned_data = worker.clean_raw_data(data)


#########  Data Analysis #########
# variables
room_id = 0
door_id = 0
#2024-04-08 9:00:00

year = 2024
month = 4
day = 8

start_time = dt(year, month, day, 12, 00, 0)
end_time = dt(year, month, day, 13, 30, 0)
first, last = True, False


analyzer = Analyzer(cleaned_data)
data_analysis = analyzer.filter_by_room(cleaned_data, room_id)
data_analysis = analyzer.filter_by_door(data_analysis, door_id)
#data_analysis = analyzer.filter_by_time(data_analysis, start_time, end_time)

#data_sophisticated, _ = analyzer.calc_patricipants_sophisticated(data_analysis, start_time, end_time, first, last)


#data_control = analyzer.calc_inside_per_min(data_analysis, n=2)
#print(data_control.head())
#mode = analyzer.calc_mode_inside(data_control)
#description = analyzer.describe_inside(data_control)
#print(description)
#print()
#print()

before, during, after = analyzer.calc_participants(data_analysis, 
                                          start_time=start_time,
                                          end_time=end_time,
                                          first=first,
                                          last=last)
#print(data_control)

#data_control, extrema, count_in, count_out = analyzer.calc_participants_extrema(data_analysis, 
#                                                  start_time, end_time,
#                                                  first, last)
#print(data_analysis)

#########  Data Visualization #########
visard = Visualizer()

#legend = ["simple aggregation"] + [f"extrema {i}" for i in range(1, len(df_list)+1)] + ["extrema"]
#visard.plot_line( [data_control] + df_list,
#                legend,
#                "time", "people_inside", f"{start_time}", extrema)

#[(description["mean"],"r"), 
#                                                                             (description["50%"],"b"), 
#                                                                             (mode, "g")]

data_list = [ before, during, after] 
legend = ["before", "during", "after"]
visard.plot_line( data_list, 
                 legend ,
                 "time", "people_inside", f"{start_time}", horizontal_lines=[])


# TODO:
# - from signal calculate something like: "participants" 
# We need one number representing the participants of course(defined time span)

# at some point introduce time limit for the calc_participants_extrema function

# - make a filter that checks for unplausible signal:
# E.g: if one person enters and one leaves after 1 second in the same door

# - make viszalization interactive (plotly)

# - incorporate measures from the manual control data

# - restructure data cleaning methods

# - make data cleaning more effective (once we have course data -> remove everything 50 minutes before first and after last)

# - Add to processing pipeline:

"""
merge1 = data1.copy(deep=True)
merge1["Time"] = merge1["Time"].dt.floor("min")

merge2 = data2.copy(deep=True)
merge2["Time"] = merge2["Time"].dt.floor("min")

# concat both dataframes
merged = pd.concat([merge1, merge2], ignore_index=True).reset_index(drop=True)
# drop unnecessary columns
columns_to_keep = ["Time", "Entering"]
columns_to_drop = [col for col in merged.columns if col not in columns_to_keep]
merged = merged.drop(columns=columns_to_drop)
merged

def calc_inside_permin(dataframe):
    
    df = dataframe.copy(deep=True).sort_values(by="Time").reset_index(drop=True)   
    
    df["people_counter"] = df.apply(lambda x: 1 if x["Entering"] == "True" else -1, axis=1)
    df_aggregated = df.groupby(by="Time").sum().reset_index()  

    
    df_inside = df_aggregated.copy(deep=True)
    df_inside["inside"] = df_aggregated["people_counter"].cumsum()
    
    # correct for an error
    df_inside["inside"] += 19
    return df_inside

df_inside = calc_inside_permin(merged)[:50]
df_inside
"""


# first lecture slot 8:30 - 10:00
#start_time, end_time = dt(year, month, day, 8, 30, 0), dt(year, month, day, 10, 0, 0)
#first, last = True, False
## second lecture slot 10:15 - 11:45
#start_time, end_time = dt(year, month, day, 10, 15, 0), dt(year, month, day, 11, 45, 0)
#first, last = True, False
# third lecture slot 12:00 - 13:30
#start_time, end_time = dt(year, month, day, 12, 0, 0), dt(year, month, day, 13, 30, 0)
#first, last = True, False
# fourth lecture slot 13:45 - 15:15
#start_time, end_time = dt(year, month, day, 13, 45, 0), dt(year, month, day, 15, 15, 0)
#first, last = False, False
# fifth lecture slot 15:30 - 17:00
#start_time, end_time = dt(year, month, day, 15, 30, 0), dt(year, month, day, 17, 0, 0)
#first, last = False, False
# sixth lecture slot 17:15 - 18:45