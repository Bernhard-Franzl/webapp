from dash import html, dcc, callback, register_page, Output, Input
from components import plot_header, course_info
from data_handler import DataHandler
from visualization.visualization import Visualizer

register_page(__name__, name="Courses Overview", order=1)
id_suffix = "overview"
## TODO:
# - restructure header in as table
# - add different header id in order to make settings persistent
# - make button to hide the course info
# - fix the axis titles in the case of only two or less rows
# - reset button for the filters -> resets them to initial values
#   which is showing all data

###### Load Data ########

data_handler = DataHandler("data")
df_participants = data_handler.get_data()
metadata_participants = data_handler.get_meta_data()


start_date = metadata_participants["start_time"].date()
end_date = metadata_participants["end_time"].date()

visard_details = Visualizer(margin=dict(l=35, r=35, t=50, b=35),
                            plot_height=850,
                            axis_title_size=16)
visard_overview = Visualizer(margin=dict(l=5, r=35, t=35, b=5),
                             plot_height=1250)
header_config = {
    "title": "Course Participants Overview",
    "description": "This page provides an overview of the onsite participants of all the courses.",
    "filtering": ["date", "room",  "number", "name", "start_time"],
    "grouping": False,
    "sorting": True,
    "mode": True,
    "figure":True,
    "dataframe": df_participants,
    "course_info": True,
}


def layout(course_id="none"):
    return html.Div(
        className="page",
        children=[
            plot_header.layout(
                start_date = start_date,
                end_date = end_date,
                course_id_default=course_id,
                id_suffix=id_suffix,
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
                                className="details-info-container",
                                id="details_course_info"
                            ),
                            html.Div(
                                className="details-plot-container",
                                children=dcc.Graph(
                                        id="participants_details_bar",
                                        config=visard_details.config
                                )
                            )
                        ]
                    )
                ]
            )
        ]
    )

input_list = plot_header.generate_input_list(header_config=header_config, id_suffix=id_suffix)
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
    [Input(f"date_picker_{id_suffix}", "start_date"),
    Input(f"date_picker_{id_suffix}", "end_date"),
    Input(f"course_number_filter_{id_suffix}", "value"),
    Input(f"course_name_filter_{id_suffix}", "value"),
    Input("participants_multi_course_bar", "clickData")]
    )
def update_details_figure(start_date_filter, end_date_filter,
                  course_number_filter, course_name_filter, clickData):

    df = df_participants.copy()
    
    ########## Filtering ########## 
    # filter by date
    df = data_handler.filter_by_date(df, start_date_filter, end_date_filter)

    # extract clickData    
    if clickData is not None:
        course_number_click = clickData["points"][0]["customdata"][0]
    else:
        course_number_click = ""          
    
    # filter by course number or name
    df, course_filtered = data_handler.filter_course(df, course_number_filter, course_name_filter, course_number_click)
            
    ########## Course Info ##########
    if course_filtered:
        info_section = course_info.generate_course_info(df)
    else:
        info_section = None
    
    ########## Plotting ##########
    if course_filtered:
        fig = visard_details.plot_course_bar(
            dataframe=df
        )
    else:
        fig = visard_details.plot_empty_course_bar()
    
    return [fig, info_section]
