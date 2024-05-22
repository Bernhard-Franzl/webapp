
from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from components import course_info
from visualization.visualization import Visualizer
from datetime import datetime, date, time
from components import plot_header

register_page(__name__, name="Course Details", order=2)

## TODO:
# - make course information -> more structured
# - institute info
# - add a table that shows the available courses

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


visard = Visualizer(plot_height=750, plot_width=750,
                    margin=dict(l=125, r=50, t=50, b=50))

header_config = {
    "title": "Course Participants Detailed View",
    "description": "This page provides a more detailed view on a single course.",
    "filtering": ["date", "number", "name"],
    "grouping": False,
    "sorting": False,
    "mode": False,
    "course_info": True,
    "figure":True 
}


    
layout = html.Div(children=[
    # plot
    html.Div(
        className="plot",
        children=[
            # Header
            plot_header.layout(
                title=header_config["title"],
                description= header_config["description"],
                filtering=header_config["filtering"],
                start_date = start_date,
                end_date = end_date,
                dataframe = df_participants,
                sorting=header_config["sorting"],
                mode=header_config["mode"],
                course_info=header_config["course_info"]
            ),
            # Plot and course info
            html.Div(
                className="course_detail_plot",
                children =[
                    html.Div(
                        course_info.initialize_layout()
                        ),
                    html.Div(
                        className=visard.get_css_class(),
                        children=dcc.Graph(
                            id="participants_single_course_bar",
                            config=visard.config
                        )
                    )
                    
                ]
            )
        ]
    )
])


input_list = plot_header.generate_input_list(header_config)
output_list = plot_header.generate_output_list(header_config, "participants_single_course_bar")
output_list.append(Output("course_info", "children"))
@callback(
    output_list,
    input_list)
def update_figure(start_date_filter, end_date_filter, course_number, course_name):
    ########## Filtering ########## 
    df = df_participants.copy()
    # filter by date
    start_time = datetime.combine(date.fromisoformat(start_date_filter) , time(hour=0, minute=0))
    end_time = datetime.combine(date.fromisoformat(end_date_filter), time(hour=23, minute=59))
    df = visard.filter_by_time(df, start_time, end_time)
    # filter by course number
    course_filtered = False
    if course_number != "":
        df = visard.filter_by_course_number(df, course_number)
        if len(df) != 0:
            course_filtered = True
    # filter by course name
    if course_name != "" and (not course_filtered):
        df = visard.filter_by_course_name(df, course_name)
        if len(df) != 0:
            course_filtered = True
            
    ########## Course Info ##########
    if course_filtered:
        info_section = course_info.generate_course_info(df)
    else:
        info_section = "Please select a course!"
    
    ########## Plotting ##########
    if course_filtered:
        fig = visard.plot_course_bar(
            dataframe=df
        )
    else:
        fig = visard.plot_empty_course_bar()
    
    return fig, info_section