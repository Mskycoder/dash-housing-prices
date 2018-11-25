import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from components import Column, Header, Row
from auth import auth

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
import plotly.graph_objs as go

app = dash.Dash(
    __name__
)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Optionally display a log in screen.                                                                   #
# If `REQUIRE_LOGIN = True` in `config.py`, then auth_instance allows you to programatically access the #
# username of the currently logged in user.                                                             #
# If `REQUIRE_LOGIN = False`, then no login screen will be displayed and `auth_instance` will be `None` #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
auth_instance = auth(app)

server = app.server  # Expose the server variable for deployments

# Standard Dash app code below

df_train = pd.read_csv('train.csv')
print(type(df_train['GrLivArea'].dtype))
app.layout = html.Div(className='container', children=[

    Header('Sample App'),
    Row([dcc.Graph(id='scatter')]),
    Row([
        Column(width=4, children='Variable'),
        Column(width=4, children='x-axis'),
        Column(width=4, children='y-axis'),
    ]),
    Row([
        Column(width=4, children=[
            dcc.Dropdown(
                id = 'variable',
                options = [{'label':el, 'value':el} for el in df_train.columns if (df_train[el].dtype.name in {'int64', 'float64'})],
                value = 'GrLivArea'
            )
        ]),
        Column(width=4, children=[
            dcc.Dropdown(
                id = 'xmode',
                options = [
                    {'label': 'linear', 'value': 'linear'},
                    {'label': 'logarithmic', 'value': 'log'}
                ],
                value = 'linear'
            )
        ]),
        Column(width=4, children=[
            dcc.Dropdown(
                id = 'ymode',
                options = [
                    {'label': 'linear', 'value': 'linear'},
                    {'label': 'logarithmic', 'value': 'log'}
                ],
                value = 'linear'
            )
        ])
        # Column(width=8, children=[
        #     dcc.Graph(id='graph')
        # ])
    ])
])


@app.callback(dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('variable', 'value'),
    dash.dependencies.Input('xmode', 'value'),
    dash.dependencies.Input('ymode', 'value')])
def update_figure(var, xmode, ymode):

    if var == 'MSSubClass':

        trace = go.Box(
            x = df_train[var],
            y = df_train['SalePrice']
            )
    else:
        trace = go.Scatter(
            x = df_train[var],
            y = df_train['SalePrice'],
            mode = 'markers'
            )
    figure = go.Figure(

        data = [trace],
        layout = go.Layout(

            title = "Housing prices",
            xaxis = dict(
                title = var,
                type = xmode,
                autorange = True
            ),
            yaxis = dict(
                title = 'SalePrice',
                type = ymode,
                autorange = True
            )
        )
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
