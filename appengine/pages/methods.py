# pages/methods.py
import dash
from dash import html, dcc  

dash.register_page(__name__, path="/methods")

def layout():  
    return html.Div([
        html.H1("Methodology", style={"textAlign": "center"}),

        html.P("This page outlines the data processing, analysis, and modeling steps used in this project."),

        html.H2("1. Data Collection"),
        html.Div([
            dcc.Markdown("""
We collected and organized data from the following sources:

- **U.S. Census Data** for years 2012, 2016, 2020, and 2024  
  - All of the tables came from S0101 and S0501 tables in the Census  
  - They include:  
    - Age and sex breakdowns  
    - Educational attainment  
    - Employment by industry  
    - Household income  
    - Housing characteristics

                         
- **California Election Results** for presidential elections in:  
  - 2004, 2008, 2012, 2016, 2020, and 2024  

These datasets were aggregated at the county level.
            """)
        ]),

        html.H2("2. Preprocessing"),
        html.Div([
            dcc.Markdown("""
We preprocessed the raw data to ensure consistency and usability:

- Normalized column names and units across years  
- Created mappings for column names to ensure consistency  
- Merged multiple census tables into unified yearly datasets  
- Filtered for relevant metrics (e.g., % with Graduate's, median income)  
- Computed derived features like Democratic-to-Republican vote ratio (`Ratio`)  
- Joined census data with election results per county
            """)
        ]),

        html.H2("3. Correlation Analysis"),
        html.Div([
            dcc.Markdown("""
To explore relationships between demographic factors and voting outcomes, we:

- Generated correlation matrices for each election year (2012–2024)  
- Identified strong positive and negative correlations  
- Found high correlation on categories like:  
  - **Education:** higher education showed positive correlation with Democratic vote share  
  - **Income:** lower-middle income groups tended to vote more Republican  
  - **Employment:** retail and construction industries leaned more Republican  
  - **Housing:** renters and smaller households correlated with Democratic votes
            """)
        ]),

        html.H2("4. Modeling"),
        html.Div([
            dcc.Markdown("""
We trained predictive models to estimate the 2024 vote ratio per county:

- **Neural Network (MLP):**  
  - Built using TensorFlow/Keras  
  - Input features included all merged census metrics  

- **Random Forest & Gradient Boosting:**  
  - Used `sklearn.ensemble` models  
  - Trained on historical features and all merged census metrics  
  - Tuned with basic hyperparameters for performance  

Each model outputs a `Predicted_Ratio` used in visual comparisons.
            """)
        ]),

        html.H2("5. Visualizations"),
        html.Div([
            dcc.Markdown("""
Key insights were visualized with interactive maps and scatter plots:

- **Choropleth Maps:**  
  - Actual 2024 vote ratios by county  
  - Predicted results by model  
  - Discrete red/blue classifications for comparison  

- **Scatter Plots:**  
  - Educational attainment vs. vote ratio  
  - Income brackets vs. vote ratio  
  - Employment sectors vs. vote ratio  
  - Household characteristics vs. vote ratio  

These helped us validate and explain model predictions using real-world data.
            """)
        ])
    ], style={"padding": "2rem"})
