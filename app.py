import dash
from dash import Dash, html, dcc
from assets import page_header

app = Dash(__name__, title="Visard", use_pages=True)

#page_header.layout(current_page="Onsite Participants"),
app.layout = html.Div([
    page_header.layout(),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)