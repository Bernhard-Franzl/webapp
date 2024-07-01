from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from datetime import datetime, date, time
from components import plot_header
from data_handling.data_handler import DataHandler
from visualization.visualization import Visualizer

#register_page(__name__, name="Courses Overview", order=1)

## TODO:
# - filter by number of dates, think of more ways to filter the data
# - reset button for the filters -> resets them to initial values
#   which is showing all data

###### Load Data ########
data_handler = DataHandler("data")
df_participants = data_handler.get_data()
metadata_participants = data_handler.get_meta_data()


start_date = metadata_participants["start_time"].date()
end_date = metadata_participants["end_time"].date()

#print(df_participants.columns)

visard = Visualizer(margin=dict(l=125, r=50, t=50, b=100))
header_config = {
    "title": "Course Participants Overview",
    "description": "This page provides an overview of the onsite participants of all the courses.",
    "filtering": ["date", "room", "start_time"],
    "grouping": False,
    "sorting": True,
    "mode": True,
    "figure":True,
}

layout = html.Div(
    className="page",
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
        ),
        html.Div(
            className="content-container",
            children=[
                html.Div(
                    className="overview-container",
                    children=dcc.Graph(
                        id="participants_multi_course_bar",
                        config=visard.config)
                ),
                html.Div(
                    className="details-container",
                    children="Hello"
                )
            ]
        )
    ]
)

input_list = plot_header.generate_input_list(header_config)
output_list = plot_header.generate_output_list(header_config, "participants_multi_course_bar")
@callback(
    output_list,
    input_list
    )
def update_figure(start_date_filter, end_date_filter, room_filter, start_time_filter, sort_by_column, ascending, graph_mode):
    
    df = df_participants.copy()
    
    ########## Filtering ##########
    # filter by date
    df = data_handler.filter_by_date(df, start_date_filter, end_date_filter)
    # filter by room
    df = data_handler.filter_by_rooms(df, room_filter)
    # filter by start_time
    df = data_handler.filter_by_start_time(df, start_time_filter)

    ########## Sorting ##########
    df = data_handler.sort_by_column(df, sort_by_column, ascending=(not ascending))
    
    ########## Plotting ##########
    fig = visard.plot_multiple_courses_bars(
        dataframe=df,
        course_numbers=df["course_number"].unique(),
        mode=graph_mode
    )
    return [fig]