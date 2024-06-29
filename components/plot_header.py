from dash import html, dcc, Input, Output
import dash_daq as daq


# gemerates the Input list
def generate_input_list(header_config, id_suffix):
    input_list = []
    
    # filering
    filter_list = header_config["filtering"]
    if "date" in filter_list:
        input_list.append(Input(
            component_id=f"date_picker_{id_suffix}",
            component_property="start_date"))
        input_list.append(Input(
            component_id=f"date_picker_{id_suffix}",
            component_property="end_date"))
        
    if "room" in filter_list:
        input_list.append(Input(
            component_id=f"room_filter_{id_suffix}",
            component_property="value"))
        
    if "calendar_week" in filter_list:
        input_list.append(Input(
            component_id=f"calendar_week_filter_{id_suffix}",
            component_property="value"))
        
    if "start_time" in filter_list:
        input_list.append(Input(
            component_id=f"start_time_filter_{id_suffix}",
            component_property="value"))
    
    if "number" in filter_list:
        input_list.append(Input(
            component_id=f"course_number_filter_{id_suffix}",
            component_property="value"))
        
    if "name" in filter_list:
        input_list.append(Input(
            component_id=f"course_name_filter_{id_suffix}",
            component_property="value"))

    # grouping
    if header_config["grouping"]:
        input_list.append(Input(
            component_id=f"graph_group_by_{id_suffix}", 
            component_property="value"))
        
    #Sorting
    if header_config["sorting"]:
        input_list.append(Input(
            component_id=f"graph_sort_by_{id_suffix}", 
            component_property="value"))
        input_list.append(Input(
            component_id="graph_sort_order", 
            component_property="on"))
        
    # mode
    if header_config["mode"]:
        input_list.append(Input(
            component_id=f"graph_mode_{id_suffix}", 
            component_property="value"))
        
    return input_list

def generate_output_list(header_config, figure_id, details):
    out_list = []
    
    if header_config["figure"]:
        out_list.append(Output(figure_id, "figure"))
    if details:
        out_list.append(Output("participants_details_bar", "figure"))
    return out_list

# generates the header layout
def layout(title,
           id_suffix, 
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
    else:
        plot_header.append(horizontal_line)
            
    # restructure header as table
    data_manipulation_section = html.Div(
            className="plot-header--data-section",
            children=[]
        )

    table = html.Table(
        className="plot-header--table",
        children = [
            html.Tr(
                className="plot-header--table-header",
                children=[
                    html.Th(
                        children="Filter By:",
                        className="plot-header--table-header-element",
                        colSpan=4
                        )
                ]
            ),
        ]
    )

    # if filtering is provided, add it to the layout
    if len(filtering) > 0:
        
        modulo_2 = len(filtering)%2
        if modulo_2 == 1:
            n_rows = len(filtering)//2 + 1
        else:
            n_rows = len(filtering)//2
        
        for i in range(n_rows):
            table.children.append(
                html.Tr(
                    className="plot-header--table-row",
                    children=[]
                )
            )

        for i, filter in enumerate(filtering):
            
            row_nr = i//2 + 1

            if filter == "date":
                start_date = kwargs["start_date"]
                end_date = kwargs["end_date"]
                table.children[row_nr].children.extend(generate_date_filter(start_date, end_date, id_suffix))
                
            elif filter == "room":
                try:
                    multi = kwargs["multi_room"]
                except KeyError:
                    multi = True
                unique_rooms = kwargs["dataframe"]["room"].unique().tolist()
                table.children[row_nr].children.extend(generate_room_filter(unique_rooms, multi, id_suffix))   
                
            elif filter == "calendar_week":
                try:
                    multi = kwargs["multi_calendar_week"]
                except KeyError:
                    multi = True

                unique_calendar_weeks = kwargs["dataframe"]["calendar_week"].unique().tolist()
                table.children[row_nr].children.extend(generate_weekday_filter(unique_calendar_weeks, multi, id_suffix))
                                                              
            elif filter == "start_time":
                start_time_list = sorted(kwargs["dataframe"]["start_time"].dt.time.unique())
                table.children[row_nr].children.extend(generate_start_time_filter(start_time_list, id_suffix))
                
            elif filter == "number":
                course_numbers = sorted(kwargs["dataframe"]["course_number"].unique())
                table.children[row_nr].children.extend(generate_number_filter(course_numbers, id_suffix, course_id_default=kwargs["course_id_default"]))
                
            elif filter == "name":
                course_names = sorted(kwargs["dataframe"]["course_name"].unique())
                table.children[row_nr].children.extend(generate_name_filter(course_names, id_suffix))
                
            else:
                raise ValueError(f"Filtering option {filter} not recognized.")
        
        data_manipulation_section.children.append(table)
     
     
    table_2 = html.Table(
        className="plot-header--table",
        children = []
    )   
        
    # if sorting and/or mode are provided, add it to the layout  
    #sorting_mode_section = html.Div(
    #        className="plot-header--section",
    #        children=html.Div(
    #            className="plot-header--section-elements",
    #            children=[]
    #        )
    #    )

    if sorting:
        sorting_section = generate_sorting_section(id_suffix)
        
        table_2.children.extend(sorting_section)
        
        if mode:
            try:
                mode_section = generate_mode_section(kwargs["mode_options"],id_suffix)
            except KeyError:
                mode_section = generate_mode_section(None, id_suffix)
            #sorting_mode_section.children.children.append(mode_section)
            
            table_2.children.extend(mode_section)
            data_manipulation_section.children.append(table_2)
            
        elif grouping:
            raise ValueError("Grouping and Sorting are not compatible.")
        
        else:
            data_manipulation_section.children.append(table_2)
               
    else:
        if mode:
            if grouping:
                grouping_section = generate_grouping_section(id_suffix)
                table_2.children.extend(grouping_section)
                
            try:
                mode_section = generate_mode_section(kwargs["mode_options"], id_suffix)
            except KeyError:
                mode_section = generate_mode_section(None, id_suffix)
                
            table_2.children.extend(mode_section)
            data_manipulation_section.children.append(table_2)
                
        else:
            pass
    
    plot_header.append(data_manipulation_section)
    plot_header.append(horizontal_line)
    return layout

def generate_date_filter(start_date, end_date, id_suffix):
    return [html.Td(
                "Date:", 
                className="plot-header--table-label"
            ),
            html.Td(
                className="plot-header--table-cell",
                children=dcc.DatePickerRange(
                    id=f"date_picker_{id_suffix}",
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
            )
    ]

def generate_room_filter(unique_rooms, multiple, id_suffix):
    
    if multiple:
        default_value = unique_rooms
    else:        
        default_value = unique_rooms[0]
    return [html.Td(
                "Room:", 
                className="plot-header--table-label"
            ),
            html.Td(
                className="plot-header--table-cell",
                children=dcc.Dropdown(
                    options=[{"label": room, "value": room} for room in unique_rooms],
                    value=default_value,
                    multi=multiple,
                    id=f"room_filter_{id_suffix}",
                    style={"height": "32px", "line-height": "32px", "min-width": "150px"},
                    persistence=True,
                    persistence_type="local",
                    persisted_props=["value"]
                )
            )
        ]
   
def generate_weekday_filter(unique_calendar_weeks, multiple, id_suffix):
    if multiple:
        default_value = unique_calendar_weeks
    else:        
        default_value = unique_calendar_weeks[0]
        
    return [html.Td(
                "Week:", 
                className="plot-header--table-label",
            ),
            html.Td(
                className="plot-header--table-cell",
                children=dcc.Dropdown(
                    options=[{"label": f"CW {cw}", "value": cw} for cw in unique_calendar_weeks],
                    value=default_value,
                    multi=multiple,
                    id=f"calendar_week_filter_{id_suffix}",
                    style={"height": "32px", "line-height": "32px", "min-width": "150px"},
                    persistence=True,
                    persistence_type="memory",
                    persisted_props=["value"]
                )
            )
        ]
       
def generate_start_time_filter(start_time_list, id_suffix):
    return[html.Td(
                "Start Time:",
                className="plot-header--table-label"
            ),
            html.Td(
                className="plot-header--table-cell",
                children=dcc.Dropdown(
                    options=[{"label": time.strftime("%H:%M") , "value": time} for time in start_time_list],
                    value=[],
                    multi=True,
                    id=f"start_time_filter_{id_suffix}",
                    style={"min-width": "150px", "max-width": "285px"},
                    persistence=True,
                    persistence_type="memory",
                    persisted_props=["value"]
                )
            )
        ]

def generate_number_filter(course_numbers, id_suffix, id_data_list="number_suggestions", course_id_default=""):
    if course_id_default != "none":
        default_value = course_id_default
    else:
        default_value = ""
    
    data_list = html.Datalist(
        id=id_data_list, 
        children=[html.Option(value=word) for word in course_numbers],
        hidden=True)
    
    return [html.Td(
                "ID:",
                className="plot-header--table-label"
            ),
            html.Td(
                className="plot-header--table-cell",
                children=[
                    dcc.Input(
                        value=default_value,
                        type="text",
                        placeholder="Course Number",
                        id=f"course_number_filter_{id_suffix}",
                        list=id_data_list,
                        style={"font-size": "18px"},
                    ),
                    data_list
                ]
            )
        ]
    
def generate_name_filter(course_names, id_suffix, id_data_list="name_suggestions"):
    
    data_list = html.Datalist(
        id=id_data_list, 
        children=[html.Option(value=word) for word in course_names],
        hidden=True)
    
    return [html.Td(
                "Title:",
                className="plot-header--table-label"
            ),
            html.Td(
                className="plot-header--table-cell",
                children=[
                    dcc.Input(
                        value="",
                        type="text",
                        placeholder="Course Name",
                        id=f"course_name_filter_{id_suffix}",
                        list=id_data_list,
                        style={"font-size": "18px"},
                    ),
                    data_list
                ]
            )
        ]
     
def generate_sorting_section(id_suffix):
    return  [html.Tr(
                className="plot-header--table-header",
                children=[
                    html.Th(
                        children="Sort By:",
                        className="plot-header--table-header-element",
                        )
                    ]
            ),
            html.Tr(
                    html.Td(
                        className="plot-header--sorting-elements",
                        children=[
                            html.Div(
                                className="plot-header--sorting-dropdown",
                                children=dcc.Dropdown(
                                    options=["course_number", "course_name", "room", "start_time", 
                                            "type", "ects", "registered_students", "duration"],
                                    value="course_number",
                                    id=f"graph_sort_by_{id_suffix}",
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
                                    persistence_type="local")
                            )
                        ]
                    )
                )
            ]   

def generate_mode_section(mode_options, id_suffix):
    if mode_options == None:
        mode_option_list = ["absolute", "relative_registered", "relative_capacity"]
    else:
        mode_option_list = mode_options
        
    return [html.Tr(
                className="plot-header--table-header",
                children=[
                    html.Th(
                        children="Frequency Mode:",
                        className="plot-header--table-header-element",
                        )
                ]
            ),
            html.Tr(
                html.Td(
                    className="plot-header--mode-dropdown",
                    children=dcc.Dropdown(
                        options=mode_option_list,
                        value=mode_option_list[0],
                        id=f"graph_mode_{id_suffix}",
                        persistence=True,
                        persistence_type="memory",
                        persisted_props=["value"]
                    ),
                )
            )
        ]

def generate_grouping_section(id_suffix):
    return [html.Tr(
                className="plot-header--table-header",
                children=[
                    html.Th(
                        children="Group By:",
                        className="plot-header--table-header-element",
                        )
                ]
            ),
            html.Tr(
                html.Td(
                    className="plot-header--grouping-dropdown",
                    children=dcc.Dropdown(
                        options=["weekday", "calendar_week", "room", "type", "duration", "start_time_string",
                                    "institute", "level", "curriculum","exam", "test", "tutorium"],
                        value=["weekday"],
                        id=f"graph_group_by_{id_suffix}",
                        multi=True,
                        persistence=True,
                        persistence_type="memory",
                        persisted_props=["value"]
                    )
                )
            )
        ]
    
    








#def generate_date_filter(start_date, end_date):
#    return html.Div(
#            className="plot-header--filtering-date",
#            children=[
#                html.Div(
#                    "Date:", 
#                    className="plot-header--filtering-element-label"
#                ),
#                dcc.DatePickerRange(
#                    id="date_picker",
#                    display_format="DD.MM.YYYY",
#                    min_date_allowed=start_date,
#                    max_date_allowed=end_date,
#                    initial_visible_month=start_date,
#                    minimum_nights=0,
#                    start_date=start_date,
#                    end_date=end_date,
#                    persistence=True,
#                    persistence_type="memory",
#                    persisted_props=["start_date", "end_date"]
#                )
#            ],
#        )

#def generate_room_filter(unique_rooms, multiple):
    
#    if multiple:
#        default_value = unique_rooms
#    else:        
#        default_value = unique_rooms[0]
#    return  html.Div(
#        className="plot-header--filtering-room",
#        children=[
#            html.Div(
#                "Room:", 
#                className="plot-header--filtering-element-label"
#            ),
#            dcc.Dropdown(
#                options=[{"label": room, "value": room} for room in unique_rooms],
#                value=default_value,
#                multi=multiple,
#                id="room_filter",
#                style={"height": "32px", "line-height": "32px", "min-width": "150px"},
#                persistence=True,
#                persistence_type="local",
#                persisted_props=["value"]
#            )
#        ],
#    )
   
#def generate_weekday_filter(unique_calendar_weeks, multiple):
#    if multiple:
#        default_value = unique_calendar_weeks
#    else:        
#        default_value = unique_calendar_weeks[0]
        
#    return html.Div(
#        className="plot-header--filtering-room",
#        children=[
#            html.Div(
#                "Week:", 
#                className="plot-header--filtering-element-label"
#            ),
#            dcc.Dropdown(
#                options=[{"label": f"CW {cw}", "value": cw} for cw in unique_calendar_weeks],
#                value=default_value,
#                multi=multiple,
#                id="calendar_week_filter",
#                style={"height": "32px", "line-height": "32px", "min-width": "150px"},
#                persistence=True,
#                persistence_type="memory",
#                persisted_props=["value"]
#            )
#        ]
#    )
       
#def generate_start_time_filter(start_time_list):
#    return html.Div(
#        className="plot-header-filtering-starttime",
#        children=[
#            html.Div(
#                "Start Time:",
#                className="plot-header--filtering-element-label"
#            ),
#            dcc.Dropdown(
#                options=[{"label": time.strftime("%H:%M") , "value": time} for time in start_time_list],
#                value=[],
#                multi=True,
#                id="start_time_filter",
#                style={"min-width": "150px", "max-width": "285px"},
#                persistence=True,
#                persistence_type="memory",
#                persisted_props=["value"]
#            )
#        ]
        
#    )

#def generate_number_filter(course_numbers, id_data_list="number_suggestions", course_id_default=""):
#    if course_id_default != "none":
#        default_value = course_id_default
#    else:
#        default_value = ""
    
#    data_list = html.Datalist(
#        id=id_data_list, 
#        children=[html.Option(value=word) for word in course_numbers],
#        hidden=True)
    
#    return html.Div(
#        className="plot-header--filtering-number",
#        children=[
#            html.Div(
#                "ID:",
#                className="plot-header--filtering-element-label"
#            ),
#            dcc.Input(
#                value=default_value,
#                type="text",
#                placeholder="Course Number",
#                id="course_number_filter",
#                list=id_data_list,
#                style={"font-size": "18px"},
#            ),
#            data_list
#        ]
#    )
    
#def generate_name_filter(course_names, id_data_list="name_suggestions"):
    
#    data_list = html.Datalist(
#        id=id_data_list, 
#        children=[html.Option(value=word) for word in course_names],
#        hidden=True)
    
#    return html.Div(
#        className="plot-header--filtering-name",
#        children=[
#            html.Div(
#                "Title:",
#                className="plot-header--filtering-element-label"
#            ),
#            dcc.Input(
#                value="",
#                type="text",
#                placeholder="Course Name",
#                id="course_name_filter",
#                list=id_data_list,
#                style={"font-size": "18px"},
#            ),
#            data_list
#        ]
#    )
     
#def generate_sorting_section():
#    return  html.Div(
#                className="plot-header--sorting",
#                children=[
#                    html.Div(
#                        "Sort By:",
#                        className="plot-header--section-title"
#                    ),
#                    html.Div(
#                        className="plot-header--sorting-elements",
#                        children=[
#                            html.Div(
#                                className="plot-header--sorting-dropdown",
#                                children=dcc.Dropdown(
#                                    options=["course_number", "course_name", "room", "start_time", 
#                                            "type", "ects", "registered_students", "duration"],
#                                    value="course_number",
#                                    id="graph_sort_by",
#                                    persistence=True,
#                                    persistence_type="memory",
#                                    persisted_props=["value"]
#                                )
#                            ),
#                            html.Div(
#                                className="plot-header--sorting-switch",
#                                children=daq.BooleanSwitch(
#                                    id="graph_sort_order",
#                                    on=False,
#                                    persistence=True,
#                                    persistence_type="local")
#                            )
#                        ]
#                    )
#                ]
#            )

#def generate_mode_section(mode_options):
#    if mode_options == None:
#        mode_option_list = ["absolute", "relative_registered", "relative_capacity"]
#    else:
#        mode_option_list = mode_options
        
#    return html.Div(
#                className="plot-header--mode",
#                children=[
#                    html.Div("Frequency Mode:",
#                            className="plot-header--section-title"
#                    ),
#                    html.Div(
#                        className="plot-header--mode-dropdown",
#                        children=dcc.Dropdown(
#                            options=mode_option_list,
#                            value=mode_option_list[0],
#                            id="graph_mode",
#                            persistence=True,
#                            persistence_type="memory",
#                            persisted_props=["value"]
#                        ),
#                    )
#                ]
#            )

#def generate_grouping_section():
#    return html.Div(
#                className="plot-header--grouping",
#                children=[
#                    html.Div("Group By:",
#                            className="plot-header--section-title"
#                    ),
#                    html.Div(
#                        className="plot-header--grouping-dropdown",
#                        children=dcc.Dropdown(
#                            options=["weekday", "calendar_week", "room", "type", "duration", "start_time_string",
#                                     "institute", "level", "curriculum","exam", "test", "tutorium"],
#                            value=["weekday"],
#                            id="graph_group_by",
#                            multi=True,
#                            persistence=True,
#                            persistence_type="memory",
#                            persisted_props=["value"]
#                        )
#                    )
#                ]
#    )






