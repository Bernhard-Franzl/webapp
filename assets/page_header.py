
import dash
from dash import html, dcc

def layout(**kwargs):
    layout = html.Div(
        className="page-header",
        children=[
            html.Div(
                dcc.Link(
                    f"{page['title']}", 
                    href=page["relative_path"], 
                    className="page-header--link"
                ),
                style={},
                className="page-header--element"
            ) for page in dash.page_registry.values()
        ]
    )
    layout.children[-1].style["border-right"] = "2px solid black"
    return layout