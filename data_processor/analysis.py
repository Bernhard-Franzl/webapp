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
    
    def calc_participants(self, dataframe, start_time, end_time, first, last):
        
        n = 1
        # make a copy of the dataframe
        df = dataframe.copy()
        # get the new start and end time
        df_during = self.filter_by_time(df, start_time, end_time)
        df_course = self.calc_inside_per_min(df_during, n ,start_time, end_time-timedelta(minutes=1))
        
        start_time_new, end_time_new = self.get_time(start_time, end_time, first, last)
        
        df_before = self.filter_by_time(df, start_time_new, start_time)
        df_before = self.calc_inside_per_min(df_before, n ,start_time_new, start_time-timedelta(minutes=1))
        
        df_after = self.filter_by_time(df, end_time, end_time_new)
        df_after = self.calc_inside_per_min(df_after, n ,end_time, end_time_new-timedelta(minutes=1))
        
        #print(self.calc_inside_per_min(df_before))
        print(df_before)
        print(df_course)
        print(df_after)
        #print(self.calc_inside_per_min(df_after))
        #start from the assumption that during the course only particpants are in the room
        return df_before, df_course, df_after

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
        start_time_new, end_time_new = self.get_time(start_time, end_time, first, last) 
        
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
            if (not first) and (not in_only.empty):
                new_index = course_attendance.index[0] - 1    
                course_attendance.loc[new_index] = last_row_in_only
                course_attendance.loc[new_index, "people_out"] = 0
                #sort by time
                course_attendance = course_attendance.sort_values(by="time").reset_index(drop=True)
            
            # add last row to the course attendance such that it spans the whole time of course
            # important if lecturer exceeds the time
            if (not last) and (not out_only.empty):
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
    def calc_participants_extrema(self, dataframe, start_time, end_time, first, last):
        
        # make a copy of the dataframe
        df = dataframe.copy()
        
        # get the new start and end time
        start_time_new, end_time_new = self.get_time(start_time, end_time, first, last)
        
        print(start_time_new, end_time_new)
        df = self.filter_by_time(df, start_time_new, end_time_new)
        df_control = self.calc_inside(df)
        
        df_course = self.filter_by_time(df_control, start_time, end_time, reset_index=False)
        first_index, last_index = df_course.index[0], df_course.index[-1]
        
        extrema = self.get_local_extrema(dataframe=df_control, n=5)
        minima_mask = extrema["min"].notnull()
        maxima_mask = extrema["max"].notnull()
        
        #indices = extrema[minima_mask].index
        #if indices[0] != 0:
        #    indices = np.insert(indices, 0, values=0)
        
        minima = extrema[minima_mask]

        minima_time_column = minima["time"]
        min_before = minima_time_column < start_time
        min_during= (minima_time_column >= start_time) & (minima_time_column <= end_time)
        min_after = minima_time_column > end_time
        
        # glob min before course    
        idx = minima[min_before]["people_inside"].argmin()
        glob_min_before = minima[min_before].iloc[idx]

        # glob min after course
        idx = minima[min_after]["people_inside"].argmin()
        glob_min_after = minima[min_after].iloc[idx]
        
        maxima = extrema[maxima_mask]
        max_time_column = maxima["time"]
        max_before = max_time_column < start_time
        max_during = (max_time_column >= start_time) & (max_time_column <= end_time)
        max_after = max_time_column > end_time
        
        extrema_before = pd.concat([min_before, max_before]).sort_index()
        extrema_during = pd.concat([min_during, max_during]).sort_index()
        extrema_after = pd.concat([min_after, max_after]).sort_index()
        # if true get index
        
        before_list = extrema_before[extrema_before].index.to_list()
        during_list = extrema_during[extrema_during].index.to_list()
        after_list =  extrema_after[extrema_after].index.to_list()

        # get the index closest to the start time in original dataframe
        #print(first_index, last_index)
        

        before_list.append(first_index)
        #print(before_list)
        during_list.insert(0, first_index)
        during_list.append(last_index)
        #print(during_list)
        after_list.insert(0, last_index)
        #print(after_list)
        # for improved sanity check -> we need it in order to check if the
        # relation between entering people before the course and leaving people after the course is plausible

        # calc people inside for chunks between extrema
        
        def calc_inside_chunks(dataframe, indices):
            df = dataframe.copy()
            
            df_list = []
            
            for i in range(0,len(indices)-1):
                #print(indices[i], indices[i+1])
                
                if i == 0:
                    mask = (df.index >= indices[i]) & (df.index <= indices[i+1])
                else:
                    mask = (df.index > indices[i]) & (df.index <= indices[i+1])
                
                inside = self.calc_inside(df[mask])
                #print(inside)
                df_list.append(inside)
                #print(inside)
                #print(inside)
                
            return df_list

        df_list_before = calc_inside_chunks(df_control, before_list)
        df_list_during = calc_inside_chunks(df_control, during_list)
        df_list_after = calc_inside_chunks(df_control, after_list)

        #sanity check:
        # number of people entering before the course should be equal to the number of people leaving after the course
        
        def process_chunk_lists(df_list):
            
                        
            sum_out = 0
            sum_in = 0
            list_in = []
            list_out = []
            
            list_in_out = []
            for chunk in df_list:
                #print(chunk)
                first_row = chunk.iloc[0]
                last_row = chunk.iloc[-1]
                
                people_inside = last_row["people_inside"]
                
                if people_inside > 0:
                    sum_in += people_inside
                    list_in.append(chunk)
                    
                elif people_inside < 0:
                    sum_out += abs(people_inside)
                    list_out.append(chunk)
                    
                else:
                    continue
                
            return sum_in, sum_out, list_in, list_out
        
        df_list = []
        sum_in_before, sum_out_before, people_in_before, people_out_before = process_chunk_lists(df_list_before)
        df_list += people_in_before
        df_list += people_out_before
        
        if len(df_list_after) > 0:
            # normal case compare before and after
            sum_in_during, sum_out_during, people_in_during, people_out_during = process_chunk_lists(df_list_during)
            print(sum_in_during, sum_out_during)
            sum_in_after, sum_out_after, people_in_after, people_out_after = process_chunk_lists(df_list_after)

        else:
            # special case compare before and during
            sum_in_after, sum_out_after, people_in_after, people_out_after = process_chunk_lists(df_list_during)
        
        print(sum_in_after, sum_out_after)
        #print(sum_in_before + sum_in_during + sum_in_after, sum_out_before + sum_out_during + sum_out_after)

        
        if first:
            count_in = sum_in_before + sum_in_during - sum_out_before
            count_out = sum_out_after + sum_out_during

        else:
            count_in = sum_in_before + sum_in_during
            count_out = sum_out_after + sum_out_during
            
        # process entirety of chunks and calcualte the number of people entering and leaving
        #df_list = df_list_before + df_list_during + df_list_after
        print("Sanity-check:", count_in, count_out)
        print()
        
        
        sum = 0
        for chunk in df_list_before:
            first_row = chunk.iloc[0]
            last_row = chunk.iloc[-1]
            
            people_inside = last_row["people_inside"]
            if people_inside > 0:
                sum += people_inside
                
        print(sum)    
        sum = 0
        for chunk in df_list_during:
            first_row = chunk.iloc[0]
            last_row = chunk.iloc[-1]
            
            people_inside = last_row["people_inside"]
            if people_inside > 0:
                sum += people_inside
        print(sum)
        
        
        
        # must hold when summed up for both doors
        #print("Sanity-check:", count_in, count_out)
        
        return df_control, extrema, count_in, count_out


    #def check_extrema(self, minima, maxima, mask_min, mask_max):
    #    # process minima
    #    if len(minima[mask_min]) > 1:
    #        # check if in between minimum is a maximum
    #        # if yes, split chunk into two
    #        min_indices = minima[mask_min].index
    #        max_indices = maxima[mask_max].index
            
    #        indices = []
    #        for i, i_1 in zip(min_indices[:-1], min_indices[1:]):
    #            max_between = max_indices[(max_indices > i) & (max_indices < i_1)]
    #            if np.any(max_between):
    #                indices.append(i)
    #                indices.append(max_between.item())
    #            else:
    #                indices.append(i)
                    
    #        indices.append(i_1)
    #        return indices 
        
    #    elif len(minima[mask_min]) == 1:
    #        return [minima[mask_min].index.item()]
    #    else:
    #        return []
