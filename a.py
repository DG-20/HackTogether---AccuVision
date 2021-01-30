# IMPORTS

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import plotly.graph_objs as go

nsdq = pd.read_csv('C:/Users/mahee/Desktop/Hacktogether/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)

# Initialize Dashboard
app = dash.Dash()

options = []
for tic in nsdq.index:
    mydict = {}
    mydict['label'] = str(nsdq.loc[tic]['Name'])
    mydict['value'] = tic
    options.append(mydict)

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),

    html.Div([
        html.H3('Enter a Stock Symbol:'),
        dcc.Dropdown(id='my_stock_picker',
                     options=options,
                     value=['TSLA'],  # Default Value
                     multi=True)
    ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '30%'}),


    html.Div([
        html.H3('Select a Start and End Date:'),
        dcc.DatePickerRange(id='my_date_picker',
                            min_date_allowed=datetime(2015, 1, 1),
                            max_date_allowed=datetime.today(),
                            start_date=datetime(2018, 1, 1),
                            end_date=datetime.today()
                            ),
    ], style={'display': 'inline-block'}),


    html.Div([
        html.Button(id='submit-btn',
                    n_clicks=0,
                    children='Submit',
                    style={'fontSize': 24, 'margin-left': '30px'}),

    ], style={'display': 'inline-block'}),


    dcc.Graph(id='my_graph',
              figure={'data': [go.Scatter(
                 x=[1, 2],
                 y=[3, 1],
                 mode='lines'
              )],
                  'layout':go.Layout(title='Default Title')},
              config={
                  'displayModeBar': False
              }
              )
])

# Add Real-Time Title Functionality


@app.callback(Output('my_graph', 'figure'),
              [Input('submit-btn', 'n_clicks')],
              [State('my_stock_picker', 'value')],
              [State('my_date_picker', 'start_date')],
              [State('my_date_picker', 'end_date')]
              )
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, 'yahoo', start, end)
        traces.append({'x': df.index, 'y': df['Adj Close'], 'name': tic})

    fig = {'data': traces,
           'layout': {'title': ', '.join(stock_ticker)+' Closing Prices'}
           }

    return fig


# Start Server
if __name__ == '__main__':
    app.run_server()
