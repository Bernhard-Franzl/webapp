from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from datetime import datetime, date, time
from assets import plot_header

from visualization.visualization import Visualizer

register_page(__name__, order=2)

## TODO:
# - add axis labels
# - fix oder of the weekdays
# - add color scheme based on groups

###### load data ########
df_participants = pd.read_csv("data/df_participants.csv")
df_participants["start_time"] = pd.to_datetime(df_participants["start_time"])
df_participants["end_time"] = pd.to_datetime(df_participants["end_time"])
df_participants["note"] = df_participants["note"].fillna("")

with open("data/metadata_participants.json", "r") as file:
    metadata_participants = json.load(file)
    metadata_participants["start_time"] = datetime.strptime(metadata_participants["start_time"], "%d.%m.%Y %H:%M")
    metadata_participants["end_time"] = datetime.strptime(metadata_participants["end_time"], "%d.%m.%Y %H:%M")
#########################

start_date = metadata_participants["start_time"].date()
end_date = metadata_participants["end_time"].date()

#print(df_participants.columns)
visard = Visualizer()

header_config = {
    "title": "Course Participants Detailed View",
    "description": "This plot provides a more detailed view on the participants of a single course.",
    "filtering": ["date", "room"],
    "grouping": True,
    "sorting": False,
    "mode": True,
    "course_info": False,
    "figure":True 
}

layout = html.Div(children=[
    # plot
    html.Div(
        className="plot",
        children=[
            plot_header.layout(
                title=header_config["title"],
                description= header_config["description"],
                filtering=header_config["filtering"],
                start_date = start_date,
                end_date = end_date,
                dataframe = df_participants,
                sorting=header_config["sorting"],
                mode=header_config["mode"],
                course_info=header_config["course_info"],
                grouping=header_config["grouping"],
            ),
            dcc.Graph(
            id="grouped_bar_chart",
            config=visard.config)
        ]
    )
])

input_list = plot_header.generate_input_list(header_config)
output_list = plot_header.generate_output_list(header_config, "grouped_bar_chart")
@callback(
    output_list,
    input_list)
def update_figure(start_date_filter, end_date_filter, room_filter, group_by, graph_mode):

    ########## Filtering ##########
    # filter by date
    start_time = datetime.combine(date.fromisoformat(start_date_filter) , time(hour=0, minute=0))
    end_time = datetime.combine(date.fromisoformat(end_date_filter), time(hour=23, minute=59))
    df = visard.filter_by_time(df_participants, start_time, end_time)
    # filter by room
    room_filter = [metadata_participants["room_to_id"][room] for room in room_filter]
    if len(room_filter) > 0:
        df = visard.filter_by_rooms(df, room_filter)
    
    
    ########## Grouping ##########
    # keep only the informative columns
    df = df[["weekday", "start_time", "end_time", 
             "present_students", "registered_students", 
             "room", "room_capacity", "type", "kind", "duration"]]
    
    # group by weekday
    if group_by == None:
        group_by = []
        
    grouped = False
    if len(group_by) == 1:
        df = visard.group_by_column(df, column=group_by)
        grouped = True
        
    elif len(group_by) > 1:
        df = visard.group_by_column(df, column=group_by)
        grouped = True
        
    else:
        grouped = False
    # ########## Sorting ##########
    # df = visard.sort_by_column(df, sort_by_column, ascending=(not ascending))
    
    ########## Plotting ##########
    if grouped:
        fig = visard.plot_grouped_bar(
            dataframe=df,
            group_by=group_by,
            mode=graph_mode
        )
    else:
        fig = visard.plot_empty_grouped_bar()
        
    return fig,