import pandas as pd
from signal_analysis import SignalAnalyzer

class CourseAnalyzer():
    
    def __init__(self, room_name, data_folder):
        
        self.df_courses = self.import_from_csv(data_folder + room_name + "_courses.csv")
        self.df_dates = self.import_from_csv(data_folder + room_name + "_dates.csv")
        self.clean_dates()

    def import_from_csv(self, path):
        try:
            data = pd.read_csv(path)
            return data
        except:
            raise("Error: Could not read file. Please check if the file exists and the path is correct!")
        
    def clean_dates(self):
        
        self.df_dates["start_time"] = self.df_dates.apply(lambda x: x["Wochentag"] + " " + x["Datum"] + " " + x["Startzeit"], axis=1)
        self.df_dates["start_time"] = pd.to_datetime(self.df_dates["start_time"], format="%a. %d.%m.%y %H:%M")
        
        
    def filter_by_date(self, date):
        return self.df_dates[self.df_dates["date"] == date]