import dash
from dash import Dash, html, dcc
from assets import page_header

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    page_header.layout(),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)