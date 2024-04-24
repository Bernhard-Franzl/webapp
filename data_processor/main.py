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
#day
start_time_int = 1715
end_time_int = 1845

day_list = [8,15,22]
for day in  day_list:

    print(f"#################### f{day}.04.2024 {start_time_int}####################")
    start_time = dt(year, month, day, start_time_int//100, start_time_int%100, 0)
    end_time = dt(year, month, day, end_time_int//100, end_time_int%100, 0)
    
    # set first true if:
    # - first lecture of the day
    # - no lecture before
    # - early termination of the last lecture
    first, last = False, False


    analyzer = Analyzer(cleaned_data)
    data_analysis = analyzer.filter_by_room(cleaned_data, room_id)

    # m is an extremely important parameter -> the one that is used to calculate the extrema
    df_control, df_list, participants, extrema = analyzer.calc_participants(data_analysis, 
                                            start_time=start_time,
                                            end_time=end_time,
                                            first=first,
                                            last=last)
    print()
    print("Participants: ", participants)
    print()
    df_before, df_during, df_after = df_list

    # if high std -> check for outliers, for example courses that end very early!
    # nice to detect irregularities in the data
    description_during = analyzer.describe_inside(df_during)
    print(description_during)

    #########  Data Visualization #########
    visard = Visualizer()
    legend = ["before", "during", "after", "minima", "maxima"]
    visard.plot_line( df_list, 
                    legend ,
                    "time", 
                    "people_inside", 
                    f"{start_time}", 
                    extrema=extrema, 
                    horizontal_lines=[])
        
    # simple + horizontal lines
    #legend = ["simple", "part. before", "part. after"]
    #visard.plot_line( [df_control], 
    #                legend ,
    #                "time", 
    #                "people_inside", 
    #                f"{start_time}", 
    #                extrema=None, 
    #                horizontal_lines=[(participants[0], "r"),
    #                                  (participants[1], "g")])


# TODO:
# - during the calculation of participants construct a signal that shows the participants over time
# we need that for nice viszalization

# - make a filter that checks for unplausible signal:
# E.g: if one person enters and one leaves after 1 second in the same door -> change direction if necessary, maybe in form of a sliding window

# - make viszalization interactive (plotly)

# - incorporate measures from the manual control data
# -> Especially inspect the signals of event type 5 followd by 6 -> could be a person entering that is cut of in the middle of the signal

# - restructure data cleaning methods, restructure api

# DONE:
# - from signal calculate something like: "participants" 
# We need one number representing the participants of course(defined time span)
# Good parameter for m: 3