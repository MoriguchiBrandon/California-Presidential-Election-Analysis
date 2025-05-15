# pages/objective.py
import dash
from dash import html, dcc

dash.register_page(__name__, path="/objective", name="Objective")

layout = html.Div(
    style={"padding": "2rem"},
    children=[
        html.H1("California Election Results Prediction", style={"marginBottom": "1rem"}),
        html.H5("Brandon Moriguchi, Jaspreet Singh"),
        html.P([
            "Project Github: ",
            html.A("California-Presidential-Election-Analysis", href="https://github.com/MoriguchiBrandon/California-Presidential-Election-Analysis", target="_blank")
        ]),
        html.Hr(),

        html.H2("Project Summary", style={"marginTop": "2rem"}),
        html.P("""
            This project aims to analyze the results of past presidential elections in California and develop a predictive
            model to forecast future outcomes. By combining historical election results
            with demographic data from the U.S. Census, we aim to identify voter trends and make informed predictions
            for the 2024 election.
        """),
        html.P("""
            We will analyze data from the 2012, 2016, 2020, and 2024 elections and apply statistical and machine
            learning techniques to build predictive models. Visualizations—such as graphs and scatter plots—will be used
            to highlight correlations between demographic variables and voting outcomes.
        """),

        html.H2("Broader Impacts", style={"marginTop": "2rem"}),
        html.Ul([
            html.Li("Enhance understanding of voting patterns across California."),
            html.Li("Provide useful insights for political campaigns, advocacy groups, and policymakers."),
            html.Li("Reveal how key factors—such as income, education, and race—shape electoral outcomes."),
            html.Li("Evaluate the accuracy of polling methods by comparing model predictions to actual results."),
        ]),
        html.P("""
            This project aims to deepen public awareness of how social and economic trends influence
            elections and support more data-informed political strategies.
        """),

        html.H2("Data Sources", style={"marginTop": "2rem"}),
        html.H4("California Secretary of State Election Results"),
        html.P("Includes detailed records of elections statewide. We'll focus on presidential results from: 2012, 2016, 2020, and 2024"),
        html.P([
            "Source: ",
            html.A("California Secretary of State", href="https://elections.cdn.sos.ca.gov/", target="_blank")
        ]),

        html.H4("U.S. Census Data"),
        html.P("Provides demographic and economic metrics across California counties."),
        html.P("Key variables include:"),
        html.Ul([
            html.Li("Race/Ethnicity"),
            html.Li("Median Household Income"),
            html.Li("Educational Attainment"),
            html.Li("Employment Sectors"),
            html.Li("Housing Characteristics"),
        ]),

        html.H4("CA Counties Geomaping"),
        html.P("Provides Geojson corrdinates for mapping California counties."),
        html.P([
            "Source: ",
            html.A("Code For Germany Github", href="https://github.com/codeforgermany/click_that_hood/blob/main/public/data/california-counties.geojson", target="_blank")
        ]),

        html.H2("Expected Major Findings", style={"marginTop": "2rem"}),

        html.H4("1. Regional Differences in Voting Preferences"),
        html.P("""
            We expect a divide between urban and rural counties, with urban areas (e.g., Los Angeles, San Francisco)
            trending Democratic, and rural areas (e.g., Kern, Modoc) leaning Republican.
        """),

        html.H4("2. Demographic Correlations"),
        html.P("The model will likely show relationships between:"),
        html.Ul([
            html.Li("Income level and party preference"),
            html.Li("Educational attainment and voting behavior"),
            html.Li("Racial/ethnic composition and party support"),
        ])

    ]
)

