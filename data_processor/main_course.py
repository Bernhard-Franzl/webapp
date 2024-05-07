from course_analysis import CourseAnalyzer
from datetime import datetime
from visulization import Visualizer
from matplotlib import pyplot as plt

#TODO:
# - people leaving early -> "diff inside" or "people out"??
# - column placement not yet correct
# - Add subtitle with additional information
# - Deal with irregular courses
# - Implement proper hover text
# - Fix distance between subplots


room_name = "HS 19"
data_dir_course = "/home/berni/github_repos/webapp"
data_dir_signal = "/home/berni/data_05_02"

worker = CourseAnalyzer(room_name=None, 
                        data_dir_course=data_dir_course,
                        data_dir_signal=data_dir_signal)


start_time = datetime(2024, 4, 8, 0, 0, 0)
end_time = datetime(2024, 4, 15, 23, 59, 0)

# must happen before handling combined courses
df = worker.filter_df_by_timestamp(dataframe=worker.df_combined, 
                                   start_time=start_time, 
                                   end_time=end_time)



# must happen before calculating participants
df = worker.handle_combined_courses(df)


#course_numbers = list(df[ "course_number"].unique())[:]

## incorporate relative values
df_result, df_list, _, _ = worker.calc_course_participants(df, mode="max")

# must be given the signal during course time -> wise to do after calc_course_participants
# or we need calc inside per min first


worker.calc_dynamics_all_dates(df_result, df_list)

#visard = Visualizer()

#visard.plot_dynamics(attendance_dynamics)













#df_result = worker.calc_relative_registered(df_result)
#df_result = worker.calc_relative_capacity(df_result)

#visard = Visualizer()

#visard.plot_multiple_courses_bars(dataframe=df_result,
#                                  course_numbers=course_numbers,
#                                  title="Participants per Course Date",
#                                  relative=False)


##print(df_result.columns[[0, 8, 19, 16, 7, 1, 5, 2, 27, 3]])
#mode = "relative_registered"
#visard.plot_multiple_courses_bars(dataframe=df_result,
#                                  course_numbers=course_numbers,
#                                  title="Participants per Course Date",
#                                  mode=mode)

# single course bar chart
#visard.plot_course_bar(dataframe=df_result, 
#                       course_number=course_numbers[0], 
#                       show_relative=True, 
#                       show_before_after=False)
































#for idx in range(len(df_result)):
    
#    df_plot_list = plot_list[idx]
#    df_plotting = visard.merge_participant_dfs(df_plot_list)

#    participants = part_list[idx]
#    horizontal_lines = [(participants[0], "black", " before"),
#                        (participants[1], "gold", " after")]


#    dataframes = df_list[idx]
#    extrema = extrema_list[idx]
#    plot_name = plot_name_list[idx]
    
#    title = "Irregular: " + str(df.iloc[idx]["irregular"])
#    visard.plot_participants(save_path = f"plots/{plot_name}.png",
#                             participants=df_plotting,
#                             df_list = dataframes,
#                             control = None,
#                             extrema = None,
#                             horizontal_lines=horizontal_lines,
#                             title=title)

    
    