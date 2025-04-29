# pages/methods.py
import dash
from dash import html

dash.register_page(__name__, path="/methods")

layout = html.Div([
    html.H1("Analytical Methods", className="mt-4"),
    html.P("""
        In this project, we used a combination of the following techniques:
    """),
    html.Ul([
        html.Li("Exploratory Data Analysis (EDA)"),
        html.Li("Regression Modeling"),
        html.Li("Clustering Algorithms"),
        html.Li("Machine Learning Predictions"),
    ]),
    html.H3("Further Reading"),
    html.P("See documentation for [Method A], [Method B], and [Method C] for deeper understanding."),
])
