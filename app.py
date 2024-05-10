from dash import Dash, html, dcc, Input, Output, callback
import dash_daq as daq
import json
import pandas as pd
from datetime import datetime, date, time

from visualization.visualization import Visualizer

app = Dash(__name__, title="Visard")

## TODO:
# - Fix note in hover text
# - ascending descending sort option


###### load data ########
df_participants = pd.read_csv("data/df_participants.csv")
df_participants["start_time"] = pd.to_datetime(df_participants["start_time"])
df_participants["end_time"] = pd.to_datetime(df_participants["end_time"])

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
    html.Div(
        className="page-header",
        children=[
            html.Div(
                "Onsite Participants",
                className="page-header--title"
            ),
        ]
    ),
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
                    className="plot-header--filtering",
                    children=[
                        html.Div("Filter By:",
                                className="plot-header--section-title"
                        ),
                        html.Div(
                            class_name="plot-header--filtering-elements",
                            children=[
                                dcc.DatePickerRange(
                                    id="date_picker",
                                    display_format="DD.MM.YYYY",
                                    min_date_allowed=start_date,
                                    max_date_allowed=end_date,
                                    initial_visible_month=start_date,
                                    minimum_nights=0,
                                    start_date=start_date,
                                    end_date=end_date,
                                ),
                            ],
                        ),
                    ]
                ),
                html.Div(
                    className="plot-header--sorting-mode",
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
                ),
            ],
        ),
        dcc.Graph(
        id="participants_multi_course_bar",
        config=visard.config)
        ]
    ),
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
def update_figure(start_date, end_date, sort_by_column, ascending, graph_mode):

    start_time = datetime.combine(date.fromisoformat(start_date) , time(hour=0, minute=0))
    end_time = datetime.combine(date.fromisoformat(end_date), time(hour=23, minute=59))
    df = visard.filter_by_time(df_participants, start_time, end_time)
    
    df = visard.sort_by_column(df, sort_by_column, ascending=(not ascending))
    fig = visard.plot_multiple_courses_bars(
        dataframe=df,
        course_numbers=df["course_number"].unique(),
        title="Participants per Course Date",
        mode=graph_mode
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)