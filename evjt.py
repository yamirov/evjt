import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from sagv_dash import sagv_layout, register_sagv_callbacks
from parameter_dash import parameter_layout, register_parameter_callbacks
from margin_dash import margin_layout, register_margin_callbacks


# Initialize the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Functional Margins', href='/margin'),
        dcc.Link('SAGV Page', href='/sagv'),
        dcc.Link('Parameter Page', href='/parameter'),
    ]),
    html.Div(id='page-content')
])

# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/parameter':
        return parameter_layout
    elif pathname == '/margin':
        return margin_layout
    else:
        return sagv_layout

# Register other callbacks
register_sagv_callbacks(app)
register_parameter_callbacks(app)
register_margin_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)