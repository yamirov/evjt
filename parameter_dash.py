from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the CSV file into a DataFrame for Parameter
df_parameter = pd.read_csv('pizdata.csv')

# Layout for Parameter page
parameter_layout = html.Div([
    html.H1("Scatter Plot Distribution for Parameter"),
    html.Div(id='scatter-plots-parameter')
])

def register_parameter_callbacks(app):
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
                fig = px.scatter(df_parameter, x='parameter', y=ch_col, title=f'{ch_col} vs Parameter')
                scatter_plots.append(dcc.Graph(figure=fig))
            return scatter_plots