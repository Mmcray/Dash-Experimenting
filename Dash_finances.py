import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pandas_datareader.data as web
import datetime
import plotly.graph_objs as go
from dash.dependencies import Input, Output
app = dash.Dash()






colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='***Learning Dash***', draggable=True, 
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Stock Daily Highs', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div(children='''
        Symbol to graph
        ''', style={
            'color': colors['text']
            }),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
                      
def update_value(input_data):
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)


    return dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': df.index, 'y' : df.High, 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )



if __name__ == '__main__':
    app.run_server()
