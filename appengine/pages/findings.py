# pages/findings.py
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/findings")

# Example chart
df_findings = pd.DataFrame({
    "Metric": ["Accuracy", "Precision", "Recall"],
    "Score": [0.91, 0.88, 0.89]
})
fig_findings = px.bar(df_findings, x="Metric", y="Score", title="Model Performance Metrics")

layout = html.Div([
    html.H1("Major Findings", className="mt-4"),
    html.P("Key results from our data analysis and modeling efforts are summarized below."),
    dcc.Graph(figure=fig_findings),
])
