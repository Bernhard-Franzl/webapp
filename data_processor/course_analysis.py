import pandas as pd
from signal_analysis import SignalAnalyzer
from datetime import datetime
import locale

class CourseAnalyzer():
    

    def __init__(self, room_name, data_folder):
        
        locale.setlocale(locale.LC_ALL, 'de_AT.utf8')
        self.room_name = room_name
        self.data_folder = data_folder
        
        self.initialize_courses()
        
        self.initialize_dates()    

        self.df_combined = self.add_course_info(self.df_dates)
        
    ###### Basic Methods #####
    def import_from_csv(self, path):
        try:
            data = pd.read_csv(path)
            return data
        except:
            raise("Error: Could not read file. Please check if the file exists and the path is correct!")
        
    def format_dates(self):
        
        self.df_dates["start_time"] = self.df_dates.apply(lambda x: x["Wochentag"] + " " + x["Datum"] + " " + x["Startzeit"], axis=1)
        self.df_dates["start_time"] = self.df_dates["start_time"].apply(lambda x: datetime.strptime(x, "%a. %d.%m.%y %H:%M"))
        
        self.df_dates["end_time"] = self.df_dates.apply(lambda x: x["Wochentag"] + " " + x["Datum"] + " " + x["Endzeit"], axis=1)
        self.df_dates["end_time"] = self.df_dates["end_time"].apply(lambda x: datetime.strptime(x, "%a. %d.%m.%y %H:%M"))
        
        self.df_dates.drop(["Datum", "Startzeit", "Endzeit"], axis=1, inplace=True)
    
    def get_course(self):
        return self.df_courses
    
    def get_dates(self):
        return self.df_dates    
    
    def rename_columns(self, dataframe, old_names, new_names):
        df = dataframe.copy(deep=True)
        df.rename(columns=dict(zip(old_names, new_names)), inplace=True)
        return df
    
    def export_to_csv(self, dataframe, path):
        dataframe.to_csv(path, index=False)
        
    def export_dates(self, name):
        self.export_to_csv(self.df_dates, self.data_folder + name + "_dates.csv")
        
    def export_courses(self, name):
        self.export_to_csv(self.df_courses, self.data_folder + name + "_courses.csv")
        
    ###### Dataframe Initialization ######
    def initialize_courses(self):
        self.df_courses = self.import_from_csv(self.data_folder + self.room_name + "_courses.csv")
        self.df_courses = self.rename_columns(self.df_courses, 
                                              ["LVA-Nr.", "LVA-Titel", "Typ", "Art", "LeiterIn", "Sem.", "ECTS", "SSt."], 
                                              ["course_number", "course_name", "type", "kind", "lecturer", "semester", "ects", "sst"])
        self.df_courses.drop("Nächster Termin", axis=1, inplace=True)
        
    def initialize_dates(self):
        self.df_dates = self.import_from_csv(self.data_folder + self.room_name + "_dates.csv")
        self.format_dates()
        self.df_dates = self.rename_columns(self.df_dates,
                                            ["LVA-Nummer", "Wochentag", "Ort", "Anmerkung"],
                                            ["course_number", "weekday", "room", "note"])

    ###### Filter Dataframes ######
    def filter_df_by_timestamp(self, dataframe, start_time, end_time):
        # only show courses betwen start and end time
        df = dataframe.copy(deep=True)
        df = df[(df["start_time"] >= start_time) & (df["end_time"] <= end_time)]
        df = df.sort_values(by="start_time").reset_index(drop=True)
        return df
    
    def filter_df_by_course(self, course_number):
        # only show courses betwen start and end time
        df = self.df_dates.copy(deep=True)
        df = self.df_dates[self.df_dates["course_number"] == course_number]
        df = df.sort_values(by="start_time").reset_index(drop=True)
        return df
    
    ###### Add Information to Dataframes ######
    def add_course_info(self, dataframe_dates):
        df = dataframe_dates.copy(deep=True)
        df = pd.merge(dataframe_dates, self.df_courses, on="course_number")
        return df