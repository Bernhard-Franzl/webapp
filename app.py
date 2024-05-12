from dash import Dash, html, dcc, Input, Output, callback
import dash_daq as daq
import json
import pandas as pd
from datetime import datetime, date, time
from assets import page_header

from visualization.visualization import Visualizer

app = Dash(__name__, title="Visard")

## TODO:
# - Fix note in hover text
# - ascending descending sort option


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

app.layout = html.Div(children=[
    # page header
    page_header.layout(current_page="Onsite Participants"),
    # plot
    html.Div(
        className="plot",
        children=[
            html.Div(
                className="plot-header",
                children=[
                    html.Div(
                        "Course Participants Overview",
                        className="plot-header--title"  
                    ),
                    html.Div(
                        "This plot provides an overview of the onsite participants of all the courses.",
                        className="plot-header--description"
                    ),
                    html.Div(
                        className="plot-header--section",
                        children=html.Div(
                            className="plot-header--filtering",
                            children=[
                                html.Div("Filter By:",
                                        className="plot-header--section-title"
                                ),
                                html.Div(
                                    className="plot-header--filtering-elements",
                                    children=[
                                        html.Div(
                                            className="plot-header--filtering-date",
                                            children=[
                                                html.Div(
                                                    "Date:", 
                                                    className="plot-header--filtering-element-label"),
                                                dcc.DatePickerRange(
                                                    id="date_picker",
                                                    display_format="DD.MM.YYYY",
                                                    min_date_allowed=start_date,
                                                    max_date_allowed=end_date,
                                                    initial_visible_month=start_date,
                                                    minimum_nights=0,
                                                    start_date=start_date,
                                                    end_date=end_date
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="plot-header--filtering-room",
                                            children=[
                                                html.Div(
                                                    "Room:", 
                                                    className="plot-header--filtering-element-label"),
                                                dcc.Dropdown(
                                                    options=[{"label": room, "value": room} for room in df_participants["room"].unique()],
                                                    value=df_participants["room"].unique().tolist(),
                                                    multi=True,
                                                    id="room_filter",
                                                    style={"height": "40px", "line-height": "40px", "min-width": "175px"}
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="plot-header-filtering-starttime",
                                            children=[
                                                html.Div(
                                                    "Time:",
                                                    className="plot-header--filtering-element-label"
                                                ),
                                                dcc.Dropdown(
                                                    options=[{"label": time, "value": time} for time in sorted(df_participants["start_time"].dt.time.unique())],
                                                    value=sorted(df_participants["start_time"].dt.time.unique()),
                                                    multi=True,
                                                    optionHeight=35,
                                                    maxHeight=50,
                                                    id="start_time_filter",
                                                    style={ "line-height": "40px", 
                                                           "min-width": "175px", "max-width": "300px", 
                                                           "max-height": "200px", "overflow": "scroll"}
                                                )
                                            ]
                                            
                                        )
                                    ]
                                ),
                            ],
                        ),
                    ),
                    html.Div(
                        className="plot-header--section",
                        children=[
                            html.Div(
                                className="plot-header--sorting",
                                children=[
                                    html.Div("Sort By:",
                                            className="plot-header--section-title"
                                    ),
                                    html.Div(
                                        className="plot-header--sorting-elements",
                                        children=[
                                            html.Div(
                                                className="plot-header--sorting-dropdown",
                                                children=dcc.Dropdown(
                                                    options=["course_number", "course_name", "room", "start_time", 
                                                            "type", "ects", "registered_students", "duration"],
                                                    value="course_number",
                                                    id="participants_graph_sort_by",
                                                )
                                            ),
                                            html.Div(
                                                className="plot-header--sorting-switch",
                                                children=daq.BooleanSwitch(
                                                    id="participants_graph_sort_order",
                                                    on=False,),
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                            html.Div(
                                className="plot-header--mode",
                                children=[
                                    html.Div("Frequency Mode:",
                                            className="plot-header--section-title"
                                    ),
                                    html.Div(
                                        className="plot-header--mode-dropdown",
                                        children=dcc.Dropdown(
                                            options=["absolute", "relative_registered", "relative_capacity"],
                                            value="absolute",
                                            id="participants_graph_mode",
                                        ),
                                    )
                                ]
                            ),  
                        ],
                    )    
                ],
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
        component_id="participants_graph_sort_by", 
        component_property="value"),
    Input(
        component_id="participants_graph_sort_order", 
        component_property="on"),
    
    # mode  
    Input(
        component_id="participants_graph_mode", 
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
    df = visard.sort_by_column(df, sort_by_column, ascending=(not ascending))
    
    ########## Plotting ##########
    fig = visard.plot_multiple_courses_bars(
        dataframe=df,
        course_numbers=df["course_number"].unique(),
        title="Participants per Course Date",
        mode=graph_mode
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)