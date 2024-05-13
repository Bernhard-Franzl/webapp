from dash import html, dcc
import dash_daq as daq


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
                    end_date=end_date
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
                style={"height": "40px", "line-height": "40px", "min-width": "175px"}
            )
        ],
    )
    
def generate_start_time_filter(start_time_list):
    return html.Div(
        className="plot-header-filtering-starttime",
        children=[
            html.Div(
                "Time:",
                className="plot-header--filtering-element-label"
            ),
            dcc.Dropdown(
                options=[{"label": time.strftime("%H:%M") , "value": time} for time in start_time_list],
                value=start_time_list,
                multi=True,
                id="start_time_filter",
                style={"min-width": "175px", "max-width": "285px"}
            )
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
                                    id="participants_graph_sort_by",
                                )
                            ),
                            html.Div(
                                className="plot-header--sorting-switch",
                                children=daq.BooleanSwitch(
                                    id="participants_graph_sort_order",
                                    on=False)
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
                            id="participants_graph_mode",
                        ),
                    )
                ]
            )
    
def layout(title, 
           description=None, 
           filtering=[], 
           sorting=True, mode=True, **kwargs):
    
    horizontal_line = html.Hr(
        style={
            "border": "0",
            "height": "1px",
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
            
        else:
            plot_header.append(sorting_mode_section)
            plot_header.append(horizontal_line)
               
    else:
        if mode:
            mode_section = generate_mode_section()
            sorting_mode_section.children.children.append(mode_section)
            
            plot_header.append(sorting_mode_section)
            plot_header.append(horizontal_line)

        else:
            pass    

    del sorting_mode_section    
    
    return layout






############ Header in plain HTML ################
#html.Div(
#    className="plot-header",
#    children=[
#        html.Div(
#            className="plot-header--section",
#            children=[
#                html.Div(
#                    "Course Participants Overview",
#                    className="plot-header--title"  
#                ),
#                html.Div(
#                    "This plot provides an overview of the onsite participants of all the courses.",
#                    className="plot-header--description"
#                ),
#            ],
#        ),
#        html.Div(
#            className="plot-header--section",
#            children=[
#                    html.Div("Filter By:",
#                            className="plot-header--section-title"
#                    ),
#                    html.Div(
#                        className="plot-header--section-elements",
#                        children=[
#                            html.Div(
#                                className="plot-header--filtering-date",
#                                children=[
#                                    html.Div(
#                                        "Date:", 
#                                        className="plot-header--filtering-element-label"),
#                                    dcc.DatePickerRange(
#                                        id="date_picker",
#                                        display_format="DD.MM.YYYY",
#                                        min_date_allowed=start_date,
#                                        max_date_allowed=end_date,
#                                        initial_visible_month=start_date,
#                                        minimum_nights=0,
#                                     #html.Div(
#    className="plot-header",
#    children=[
#        html.Div(
#            className="plot-header--section",
#            children=[
#                html.Div(
#                    "Course Participants Overview",
#                    className="plot-header--title"  
#                ),
#                html.Div(
#                    "This plot provides an overview of the onsite participants of all the courses.",
#                    className="plot-header--description"
#                ),
#            ],
#        ),
#        html.Div(
#            className="plot-header--section",
#            children=[
#                    html.Div("Filter By:",
#                            className="plot-header--section-title"
#                    ),
#                    html.Div(
#                        className="plot-header--section-elements",
#                        children=[
#                            html.Div(
#                                className="plot-header--filtering-date",
#                                children=[
#                                    html.Div(
#                                        "Date:", 
#                                  )
#                                ],
#                            ),
#                            html.Div(
#                                className="plot-header--filtering-room",
#                                children=[
#                                    html.Div(
#                                        "Room:", 
#                                        className="plot-header--filtering-element-label"),
#                                    dcc.Dropdown(
#                                        options=[{"label": room, "value": room} for room in df_participants["room"].unique().tolist()],
#                                        value=df_participants["room"].unique().tolist(),
#                                        multi=True,
#                                        id="room_filter",
#                                        style={"height": "40px", "line-height": "40px", "min-width": "175px"}
#                                    )
#                                ],
#                            ),
#                            html.Div(
#                                className="plot-header-filtering-starttime",
#                                children=[
#                                    html.Div(
#                                        "Time:",
#                                        className="plot-header--filtering-element-label"
#                                    ),
#                                    dcc.Dropdown(
#                                        options=[{"label": time.strftime("%H:%M") , "value": time} for time in sorted(df_participants["start_time"].dt.time.unique())],
#                                        value=sorted(df_participants["start_time"].dt.time.unique()),
#                                        multi=True,
#                                        id="start_time_filter",
#                                        style={"min-width": "175px", "max-width": "285px"}
#                                    )
#                                ]
                                
#                            )
#                        ]
#                    ),
#            ],
#        ),
#        html.Div(
#            className="plot-header--section",
#            children=html.Div(
#                className="plot-header--section-elements",
#                children=[
#                    html.Div(
#                        className="plot-header--sorting",
#                        children=[
#                            html.Div("Sort By:",
#                                    className="plot-header--section-title"
#                            ),
#                            html.Div(
#                                className="plot-header--sorting-elements",
#                                children=[
#                                    html.Div(
#                                        className="plot-header--sorting-dropdown",
#                                        children=dcc.Dropdown(
#                                            options=["course_number", "course_name", "room", "start_time", 
#                                                    "type", "ects", "registered_students", "duration"],
#                                            value="course_number",
#                                            id="participants_graph_sort_by",
#                                        )
#                                    ),
#                                    html.Div(
#                                        className="plot-header--sorting-switch",
#                                        children=daq.BooleanSwitch(
#                                            id="participants_graph_sort_order",
#                                            on=False)
#                                    )
#                                ]
#                            )
#                        ]
#                    ),
#                    html.Div(
#                        className="plot-header--mode",
#                        children=[
#                            html.Div("Frequency Mode:",
#                                    className="plot-header--section-title"
#                            ),
#                            html.Div(
#                                className="plot-header--mode-dropdown",
#                                children=dcc.Dropdown(
#                                    options=["absolute", "relative_registered", "relative_capacity"],
#                                    value="absolute",
#                                    id="participants_graph_mode",
#                                ),
#                            )
#                        ]
#                    ),  
#                ],
#            )
#        )    
#    ],
#),