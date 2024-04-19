import os
from datetime import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

class Preprocessor:
    
    data_directory = "archive"
    date_format = "%Y-%m-%d"
    last_synchronized = "2024-04-07"
    last_synchronized_dt = dt.strptime(last_synchronized, date_format)
    raw_data_format = ['Entering', 'Time', 'People_IN', 'People_OUT', 'IN_Support_Count', 'OUT_Support_Count', 'One_Count_1', 'One_Count_2']
    def __init__(self, path_to_data, room_to_id, door_to_id):
        self.path_to_data = path_to_data # /home/pi_server
        self.room_to_id = room_to_id
        self.door_to_id = door_to_id
              
    # get all subdirectories of a directory
    def get_all_sub_directories(self, path_to_dir):
        sub_dirs = sorted(list(os.walk(path_to_dir))[0][1])
        return sub_dirs
    
    def get_all_sub_files(self, path_to_dir): 
        sub_files = sorted(list(os.walk(path_to_dir))[0][2])
        return sub_files
    
    # check if data has already been processed according to the last synchronization date
    def filter_directories(self, directories:list):
        filtered_dirs = []
        for x in directories:
            day = dt.strptime(x.split("_")[-1], self.date_format)
            if self.last_synchronized_dt < day:
                filtered_dirs.append(x)
        return filtered_dirs

    # get list of data directories inside the main data directory        
    def get_list_of_data_dirs(self):
        path = os.path.join(self.path_to_data, self.data_directory)
        sub_dirs = self.get_all_sub_directories(path)
        filtered = self.filter_directories(sub_dirs)
        return filtered
     
     
    #######  Data Extraction Methods ########
    def get_data(self, file_name):
        with open(file_name, "r") as file:
            data = file.readlines()
        return data

    def change_time_format(self, dataframe):
        df = dataframe.copy()
        df["Time"] = df["Time"].apply(lambda x: dt.strptime(x, "%a %b %d %H:%M:%S %Y"))
        return df
        
    def accumulate_raw_data(self, data_directories):
        
        accumulated_format = self.raw_data_format + ["Room_ID", "Door_ID"]
        df_accumulated = pd.DataFrame(columns=self.raw_data_format)
        samples = 0
        for data_dir_name in data_directories:

            path = os.path.join(self.path_to_data, self.data_directory, data_dir_name)
            file_list = self.get_all_sub_files(path)
            
            # sanity check
            if file_list != ["door1.csv", "door2.csv", "format.csv"]:
                raise ValueError("Data directory does not contain the correct files")
            
            room_name = data_dir_name.split("_")[1]
            room_id = self.room_to_id[room_name]
            
            for x in file_list[:-1]:
                
                door_name = x.split(".")[0]
                door_id = self.door_to_id[door_name]
                
                file_path = os.path.join(path, x) 

                df = pd.read_csv(file_path, names=self.raw_data_format)
                
                df = self.change_time_format(df).sort_values(by="Time", ascending=False)
                df["Room_ID"] = room_id
                df["Door_ID"] = door_id

                samples += len(df)
                df_accumulated = pd.concat([df_accumulated, df], axis=0)
        
        return df_accumulated.reset_index(drop=True)
      
    #######  Data Processing Methods ########
    def correct_entering_column(self, entry):
        if entry == "True":
            return 1
        elif entry == "False":
            return 0
        else:
            return int(entry)
        
    def clean_raw_data(self, dataframe):
        df = dataframe.copy()
        # correct the data types
        for col in df.columns[2:]:
            df[col] = df[col].astype(int)
        df["event_type"] = df["Entering"].apply(lambda x: self.correct_entering_column(x))
        
        # convert columnnames to lowercase
        df.columns = df.columns.str.lower()
        
        # rename columns
        df = df.rename(columns={"one_count_1":"sensor_one_support_count", 
                                "one_count_2":"sensor_two_support_count"})

        # drop unneccessary columns
        df = df.drop(columns=["entering", "people_in", "people_out"])
        
        # only keep rows with event_type 1 or 0
        df = df[df["event_type"].isin([0,1])]
        
        # deal with events with low directional support!
        
        # sort by time
        df = df.sort_values(by="time", ascending=True).reset_index(drop=True)
        return df

    def filter_by_room(self, dataframe, room_id):
        df = dataframe.copy()
        mask = df["room_id"] == room_id
        return df[mask]
    
    def filter_by_door(self, dataframe, door_id):
        df = dataframe.copy()
        mask = df["door_id"] == door_id
        return df[mask]
    
    def filter_by_time(self, dataframe, start_time, end_time):
        df = dataframe.copy()
        mask = (df["time"] >= start_time) & (df["time"] <= end_time)
        return df[mask]
    
    
    # calc people entering and leaving
    def calc_people_in_out(self, dataframe):
        df = dataframe.copy()
        
        # cum sum of event type for people in
        df["people_in"] = df["event_type"].cumsum()
        # cum sum of inverted event type for people out
        df["people_out"] = df["event_type"].apply(lambda x: 1-x).cumsum()

        print(df)
    
    #######  Data Visualization Methods ########
    def plot_data(self, dataframe):
        
        df = dataframe.copy()
        
        # filter by room and door
        df = self.filter_by_room(df, 0)
        df = self.filter_by_door(df, 0)
        
        #df_plot = df[mask].sort_values(by="time", ascending=True)
        
        #df_plot.plot(x="time", y="event_type", kind="bar")
        
        #plt.show()