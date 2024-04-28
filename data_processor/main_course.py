from course_analysis import CourseAnalyzer
from datetime import datetime


room_name = "HS 18"
data_folder = ""


worker = CourseAnalyzer(room_name, data_folder)


start_time = datetime(2024, 4, 8, 0, 0, 0)
end_time = datetime(2024, 4, 14, 23, 59, 0)

df = worker.filter_df_by_timestamp(worker.df_combined, start_time, end_time)
print(df)