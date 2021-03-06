# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

def dashplot(fig):
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.Div(['d_peak', dcc.Input(id='d_peak', value=98, type='int')]),
        html.Div(['d_peak', dcc.Input(id='d_peak', value=98, type='number')]),
        html.Div(['r1', dcc.Input(id='r1', value=3.67, type='number')]),
        html.Div(['sigma_s', dcc.Input(id='sigma_s', value=3.55, type='number')]),
        dcc.Graph(id='Surface Simulation', figure=fig)
    ])

    if __name__ == '__main__':
        app.run_server(debug=True)
