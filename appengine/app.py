import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Main layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Navigation", className="display-6"),
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
        
        dbc.Col(dash.page_container, width=10),
    ])
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)

