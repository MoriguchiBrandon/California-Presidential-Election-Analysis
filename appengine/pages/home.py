# pages/home.py

import pandas as pd
import json
import requests
import plotly.express as px
from dash import html, dcc, register_page, callback, Output, Input

# Required for Dash pages system
register_page(__name__, path="/", name="Home")

# --- Load your election data (GLOBAL) ---
pres_election_2024 = pd.read_csv('https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/pres_election_2024.csv')

# Load GeoJSON
url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/california-counties.geojson"
response = requests.get(url)
counties_geojson = response.json()

# Load model predictions
model_predictions = {
    "NN": pd.read_csv('https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/2024_prediction_NN.csv'),
    "RF": pd.read_csv('https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/2024_prediction_RandomForest.csv'),
    "GB": pd.read_csv('https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/2024_prediction_GradientBoost.csv')
}

# --- Main Election Figure ---
fig_main = px.choropleth_mapbox(
    pres_election_2024,
    geojson=counties_geojson,
    locations='Name',
    featureidkey='properties.name',
    color='Ratio',
    color_continuous_scale="RdBu",
    range_color=[0, 2],
    mapbox_style="carto-positron",
    zoom=5,
    center={"lat": 37.5, "lon": -119.5},
    opacity=0.6,
)
fig_main.update_layout(
    title="California 2024 Presidential Election Results by County",
    height=800,
)

# --- Layout ---
def layout():
    return html.Div([
        html.H1("California 2024 Presidential Election Analysis", style={"textAlign": "center"}),
        html.P(
            "Welcome! This project visualizes and analyzes how California counties voted in the 2024 Presidential election.",
            style={"textAlign": "center", "fontSize": "18px"}
        ),
        dcc.Graph(figure=fig_main),

        html.Hr(),

        html.H2("Model Predictions", style={"textAlign": "center"}),

        dcc.RadioItems(
            id='model-toggle',
            options=[
                {'label': 'Neural Network', 'value': 'NN'},
                {'label': 'Random Forest', 'value': 'RF'},
                {'label': 'Gradient Boosting', 'value': 'GB'},
            ],
            value='GB',  # default = Gradient Boost
            labelStyle={'display': 'inline-block', 'margin': '10px'},
            style={'textAlign': 'center'}
        ),

        dcc.Graph(id='prediction-graph')
    ])

# --- Callback for updating prediction graph ---
@callback(
    Output('prediction-graph', 'figure'),
    Input('model-toggle', 'value')
)
def update_prediction(selected_model):
    pred_df = model_predictions[selected_model]
    fig = px.choropleth_mapbox(
        pred_df,
        geojson=counties_geojson,
        locations='Name',
        featureidkey='properties.name',
        color='Predicted_Ratio',
        color_continuous_scale="RdBu",
        range_color=[0, 2],
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 37.5, "lon": -119.5},
        opacity=0.6,
    )
    fig.update_layout(
        title=f"Predicted 2024 Ratios ({selected_model})",
        height=800,
    )
    return fig
