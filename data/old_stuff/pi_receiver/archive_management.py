import os
import glob
import datetime
import re
import shutil

path="/home/pi_receiver/"
pattern="data_*/"
stored_days = 14

time_stamp = datetime.datetime.now()

cur_date = str(time_stamp.date())
#cur_date = str(time_stamp)


for data_dir_path in glob.glob(path + pattern):

    room_name = list(filter(None, re.split("data_*|/", data_dir_path)))[-1]

    archive_directory = path + "archive/"
    if not os.path.isdir(archive_directory):
        os.makedirs(archive_directory) 
    
    # check if too many files exist only store locally the last 2 weeks
    sub_dir_list = sorted(glob.glob(archive_directory + "*"), reverse=True)
    for dir in sub_dir_list[stored_days-1:]:
        shutil.rmtree(dir)

    # add current file
    archive_sub_directory = archive_directory + f"data_{room_name}_" + cur_date 
    if not os.path.isdir(archive_sub_directory):
        shutil.copytree(data_dir_path, archive_sub_directory)  



