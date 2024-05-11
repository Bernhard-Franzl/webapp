
from dash import html

def layout(current_page, **kwargs):
    
    layout = html.Div(
        className="page-header",
        children=[
            html.Div(
                "Onsite Participants",
                className="page-header--title"
            ),
        ]
    )
    
    return layout