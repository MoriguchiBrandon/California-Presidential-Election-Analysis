# pages/home.py

import pandas as pd
import json
import requests
import plotly.express as px
from dash import html, dcc, register_page, callback, Output, Input
from google.cloud import storage
from io import StringIO

# Set up GCS client
client = storage.Client()

# Bucket and blob names
bucket_name = 'cleaned_dfs_census_data'

# Function to read CSV from GCS
def read_gcs_csv(bucket_name, file_name):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_text()
    return pd.read_csv(StringIO(data))

# Required for Dash pages system
register_page(__name__, path="/", name="Home")

# --- Load election data (GLOBAL) ---
pres_election_2024 = read_gcs_csv(bucket_name, 'pres_election_2024.csv')

# Adding a row for which way the county voted
pres_election_2024['Party'] = pres_election_2024['Ratio'].apply(lambda x: 'dem' if x >= 1 else 'rep')
color_discrete_map = {
    'dem': 'blue',
    'rep': 'red'
}

# Load GeoJSON
url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/california-counties.geojson"
response = requests.get(url)
counties_geojson = response.json()

# Load model predictions
model_predictions = {
    "MLP": pd.read_csv('https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/2024_prediction_NN.csv'),
    "RF": pd.read_csv('https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/2024_prediction_RandomForest.csv'),
    "GB": pd.read_csv('https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/2024_prediction_GradientBoost.csv')
}

# Add 'Party' column to each model prediction DataFrame
for model_name, df in model_predictions.items():
    df['Party'] = df['Predicted_Ratio'].apply(lambda x: 'dem' if x >= 1 else 'rep')

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

# --- red or blue Election Figure ---
fig_discrete = px.choropleth_mapbox(
    pres_election_2024,
    geojson=counties_geojson,
    locations='Name',
    featureidkey='properties.name',
    color='Party',
    color_discrete_map=color_discrete_map,
    mapbox_style="carto-positron",
    zoom=5,
    center={"lat": 37.5, "lon": -119.5},
    opacity=0.6,
)
fig_discrete.update_layout(
    title="California 2024 Presidential Election Results by County (Red/Blue)",
    height=800,
)

# --- Layout ---
def layout():
    return html.Div([
        html.H1("California 2024 Presidential Election Analysis", style={"textAlign": "center"}),
        html.P(
            "Welcome! This project visualizes and analyzes how California counties voted in the 2024 Presidential election.",
            style={"textAlign": "center", "fontSize": "18px"}),
        
        dcc.Graph(figure=fig_main),
        html.P(
        """
        This is a map of California with each county within the state colored by a gradient of the ratio of democrat votes 
        divided by Republican votes within the county.
        """,
        style={"padding": "20px", "fontSize": "16px", "textAlign": "center"}),

        html.Hr(),

        html.H2("Model Predictions", style={"textAlign": "center"}),

        dcc.RadioItems(
            id='model-toggle',
            options=[
                {'label': 'Multi-Layer Perceptron', 'value': 'MLP'},
                {'label': 'Random Forest', 'value': 'RF'},
                {'label': 'Gradient Boosting', 'value': 'GB'},
            ],
            value='GB',  # default = Gradient Boost
            labelStyle={'display': 'inline-block', 'margin': '10px'},
            style={'textAlign': 'center'}
        ),

        dcc.Graph(id='prediction-graph'),

        html.P(
        """
        This is a map of California with each county within the state colored by a gradient of the Predicted ratio of democrat votes 
        divided by Republican votes. We trained and tested 3 models to predict county ratio, and the results can be viewed by selecting 
        which model to view in the buttons above.
        """,
        style={"padding": "20px", "fontSize": "16px", "textAlign": "center"}),

        html.Hr(),

        html.H2("Comparison: Actual vs. Model Color Mapping", style={"textAlign": "center"}),

        html.Div([
            dcc.Graph(id='left-choropleth', figure=fig_discrete, style={'flex': 1}),
            dcc.Graph(id='right-choropleth', style={'flex': 1}),
        ], style={'display': 'flex', 'flexDirection': 'row'}),

        html.P(
        """
        These two maps compare the actual 2024 election results by county (left) with the predicted party outcome 
        based on the selected machine learning model (right). Counties shaded in blue were won or predicted to be won 
        by the Democratic candidate, while red counties indicate a Republican win or prediction. 
        This comparison helps visualize where the model's predictions align with or diverge from the real outcomes.
        """,
        style={"padding": "20px", "fontSize": "16px", "textAlign": "center"})
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

@callback(
Output('right-choropleth', 'figure'),
Input('model-toggle', 'value')
)
def update_color_map(selected_model):
    pred_df = model_predictions[selected_model]
    fig = px.choropleth_mapbox(
        pred_df,
        geojson=counties_geojson,
        locations='Name',
        featureidkey='properties.name',
        color='Party',  
        color_discrete_map=color_discrete_map,
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 37.5, "lon": -119.5},
        opacity=0.6,)
    fig.update_layout(
        title=f"Model ({selected_model}) – Predicted Election Results by County (Red/Blue)",
        height=800,
        margin={"r":0, "t":50, "l":0, "b":0}
    )
    return fig
   