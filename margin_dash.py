from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import os
import glob


# Function to get the list of CSV files from the specified directory and its subfolders
def get_csv_files(directory):
    return glob.glob(os.path.join(directory, '**/*.csv'), recursive=True)

# Function to load a specific CSV file into a DataFrame
def load_csv_file(file_path):
    return pd.read_csv(file_path)

# Function to load all CSV files into a single DataFrame
def load_all_csv_files(directory):
    all_files = get_csv_files(directory)
    df_list = [pd.read_csv(file) for file in all_files]
    return pd.concat(df_list, ignore_index=True)

# Directory containing the CSV files
csv_directory = r'\\ger\ec\proj\ha\sa\Groups\FV\Memory\Volume_Results\LNL\margin_scanner_hist'

# Get the list of CSV files
csv_files = get_csv_files(csv_directory)

# Load all CSV files as the default DataFrame
df_sagv = load_all_csv_files(csv_directory)

# Get the list of parameter columns for the x-axis options
#parameter_columns = [col for col in df_sagv.columns if col not in ['neg_value', 'pos_value', 'sagv']]
parameter_columns = df_sagv['parameter'].unique()

# Get the unique values for the sagv filter dropdown
sagv_values = df_sagv['sagv'].unique()

# Get the unique values for the sagv filter dropdown
host_values = df_sagv['Host Name'].unique()

mrc_ver_values = sorted(df_sagv['mrc ver'].astype('str').unique()) 

# Layout for SAGV page
margin_layout = html.Div([
    html.H1("Margins"),
    html.Div([
        dcc.Dropdown(
            id='csv-file-dropdown',
            options=[{'label': os.path.basename(file), 'value': file} for file in csv_files] + [{'label': 'Load All CSV Files', 'value': 'all'}],
            value='all',
            clearable=False
        ),
        dcc.Dropdown(
            id='mrc-ver-dropdown',
            multi=True,
            placeholder='Select MRC Ver'
        ),
        dcc.Dropdown(
            id='sagv-filter-dropdown',
            options=[{'label': str(val), 'value': str(val)} for val in sagv_values],
            placeholder='Filter by SAGV value'
        ),
        dcc.Dropdown(
            id='host-filter-dropdown',
            options=[{'label': str(val), 'value': str(val)} for val in host_values],
            multi= True,
            placeholder='Host name' 
        ),
        html.Button('Apply Filter', id='filter-button', n_clicks=0)
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    html.Div(id='scatter-plots-margin', style={'width': '75%', 'display': 'inline-block', 'paddingLeft': '5%'})
])

def register_margin_callbacks(app):

    # Callback to update the mrc ver dropdown options based on the filtered data
    @app.callback(
        Output('mrc-ver-dropdown', 'options'),
        [Input('filter-button', 'n_clicks')],
        [State('csv-file-dropdown', 'value'), State('host-filter-dropdown', 'value'), State('sagv-filter-dropdown', 'value')]
    )
    def update_mrc_ver_options(n_clicks, csv_file, host_filter, sagv_filter):
        if csv_file == 'all':
            filtered_df = df_sagv
        else:
            filtered_df = load_csv_file(csv_file)

        if sagv_filter:
            filtered_df = filtered_df[filtered_df['sagv'].astype(str).str.contains(sagv_filter)]

        if host_filter:
            filtered_df = filtered_df[filtered_df['Host Name'].astype(str).isin(host_filter)]

        mrc_ver_values = sorted(filtered_df['mrc ver'].astype('str').unique())
        return [{'label': val, 'value': val} for val in mrc_ver_values]


    # Callback to update the scatter plots for SAGV page
    @app.callback(
        Output('scatter-plots-margin', 'children'),
        [Input('filter-button', 'n_clicks')],
        [State('csv-file-dropdown', 'value'), State('host-filter-dropdown', 'value'), State('sagv-filter-dropdown', 'value'),State('mrc-ver-dropdown', 'value')]
        #[State('csv-file-dropdown', 'value'), State('sagv-filter-dropdown', 'value')]
    )
    def update_scatter_plots_margin(n_clicks, csv_file, host_filter, sagv_filter,mrc_ver_filter):
        if csv_file == 'all':
            filtered_df = df_sagv
        else:
            filtered_df = load_csv_file(csv_file)
        
        if sagv_filter:
            filtered_df = filtered_df[filtered_df['sagv'].astype(str).str.contains(sagv_filter)]
       
        if host_filter:
            filtered_df = filtered_df[filtered_df['Host Name'].astype(str).isin(host_filter)]

        if mrc_ver_filter:
            filtered_df = filtered_df[filtered_df['mrc ver'].astype('str').isin(mrc_ver_filter)]

        scatter_plots = []
        for parameter in parameter_columns:
            filtered_parameter_df = filtered_df[filtered_df['parameter'] == parameter].sort_values(by='mrc ver')
            fig = px.scatter(filtered_parameter_df, x='mrc ver', y=['neg_value', 'pos_value'], title=f'{parameter}')
            scatter_plots.append(dcc.Graph(figure=fig))
        
        return scatter_plots