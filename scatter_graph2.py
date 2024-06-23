import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the CSV file into a DataFrame
df = pd.read_csv('pizdata.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('SAGV Page', href='/sagv'),
        html.Br(),
        dcc.Link('Parameter Page', href='/parameter'),
    ]),
    html.Div(id='page-content')
])

# Layout for SAGV page
sagv_layout = html.Div([
    html.H1("Scatter Plot Distribution for SAGV"),
    html.Div(id='scatter-plots-sagv')
])

# Layout for Parameter page
parameter_layout = html.Div([
    html.H1("Scatter Plot Distribution for Parameter"),
    html.Div(id='scatter-plots-parameter')
])

# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/parameter':
        return parameter_layout
    else:
        return sagv_layout

# Callback to update the scatter plots for SAGV page
@app.callback(
    Output('scatter-plots-sagv', 'children'),
    [Input('url', 'pathname')]
)
def update_scatter_plots_sagv(pathname):
    if pathname == '/sagv':
        # Columns to plot
        ch_columns = [f'ch{i}ccc' for i in range(8)]

        # Create scatter plots
        scatter_plots = []
        for ch_col in ch_columns:
            fig = px.scatter(df, x='sagv', y=ch_col, title=f'{ch_col} vs sagv')
            scatter_plots.append(dcc.Graph(figure=fig))

        return scatter_plots

# Callback to update the scatter plots for Parameter page
@app.callback(
    Output('scatter-plots-parameter', 'children'),
    [Input('url', 'pathname')]
)
def update_scatter_plots_parameter(pathname):
    if pathname == '/parameter':
        # Columns to plot
        ch_columns = [f'ch{i}ccc' for i in range(8)]

        # Create scatter plots
        scatter_plots = []
        for ch_col in ch_columns:
            fig = px.scatter(df, x='parameter', y=ch_col, title=f'{ch_col} vs Parameter')
            scatter_plots.append(dcc.Graph(figure=fig))

        return scatter_plots

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)