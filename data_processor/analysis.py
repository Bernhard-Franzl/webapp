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
    
    def filter_by_time(self, dataframe, start_time=None, end_time=None, reset_index=True):
        
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
        if reset_index:
            return df[mask].reset_index(drop=True)
        else:
            return df[mask]
    
    
    ######## Statistical Methods ########
    def calc_mean_inside(self, dataframe):
        df = dataframe.copy()
        return df["people_inside"].mean()
    
    def calc_median_inside(self, dataframe):
        df = dataframe.copy()
        return df["people_inside"].median()
    
    def calc_mode_inside(self, dataframe):
        df = dataframe.copy()
        return int(df["people_inside"].mode())
    
    def calc_std_inside(self, dataframe):
        df = dataframe.copy()
        return df["people_inside"].std()
    
    def describe_inside(self, dataframe):
        df = dataframe.copy()
        return df["people_inside"].describe()
    
    
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
    
    def calc_inside_per_min(self, dataframe, n=1, start=None, end=None):
        
        df = dataframe.copy()
        
        # add a check if n is a divisor of the time span
        
        
        df["people_in"] = df["event_type"].apply(lambda x: 1 if x == 1 else 0)
        df["people_out"] = df["event_type"].apply(lambda x: 1 if x == 0 else 0)
        
        
        idx = pd.date_range(start=start, end=end, freq=f'{n}min')
        
        df = df.set_index("time")\
                .resample(f"{n}min")\
                .sum().reindex(idx, fill_value=0).reset_index()
        df.rename(columns={"index":"time"}, inplace=True)
        
        df["people_in"] = df["people_in"].cumsum()
        df["people_out"] = df["people_out"].cumsum()
        df["people_inside"] = df["people_in"] - df["people_out"]
        
        return df
            
    def get_time(self, start_time, end_time, first, last):
                
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
    
    def get_people_inside(self, dataframe):
        return dataframe.iloc[-1]["people_inside"]
    
    def get_people_in(self, dataframe):
        return dataframe.iloc[-1]["people_in"]
    
    def get_people_out(self, dataframe):
        return dataframe.iloc[-1]["people_out"]
        
    def calc_participants(self, dataframe, start_time, end_time, first, last):
        
        n = 1
        # make a copy of the dataframe
        df = dataframe.copy()
        
        # get the new start and end time
        df_during = self.filter_by_time(df, start_time, end_time)
        df_during = self.calc_inside_per_min(df_during, n ,start_time, end_time-timedelta(minutes=1))
        
        start_time_new, end_time_new = self.get_time(start_time, end_time, first, last)
        
        df_before = self.filter_by_time(df, start_time_new, start_time)
        df_before = self.calc_inside_per_min(df_before, n ,start_time_new, start_time-timedelta(minutes=1))
        
        df_after = self.filter_by_time(df, end_time, end_time_new)
        df_after = self.calc_inside_per_min(df_after, n ,end_time, end_time_new-timedelta(minutes=1))

        df_control = self.filter_by_time(df, start_time_new, end_time_new)
        df_control = self.calc_inside_per_min(df_control, n ,start_time_new, end_time_new-timedelta(minutes=1))
        #in_before = self.get_people_in(df_before)
        #out_before = self.get_people_out(df_before)
        
        #in_during = self.get_people_in(df_during)
        #out_during = self.get_people_out(df_during)
        
        #in_after = self.get_people_in(df_after)
        #out_after = self.get_people_out(df_after)
        def process_part(dataframe, n=10, before=True, first=False, last=False):
            df = dataframe.copy()
            
            extrema = self.get_local_extrema(dataframe=df, n=n)
            minima_mask = extrema["min"].notnull()
            maxima_mask = extrema["max"].notnull()
            
            min = extrema[minima_mask]
            max = extrema[maxima_mask]
            
            # differentiate between before and after
            # before take first global min
            # after take last global min
            inside_col = min["people_inside"]
            global_min_indices  = min.index
            #global_min_indices = min[inside_col == inside_col.min()].index
            
            if before:
                if first:
                    glob_min_idx = global_min_indices[0]
                else: 
                    glob_min_idx = global_min_indices[-1]
                    
            else:
                if last:
                    glob_min_idx = global_min_indices[-1]
                else:
                    glob_min_idx = global_min_indices[0]

            glob_min = min.loc[glob_min_idx]
            glob_min_time = glob_min["time"]
            
            counter=0
            before_min = df[df["time"] < glob_min_time]
            after_min = df[df["time"] >= glob_min_time]

            if before:
                if not before_min.empty:
                    counter += before_min.iloc[-1]["people_in"]
                if not after_min.empty:
                    inside_col = after_min["people_inside"]
                    counter += inside_col.iloc[-1] - inside_col.iloc[0]
            else:

                if not before_min.empty:
                    counter += abs(before_min.iloc[-1]["people_inside"])
                if not after_min.empty:
                    outside_col = after_min["people_out"]
                    counter += outside_col.iloc[-1] - outside_col.iloc[0]
                
            return extrema, counter
        
        m = 3
        extrema_b, inside_b = process_part(df_before, n=m, before=True, first=first, last=last)
        extrema_a, outside_a = process_part(df_after, n=m, before=False, first=first, last=last)
        
        median_inside = self.calc_median_inside(df_during)
        # inside_b + people_inside_during - outside_a = 0
        print("#### Sanity Check #####")
        print(inside_b + df_during.iloc[-1]["people_inside"] - outside_a)
        print("#######################")

        participants_b = inside_b + median_inside
        participants_a = outside_a - df_during.iloc[-1]["people_inside"] + median_inside 
        
        extrema = pd.concat([extrema_b, extrema_a])
        
        
        return df_control, [df_before, df_during, df_after], (participants_b, participants_a), extrema

    def calc_participants_simple(self, dataframe, start_time, end_time):
        df = dataframe.copy()
        
        start_time_new = datetime(start_time.year, start_time.month, start_time.day, 7, 45, 0)
        
        df = self.filter_by_time(df, start_time_new, end_time)
        df = self.calc_inside(df)
        
        return df
 