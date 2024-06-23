from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the CSV file into a DataFrame for SAGV
df_sagv = pd.read_csv('pizdata.csv')

# Layout for SAGV page
sagv_layout = html.Div([
    html.H1("Scatter Plot Distribution for SAGV"),
    html.Div(id='scatter-plots-sagv')
])

def register_sagv_callbacks(app):
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
                fig = px.scatter(df_sagv, x='sagv', y=ch_col, title=f'{ch_col} vs sagv')
                scatter_plots.append(dcc.Graph(figure=fig))
            return scatter_plots