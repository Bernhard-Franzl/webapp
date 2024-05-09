import pandas as pd
from datetime import datetime
import json
from visualization import Visualizer

df_participants = pd.read_csv("data/df_participants.csv")
df_participants["start_time"] = pd.to_datetime(df_participants["start_time"])
df_participants["end_time"] = pd.to_datetime(df_participants["end_time"])

with open("data/metadata_participants.json", "r") as file:
    metadata_participants = json.load(file)
    metadata_participants["start_time"] = datetime.strptime(metadata_participants["start_time"], "%d.%m.%Y %H:%M")
    metadata_participants["end_time"] = datetime.strptime(metadata_participants["end_time"], "%d.%m.%Y %H:%M")


visard = Visualizer()

#visard.plot_multiple_courses_bars(dataframe=df_participants,
#                                  course_numbers=metadata_participants["course_numbers"],
#                                  title="Participants per Course Date",
#                                  relative=False)


#print(df_result.columns[[0, 8, 19, 16, 7, 1, 5, 2, 27, 3]])
mode = "relative_registered"
fig = visard.plot_multiple_courses_bars(dataframe=df_participants,
                                  course_numbers=metadata_participants["course_numbers"],
                                  title="Participants per Course Date",
                                  mode=mode)
fig.show(config=visard.config)
# single course bar chart
#visard.plot_course_bar(dataframe=df_result, 
#                       course_number=course_numbers[0], 
#                       show_relative=True, 
#                       show_before_after=False)
