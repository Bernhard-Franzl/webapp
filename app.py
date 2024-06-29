import dash
from dash import Dash, html
from components import page_header

app = Dash(__name__,
           use_pages=True,
           suppress_callback_exceptions=True)

app.layout = html.Div([
    page_header.layout(),
    dash.page_container
    ],
    style={"margin":"0px",
           "padding":"0px"}
)

if __name__ == '__main__':
    app.run(debug=True)