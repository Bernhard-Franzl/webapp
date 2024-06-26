from dash import  html, dcc, callback, register_page
from components import plot_header
from data_handler import DataHandler

from visualization.visualization import Visualizer

register_page(__name__, name="Grouped Data" ,order=4)


###### Load Data ########
data_handler = DataHandler("data")
df_participants = data_handler.get_data()
metadata_participants = data_handler.get_meta_data()

start_date = metadata_participants["start_time"].date()
end_date = metadata_participants["end_time"].date()

visard = Visualizer(plot_height=750, plot_width=1200)

header_config = {
    "title": "Grouped Onsite Participants Data",
    "description": "This page visualizes the data grouped by a selection of features.",
    "filtering": ["date", "room", "start_time"],
    "grouping": True,
    "sorting": False,
    "dataframe": df_participants,
    "mode": True,
    "course_info": False,
    "figure":True 
}

layout = html.Div(
    className="page",
    children=[
        plot_header.layout(
            start_date = start_date,
            end_date = end_date,
            **header_config
        ),
        html.Div(
            className=visard.get_css_class(),
            children=[
                dcc.Graph(
                    id="grouped_bar_chart",
                    config=visard.config)
            ]
        )
    ]
)

input_list = plot_header.generate_input_list(header_config)
output_list = plot_header.generate_output_list(header_config, "grouped_bar_chart", details=False)
@callback(
    output_list,
    input_list)
def update_figure(start_date_filter, end_date_filter, room_filter, start_time_filter, group_by, graph_mode):
   
    df = df_participants.copy()
    
    ########## Filtering ##########
    # filter by date
    df = data_handler.filter_by_date(df, start_date_filter, end_date_filter)
    # filter by room
    df = data_handler.filter_by_rooms(df, room_filter)
    # filter by start time
    df = data_handler.filter_by_start_time(df, start_time_filter)
    
    
     ########## Grouping ##########
    # keep only the informative columns
    df, grouped = data_handler.group_data(df, group_by)
    
    if grouped:
        fig = visard.plot_grouped_bar(
            dataframe=df,
            group_by=group_by,
            mode=graph_mode
        )
    else:
        fig = visard.plot_empty_grouped_bar()
        
    return fig,