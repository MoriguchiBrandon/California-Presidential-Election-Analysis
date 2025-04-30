import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc, callback, Input, Output
from google.cloud import storage
import pandas as pd
from io import StringIO

# Set up GCS client
client = storage.Client()

# Load datasets from GCS
def read_gcs_csv(bucket_name, file_name):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_text()
    return pd.read_csv(StringIO(data))

bucket_name = 'cleaned_dfs_census_data'
df_2016 = read_gcs_csv(bucket_name, 'df_2016.csv')
df_2020 = read_gcs_csv(bucket_name, 'df_2020.csv')
df_2024 = read_gcs_csv(bucket_name, 'df_2024.csv')
pres_election_2016 = read_gcs_csv(bucket_name, 'pres_election_2016.csv')
pres_election_2020 = read_gcs_csv(bucket_name, 'pres_election_2020.csv')
pres_election_2024 = read_gcs_csv(bucket_name, 'pres_election_2024.csv')

merged_2016 = df_2016.merge(pres_election_2016[['Name', 'Ratio']], on='Name')
merged_2020 = df_2020.merge(pres_election_2020[['Name', 'Ratio']], on='Name')
merged_2024 = df_2024.merge(pres_election_2024[['Name', 'Ratio']], on='Name')

# Column Mappings
column_mapping_positive = {
    'graduate': {
        'col': 'Estimate!!Native!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree',
        'label': "Graduate Degree (%)"
    },
    'industry': {
        'col': 'Estimate!!Native!!Civilian employed population 16 years and over!!INDUSTRY!!Professional, scientific, and management, and administrative and waste management services',
        'label': "Professional/Scientific Employment (%)"
    },
    'high_income': {
        'col': 'Estimate!!Native!!EARNINGS IN THE PAST 12 MONTHS (IN 2023 INFLATION-ADJUSTED DOLLARS) FOR FULL-TIME, YEAR-ROUND WORKERS!!Population 16 years and over with earnings!!$75,000 or more',
        'label': "High Income ($75k+) (%)"
    },
    'foreign_rooms': {
        'col': 'Estimate!!Foreign-born!!Occupied housing units!!ROOMS!!2 or 3 rooms',
        'label': "Foreign-born Households (2–3 Rooms) (%)"
    },
    'total_rooms': {
        'col': 'Estimate!!Total!!Occupied housing units!!ROOMS!!2 or 3 rooms',
        'label': "All Households (2–3 Rooms) (%)"
    }
}
column_mapping_negative = {
    'some_college': {
        'col': "Estimate!!Native!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Some college or associate's degree",
        'label': "Some College or Associate's Degree (%)"
    },
    'low_income': {
        'col': 'Estimate!!Native!!EARNINGS IN THE PAST 12 MONTHS (IN 2023 INFLATION-ADJUSTED DOLLARS) FOR FULL-TIME, YEAR-ROUND WORKERS!!Population 16 years and over with earnings!!$35,000 to $49,999',
        'label': "Low Income ($35k–$50k) (%)"
    },
    'retail_trade': {
        'col': 'Estimate!!Native!!Civilian employed population 16 years and over!!INDUSTRY!!Retail trade',
        'label': "Retail Trade Employment (%)"
    },
    'married_poverty': {
        'col': 'Estimate!!Native!!POVERTY STATUS IN THE PAST 12 MONTHS!!POVERTY RATES FOR FAMILIES FOR WHOM POVERTY STATUS IS DETERMINED!!Married-couple family',
        'label': "Married Couples in Poverty (%)"
    },
    'six_seven_rooms': {
        'col': 'Estimate!!Total!!Occupied housing units!!ROOMS!!6 or 7 rooms',
        'label': "Households with 6–7 Rooms (%)"
    }
}

# Page layout
layout = html.Div([
    html.H1("Findings: Voter Trends Analysis", style={"textAlign": "center"}),

    # First Text Group: Introduction to Positive Correlation
    html.Div([ 
        html.H2("Metrics with Positive Correlation to Democratic Vote Share"),
        html.P("""
        This graph allows exploration of metrics that have shown a positive correlation with Democratic vote share — in other words, as these metrics increase, support for Democratic candidates tends to rise relative to Republican candidates.
        """),
        html.Ul([
            html.Li("Graduate Degree (%): Counties with a higher share of highly educated individuals tend to vote more Democratic."),
            html.Li("Professional/Scientific Employment (%): A greater presence of white-collar industries like tech, management, and science is associated with stronger Democratic support."),
            html.Li("High Income ($75k+) (%): Higher income brackets, especially in urban or coastal counties, tend to lean more Democratic."),
            html.Li("Foreign-born Households (2–3 Rooms): Concentrations of immigrant populations in more modest housing situations also show a link to higher Democratic ratios."),
            html.Li("All Households (2–3 Rooms): Smaller housing units may signal urban density, which often aligns with Democratic trends."),
        ]),
    ], style={"width": "80%", "margin": "auto"}),

    # Positive Correlation Plot
    html.Div([ 
        html.H2("Positive Correlation Metrics"),
        dcc.Dropdown(
            id='metric-dropdown-positive',
            options=[{'label': v['label'], 'value': k} for k, v in column_mapping_positive.items()],
            value='graduate',
            clearable=False,
            style={'width': '80%', 'margin': 'auto'}
        ),
        dcc.Graph(id='positive-graph'),
    ], style={"width": "80%", "margin": "auto"}),

    # Second Text Group: Introduction to Negative Correlation
    html.Div([ 
        html.H2("Metrics with Negative Correlation to Democratic Vote Share"),
        html.P("""
        This second graph focuses on metrics with an inverse (negative) correlation, meaning that counties with higher values for these features tend to lean more Republican.
        """),
        html.Ul([
            html.Li("Some College or Associate's Degree (%): Mid-level education without a bachelor’s degree may reflect working-class populations who have trended more Republican."),
            html.Li("Low Income ($35k–$50k) (%): Lower income brackets, especially in rural counties, often show stronger Republican support."),
            html.Li("Retail Trade Employment (%): Higher employment in lower-wage, service-oriented sectors like retail is negatively correlated with Democratic vote share."),
            html.Li("Married Couples in Poverty (%): Traditional family structures in economic distress may signal communities with more conservative leanings."),
            html.Li("Households with 6–7 Rooms (%): Larger homes outside of major metro areas may correlate with suburban or rural living, often favoring Republicans."),
        ]),
    ], style={"width": "80%", "margin": "auto"}),

    # Negative Correlation Plot
    html.Div([ 
        html.H2("Negative Correlation Metrics"),
        dcc.Dropdown(
            id='metric-dropdown-negative',
            options=[{'label': v['label'], 'value': k} for k, v in column_mapping_negative.items()],
            value='some_college',
            clearable=False,
            style={'width': '80%', 'margin': 'auto'}
        ),
        dcc.Graph(id='negative-graph'),
    ], style={"width": "80%", "margin": "auto"}),

    # Third Text Group: Observed Decline in Democratic Vote Ratio
    html.Div([ 
        html.H2("Observed Decline in Democratic Vote Ratio Over Time"),
        html.P("""
        An overarching trend visible across the graphs is a gradual decrease in the Democratic-to-Republican vote ratio from 2016 to 2024. Several key factors likely contribute to this shift.
       """),
        html.P("""
        Here are some explanations for why we can visualize this decline:
        """),
        html.H3("Republican Gains Among Key Demographics"),
        html.P("""
        In the 2024 election, former President Donald Trump made significant inroads with key voter groups that had traditionally supported Democrats. One of the most notable shifts occurred within Latino and Black voter groups, particularly among women. Despite Democratic efforts to secure these groups, Trump improved his performance, especially in key battleground states such as Florida and Arizona.
        """),
        dcc.Markdown("""
        Source: [AP News: Women, Latinos, and Black Voters Shift in 2024 Election](https://apnews.com/article/election-harris-trump-women-latinos-black-voters-0f3fbda3362f3dcfe41aa6b858f22d12)
        """),
        html.H3("Decline in Democratic Turnout"),
        html.P("""
        Voter turnout for Democrats dropped sharply in 2024. Kamala Harris received 12 million fewer votes than Joe Biden did in 2020 — a 15% decline. This downturn was concentrated in urban cores and suburban areas, where Democratic support has historically been strongest. Meanwhile, Trump maintained nearly the same vote count as in 2020, giving Republicans a relative advantage.
        """),
        dcc.Markdown("""
        Source: [The Washington Post: Voter Turnout and Trump’s Stability](https://www.washingtonpost.com/)
        """),
    ], style={"width": "80%", "margin": "auto"})
])

# Callback for positive correlation plot
@callback(
    Output('positive-graph', 'figure'),
    Input('metric-dropdown-positive', 'value')
)
def update_positive_figure(selected_metric):
    col = column_mapping_positive[selected_metric]['col']
    label = column_mapping_positive[selected_metric]['label']
    fig = go.Figure()

    for year, df, color in zip(['2016', '2020', '2024'], [merged_2016, merged_2020, merged_2024], ['green', 'red', 'blue']):
        fig_part = px.scatter(df, x=col, y='Ratio', trendline='ols',
                              labels={col: label, 'Ratio': 'Vote Ratio (Dem / Rep)'})
        for trace in fig_part.data:
            fig.add_trace(go.Scatter(
                x=trace.x, y=trace.y,
                mode=trace.mode,
                name=f"{year}" + (' Regression' if trace.mode == 'lines' else ''),
                marker=dict(color=color) if trace.mode == 'markers' else None,
                line=dict(color=color, dash='dash') if trace.mode == 'lines' else None
            ))

    fig.update_layout(
        title=f"{label} vs. Democratic/Republican Vote Ratio (2016, 2020, 2024)",
        xaxis_title=label,
        yaxis_title="Vote Ratio (Dem / Rep)",
        showlegend=True,
        template='plotly_white',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False, dtick=1)
    )
    return fig

# Callback for negative correlation plot
@callback(
    Output('negative-graph', 'figure'),
    Input('metric-dropdown-negative', 'value')
)
def update_negative_figure(selected_metric):
    col = column_mapping_negative[selected_metric]['col']
    label = column_mapping_negative[selected_metric]['label']
    fig = go.Figure()

    for year, df, color in zip(['2016', '2020', '2024'], [merged_2016, merged_2020, merged_2024], ['green', 'red', 'blue']):
        fig_part = px.scatter(df, x=col, y='Ratio', trendline='ols',
                              labels={col: label, 'Ratio': 'Vote Ratio (Dem / Rep)'})
        for trace in fig_part.data:
            fig.add_trace(go.Scatter(
                x=trace.x, y=trace.y,
                mode=trace.mode,
                name=f"{year}" + (' Regression' if trace.mode == 'lines' else ''),
                marker=dict(color=color) if trace.mode == 'markers' else None,
                line=dict(color=color, dash='dash') if trace.mode == 'lines' else None
            ))

    fig.update_layout(
        title=f"{label} vs. Democratic/Republican Vote Ratio (2016, 2020, 2024)",
        xaxis_title=label,
        yaxis_title="Vote Ratio (Dem / Rep)",
        showlegend=True,
        template='plotly_white',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False, dtick=1)
    )
    return fig

# Register page
from dash import register_page
register_page(__name__, path="/findings")
