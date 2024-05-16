from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from datetime import datetime, date, time
from assets import plot_header

from visualization.visualization import Visualizer

register_page(__name__, path="/", order=0)

## TODO:
# - do the mode handling with the separate function
# - cache current state of the filters
# - reset button for the filters

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
    "title": "Course Participants Overview",
    "description": "This plot provides an overview of the onsite participants of all the courses.",
    "filtering": ["date", "room", "start_time"],
    "grouping": False,
    "sorting": True,
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
                description=header_config["description"],
                filtering=header_config["filtering"],
                start_date = start_date,
                end_date = end_date,
                dataframe = df_participants,
                grouping=header_config["grouping"],
                sorting=header_config["sorting"],
                mode=header_config["mode"],
                course_info=header_config["course_info"]
            ),
            dcc.Graph(
            id="participants_multi_course_bar",
            config=visard.config)
        ]
    )
])

@callback(
    Output(
        component_id="participants_multi_course_bar", 
        component_property="figure"),
    
    # filter
    # date picker
    Input(
        component_id="date_picker",
        component_property="start_date"),
    Input(
        component_id="date_picker",
        component_property="end_date"),
    # room filter
    Input(
        component_id="room_filter",
        component_property="value"),
    # start time filter
    Input(
        component_id="start_time_filter",
        component_property="value"),
    
    # sorting
    Input(
        component_id="graph_sort_by", 
        component_property="value"),
    Input(
        component_id="graph_sort_order", 
        component_property="on"),
    
    # mode  
    Input(
        component_id="graph_mode", 
        component_property="value"),
    )
def update_figure(start_date_filter, end_date_filter, room_filter, start_time_filter, sort_by_column, ascending, graph_mode):

    ########## Filtering ##########
    # filter by date
    start_time = datetime.combine(date.fromisoformat(start_date_filter) , time(hour=0, minute=0))
    end_time = datetime.combine(date.fromisoformat(end_date_filter), time(hour=23, minute=59))
    df = visard.filter_by_time(df_participants, start_time, end_time)
    # filter by room
    room_filter = [metadata_participants["room_to_id"][room] for room in room_filter]
    if len(room_filter) > 0:
        df = visard.filter_by_rooms(df, room_filter)
    # filter by start_time
    if len(start_time_filter) > 0:
        start_time_filter = [time.fromisoformat(time_str) for time_str in start_time_filter]
        df = visard.filter_by_start_time(df, start_time_filter)

    
    ########## Sorting ##########
    
    df = visard.sort_by_column(df, [sort_by_column, "start_time"], ascending=(not ascending))
    
    ########## Plotting ##########
    fig = visard.plot_multiple_courses_bars(
        dataframe=df,
        course_numbers=df["course_number"].unique(),
        mode=graph_mode
    )
    return fig