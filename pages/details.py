
from dash import Dash, html, dcc, Input, Output, callback, register_page, page_registry
import json
import pandas as pd
from components import course_info
from visualization.visualization import Visualizer
from datetime import datetime, date, time
from components import plot_header
from data_handler import DataHandler

register_page(__name__,name="Course Details", path_template="/details/<course_id>",order=3)


## TODO:
# - make course information -> more structured
# - institute info
# - add a table that shows the available courses

###### Load Data ########
data_handler = DataHandler("data")
df_participants = data_handler.get_data()
metadata_participants = data_handler.get_meta_data()

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
    "dataframe": df_participants,
    "course_info": True,
    "figure":True 
}


def layout(course_id="none"):
    return html.Div(
        className="page",
        children=[
            # Header
            plot_header.layout(
                start_date = start_date,
                end_date = end_date,
                course_id_default=course_id,
                **header_config
                
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




input_list = plot_header.generate_input_list(header_config)
output_list = plot_header.generate_output_list(header_config, "participants_single_course_bar")
output_list.append(Output("course_info", "children"))
@callback(
    output_list,
    input_list)
def update_figure(start_date_filter, end_date_filter, course_number, course_name):
    
    df = df_participants.copy()
    
    ########## Filtering ########## 
    # filter by date
    df = data_handler.filter_by_date(df, start_date_filter, end_date_filter)
    # filter by course number or name
    df, course_filtered = data_handler.filter_course(df, course_number, course_name)
            
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