import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pandas_datareader.data as web
import datetime
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime.now()
df = web.DataReader("TSLA", 'yahoo', start, end)


app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])

inputA = html.Div(
    [
        ("Input Stock Ticker"),
        dbc.Input(id="input", placeholder="AAPL, TSLA, ETC..", bs_size="md", className="mb-3"),
    ]
)

inputB = html.Div(
    [
        ("Input Stock Ticker #2"),
        dbc.Input(id="inputB", placeholder="AAPL, TSLA, ETC..", bs_size="md", className="mb-3"),
    ]
)


app.layout = dbc.Container(
    [
        html.H1(("Stock Comparison"), style={'textAlign': 'center'}),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(inputA, width=3),
                dbc.Col(inputB, width={"size" : 3, "offset" : 3}),
            ]
                ),
        dbc.Row(
            [
               dbc.Col(id='output-graph', width=5),
               dbc.RadioItems(
                    id='yahoo_columns',
                    options=[
                        {"label": "High", "value": df.High},
                        {"label": "Low", "value": df.Low},
                        {"label": "Open", "value": df.Open},
                        {"label": "Close", "value": df.Close},
                            ]
                                ),
               dbc.Col(id='output-graphB',width=5),
            ]
                )
        
    ], fluid=True
)


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    Input(component_id='input', component_property='value'),
    Input(component_id='yahoo_columns', component_property='value')
)
def update_value(input_data, yaxis):
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)

    return dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': df.index, 'y' : yaxis, 'type': 'line', 'name': input_data},
            ],
            'layout': go.Layout(                                
                                xaxis =  {                                     
                                    'showgrid': False
                                         },
                                yaxis = {                              
                                   'showgrid': False
                                        }
                                )
                }
    )


@app.callback(
    Output(component_id='output-graphB', component_property='children'),
    Input(component_id='inputB', component_property='value'),
    Input(component_id='yahoo_columns', component_property='value')
)
def update_valueB(input_data, yaxis):
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)

    return dcc.Graph(
        id='Graph2',
        figure={
            'data': [
                {'x': df.index, 'y' : yaxis, 'type': 'line', 'name': input_data},
            ]
                }
    )

if __name__ == '__main__':
    app.run_server()
