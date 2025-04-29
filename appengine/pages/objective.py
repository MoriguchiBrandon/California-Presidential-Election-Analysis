# pages/objective.py
import dash
from dash import html

dash.register_page(__name__, path="/objective")

layout = html.Div([
    html.H1("Project Objectives", className="mt-4"),
    html.P("""
        The primary objectives of this project are:
        - Understand key patterns and trends
        - Provide actionable insights
        - Use robust and transparent analytical methods
    """),
    html.H3("Data Sources", className="mt-4"),
    html.Ul([
        html.Li("Source 1: [Dataset Name]"),
        html.Li("Source 2: [Another Dataset]"),
    ]),
])
