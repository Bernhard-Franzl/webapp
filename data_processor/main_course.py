from course_analysis import CourseAnalyzer



room_name = "HS 18"
data_folder = ""


worker = CourseAnalyzer(room_name, data_folder)

print(worker.df_dates)