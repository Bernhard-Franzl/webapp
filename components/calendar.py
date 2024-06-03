from dash import Dash, html, dash_table
import dash_ag_grid as dag
from datetime import datetime, date, time, timedelta
import pandas as pd
import json

weekday_to_id = {
    "Mo.": 0,
    "Di.": 1,
    "Mi.": 2,
    "Do.": 3,
    "Fr.": 4,
    "Sa.": 5,
    "So.": 6,
}

def convert_start_end_time(dataframe):
    df = dataframe.copy()
    min_time = df["start_time"].min()
    max_time = df["end_time"].max()
    df["start_time"] = df["start_time"].apply(lambda x: x.replace(year=min_time.year, 
                                                                      month=min_time.month, 
                                                                      day=min_time.day))
    df["start_time_string"] = df["start_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    df["end_time"] = df["end_time"].apply(lambda x: x.replace(year=min_time.year, 
                                                                  month=min_time.month, 
                                                                  day=min_time.day)- timedelta(minutes=15))
    return df, min_time, max_time

def generate_new_index(dataframe):
    min_time = dataframe["start_time"].min()
    max_time = dataframe["end_time"].max() + timedelta(minutes=15)
    new_index = pd.date_range(start=min_time, end=max_time, freq="15min")
    return new_index

def generate_context_dictionary(dataframe):
    df = dataframe.copy()
    info_look_up = df.set_index(["start_time_string", "weekday"]).to_dict(orient="index")
    dict_to_rowspan = {}
    for key in info_look_up:
        values = info_look_up[key]
        try:
            dict_to_rowspan[key[1]][key[0]] = values
        except KeyError:
            dict_to_rowspan[key[1]] ={key[0]: values}
            
    return dict_to_rowspan

def define_columns(table):
    datetime_obj = "d3.timeParse('%Y-%m-%dT%H:%M:%S')(params.data.time)"
    columnDefs = [{"field": weekday,
                "rowSpan":{"function": f"rowSpanningComplex(params)"},
                "cellRenderer":"RowSpanningComplexCellRenderer",
                } for weekday in table.columns[1:]]
    
    columnDefs.insert(
        0, 
        {"field":"time",
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
    return columnDefs