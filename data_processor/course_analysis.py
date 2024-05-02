import pandas as pd
from signal_analysis import SignalAnalyzer
from preprocessing import Preprocessor
from datetime import datetime, timedelta
import os
from tqdm import tqdm

class CourseAnalyzer():
    
    room_to_id ={"HS18":0, "HS 18":0, "HS19":1, "HS 19": 1}
    door_to_id = {"door1":0, "door2":1}

    def __init__(self, data_dir_course, data_dir_signal, room_name=None):

        self.room_name = room_name
        
        self.data_dir_course = data_dir_course
        self.data_dir_signal = data_dir_signal
        
        self.preprocessor = Preprocessor(self.data_dir_signal, self.room_to_id, self.door_to_id)
        
        self.df_courses = self.initialize_courses()
        self.df_dates = self.initialize_dates()   
        self.df_combined = self.add_course_info(self.df_dates)

        # get signal data
        cleaned_data = self.preprocessor.apply_preprocessing()
        self.signal_analyzer = SignalAnalyzer()
        
        self.df_combined.drop("room_id_y", axis=1, inplace=True)
        self.df_combined.rename(columns={"room_id_x":"room_id"}, inplace=True)

        if self.room_name is None:
            self.df_signal = cleaned_data
            del cleaned_data
        else:
            self.df_signal = self.signal_analyzer.filter_by_room(cleaned_data, self.room_to_id[room_name])
            

    ###### Basic Methods #####
    def import_from_csv(self, path):
        try:
            data = pd.read_csv(path)
            return data
        except:
            raise("Error: Could not read file. Please check if the file exists and the path is correct!")
        
    def format_dates(self, dataframe_dates):
        df_dates = dataframe_dates.copy(deep=True)
        
        df_dates["start_time"] = df_dates.apply(lambda x: x["Datum"] + " " + x["Startzeit"], axis=1)
        df_dates["start_time"] = df_dates["start_time"].apply(lambda x: datetime.strptime(x, "%d.%m.%y %H:%M"))
        
        df_dates["end_time"] = df_dates.apply(lambda x: x["Datum"] + " " + x["Endzeit"], axis=1)
        df_dates["end_time"] = df_dates["end_time"].apply(lambda x: datetime.strptime(x, "%d.%m.%y %H:%M"))
        
        df_dates.drop(["Datum", "Startzeit", "Endzeit"], axis=1, inplace=True)
        
        return df_dates
    
    def get_course(self):
        return self.df_courses
    
    def get_dates(self):
        return self.df_dates    
    
    def get_combined(self):
        return self.df_combined
     
    def rename_columns(self, dataframe, old_names, new_names):
        df = dataframe.copy(deep=True)
        df.rename(columns=dict(zip(old_names, new_names)), inplace=True)
        return df
    
    def export_to_csv(self, dataframe, path):
        dataframe.to_csv(path, index=False)
        
    def export_dates(self, name):
        self.export_to_csv(self.df_dates, self.data_dir_course + name + "_dates.csv")
        
    def export_courses(self, name):
        self.export_to_csv(self.df_courses, self.data_dir_course + name + "_courses.csv")

    def format_course_number(self, course_number):
        if type(course_number) == str:
            return course_number
        else:
            return "{:.3f}".format(course_number)

    ###### Dataframe Initialization ######
    def initialize_courses(self):
        if self.room_name is None:
            sub_files = [x for x in self.preprocessor.get_all_sub_files(self.data_dir_course) if "courses" in x]
        
            dataframes = []
            for file in sub_files:
                df_courses = self.import_from_csv(os.path.join(self.data_dir_course, file))
                df_courses["room_id"] = self.room_to_id[file.split("_")[0]]
                dataframes.append(df_courses)
            df_courses = pd.concat(dataframes, axis=0).reset_index(drop=True)
                
        else:
            df_courses = self.import_from_csv(os.path.join(self.data_dir_course, self.room_name + "_courses.csv"))
            df_courses["room_id"] = self.room_to_id[self.room_name]
            
        df_courses = self.rename_columns(df_courses, 
                                              ["LVA-Nr.", "LVA-Titel", "Typ", "Art", "LeiterIn", "Sem.", "ECTS", "SSt."], 
                                              ["course_number", "course_name", "type", "kind", "lecturer", "semester", "ects", "sst"])
        df_courses["course_number"] = df_courses["course_number"].apply(lambda x: self.format_course_number(x))
        df_courses.drop("Nächster Termin", axis=1, inplace=True)
        
        return df_courses
        
    def initialize_dates(self):
        if self.room_name is None:
            sub_files = [x for x in self.preprocessor.get_all_sub_files(self.data_dir_course) if "dates" in x]
            
            dataframes = []
            for file in sub_files:
                df_dates = self.import_from_csv(os.path.join(self.data_dir_course, file))
                df_dates["room_id"] = self.room_to_id[file.split("_")[0]]
                dataframes.append(df_dates)
                
            df_dates = pd.concat(dataframes, axis=0).reset_index(drop=True)
                
        else:
            df_dates = self.import_from_csv(os.path.join(self.data_dir_course, self.room_name + "_dates.csv"))
            df_dates["room_id"] = self.room_to_id[self.room_name]
                    
        df_dates = self.format_dates(df_dates)
        df_dates = self.rename_columns(df_dates,
                                            ["LVA-Nummer", "Wochentag", "Ort", "Anmerkung"],
                                            ["course_number", "weekday", "room", "note"])
        df_dates["course_number"] = df_dates["course_number"].apply(lambda x: self.format_course_number(x))
            
        return df_dates


    ###### Filter Dataframes ######
    def filter_df_by_timestamp(self, dataframe, start_time, end_time):
        # only show courses betwen start and end time
        df = dataframe.copy(deep=True)
        df = df[(df["start_time"] >= start_time) & (df["end_time"] <= end_time)]
        df = df.sort_values(by="start_time").reset_index(drop=True)
        return df
    
    def filter_df_by_course(self, dataframe, course_number):
        # only show courses betwen start and end time
        df = dataframe.copy(deep=True)
        df = df[df["course_number"] == course_number]
        df = df.sort_values(by="start_time").reset_index(drop=True)
        return df
    
    def filter_df_by_date(self, dataframe, date):
        # only show courses betwen start and end time
        df = dataframe.copy(deep=True)
        mask = df["start_time"].dt.date == date
        df = df[mask]
        df = df.sort_values(by="start_time").reset_index(drop=True)
        return df

    def filter_df_by_room(self, dataframe, room_id):
        # only show courses betwen start and end time
        df = dataframe.copy(deep=True)
        df = df[df["room_id"] == room_id]
        df = df.sort_values(by="start_time").reset_index(drop=True)
        return df
   
    def filter_df_by_courses(self, dataframe, course_numbers):
        # only show courses betwen start and end time
        df = dataframe.copy(deep=True)
        df = df[df["course_number"].isin(course_numbers)]
        df = df.sort_values(by="start_time").reset_index(drop=True)
        return df
    
    ###### Course Analysis Methods ######
    def add_course_info(self, dates_dataframe):
        df = dates_dataframe.copy(deep=True)
        df = pd.merge(df, self.df_courses, on="course_number")
        return df
    
    def get_first_last(self, df_first_last, start_time, end_time):
        
        first = False
        last = False
        
        delta = timedelta(hours=1)
        # check if first lecture of the day or no lecture before:
        
        mask_first = ((start_time-delta) < df_first_last["end_time"]) & (df_first_last["end_time"]  < start_time)
        first = not mask_first.any()

        mask_last = ((end_time+delta) > df_first_last["start_time"]) & (df_first_last["start_time"]  > end_time)
        last = not mask_last.any()
        
        return first, last
    
    def calc_course_participants(self, dates_dataframe):
        
        df = dates_dataframe.copy(deep=True)
    
        
        cur_date = None
        cur_room = None
        
        plot_list = []
        extrema_list = []
        df_list = []
        part_list = []
        plot_name = []
        
        for i,row in tqdm(df.iterrows(), total=len(df)):
            
            if self.room_name is None:
                if (cur_date != row["start_time"].date()) or (cur_room != row["room_id"]):
                    # we could somehow chache it to avoid recalculating
                    cur_date = row["start_time"].date()
                    df_first_last = self.filter_df_by_date(self.df_dates, cur_date)
                    cur_room = row["room_id"]
                    df_first_last = self.filter_df_by_room(df_first_last, cur_room)
                    
                df_signal = self.signal_analyzer.filter_by_room(self.df_signal, cur_room)
                
            else:
                if (cur_date != row["start_time"].date()):
                    cur_date = row["start_time"].date()
                    df_first_last = self.filter_df_by_date(self.df_dates, cur_date)
                    
                df_signal = self.df_signal
                
                
            start_time = row["start_time"]
            end_time = row["end_time"]
            #print(start_time, "|", end_time)
            
            # check if first or last lecture of the day
            first, last = self.get_first_last(df_first_last, start_time, end_time)
            #print(first, "|", last)

            dataframes, participants, extrema, df_plot_list =  self.signal_analyzer.calc_participants(dataframe = df_signal, 
                                                                            start_time = start_time, 
                                                                            end_time = end_time, 
                                                                            first = first, 
                                                                            last = last, 
                                                                            control=False)
            

            df.loc[i, "present_students_b"] = participants[0]
            df.loc[i, "present_students_a"] = participants[1]
            df.loc[i, "present_students"] = (participants[0] + participants[1])//2
            
            df.loc[i, "first"] = first
            df.loc[i, "last"] = last
            
            #print(self.signal_analyzer.describe_inside(dataframes[1]))
            #df.loc[i, "std_during"] = self.signal_analyzer.describe_inside(dataframes[1])["std"]
            
            # description of during dataframe
            df_during = dataframes[1]
            description_during = self.signal_analyzer.describe_inside(df_during)
            
            max_min = description_during["max"] - description_during["min"]
            df.loc[i, "max-min"] = max_min
            df.loc[i, "min_idx"] = df_during["people_inside"].argmin()
            
            min_diff_idx = df_during["people_inside"].diff().argmin()
            df.loc[i, "min_diff_indx"] = df_during["people_inside"].diff().argmin()
            
            duration = end_time - start_time
            duration_min = duration.total_seconds()//60
            df.loc[i, "duration"] = duration_min
            df.loc[i, "overlength"] = duration > timedelta(hours=1, minutes=30)
            
            # before 80% of the time is over, the minimum is reached
            constraint1 = min_diff_idx/duration_min < 0.8  
            # max-min > 0.8 * present_students
            constraint2 = max_min > 0.8 * df.loc[i, "present_students"]
            
            df.loc[i, "irregular"] = (constraint1 & constraint2) | df.loc[i, "overlength"]
            
            
            plot_list.append(df_plot_list)
            extrema_list.append(extrema)
            df_list.append(dataframes)
            part_list.append(participants)
            plot_name.append(f"{start_time}")
            

        return df, df_list, part_list, extrema_list, plot_list, plot_name
        
    
    
    
    