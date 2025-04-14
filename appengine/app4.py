# app_edu_vote.py

import pandas as pd
import requests
from dash import Dash, html, dcc
import plotly.express as px

# ------------------ Data Setup ------------------

def fetch_and_prepare_data():
    # S0101: Demographics
    url1 = "https://api.census.gov/data/2016/acs/acs5/subject?get=group(S0101)&ucgid=pseudo(0400000US06$0500000)"
    data1 = requests.get(url1).json()
    df1 = pd.DataFrame(data1[1:], columns=data1[0])

    # S0501: Nativity and earnings
    url2 = "https://api.census.gov/data/2016/acs/acs5/subject?get=group(S0501)&ucgid=pseudo(0400000US06$0500000)"
    data2 = requests.get(url2).json()
    df2 = pd.DataFrame(data2[1:], columns=data2[0])

    # Variable labels
    vars_url = "https://api.census.gov/data/2016/acs/acs5/subject/variables.json"
    vars_data = requests.get(vars_url).json()['variables']

    def label_cols(df):
        new_cols = {}
        for col in df.columns:
            if col in vars_data:
                new_cols[col] = vars_data[col]['label']
        df.rename(columns=new_cols, inplace=True)
        return df

    df1 = label_cols(df1)
    df2 = label_cols(df2)

    df1 = df1.loc[:, ~df1.columns.str.contains('Margin|Percent|Median|Geography|Ratio|S0101')]
    df2 = df2.loc[:, ~df2.columns.str.contains('Margin|Percent|Median|Geography|Ratio|S0501')]

    merged = pd.merge(df1, df2, on='NAME', how='outer')
    merged['County'] = merged['NAME'].str.replace(' County, California', '', regex=False).str.title()

    # Election data
    election_url = 'https://raw.githubusercontent.com/yourusername/yourrepo/main/csv-candidates-2016-cleaned.csv'  # Use GitHub or GCS to host this
    election_df = pd.read_csv(election_url)
    election_df['County'] = election_df['County'].str.title()
    merged = pd.merge(merged, election_df, on='County', how='inner')

    merged['Ratio'] = merged['Democratic Vote Total'] / merged['Republican Vote Total']
    return merged

merged_df = fetch_and_prepare_data()

# ------------------ Plot Definitions ------------------

def make_scatter(x_col, title, xlabel):
    fig = px.scatter(merged_df, x=x_col, y='Ratio',
                     labels={'x': xlabel, 'Ratio': 'Dem/Rep Vote Ratio'},
                     title=title)
    fig.update_layout(height=400)
    return fig

plots = [
    {
        "title": "Bachelor's Degree or Higher vs. Vote Ratio",
        "x_col": "Total!!Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree",
        "xlabel": "Percent with Graduate or Professional Degree"
    },
    {
        "title": "Some College or Associate Degree vs. Vote Ratio",
        "x_col": "Native!!Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Some college or associate's degree",
        "xlabel": "Percent with Some College or Associate Degree"
    },
    {
        "title": "Science/Management Industry vs. Vote Ratio",
        "x_col": "Native!!Estimate!!INDUSTRY!!Professional, scientific, and management, and administrative and waste management services",
        "xlabel": "Percent Employed in Science/Management"
    },
    {
        "title": "Income $25K–$35K vs. Vote Ratio",
        "x_col": "Native!!Estimate!!EARNINGS IN THE PAST 12 MONTHS (IN 2016 INFLATION-ADJUSTED DOLLARS) FOR FULL-TIME, YEAR-ROUND WORKERS!!Population 16 years and over with earnings!!$25,000 to $34,999",
        "xlabel": "Percent Earning $25K–$35K"
    }
]

# ------------------ Dash App ------------------

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("2016 Presidential Vote Ratio vs. Socioeconomic Factors"),
    html.Div([dcc.Graph(figure=make_scatter(p['x_col'], p['title'], p['xlabel'])) for p in plots])
])

if __name__ == '__main__':
    app.run(debug=True)
