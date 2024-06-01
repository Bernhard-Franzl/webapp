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


def layout(df_participants, metadata_participants):
    
    
    data = df_participants[df_participants["calendar_week"] == 15]
    data = data[data["room_id"] == 0]
    
    # remove day from datetime
    min_date = data["start_time"].min()
    data["start_time"] = data["start_time"].apply(lambda x: x.replace(year=min_date.year, month=min_date.month, day=min_date.day))
    data["end_time"] = data["end_time"].apply(lambda x: x.replace(year=min_date.year, month=min_date.month, day=min_date.day)- timedelta(minutes=15))
    # pivot table that shows the course number for each weekday and start_time and end_time
    table = data.pivot_table(index=["start_time"], 
                             columns=["weekday"], 
                             values="course_number",
                             aggfunc="first")
    #table_end  = data.pivot_table(index=["end_time"],
    #                            columns=["weekday"],
    #                            values="course_number",
    #                            aggfunc="first")
    #table = table_start.combine_first(table_start)
    
    # new index
    min_time = data["start_time"].min()
    max_time = data["end_time"].max() + timedelta(minutes=15)
    new_index = pd.date_range(start=min_time, end=max_time, freq="15min")

    # make sure that with that with start_time, weekday and course_number we can identify a unique row
    data_grouped = data.set_index(["start_time", "weekday"])
    info_look_up = data_grouped.to_dict(orient="index")
    
    
    table = table.resample("15min").first().reindex(new_index, fill_value=None)


    # for the right order of weekdays
    weekday_list = sorted([weekday_to_id[weekday] for weekday in data["weekday"].unique()])
    weekday_list = [list(weekday_to_id)[weekday] for weekday in weekday_list]
    table = table[weekday_list]

    # weekdays as columns
    datetime_obj = "d3.timeParse('%Y-%m-%dT%H:%M:%S')(params.data.time)"
    table = table.reset_index().rename(columns={"index":"time"})

    columnDefs = [{"field": weekday} for weekday in table.columns[1:]]

    columnDefs[1]['rowSpan'] = {"function": f"rowSpanningComplex(params)"}
    
    columnDefs.insert(0, {"field":"time",
                "valueGetter": {"function": datetime_obj},
                "valueFormatter": {"function": f"d3.timeFormat('%H:%M')({datetime_obj})"}
                })
    
    row_data = table.to_dict(orient="records")
    
    grid = dag.AgGrid(
        id="calendar_table",
        rowData=row_data,
        columnDefs=columnDefs,
        columnSize="sizeToFit",
        dashGridOptions = {"suppressFieldDotNotation": True,
                           "suppressRowTransform": True,
                           "context":"hello",}, # extremely nice we can pass data for rowSpanningComplex
    )

    return html.Div(
        className="calendar",
        children=[
            grid
        ]
    )