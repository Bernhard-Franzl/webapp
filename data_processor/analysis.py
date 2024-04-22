import pandas as pd
from datetime import datetime, time, timedelta 
from scipy.signal import argrelextrema
import numpy as np

class Analyzer():
    def __init__(self, dataframe):
        # cleaned raw data
        self.dataframe = dataframe

    #######  Data Filtering Methods ########
    def filter_by_room(self, dataframe, room_id):
        df = dataframe.copy()
        mask = df["room_id"] == room_id
        return df[mask].reset_index(drop=True)
    
    def filter_by_door(self, dataframe, door_id):
        df = dataframe.copy()
        mask = df["door_id"] == door_id
        return df[mask].reset_index(drop=True)
    
    def filter_by_time(self, dataframe, start_time=None, end_time=None):
        
        # if no start time and end time is given throw exception
        if (start_time == None) and (end_time == None):
            raise Exception("No start and end time given")
        # if no start time given, set it to the minimum time in the dataframe
        if start_time == None:
            start_time = dataframe["time"].min()
        #if no end time given, set it to the maximum time in the dataframe
        if end_time == None:
            end_time = dataframe["time"].max()
            
        df = dataframe.copy()
        mask = (df["time"] >= start_time) & (df["time"] <= end_time)
        
        return df[mask].reset_index(drop=True)
    
    ########  Data Analysis Methods ########
    # calc people entering and leaving
    def calc_entering_leaving(self, dataframe):
        df = dataframe.copy()
        
        # cum sum of event type for people in
        df["people_in"] = df["event_type"].cumsum()
        # cum sum of inverted event type for people out
        df["people_out"] = df["event_type"].apply(lambda x: 1-x).cumsum()
        
        return df

    def calc_inside(self, dataframe):
        # make a copy of the dataframe
        df = dataframe.copy()
        # calc people entering and leaving
        df = self.calc_entering_leaving(df)
        # calc people in room a a given time
        df["people_inside"] = df["people_in"] - df["people_out"]
        return df

    def get_start_time(self, start_time, end_time, first, last):
                
        if first:
            start_time_new = start_time - timedelta(hours=1)
        else:
            start_time_new = start_time - timedelta(minutes=15)
            
        if last:
            end_time_new = end_time + timedelta(hours=1)
        else:
            end_time_new = end_time + timedelta(minutes=15)
            
        return start_time_new, end_time_new
    
    def get_local_extrema(self, dataframe, n):
        df = dataframe.copy()

        df['min'] = df.iloc[argrelextrema(df.people_inside.values, 
                                          np.less_equal,
                                          order=n)[0]]["people_inside"]
        df['max'] = df.iloc[argrelextrema(df.people_inside.values,
                                            np.greater_equal,
                                            order=n)[0]]["people_inside"]
        return df
    
    def calc_participants_simple(self, dataframe, start_time, end_time):
        df = dataframe.copy()
        
        start_time_new = datetime(start_time.year, start_time.month, start_time.day, 7, 45, 0)
        
        df = self.filter_by_time(df, start_time_new, end_time)
        df = self.calc_inside(df)
        
        return df
  
    def calc_patricipants_sophisticated(self, dataframe, start_time, end_time, first, last):
       
        # make a copy of the dataframe
        df = dataframe.copy()
        
        # get the new start and end time
        start_time_new, end_time_new = self.get_start_time(start_time, end_time, first, last) 
        
        #mid_point = start_time + (end_time - start_time) / 2
        df = self.filter_by_time(df, start_time_new, end_time_new)
        
        # calculate the number of people inside the room before the course
        in_only = df[df["time"] < (start_time)]
        in_only = self.calc_entering_leaving(in_only)

        if in_only.empty or first:
            in_only_count = 0
        else:
            last_row_in_only = in_only.iloc[-1]
            in_only_count = last_row_in_only["people_in"]
        #print(in_only_count)
        
        out_only = df[df["time"] > end_time]
        out_only = self.calc_entering_leaving(out_only)
        
        if out_only.empty or last:
            out_only_count = 0
        else:
            out_only_count = out_only["people_out"].iloc[-1]
        #print(in_only)    
        # calculate the number of people inside the room during the course
        
        if first & last:
            course_attendance = df[(df["time"] >= start_time_new) & (df["time"] <= end_time_new)]
            
        elif first or last:
            if first:
                course_attendance = df[(df["time"] >= start_time_new) & (df["time"] <= end_time)]
            else:
                course_attendance = df[(df["time"] >= start_time) & (df["time"] <= end_time_new)]
                
        else:
            course_attendance = df[(df["time"] >= start_time) & (df["time"] <= end_time)]
        
        if in_only.empty & course_attendance.empty:
            raise ValueError("No data for the given course time!")
        else:
            course_attendance = self.calc_entering_leaving(course_attendance)            
            course_attendance["people_in"] += in_only_count
        
            # add first row to the course attendance such that it spans the whole time of course
            if not first:
                new_index = course_attendance.index[0] - 1    
                course_attendance.loc[new_index] = last_row_in_only
                course_attendance.loc[new_index, "people_out"] = 0
                #sort by time
                course_attendance = course_attendance.sort_values(by="time").reset_index(drop=True)
            
            # add last row to the course attendance such that it spans the whole time of course
            # important if lecturer exceeds the time
            if not last:
                new_index = course_attendance.index[-1] + 1
                last_row_ca = course_attendance.iloc[-1]
                people_in = last_row_ca["people_in"]
                people_out = last_row_ca["people_out"]
                course_attendance.loc[new_index] = out_only.iloc[0]
                course_attendance.loc[new_index, "people_in"] = people_in
                course_attendance.loc[new_index, "people_out"] = people_out +1
            
            # calc people inside during course
            course_attendance["people_inside"] = course_attendance["people_in"] - course_attendance["people_out"]
            

        # sanity check if number of people leaving is reasonable
        sanity_check = (course_attendance["people_inside"].iloc[-1], out_only_count)
        
        return course_attendance, sanity_check
      
    # calculate people present at a course
    def calc_participants_extrema(self, dataframe, start_time, end_time, first=False, last=False):
        
        # make a copy of the dataframe
        df = dataframe.copy()
        
        # get the new start and end time
        start_time_new, end_time_new = self.get_start_time(start_time, end_time, first, last)
        df_control = self.calc_participants_simple(df, start_time_new, end_time_new)
        
        
        
        extrema = self.get_local_extrema(dataframe=df_control, n=50)
        indices = extrema[extrema["min"].notnull()].index
        
        
        df_extrema = df_control.copy().drop(columns=["people_in", "people_out", "people_inside"])
        
        df_list = []
        for i in range(0,len(indices)-1):
            print(indices[i], indices[i+1])
            if i == 0:
                mask = (extrema.index >= indices[i]) & (extrema.index <= indices[i+1])
            else:
                mask = (extrema.index > indices[i]) & (extrema.index <= indices[i+1])
            
            inside = self.calc_inside(df_extrema[mask])
            print(inside)
            df_list.append(inside)
        

        # calc people inside between the extrema -> course attendance
        
        #course_attendance, sanity_check = self.calc_patricipants_sophisticated(df, start_time, end_time, first, last)
        
        return df_control, df_list, extrema #course_attendance, sanity_check, df_control, extrema