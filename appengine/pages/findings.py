# pages/findings.py

import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
from google.cloud import storage
import pandas as pd
from io import StringIO

# Set up GCS client
client = storage.Client()

# Bucket and blob names
bucket_name = 'cleaned_dfs_census_data'
file_names = ['df_2016.csv', 'df_2020.csv', 'df_2024.csv']

# Function to read CSV from GCS
def read_gcs_csv(bucket_name, file_name):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_text()  # download as text
    return pd.read_csv(StringIO(data))  # load CSV from the string

# Load datasets from GCS
df_2016 = read_gcs_csv(bucket_name, 'df_2016.csv')
df_2020 = read_gcs_csv(bucket_name, 'df_2020.csv')
df_2024 = read_gcs_csv(bucket_name, 'df_2024.csv')


# Load pres_election data from GitHub
url_2016 = 'https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/pres_election_2016.csv'
url_2020 = 'https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/pres_election_2020.csv'
url_2024 = 'https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/pres_election_2024.csv'

pres_election_2016 = pd.read_csv(url_2016)
pres_election_2020 = pd.read_csv(url_2020)
pres_election_2024 = pd.read_csv(url_2024)


merged_2016 = df_2016.merge(pres_election_2016[['Name', 'Ratio']], on='Name')
merged_2020 = df_2020.merge(pres_election_2020[['Name', 'Ratio']], on='Name')
merged_2024 = df_2024.merge(pres_election_2024[['Name', 'Ratio']], on='Name')

# Create the figure (same as your code)
fig = go.Figure()

# 2024 data
fig_2024 = px.scatter(merged_2024, 
                      x="Estimate!!Total!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree", 
                      y="Ratio", 
                      labels={...},
                      trendline="ols",
                      title="Bachelor's Degree % vs. Democratic/Republican Vote Ratio (2012, 2016, 2020, 2024)")

for trace in fig_2024.data:
    if trace.mode == 'markers':
        fig.add_trace(go.Scatter(x=trace.x, y=trace.y, mode='markers', name='2024', marker=dict(color='blue')))
    elif trace.mode == 'lines':
        fig.add_trace(go.Scatter(x=trace.x, y=trace.y, mode='lines', name='2024 Regression', line=dict(color='blue', dash='dash')))

# 2020 (Plotly Express with regression line)
fig_2020 = px.scatter(merged_2020, 
                      x="Estimate!!Total!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree", 
                      y="Ratio", 
                      labels={
                          "Estimate!!Total!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree": "Bachelor's Degree or Higher (%)",
                          "Ratio": "Vote Ratio (Dem / Rep)"
                      },
                      trendline="ols")

# Add 2020 data and regression line to the main figure with a specific color
for trace in fig_2020.data:
    if trace.mode == 'markers':
        fig.add_trace(go.Scatter(
            x=trace.x, y=trace.y, mode='markers', name='2020', marker=dict(color='red')
        ))
    elif trace.mode == 'lines':
        fig.add_trace(go.Scatter(
            x=trace.x, y=trace.y, mode='lines', name='2020 Regression', line=dict(color='red', dash='dash')
        ))

# 2016 (Plotly Express with regression line)
fig_2016 = px.scatter(merged_2016, 
                      x="Estimate!!Total!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree", 
                      y="Ratio", 
                      labels={
                          "Estimate!!Total!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree": "Bachelor's Degree or Higher (%)",
                          "Ratio": "Vote Ratio (Dem / Rep)"
                      },
                      trendline="ols")

# Add 2016 data and regression line to the main figure with a specific color
for trace in fig_2016.data:
    if trace.mode == 'markers':
        fig.add_trace(go.Scatter(
            x=trace.x, y=trace.y, mode='markers', name='2016', marker=dict(color='green')
        ))
    elif trace.mode == 'lines':
        fig.add_trace(go.Scatter(
            x=trace.x, y=trace.y, mode='lines', name='2016 Regression', line=dict(color='green', dash='dash')
        ))

# Update layout with title, axis labels, and grid lines
fig.update_layout(
    title="Graduate's Degree % vs. Democratic/Republican Vote Ratio (2016, 2020, 2024)",
    xaxis_title="Graduate's Degree or Higher (%)",
    yaxis_title="Vote Ratio (Dem / Rep)",
    showlegend=True,
    xaxis=dict(
        showgrid=True,  # Show grid lines
        gridcolor='rgba(0, 0, 0, 0.1)',  # Grid color
        zeroline=False  # Remove the line at zero
    ),
    yaxis=dict(
        showgrid=True,  # Show grid lines
        gridcolor='rgba(0, 0, 0, 0.1)',  # Grid color
        dtick=1,  # Set the tick interval for y-axis at every integer
        zeroline=False  # Remove the line at zero
    )
)

# Layout for the findings page
layout = html.Div([
    html.H1("Findings: Voter Trends Analysis", style={"textAlign": "center"}),
    dcc.Graph(figure=fig),  # Here, you add the figure to the layout
])

# Don't forget to register your page
from dash import register_page
register_page(__name__, path="/findings")
