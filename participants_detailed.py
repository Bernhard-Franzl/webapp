from dash import Dash, html, dcc, Input, Output, callback
import json
import pandas as pd
from visualization.visualization import Visualizer
from datetime import datetime, date, time
from assets import page_header, plot_header

app = Dash(__name__, title="Visard")

## TODO:
# - Introduce filter by course name and/or course number


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
    "filtering": ["date"],
    "sorting": True,
    "mode": True,
}

app.layout = html.Div(children=[
    # page header
    page_header.layout(current_page="Onsite Participants"),
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
                mode=header_config["mode"]
            ),
            dcc.Graph(
            id="participants_single_course_bar",
            config=visard.config)
        ]
    )
])

def make_input_list(header_config):
    input_list = []
    
    # filering
    filter_list = header_config["filtering"]
    if "date" in filter_list:
        input_list.append(Input(
            component_id="date_picker",
            component_property="start_date"))
        input_list.append(Input(
            component_id="date_picker",
            component_property="end_date"))
        
    if "room" in filter_list:
        input_list.append(Input(
            component_id="room_filter",
            component_property="value"))
        
    if "start_time" in filter_list:
        input_list.append(Input(
            component_id="start_time_filter",
            component_property="value"))
    
    
    #Sorting
    if header_config["sorting"]:
        input_list.append(Input(
            component_id="graph_sort_by", 
            component_property="value"))
        input_list.append(Input(
            component_id="graph_sort_order", 
            component_property="on"))
        
        
    # mode
    if header_config["mode"]:
        input_list.append(Input(
            component_id="graph_mode", 
            component_property="value"))
        
    return input_list

input_list = make_input_list(header_config)    
@callback(
    [Output(
        component_id="participants_single_course_bar", 
        component_property="figure")],
    
    # filter
    input_list)
def update_figure(start_date_filter, end_date_filter, sort_by_column, ascending, graph_mode):
    ########## Filtering ##########
    course_number = "136.309"
    df = visard.filter_by_course_number(df_participants, course_number)
    
    # filter by date
    start_time = datetime.combine(date.fromisoformat(start_date_filter) , time(hour=0, minute=0))
    end_time = datetime.combine(date.fromisoformat(end_date_filter), time(hour=23, minute=59))
    df = visard.filter_by_time(df, start_time, end_time)
    
    ########## Sorting ##########
    df = visard.sort_by_column(df, sort_by_column, ascending=(not ascending))
    print(df)
    ########## Plotting ##########
    fig = visard.plot_course_bar(
        dataframe=df,
        mode=graph_mode
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)