from dash import html, dcc, callback, register_page, Output
from components import plot_header, course_info
from data_handler import DataHandler
from visualization.visualization import Visualizer

register_page(__name__, name="Courses Overview", order=1)

## TODO:
# - incorporate the course info section
# - fix the axis titles in the case of only two or less rows
# - reset button for the filters -> resets them to initial values
#   which is showing all data
# - fix that you can either filter by course number or course name if one is selected the
#  other one should be disabled!

###### Load Data ########
data_handler = DataHandler("data")
df_participants = data_handler.get_data()
metadata_participants = data_handler.get_meta_data()


start_date = metadata_participants["start_time"].date()
end_date = metadata_participants["end_time"].date()

visard_details = Visualizer(margin=dict(l=35, r=35, t=35, b=35),
                            plot_height=750)
visard_overview = Visualizer(margin=dict(l=5, r=35, t=35, b=5),
                             plot_height=1250)
header_config = {
    "title": "Course Participants Overview",
    "description": "This page provides an overview of the onsite participants of all the courses.",
    "filtering": ["date", "room", "start_time", "number", "name"],
    "grouping": False,
    "sorting": True,
    "mode": True,
    "figure":True,
    "dataframe": df_participants,
    "course_info": True,
}



def layout():
    return html.Div(
        className="page",
        children=[
            plot_header.layout(
                start_date = start_date,
                end_date = end_date,
                course_id_default="",
                **header_config
            ),
            html.Div(
                className="content-container",
                children=[
                    html.Div(
                        className="overview-container",
                        children=[
                            html.Div(
                                id="id-overview-yaxis-container",
                                className="overview-yaxis-container"
                            ),
                            html.Div(
                                className="overview-plot-container",
                                children=dcc.Graph(
                                    id="participants_multi_course_bar",
                                    config=visard_overview.config)
                            ),
                            html.Div(
                            className="overview-xaxis-container",
                            children="Course Number")
                        ]
                    ),
                    html.Div(
                        className="details-container",
                        children =[
                            html.Div(
                                course_info.initialize_layout(id="details_course_info")
                            ),
                            dcc.Graph(
                                    id="participants_details_bar",
                                    config=visard_details.config
                            )
                        ]
                    )
                ]
            )
        ]
    )


input_list = plot_header.generate_input_list(header_config=header_config)
output_list = plot_header.generate_output_list(header_config=header_config, 
                                               figure_id="participants_multi_course_bar", 
                                               details=True)
@callback(
    [Output("participants_multi_course_bar", "figure"),
    Output("id-overview-yaxis-container", "children")],
    input_list
    )
def update_overview_figure(start_date_filter, end_date_filter, room_filter, start_time_filter, 
                  course_number_filter, course_name_filter, sort_by_column, ascending, graph_mode):
    
    df = df_participants.copy()
    
    ########## Filtering ##########
    # filter by date
    df = data_handler.filter_by_date(df, start_date_filter, end_date_filter)
    # filter by room
    df = data_handler.filter_by_rooms(df, room_filter)
    # filter by start_time
    df = data_handler.filter_by_start_time(df, start_time_filter)

    ########## Sorting ##########
    df = data_handler.sort_by_column(df, sort_by_column, ascending=(not ascending))
    
    y_title = [html.Div("Onsite Participants", style={"font-weight":"bold"}), html.Div(visard_overview.handle_mode_y_title(graph_mode))]
    
    ########## Plotting ##########
    fig_overview = visard_overview.plot_multiple_courses_bars(
        dataframe=df,
        course_numbers=df["course_number"].unique(),
        mode=graph_mode
    )
    return fig_overview, y_title

@callback(
    [Output("participants_details_bar", "figure"),
     Output("details_course_info", "children")],
    input_list
    )
def update_details_figure(start_date_filter, end_date_filter, room_filter, start_time_filter, 
                  course_number_filter, course_name_filter, sort_by_column, ascending, graph_mode):
    
    df = df_participants.copy()
    
    ########## Filtering ########## 
    # filter by date
    df = data_handler.filter_by_date(df, start_date_filter, end_date_filter)
    # filter by course number or name
    df, course_filtered = data_handler.filter_course(df, course_number_filter, course_name_filter)
            
    ########## Course Info ##########
    if course_filtered:
        info_section = course_info.generate_course_info(df)
    else:
        info_section = "Please select a course!"
    
    ########## Plotting ##########
    if course_filtered:
        fig = visard_details.plot_course_bar(
            dataframe=df
        )
    else:
        fig = visard_details.plot_empty_course_bar()
    
    return [fig, info_section]
