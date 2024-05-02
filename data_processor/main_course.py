from course_analysis import CourseAnalyzer
from datetime import datetime
from visulization import Visualizer

#TODO:
# - multiple courses bar chart
# - Better title for the plots: "Participants per Course Date" as subtiltle
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
end_time = datetime(2024, 5, 1, 23, 59, 0)


df = worker.filter_df_by_timestamp(dataframe=worker.df_combined, 
                                   start_time=start_time, 
                                   end_time=end_time)



course_numbers = list(df["course_number"].unique())[:10]
df = worker.filter_df_by_courses(df, course_numbers)
df = df.drop_duplicates()

df_result, _, _, _, _, _= worker.calc_course_participants(df)


visard = Visualizer()

#visard.plot_multiple_courses_line(dataframe=df_result,
#                                  lva_numbers = course_numbers,
#                                  file_name = "multiple_courses.png",
#                                  title="Participants per Course Date")

visard.plot_multiple_courses_bars(dataframe=df_result,
                                  lva_numbers=course_numbers,
                                  title="Participants per Course Date")

# single course bar chart
# visard.plot_course_bar(dataframe=df_result,
#                             file_name = f"{lva_number}.png",
#                             title="Participants per Course Date",
#                             show_relative=True,
#                             show_before_after=False)

































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

    
    