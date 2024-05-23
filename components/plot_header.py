from dash import html, dcc, Input, Output
import dash_daq as daq


# gemerates the Input list
def generate_input_list(header_config):
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
    if "number" in filter_list:
        input_list.append(Input(
            component_id="course_number_filter",
            component_property="value"))
        
    if "name" in filter_list:
        input_list.append(Input(
            component_id="course_name_filter",
            component_property="value"))

    # grouping
    if header_config["grouping"]:
        input_list.append(Input(
            component_id="graph_group_by", 
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

def generate_output_list(header_config, figure_id):
    out_list = []
    
    if header_config["figure"]:
        out_list.append(Output(figure_id, "figure"))
        
    return out_list

# generates the header layout
def layout(title, 
           description=None, 
           filtering=[], 
           sorting=False, 
           mode=False,
           grouping=False,
           **kwargs):
    
    horizontal_line = html.Hr(
        style={
            "border": "0",
            "height": "2px",
            "color": "lightgrey",
            "backgroundColor": "lightgrey",
            }
        )
    
    # initialize layout
    # title is compulsory
    layout = html.Div(
        className="plot-header",
        children=[
            html.Div(
                className="plot-header--section",
                children=[
                    html.Div(
                        title,
                        className="plot-header--title"  
                    ),
                ]
            ),
        ]
    )
    
    plot_header = layout.children
    
    # if description is provided, add it to the layout
    if description != None:
        title_section = plot_header[0]
        description_section = html.Div(
            description,
            className="plot-header--description"
        )
        title_section.children.append(description_section)
        plot_header.append(horizontal_line)

    # if filtering is provided, add it to the layout
    if len(filtering) > 0:
        filtering_section = html.Div(
            className="plot-header--section",
            children=[
                html.Div(
                    "Filter By:",
                    className="plot-header--section-title"
                ),
                html.Div(
                    className="plot-header--section-elements",
                    children=[]
                )
            ]
        )
        
        for filter in filtering:
            if filter == "date":
                start_date = kwargs["start_date"]
                end_date = kwargs["end_date"]
                filtering_section.children[1].children.append(generate_date_filter(start_date, end_date))
                
            elif filter == "room":
                unique_rooms = kwargs["dataframe"]["room"].unique().tolist()
                filtering_section.children[1].children.append(generate_room_filter(unique_rooms))   
                
            elif filter == "start_time":
                start_time_list = sorted(kwargs["dataframe"]["start_time"].dt.time.unique())
                filtering_section.children[1].children.append(generate_start_time_filter(start_time_list))
                
            elif filter == "number":
                course_numbers = sorted(kwargs["dataframe"]["course_number"].unique())
                filtering_section.children[1].children.append(generate_number_filter(course_numbers))
                
            elif filter == "name":
                course_names = sorted(kwargs["dataframe"]["course_name"].unique())
                filtering_section.children[1].children.append(generate_name_filter(course_names))
                
            else:
                raise ValueError(f"Filtering option {filter} not recognized.")
        
        plot_header.append(filtering_section)
        plot_header.append(horizontal_line)
        
        
    # if sorting and/or mode are provided, add it to the layout  
    sorting_mode_section = html.Div(
            className="plot-header--section",
            children=html.Div(
                className="plot-header--section-elements",
                children=[]
            )
        )

    if sorting:
        sorting_section = generate_sorting_section()
        sorting_mode_section.children.children.append(sorting_section)
        
        if mode:
            mode_section = generate_mode_section()
            sorting_mode_section.children.children.append(mode_section)
            
            plot_header.append(sorting_mode_section)
            plot_header.append(horizontal_line)
            
        elif grouping:
            raise ValueError("Grouping and Sorting are not compatible.")
        
        else:
            plot_header.append(sorting_mode_section)
            plot_header.append(horizontal_line)
               
    else:
        if mode:
            if grouping:
                grouping_section = generate_grouping_section()
                sorting_mode_section.children.children.append(grouping_section)
                
            mode_section = generate_mode_section()
            sorting_mode_section.children.children.append(mode_section)
            
            plot_header.append(sorting_mode_section)
            plot_header.append(horizontal_line)
                
        else:
            pass
        
    del sorting_mode_section    
    
    return layout

def generate_date_filter(start_date, end_date):
    return html.Div(
            className="plot-header--filtering-date",
            children=[
                html.Div(
                    "Date:", 
                    className="plot-header--filtering-element-label"
                ),
                dcc.DatePickerRange(
                    id="date_picker",
                    display_format="DD.MM.YYYY",
                    min_date_allowed=start_date,
                    max_date_allowed=end_date,
                    initial_visible_month=start_date,
                    minimum_nights=0,
                    start_date=start_date,
                    end_date=end_date,
                    persistence=True,
                    persistence_type="memory",
                    persisted_props=["start_date", "end_date"]
                )
            ],
        )

def generate_room_filter(unique_rooms):
    return  html.Div(
        className="plot-header--filtering-room",
        children=[
            html.Div(
                "Room:", 
                className="plot-header--filtering-element-label"
            ),
            dcc.Dropdown(
                options=[{"label": room, "value": room} for room in unique_rooms],
                value=unique_rooms,
                multi=True,
                id="room_filter",
                style={"height": "32px", "line-height": "32px", "min-width": "150px"},
                persistence=True,
                persistence_type="memory",
                persisted_props=["value"]
            )
        ],
    )
    
def generate_start_time_filter(start_time_list):
    return html.Div(
        className="plot-header-filtering-starttime",
        children=[
            html.Div(
                "Start Time:",
                className="plot-header--filtering-element-label"
            ),
            dcc.Dropdown(
                options=[{"label": time.strftime("%H:%M") , "value": time} for time in start_time_list],
                value=[],
                multi=True,
                id="start_time_filter",
                style={"min-width": "150px", "max-width": "285px"},
                persistence=True,
                persistence_type="memory",
                persisted_props=["value"]
            )
        ]
        
    )

def generate_number_filter(course_numbers, id_data_list="number_suggestions"):
    
    data_list = html.Datalist(
        id=id_data_list, 
        children=[html.Option(value=word) for word in course_numbers],
        hidden=True)
    
    return html.Div(
        className="plot-header--filtering-number",
        children=[
            html.Div(
                "ID:",
                className="plot-header--filtering-element-label"
            ),
            dcc.Input(
                value="",
                type="text",
                placeholder="Course Number",
                id="course_number_filter",
                list=id_data_list,
                style={"font-size": "18px"},
            ),
            data_list
        ]
    )
    
def generate_name_filter(course_names, id_data_list="name_suggestions"):
    
    data_list = html.Datalist(
        id=id_data_list, 
        children=[html.Option(value=word) for word in course_names],
        hidden=True)
    
    return html.Div(
        className="plot-header--filtering-name",
        children=[
            html.Div(
                "Title:",
                className="plot-header--filtering-element-label"
            ),
            dcc.Input(
                value="",
                type="text",
                placeholder="Course Name",
                id="course_name_filter",
                list=id_data_list,
                style={"font-size": "18px"}
            ),
            data_list
        ]
    )
     
def generate_sorting_section():
    return  html.Div(
                className="plot-header--sorting",
                children=[
                    html.Div(
                        "Sort By:",
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
                                    id="graph_sort_by",
                                    persistence=True,
                                    persistence_type="memory",
                                    persisted_props=["value"]
                                )
                            ),
                            html.Div(
                                className="plot-header--sorting-switch",
                                children=daq.BooleanSwitch(
                                    id="graph_sort_order",
                                    on=False,
                                    persistence=True,
                                    persistence_type="memory")
                            )
                        ]
                    )
                ]
            )

def generate_mode_section():
    return html.Div(
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
                            id="graph_mode",
                            persistence=True,
                            persistence_type="memory",
                            persisted_props=["value"]
                        ),
                    )
                ]
            )

def generate_grouping_section():
    return html.Div(
                className="plot-header--grouping",
                children=[
                    html.Div("Group By:",
                            className="plot-header--section-title"
                    ),
                    html.Div(
                        className="plot-header--grouping-dropdown",
                        children=dcc.Dropdown(
                            options=["weekday", "room", "type", "duration", "start_time_string"],
                            value=["weekday"],
                            id="graph_group_by",
                            multi=True,
                            persistence=True,
                            persistence_type="memory",
                            persisted_props=["value"]
                        )
                    )
                ]
    )