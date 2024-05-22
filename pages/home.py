from dash import Dash, html, dcc, Input, Output, callback, register_page
import json
import pandas as pd
from datetime import datetime, date, time
from components import plot_header

from visualization.visualization import Visualizer

register_page(__name__, path="/", order=0)

layout = html.Div(children=[
    # plot
    html.Div(
        className="plot",
        children=[
            "Hello World"
        ]
    )
])