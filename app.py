import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from components import Column, Header, Row
# from auth import auth

import pandas as pd
import numpy as np
import warnings
import plotly.graph_objs as go
import json

app = dash.Dash(
    __name__
)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Optionally display a log in screen.                                                                   #
# If `REQUIRE_LOGIN = True` in `config.py`, then auth_instance allows you to programatically access the #
# username of the currently logged in user.                                                             #
# If `REQUIRE_LOGIN = False`, then no login screen will be displayed and `auth_instance` will be `None` #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# auth_instance = auth(app)

server = app.server  # Expose the server variable for deployments

# Standard Dash app code below
fp = open("data/data_description.json", "r")
data_dict = json.load(fp)
fp.close()
df_train = pd.read_csv('data/train.csv')
df = df_train.drop(columns=["Id"])
print(df.columns)
app.layout = html.Div(className='container', children=[

    Header('Housing Prices Explorer'),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Scatter plot', children=dcc.Graph(id='scatter')),
        dcc.Tab(label='Box plot', children=dcc.Graph(id='box')),
    ]),
    # Row([
    #     Column(width=6, children=[
    #         dcc.Graph(id='scatter')
    #     ]),
    #     Column(width=6, children=[
    #         dcc.Graph(id='box')
    #     ]),
    # ]),
    Row([
        Column(width=6, children=[
            html.Div("Variable"),
            dcc.Dropdown(
                id = 'variable',
                options = [{'label':el, 'value':el} for el in df.columns if (df[el].dtype.name in {'int64', 'float64'})],
                value = 'GrLivArea'
            )
        ]),
        Column(width=3, children=[
            html.Div("x-axis"),
            dcc.RadioItems(
                id = 'xmode',
                options = [
                    {'label': 'linear', 'value': 'linear'},
                    {'label': 'logarithmic', 'value': 'log'}
                ],
                value = 'linear'
            )
        ]),
        Column(width=3, children=[
            html.Div("y-axis"),
            dcc.RadioItems(
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
    ]),
    html.Div("https://github.com/Mskycoder/dash-housing-prices")
])


@app.callback(dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('variable', 'value'),
    dash.dependencies.Input('xmode', 'value'),
    dash.dependencies.Input('ymode', 'value')])
def update_scatter(var, xmode, ymode):

    trace = go.Scatter(
        x = df[var],
        y = df['SalePrice'],
        mode = 'markers'
    )
    figure = go.Figure(

        data = [trace],
        layout = go.Layout(

            title = "{}".format(data_dict[var]),
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


@app.callback(dash.dependencies.Output('box', 'figure'),
    [dash.dependencies.Input('variable', 'value')])
def update_box(var):


    trace = go.Box(
        x = df[var],
        y = df['SalePrice']
    )

    figure = go.Figure(

        data = [trace],
        layout = go.Layout(

            title = "{}".format(data_dict[var]),
            xaxis = dict(
                title = var,
                autorange = True
            ),
            yaxis = dict(
                title = 'SalePrice',
                autorange = True
            )
        )
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
