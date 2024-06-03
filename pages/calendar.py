from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from datetime import datetime, date, time, timedelta
from components import plot_header
import dash_ag_grid as dag

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
visard = Visualizer()

header_config = {
    "title": "Calendar View",
    "filtering": ["room", "calendar_week"],
    "grouping": False,
    "sorting": False,
    "mode": False,
    "figure":False,
    "dataframe": df_participants,
    "multi_calendar_week":False,
    "multi_room":False
}
layout = html.Div(
    className="page",
    children=[
        plot_header.layout(
            title=header_config["title"],
            filtering=header_config["filtering"],
            dataframe = header_config["dataframe"],
            multi_room = header_config["multi_room"],
            multi_calendar_week = header_config["multi_calendar_week"]
        ),
        html.Div(
            className="button-container",
            children=[
                html.Button("Reset Column Size", 
                            id="button-size-to-fit-callback",
                            className="button-reset")
            ]
        ),
        html.Div(
            className="calendar",
            children=[
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
     Output("calendar-grid", "dashGridOptions")],
    plot_header.generate_input_list(header_config))
def update_calendar(room_filter, calendar_week_filter):

    ########## Filtering ##########
    # filter by date
    #start_time = datetime.combine(date.fromisoformat(start_date_filter) , time(hour=0, minute=0))
    #end_time = datetime.combine(date.fromisoformat(end_date_filter), time(hour=23, minute=59))
    #df = visard.filter_by_time(df_participants, start_time, end_time)
    # filter by room
    df =  df_participants.copy()
    
    df = df[df["calendar_week"] == calendar_week_filter]
    # filter by calendar week
    
    # filter by room
    if type(room_filter) == list:
        room_filter = [metadata_participants["room_to_id"][room] for room in room_filter]
        if len(room_filter) > 0:
            df = visard.filter_by_rooms(df, room_filter)
    else:
        df = visard.filter_by_rooms(df, [metadata_participants["room_to_id"][room_filter]])
    
    
    # convert start_time and end_time to suitable format
    df, min_time, max_time = calendar.convert_start_end_time(df)
    # first date of calendar week
    monday = datetime.strptime(f"{min_time.year}-{calendar_week_filter}" + '-1', "%Y-%W-%w")
    sunday = monday + timedelta(days=6)
    
    print(monday, sunday)
    # new index
    new_index = calendar.generate_new_index(df)
    # make sure that with start_time, weekday and course_number we can identify a unique row
    context_dictionary = calendar.generate_context_dictionary(df)
    
    
    # pivot table that shows the course number for each weekday and start_time and end_time
    table = df.pivot_table(index=["start_time"], 
                             columns=["weekday"], 
                             values="course_number",
                             aggfunc="first")        
    # resample pivot table
    table = table.resample("15min").first().reindex(new_index, fill_value=None)
    # order the columns of the table
    weekday_list = sorted([weekday_to_id[weekday] for weekday in df["weekday"].unique()])
    weekday_list = [list(weekday_to_id)[weekday] for weekday in weekday_list]
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
    
    return columnDefs, rowData, dashGridOptions

@callback(
    Output("calendar-grid", "columnSize"),
    Input("button-size-to-fit-callback", "n_clicks"),
)
def update_column_size_callback(_):
    return "responsiveSizeToFit"