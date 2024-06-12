from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
import numpy as np
from datetime import datetime, date, time, timedelta
from components import plot_header
import dash_ag_grid as dag

from data_handler import DataHandler
from visualization.visualization import Visualizer
from components import calendar

register_page(__name__, name="Calendar View", order=2)
weekday_to_id = {
    "Mo.": 0,
    "Di.": 1,
    "Mi.": 2,
    "Do.": 3,
    "Fr.": 4,
    "Sa.": 5,
    "So.": 6,
}

###### Load Data ########
DataHandler = DataHandler("data")
df_participants = DataHandler.get_data()
metadata_participants = DataHandler.get_meta_data()


#########################
visard = Visualizer()

header_config = {
    "title": "Calendar View",
    "filtering": ["room", "calendar_week"],
    "dataframe": df_participants,
    "multi_room":False,
    "mode": True,
    "multi_calendar_week":False,
    "grouping": False,
    "sorting": False,
    "figure":False,
    "mode_options": ["relative_capacity", "relative_registered"],
}

layout = html.Div(
    className="page",
    children=[
        plot_header.layout(
            **header_config
        ),
        html.Div(
            className="calendar",
            children=[
                html.Div(
                    className="calendar-header",
                    children=[
                        html.Div(
                            id="calendar-room-id",
                            className="calendar-header-room"
                            ),
                        html.Div(
                            id="calendar-title-id",
                            className="calendar-header-title"
                        ),
                        html.Div(
                            className="button-container",
                            children=[
                                html.Button("Reset Column Size", 
                                            id="button-size-to-fit-callback",
                                            className="button-reset")
                            ]
                        )
                    ]
                ),
                dag.AgGrid(
                    id="calendar-grid",
                    className="ag-grid",
                    columnSize="responsiveSizeToFit",
                    dangerously_allow_code=True,
                    style={"height": "750px", "width": "750px"},
                    defaultColDef={"editable": False,
                                    "sortable": False,
                                    "suppressMovable":True}
                )
            ]
    )
        
])

@callback(
    [Output("calendar-grid", "columnDefs"),
     Output("calendar-grid", "rowData"),
     Output("calendar-grid", "dashGridOptions"),
     Output("calendar-title-id", "children"),
     Output("calendar-room-id", "children")],
    plot_header.generate_input_list(header_config))
def update_calendar(room_filter, calendar_week_filter, mode):

    ########## Filtering ##########
    # filter by room
    df =  df_participants.copy()
    
    # filter by calendar week
    df = DataHandler.filter_column_by_value(df, "calendar_week", calendar_week_filter)
    # filter by room
    df = DataHandler.filter_by_rooms(df, room_filter)
    
    
    ########### Calendar ###########
    # convert start_time and end_time to suitable format
    df, min_time, max_time = calendar.convert_start_end_time(df)
    # first date of calendar week
    monday = datetime.strptime(f"{min_time.year}-{calendar_week_filter}" + '-1', "%Y-%W-%w")
    sunday = monday + timedelta(days=6)

    # new index
    new_index = calendar.generate_new_index(df)
    # make sure that with start_time, weekday and course_number we can identify a unique row
    df["mode"] = mode
    context_dictionary = calendar.generate_context_dictionary(df)
    
    # pivot table that shows the course number for each weekday and start_time and end_time
    weekday_list = ["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa."]
    table = df.pivot_table(index=["start_time"], 
                            columns=["weekday"], 
                            values="course_number",
                            aggfunc="first") 
    
    
    # add missing columns
    table_columns = table.columns
    if "Sa." not in table_columns:
        weekday_list.remove("Sa.")
        
    for weekday in weekday_list:
        if weekday not in table.columns:
            table[weekday] = None

    # resample pivot table
    table = table.resample("15min").first().reindex(new_index, fill_value=None)
    table = table[weekday_list]
    # reset index
    table = table.reset_index().rename(columns={"index":"time"})
    
    # get columnDefs
    columnDefs = calendar.define_columns(table)
    # get rowData
    rowData = table.to_dict(orient="records")
    # define grid
    dashGridOptions = {"suppressFieldDotNotation": True,
                       "suppress_callback_exceptions":True,
            "suppressRowTransform": True,
            "context":context_dictionary}
    
    ### Calendar Header ###
    calendar_title = [
        html.Div(
            f"Calendar Week {calendar_week_filter}", 
            style={"font-weight":"bold"}
        ),
        html.Div(f"{monday.strftime('%d.%m.%Y')} - {sunday.strftime('%d.%m.%Y')}")
    ]
    room_info = [
        html.Div(
            f"{room_filter}", 
            style={"font-weight":"bold"}
        ),
        html.Div(f"Capacity: {int(df["room_capacity"].unique())}")
    ]
    return columnDefs, rowData, dashGridOptions, calendar_title, room_info

@callback(
    Output("calendar-grid", "columnSize"),
    Input("button-size-to-fit-callback", "n_clicks"),
)
def update_column_size_callback(_):
    return "responsiveSizeToFit"