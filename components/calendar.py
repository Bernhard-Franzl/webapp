from dash import Dash, html, dash_table
import dash_ag_grid as dag
from datetime import datetime, date, time
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
    
    data["start_time"] = data["start_time"].dt.time
    
    #df["people_in"] = df["event_type"].apply(lambda x: 1 if x == 1 else 0)
    #df["people_out"] = df["event_type"].apply(lambda x: 1 if x == 0 else 0)
    
    #idx = pd.date_range(start=start, end=end, freq=f'{n}min')
    
    #df = df.set_index("time")\
    #        .resample(f"{n}min")\
    #        .sum().reindex(idx, fill_value=0).reset_index()

    #df.rename(columns={"index":"time"}, inplace=True)
    
    #df["people_in"] = df["people_in"].cumsum()
    #df["people_out"] = df["people_out"].cumsum()
    #df["people_inside"] = df["people_in"] - df["people_out"]
        
        
    table = data.pivot_table(index=["start_time"], 
                             columns=["weekday"], 
                             values="course_number",
                             aggfunc="first").fillna("")
    
    print(table.resample("15min"))
    #print(table.set_index("start_time").resample(f"15min").sum())
    #table.index = table.index.date()
    
    
    weekday_list = sorted([weekday_to_id[weekday] for weekday in data["weekday"].unique()])
    weekday_list = [list(weekday_to_id)[weekday] for weekday in weekday_list]
    table = table[weekday_list]
    

    print(table)



    # weekdays as columns
    table = table.reset_index()
    columns = [{"field": weekday} for weekday in table.columns]
    row_data = table.to_dict(orient="records")

    
    grid = dag.AgGrid(
        id="get-started-example-basic",
        rowData=row_data,
        columnDefs=columns,
        dashGridOptions = {"suppressFieldDotNotation": True}
    )
    

    return html.Div(
        className="calendar",
        children=[
            grid
        ]
    )