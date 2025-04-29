# pages/home.py

import pandas as pd
import json
import requests
import plotly.express as px
from dash import html, dcc, register_page

# Required for Dash pages system
register_page(__name__, path="/", name="Home")

# Load your election data
pres_election_2024 = pd.read_csv('https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/pres_election_2024.csv')

# Load the GeoJSON for California counties
url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/california-counties.geojson"
response = requests.get(url)
counties_geojson = response.json()

 

fig = px.choropleth_mapbox(
    pres_election_2024,
    geojson=counties_geojson,  # your loaded geojson file
    locations='Name',            # your county names
    featureidkey='properties.name',  # MATCHING property inside geojson
    color='Ratio',               # column with democrat/republican ratio
    color_continuous_scale="RdBu",  
    range_color=[0, 2],  # Set the range for the color scale explicitly
    mapbox_style="carto-positron",
    zoom=5.2,
    center={"lat": 37.5, "lon": -119.5},
    opacity=0.6,
)

# Adjust layout for better display
fig.update_layout(
    title="California 2024 Presidential Election Results by County",
    geo=dict(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="white",
        showlakes=True,
        lakecolor="lightblue"
    ),
    height=800
)



# Create the layout for the home page
layout = html.Div([
    html.H1("California 2024 Presidential Election Analysis", style={"textAlign": "center"}),
    html.P("Welcome! This project visualizes and analyzes how California counties voted in the 2024 Presidential election.", style={"textAlign": "center", "fontSize": "18px"}),
    dcc.Graph(figure=fig)
])
