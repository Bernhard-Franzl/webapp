from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from datetime import datetime, date, time
from components import plot_header

from visualization.visualization import Visualizer

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
                        "Welcome to the dashboard! This pages explains the available pages and features.",
                        className="home-page--description"
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
                           html.P(
                                style={"display":"flex", "flexDirection":"column"},
                                children=[
                                    html.Div(
                                        className="home-page--list-item",
                                        children=[
                                            html.Div("Course Overview:",
                                                    className="home-page--list-item-label"),
                                            html.Div("Provides an overview of the onsite participants of all the course in the selected data.",
                                                    className="home-page--list-item-description")
                                        ]
                                    ),
                                    html.Div(
                                        className="home-page--list-item",
                                        children=[
                                            html.Div("Course Details:",
                                                    className="home-page--list-item-label"),
                                            html.Div("Provides a detailed view of the course information and the participants of a single course.",	
                                                    className="home-page--list-item-description")
                                        ]
                                    ),
                                    html.Div(
                                        className="home-page--list-item",
                                        children=[
                                            html.Div("Grouped Data:",
                                                    className="home-page--list-item-label"),
                                            html.Div("Illustrates the effect of grouping the data by different features.",
                                                    className="home-page--list-item-description")
                                        ]
                                    )
                                ]
                            )
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
                        className="plot-header--description",
                        children=[
                            html.P(
                                "The plot header is the top part of every page." + 
                                "It contains the title, description and data manipulation options."
                            ),
                            html.P(
                                "The data manipulation options are:"
                            ),
                            html.P(
                                style={"display":"flex", "flexDirection":"column"},
                                children=[
                                    html.Div(
                                        className="home-page--list-item",
                                        children=[
                                            html.Div("Filter By:", 
                                                    className="home-page--list-item-label"),
                                            html.Div("Allows you to filter the data by date, room, start time and course title/number.",
                                                    className="home-page--list-item-description")
                                        ]
                                    ),
                                    html.Div(
                                        className="home-page--list-item",
                                        children=[
                                            html.Div("Group By:", 
                                                    className="home-page--list-item-label"),
                                            html.Div("Allows you to group the data by a specific feature.",
                                                    className="home-page--list-item-description")
                                        ]
                                    ),
                                    html.Div(
                                        className="home-page--list-item",
                                        children=[
                                            html.Div("Sort By:", 
                                                    className="home-page--list-item-label"),
                                            html.Div("Allows you to sort the data by a specific feature.",
                                                    className="home-page--list-item-description")
                                        ]
                                    ),
                                    html.Div(
                                        className="home-page--list-item",
                                        children=[
                                            html.Div("Mode:", 
                                                    className="home-page--list-item-label"),
                                            html.Div("Allows you to switch between absolute and relative frequencies. " +
                                                     "For the relative frequencies, the data is either normalized by the number of registered students or the room capacity.",
                                                    className="home-page--list-item-description")
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )    
                ]
            ),
            horizontal_line,
        ]
    )
)