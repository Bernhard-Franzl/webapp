from course_analysis import CourseAnalyzer
from datetime import datetime
from visulization import Visualizer

#TODO:
# - multiple courses bar chart
# - Better title for the plots: "Participants per Course Date" as subtiltle
# - Implementer prober hover text
# - Fix distance between subplots


room_name = "HS 19"
data_dir_course = "/home/berni/github_repos/webapp"
data_dir_signal = "/home/berni/data_04_29"

worker = CourseAnalyzer(room_name=None, 
                        data_dir_course=data_dir_course,
                        data_dir_signal=data_dir_signal)


start_time = datetime(2024, 4, 8, 0, 0, 0)
end_time = datetime(2024, 4, 28, 23, 59, 0)


df = worker.filter_df_by_timestamp(worker.df_combined, start_time, end_time)
print(df)

lva_number = "366.560"
df = worker.filter_df_by_course(df, lva_number)


df_result, _, _, _, _, _= worker.calc_course_participants(df)

visard = Visualizer()

visard.plot_course_participants_bar(dataframe=df_result,
                             file_name = f"{lva_number}.png",
                             title="Participants per Course Date",
                             show_relative=True,
                             show_before_after=False)

































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

    
    