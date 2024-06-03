from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from datetime import datetime, date, time, timedelta
from components import plot_header

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

layout = html.Div(
    className="page",
    children=[
        plot_header.layout(
            title="Calendar View",
            filtering=["room"],
            dataframe = df_participants,
        ),
        calendar.layout(df_participants, metadata_participants)
        
])

@callback(
    [Output("calendar-grid", "rowData"),
     Output("calendar-grid", "columnDefs"),
     Output("calendar-grid", "dashGridOptions"),],
    [Input("room_filter", "value")])
def update_calendar(room_filter):

    ########## Filtering ##########
    # filter by date
    #start_time = datetime.combine(date.fromisoformat(start_date_filter) , time(hour=0, minute=0))
    #end_time = datetime.combine(date.fromisoformat(end_date_filter), time(hour=23, minute=59))
    #df = visard.filter_by_time(df_participants, start_time, end_time)
    # filter by room
    df =  df_participants.copy()
    
    df = df[df["calendar_week"] == 15]
    
    room_filter = [metadata_participants["room_to_id"][room] for room in room_filter]
    if len(room_filter) > 0:
        df = visard.filter_by_rooms(df, room_filter)
  
    min_date = df["start_time"].min()
    df["start_time"] = df["start_time"].apply(lambda x: x.replace(year=min_date.year, 
                                                                      month=min_date.month, 
                                                                      day=min_date.day))
    df["end_time"] = df["end_time"].apply(lambda x: x.replace(year=min_date.year, 
                                                                  month=min_date.month, 
                                                                  day=min_date.day)- timedelta(minutes=15))      
    # pivot table that shows the course number for each weekday and start_time and end_time
    table = df.pivot_table(index=["start_time"], 
                             columns=["weekday"], 
                             values="course_number",
                             aggfunc="first")
    # new index
    min_time = df["start_time"].min()
    max_time = df["end_time"].max() + timedelta(minutes=15)
    new_index = pd.date_range(start=min_time, end=max_time, freq="15min")
    
    # make sure that with that with start_time, weekday and course_number we can identify a unique row
    df["start_time_string"] = df["start_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    data_grouped = df.set_index(["start_time_string", "weekday"])
    info_look_up = data_grouped.to_dict(orient="index")
    dict_to_rowspan = {}
    for key in info_look_up:
        values = info_look_up[key]
        try:
            dict_to_rowspan[key[1]][key[0]] = values
        except KeyError:
            dict_to_rowspan[key[1]] ={key[0]: values}
            
    table = table.resample("15min").first().reindex(new_index, fill_value=None)
    
    # for the right order of weekdays
    weekday_list = sorted([weekday_to_id[weekday] for weekday in df["weekday"].unique()])
    weekday_list = [list(weekday_to_id)[weekday] for weekday in weekday_list]
    table = table[weekday_list]   
    
    datetime_obj = "d3.timeParse('%Y-%m-%dT%H:%M:%S')(params.data.time)"
    table = table.reset_index().rename(columns={"index":"time"})

    columnDefs = [{"field": weekday,
                   "rowSpan":{"function": f"rowSpanningComplex(params)"},
                   "cellRenderer":"RowSpanningComplexCellRenderer",
                   } for weekday in table.columns[1:]]
    columnDefs.insert(0, {"field":"time",
                          "headerName":"",
                "valueGetter": {"function": datetime_obj},
                "cellRenderer":"TimeCellRenderer",
                "cellClass": "calendar--time-cell",
                'suppressSizeToFit': True,
                "resizable": False,
                "pinned": "left",
                "width": 70,
                "valueFormatter": {"function": f"d3.timeFormat('%H:%M')({datetime_obj})"}
                })
    
    rowData = table.to_dict(orient="records")
    dashGridOptions = {"suppressFieldDotNotation": True,
                    "suppressRowTransform": True,
                    "context":dict_to_rowspan,
                    },
    return rowData, columnDefs, dashGridOptions