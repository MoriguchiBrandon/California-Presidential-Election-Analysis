# U.S. Election Analysis Dashboard

This project is a **data visualization web app** built with [Plotly Dash](https://dash.plotly.com/), hosted on **Google App Engine**. It explores the relationship between **U.S. county-level demographic and economic indicators** and **presidential election results** across 2016, 2020, and 2024.

# Link to app

[California Election Prediction Analysis](https://my-project-452121.wl.r.appspot.com)

##  Repository Structure

```
.
├── appengine
│   ├──app.yaml                 # App Engine configuration
│   ├── requirements.txt         # Python dependencies
│   ├──app.py                   # Dash app entry point
│   ├── assets/                  # Static image
│   │    └── Navigation.jpg
├───└──pages/                   # Route-based Dash pages
│        ├── home.py
│        ├── objective.py
│        ├── methods.py
│        └── findings.py
├──election data/           # Processed CSV files for dashboard use
│   ├── 2016.csv
│   ├── 2020.csv
│   ├── 2024.csv
│   └── ...
└── Census vs Results.ipynb  # Analysis & modeling notebook
```

##  Live App Structure

The site is structured into multiple navigable pages:

- **Home:** Overview and entry point
- **Project Objective:** Explains the motivation and goals
- **Analytical Methods:** Shows data sources, cleaning steps, correlation analysis, and model training
- **Major Findings:** Displays key relationships and insights using interactive visualizations

##  Data Analysis

All preprocessing and analysis were conducted in the `Census vs Results.ipynb` Jupyter notebook. Steps included:

- Merging county-level election results and census data (2016–2024)
- Calculating correlation matrices to identify impactful features
- Plotting feature importance visually
- Training the following models:
  - **Multilayer Perceptron (MLP)**
  - **Random Forest**
  - **Gradient Boosting**

Results were exported as CSV files and visualized within the app.

##  Dashboard Features

- Interactive scatter plots by metric and year
- Side-by-side comparison of features positively and negatively correlated with Democratic/Republican vote ratios
- Responsive layout and clean navigation

##  Deployment: Google App Engine

The app is deployed to Google Cloud using **App Engine Standard Environment**.


##  Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

### Key packages:
- `dash`
- `dash-bootstrap-components`
- `plotly`
- `pandas`
- `scikit-learn`
- `matplotlib`
- `seaborn`

##  Notes

- Data files used in the app are static CSVs output from the notebook.
- The notebook is **not used in the app runtime**, but all CSVs are derived from it.
- Static files like images should be placed in the `assets/` folder for automatic loading by Dash.


