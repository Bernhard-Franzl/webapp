import pandas as pd
import os
import json 
from datetime import datetime, date, time

class DataHandler:
    
    weekday_to_id = {
        "Mo.": 0,
        "Di.": 1,
        "Mi.": 2,
        "Do.": 3,
        "Fr.": 4,
        "Sa.": 5,
        "So.": 6,
    }
    
    def __init__(self, path_to_data):
        
        self.path_to_data = path_to_data
        self.data, self.meta_data = self.load_data(self.path_to_data)
        
        self.last_course_filter = ""
        self.last_course_filter_mode = ""

    ########## Load data ##########
    def load_data(self, path_to_data):
        
        data_path = os.path.join(path_to_data, "df_participants.csv")
        
        data = pd.read_csv(data_path)
        data["start_time"] = pd.to_datetime(data["start_time"])
        data["end_time"] = pd.to_datetime(data["end_time"])
        data["note"] = data["note"].fillna("")
        data["time_span_str"] = data.apply(lambda x: f"{x['start_time'].strftime('%H:%M')}-{x['end_time'].strftime('%H:%M')}", axis=1)
        data["start_time_string"] = data["start_time"].dt.strftime("%H:%M")
        # convert calendar_week to string
        data["calendar_week"] = data["calendar_week"].astype(str)
        
        meta_data_path = os.path.join(path_to_data, "metadata_participants.json")
        with open(meta_data_path, "r") as file:
            meta_data = json.load(file)
            meta_data["start_time"] = datetime.strptime(meta_data["start_time"], "%d.%m.%Y %H:%M")
            meta_data["end_time"] = datetime.strptime(meta_data["end_time"], "%d.%m.%Y %H:%M")
        
        return data, meta_data
    
    ######### Get data ##########
    def get_data(self):
        return self.data
    
    def get_meta_data(self):
        return self.meta_data
    
    ########## Filter functions ##########
    def filter_column_by_value(self, dataframe, column, value):
        return dataframe[dataframe[column] == value]
    
    def filter_column_by_list(self, dataframe, column, value_list):
        return dataframe[dataframe[column].isin(value_list)]
    
    def filter_column_by_range(self, dataframe, column, start=None, end=None):
        # check if start or end is given
        if (start == None) and (end == None):
            raise ValueError("Either start or end must be given")
        
        elif (start != None) and (end == None):
            return dataframe[dataframe[column] >= start]
        
        elif (start == None) and (end != None):
            return dataframe[dataframe[column] <= end]
        
        else:
            return dataframe[(dataframe[column] >= start) & (dataframe[column] <= end)]
        
    def filter_by_rooms(self, dataframe, rooms):
        
        if type(rooms) == str:
            rooms = [rooms]
        elif type(rooms) == list:
            
            if len(rooms) == 0:
                return dataframe
            
            rooms = rooms
        else:
            raise ValueError("rooms must be a string or a list of strings")
        
        room_id_list = [self.meta_data["room_to_id"][room] for room in rooms]
        
        return self.filter_column_by_list(dataframe, "room_id", room_id_list)

    def filter_by_date(self, dataframe, start_date, end_date):

        if type(start_date) == str:
            start_date = date.fromisoformat(start_date)
        if type(end_date) == str:
            end_date = date.fromisoformat(end_date)
        dataframe["start_date"] = dataframe["start_time"].dt.date
        return self.filter_column_by_range(dataframe, "start_date", start_date, end_date)
    
    def filter_by_start_time(self, dataframe, start_time):
                
        if type(start_time) == str:
            start_time = [time.fromisoformat(start_time)]
            
        elif type(start_time) == list:
            
            if len(start_time) == 0:
                return dataframe
            
            start_time = [time.fromisoformat(time_str) for time_str in start_time]
        else:
            raise ValueError("start_time must be a string or a list of strings")
        
        dataframe["start_time_time"] = dataframe["start_time"].dt.time
        return self.filter_column_by_list(dataframe, "start_time_time", start_time)
    
    def filter_by_course_number(self, dataframe, course_number):
        return self.filter_column_by_value(dataframe, "course_number", course_number)
    
    def filter_by_course_name(self, dataframe, course_name):
        return self.filter_column_by_value(dataframe, "course_name", course_name)
    
    def filter_course(self, dataframe, course_number_filter, course_name_filter, course_number_click):

        course_filtered = False
        
        if (course_number_click != "") and (self.last_course_filter != course_number_click):
            dataframe = self.filter_by_course_number(dataframe, course_number_click)
            if len(dataframe) != 0:
                course_filtered = True
                self.last_course_filter = course_number_click
                  
        elif (course_number_filter != "") and (self.last_course_filter != course_number_filter):
            dataframe = self.filter_by_course_number(dataframe, course_number_filter)
            if len(dataframe) != 0:
                course_filtered = True
                self.last_course_filter = course_number_filter
                
        elif (course_name_filter != "") and (self.last_course_filter != course_name_filter):
            dataframe = self.filter_by_course_name(dataframe, course_name_filter)
            if len(dataframe) != 0:
                course_filtered = True
                self.last_course_filter = course_name_filter
        else:
            self.last_course_filter = ""
        
        return dataframe, course_filtered
                
    ######### Grouping functions ##########
    def prepare_data_for_grouping(self, dataframe):
        if "instute" in dataframe.columns:
            dataframe = dataframe.rename(columns={"instute":"institute"})
            
        df = dataframe[["calendar_week", "weekday", "start_time_string",
             "present_students", "registered_students", 
             "room", "room_capacity", "type", "kind", "duration",
             "institute", "level", "curriculum", "exam", "test", "tutorium"]]
        
        return df
        
    def group_by_column(self, dataframe, column, agg_function="sum"):
        if agg_function == "sum":
            return dataframe.groupby(column).sum().reset_index()
        else:
            raise ValueError("agg_function must be 'sum'")
        
    def group_data(self, dataframe, group_by):
        
        df = dataframe.copy()
        
        df = self.prepare_data_for_grouping(df)

        grouped = False
        if group_by == None:
            group_by = []
            
        if len(group_by) > 0:
            if "weekday" in group_by:
                # convert weekday to index for correct order
                df["weekday"] = df["weekday"].apply(lambda x: self.weekday_to_id[x])
                df = self.group_by_column(df, column=group_by)
                # convert weekday back
                df["weekday"] = df["weekday"].apply(lambda x: list(self.weekday_to_id)[x])
                
            else:
                df = self.group_by_column(df, column=group_by)
                
            grouped = True
            return df, grouped
        
        else:
            return df, grouped
        
    ######### Sorting functions ##########
    def sort_by_column(self, dataframe, column, ascending=True):
        return dataframe.sort_values(by=[column, "start_time"], ascending=ascending)
        