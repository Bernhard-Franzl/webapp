
from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from visualization.visualization import Visualizer
from datetime import datetime, date, time
from assets import plot_header

register_page(__name__, order=1)

## TODO:
# - add subplot titles
# - institute info

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


visard = Visualizer()

header_config = {
    "title": "Course Participants Detailed View",
    "description": "This plot provides a more detailed view on the participants of a single course.",
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
            dcc.Graph(
            id="participants_single_course_bar",
            config=visard.config)
        ]
    )
])


input_list = plot_header.generate_input_list(header_config)
output_list = plot_header.generate_output_list(header_config, "participants_single_course_bar")
@callback(
    output_list,
    input_list)
def update_figure(start_date_filter, end_date_filter, course_number, course_name):
    ########## Filtering ##########    
    # filter by date
    start_time = datetime.combine(date.fromisoformat(start_date_filter) , time(hour=0, minute=0))
    end_time = datetime.combine(date.fromisoformat(end_date_filter), time(hour=23, minute=59))
    df = visard.filter_by_time(df_participants, start_time, end_time)
    # filter by course number
    course_filtered = False
    if course_number != "":
        df = visard.filter_by_course_number(df_participants, course_number)
        if len(df) != 0:
            course_filtered = True
    # filter by course name
    if course_name != "" and (not course_filtered):
        df = visard.filter_by_course_name(df, course_name)
        if len(df) != 0:
            course_filtered = True
            
    ########## Course Info ##########
    if course_filtered:
        course_info = plot_header.generate_course_info(df)
    else:
        course_info = "Nothing to show."
    
    ########## Plotting ##########
    if course_filtered:
        fig = visard.plot_course_bar(
            dataframe=df
        )
    else:
        fig = visard.plot_empty_course_bar()
    
    return fig, course_info