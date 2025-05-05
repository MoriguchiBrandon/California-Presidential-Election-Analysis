import dash
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Main layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(
                src="/assets/Navigation.jpg",  
                style={"width": "100%", "margin-bottom": "1rem"}
            ),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Project Objective", href="/objective", active="exact"),
                    dbc.NavLink("Analytical Methods", href="/methods", active="exact"),
                    dbc.NavLink("Major Findings", href="/findings", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ], width=2, style={"background-color": "#f8f9fa", "padding": "20px", "height": "100vh"}),

        # Main content area
        dbc.Col([
            page_container
        ], width=10, style={"padding": "20px"})
    ])
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)

