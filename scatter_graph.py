import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the CSV file into a DataFrame
df = pd.read_csv('pizdata.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Scatter Plot Distribution"),
    dcc.Dropdown(
        id='group-by-dropdown',
        options=[
            {'label': 'sagv', 'value': 'sagv'},
            {'label': 'Parameter', 'value': 'parameter'}
        ],
        value='sagv',
        clearable=False
    ),
    html.Div(id='scatter-plots')
])

# Callback to update the scatter plots based on the selected group-by column
@app.callback(
    Output('scatter-plots', 'children'),
    [Input('group-by-dropdown', 'value')]
)
def update_scatter_plots(group_by_column):
    # Columns to plot
    ch_columns = [f'ch{i}ccc' for i in range(8)]

    # Create scatter plots
    scatter_plots = []
    for ch_col in ch_columns:
        fig = px.scatter(df, x=group_by_column, y=ch_col, title=f'{ch_col} vs {group_by_column}')
        scatter_plots.append(dcc.Graph(figure=fig))

    return scatter_plots

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)