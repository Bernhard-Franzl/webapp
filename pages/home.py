from dash import html, register_page

register_page(__name__, path="/", order=0)

horizontal_line = html.Hr(
    style={
        "border": "0",
        "height": "2px",
        "color": "lightgrey",
        "backgroundColor": "lightgrey",
        }
    )

layout = html.Div(
    className="page",
    children = html.Div(
        className="home-page",
        children=[
            # Title
            html.Div(
                className="home-page--section",
                children=[
                    html.Div(
                        "Home",
                        className="home-page--title" 
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                "Welcome to the dashboard! This tool is designed to help you manage and analyze course schedules, participants, and room allocations effectively. Below is an overview of the available features and sections.",
                            )
                        ],
                        className="home-page--description"
                    )
                ]
            ),
            horizontal_line,
            # Data explanation
            html.Div(
                className="home-page--section",
                children=[
                    html.Div(
                        "Data",
                        className="home-page--section-title"
                    ),
                    html.Div(
                        className="home-page--description",
                        children=[
                            html.P(
                                "The dataset includes information about all the courses and their respective dates held in HS18 and HS19, from April 8, 2024, to June 28, 2024. It comprises 386 samples and 45 features, with each sample representing a specific course date."
                            )]
                    )
                ]
            ),   
            horizontal_line,
            # Pages explanation
            html.Div(
                className="home-page--section",
                children=[
                    html.Div(
                        "Pages",
                        className="home-page--section-title"
                    ),
                    html.Div(
                        className="home-page--description",
                        children=[
                            html.P(
                                "The dashboard contains the following pages:"
                            ),
                            html.Table(
                                className="home-page--table",
                                children = [
                                    html.Tr(
                                        className="home-page--table-row",
                                        children=[
                                            html.Td("Course Overview:",
                                                    className="home-page--list-item-label-pages"), 
                                            html.Td("Provides an overview of the onsite participants of all the course in the selected data.",
                                                    className="home-page--list-item-description")]
                                        ),
                                    html.Tr(
                                        className="home-page--table-row",
                                        children=[
                                            html.Td("Calendar View:",
                                                    className="home-page--list-item-label-pages"), 
                                            html.Td("Shows the distribution of the courses over a chosen calendar week and a chosen room.",
                                                    className="home-page--list-item-description")]
                                        ),
                                    #html.Tr(
                                    #    className="home-page--table-row",
                                    #    children=[
                                    #        html.Td("Course Details:",
                                    #                className="home-page--list-item-label-pages"), 
                                    #        html.Td("Provides a detailed view of the course information and the participants of a single course.",
                                    #                className="home-page--list-item-description")
                                    #        ]
                                    #    ),
                                    html.Tr(
                                        className="home-page--table-row",
                                        children=[
                                            html.Td("Grouped Data:",
                                                    className="home-page--list-item-label-pages"), 
                                            html.Td("Illustrates the effect of grouping the data by different features.",
                                                    className="home-page--list-item-description")
                                            ]
                                        )
                                    ],
                                ),
                        ]
                    )
                ]
            ),
            horizontal_line,
            # Plot header explanation
            html.Div(
                className="home-page--section",
                children=[
                    html.Div(
                        "Plot Header",
                        className="home-page--section-title"
                    ),
                    html.Div(
                        className="home-page--description",
                        children=[
                            html.Div(
                                "The plot header is the top part of every page." + 
                                "It contains the title, description and data manipulation options."
                            ),
                            html.P(
                                "The data manipulation options are:"
                            ),
                            html.Table(
                                className="home-page--table",
                                children = [
                                    html.Tr(
                                        className="home-page--table-row",
                                        children=[
                                            html.Td("Filter By:",
                                                    className="home-page--list-item-label-header"), 
                                            html.Td("Allows you to filter the data by date, room, start time and course title/number.",
                                                    className="home-page--list-item-description")]
                                        ),
                                    html.Tr(
                                        className="home-page--table-row",
                                        children=[
                                            html.Td("Group By:",
                                                    className="home-page--list-item-label-header"), 
                                            html.Td("Allows you to group the data by a specific feature.",
                                                    className="home-page--list-item-description")]
                                        ),
                                    html.Tr(
                                        className="home-page--table-row",
                                        children=[
                                            html.Td("Sort By:",
                                                    className="home-page--list-item-label-header"), 
                                            html.Td("Allows you to sort the data by a specific feature.",
                                                    className="home-page--list-item-description")
                                            ]
                                        ),
                                    html.Tr(
                                        className="home-page--table-row",
                                        children=[
                                            html.Td("Frequency Mode:",
                                                    className="home-page--list-item-label-header"), 
                                            html.Td("Lets you switch between absolute and relative frequencies. For the relative frequencies, the data is either normalized by the number of registered students or the room capacity.",
                                                    className="home-page--list-item-description")
                                            ]
                                        )
                                    ],
                                ),
                        ]
                    )    
                ]
            ),
            horizontal_line,
        ]
    )
)


                            # html.P(
                            #     style={"display":"flex", "flexDirection":"column"},
                            #     children=[
                            #         html.Div(
                            #             className="home-page--list-item",
                            #             children=[
                            #                 html.Div("Filter By:", 
                            #                         className="home-page--list-item-label"),
                            #                 html.Div("Allows you to filter the data by date, room, start time and course title/number.",
                            #                         className="home-page--list-item-description")
                            #             ]
                            #         ),
                            #         html.Div(
                            #             className="home-page--list-item",
                            #             children=[
                            #                 html.Div("Group By:", 
                            #                         className="home-page--list-item-label"),
                            #                 html.Div("Allows you to group the data by a specific feature.",
                            #                         className="home-page--list-item-description")
                            #             ]
                            #         ),
                            #         html.Div(
                            #             className="home-page--list-item",
                            #             children=[
                            #                 html.Div("Sort By:", 
                            #                         className="home-page--list-item-label"),
                            #                 html.Div("Allows you to sort the data by a specific feature.",
                            #                         className="home-page--list-item-description")
                            #             ]
                            #         ),
                            #         html.Div(
                            #             className="home-page--list-item",
                            #             children=[
                            #                 html.Div("Mode:", 
                            #                         className="home-page--list-item-label"),
                            #                 html.Div("Allows you to switch between absolute and relative frequencies. " +
                            #                          "For the relative frequencies, the data is either normalized by the number of registered students or the room capacity.",
                            #                         className="home-page--list-item-description")
                            #             ]
                            #         )
                            #     ]
                            # ),
                            
                #    html.P(
                #                 style={"display":"flex", "flexDirection":"column"},
                #                 children=[
                #                     html.Div(
                #                         className="home-page--list-item",
                #                         children=[
                #                             html.Div("Course Overview:",
                #                                     className="home-page--list-item-label"),
                #                             html.Div("Provides an overview of the onsite participants of all the course in the selected data.",
                #                                     className="home-page--list-item-description")
                #                         ]
                #                     ),
                #                     html.Div(
                #                         className="home-page--list-item",
                #                         children=[
                #                             html.Div("Calendar View:",
                #                                      className="home-page--list-item-label"),
                #                             html.Div("Illustrates the distribution of the courses over a chosen calendar week and a chosen room.",)
                #                                   ]
                                        
                #                     ),
                #                     html.Div(
                #                         className="home-page--list-item",
                #                         children=[
                #                             html.Div("Course Details:",
                #                                     className="home-page--list-item-label"),
                #                             html.Div("Provides a detailed view of the course information and the participants of a single course.",	
                #                                     className="home-page--list-item-description")
                #                         ]
                #                     ),
                #                     html.Div(
                #                         className="home-page--list-item",
                #                         children=[
                #                             html.Div("Grouped Data:",
                #                                     className="home-page--list-item-label"),
                #                             html.Div("Illustrates the effect of grouping the data by different features.",
                #                                     className="home-page--list-item-description")
                #                         ]
                #                     )
                #                 ]
                #             )