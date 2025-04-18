import pandas as pd
import requests
from dash import Dash, html, dcc
import plotly.express as px

# ------------------ Data Setup ------------------

def fetch_and_prepare_data():
    def check_api(url):
        """Helper function to check if the API request is successful."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Successfully fetched data from {url}")
                return response.json()
            else:
                print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def check_excel(url):
        """Helper function to check if Excel file can be accessed."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Successfully fetched election data from {url}")
                return response.content  # Return the raw binary content of the Excel file
            else:
                print(f"Failed to fetch election data from {url}. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching election data from {url}: {e}")
            return None

    # Fetch S0101 Demographics Data
    url1 = "https://api.census.gov/data/2016/acs/acs5/subject?get=group(S0101)&ucgid=pseudo(0400000US06$0500000)"
    data1 = check_api(url1)
    if not data1:
        return pd.DataFrame()
    df1 = pd.DataFrame(data1[1:], columns=data1[0])

    # Fetch S0501 Nativity/Earnings Data
    url2 = "https://api.census.gov/data/2016/acs/acs5/subject?get=group(S0501)&ucgid=pseudo(0400000US06$0500000)"
    data2 = check_api(url2)
    if not data2:
        return pd.DataFrame()
    df2 = pd.DataFrame(data2[1:], columns=data2[0])

    # Fetch variable labels
    vars_url = "https://api.census.gov/data/2016/acs/acs5/subject/variables.json"
    vars_data = check_api(vars_url)
    if not vars_data or 'variables' not in vars_data:
        print("Failed to fetch variable labels.")
        vars_data = {}

    def label_cols(df):
        new_cols = {col: vars_data[col]['label'] for col in df.columns if col in vars_data}
        df.rename(columns=new_cols, inplace=True)
        return df

    df1 = label_cols(df1)
    df2 = label_cols(df2)

    # Clean and merge
    df1 = df1.loc[:, ~df1.columns.str.contains('Margin|Percent|Median|Geography|Ratio')]
    df2 = df2.loc[:, ~df2.columns.str.contains('Margin|Percent|Median|Geography|Ratio')]

    merged = pd.merge(df1, df2, on='NAME', how='outer')
    merged['County'] = merged['NAME'].str.replace(' County, California', '', regex=False).str.title()

    try:
        election_url = 'https://raw.githubusercontent.com/MoriguchiBrandon/California-Presidential-Election-Analysis/main/electionData/csv-candidates-2016.csv'
        election_df = pd.read_csv(election_url)
        print("Successfully fetched election data from", election_url)
    
        election_df['County'] = election_df['County'].str.title()
        merged = pd.merge(merged, election_df, on='County', how='inner')
        merged['Ratio'] = merged['Democratic Vote Total'] / merged['Republican Vote Total']
    except Exception as e:
        print("Failed to load or merge election data:", e)
        return pd.DataFrame()


    # Ensure that the merged dataset is not empty
    if merged.empty:
        print("Warning: Merged dataset is empty.")
        return pd.DataFrame()

    return merged


merged_df = fetch_and_prepare_data()

# ------------------ Plot Definitions ------------------

def make_scatter(x_col, title, xlabel):
    # Check if the columns exist in the DataFrame before trying to drop NaNs
    if x_col not in merged_df.columns or 'Ratio' not in merged_df.columns:
        print(f"Warning: Missing columns for {title}. Skipping plot.")
        return px.scatter()

    # Drop rows with NaN values in the columns used for plotting
    df_plot = merged_df.dropna(subset=[x_col, 'Ratio'])
    if df_plot.empty:
        print(f"Warning: No valid data for {title}. Skipping plot.")
        return px.scatter()

    fig = px.scatter(
        df_plot,
        x=x_col,
        y='Ratio',
        labels={'x': xlabel, 'Ratio': 'Dem/Rep Vote Ratio'},
        title=title
    )
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
    html.Div([
        dcc.Graph(figure=make_scatter(p['x_col'], p['title'], p['xlabel'])) for p in plots
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
