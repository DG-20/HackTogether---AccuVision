import dash 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go

#Started the app
app = dash.Dash(__name__)

#Reading data
df = pd.read_csv("data/test.csv")

#Line graph object created

app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Sat', 'value': ' Sat'},
            {'label': 'Sun', 'value': ' Sun'},
            {'label': 'Mon', 'value': ' Mon'}
        ],
        value=' Sat'
    ),
    html.Div(id='dd-output-container')
])
fig = px.line(df, x="Time of Day", y=" Sat", title="Stuff")
suppress_callback_exceptions=True
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    fig = px.line(df, x="Time of Day", y=value, title="Stuff")
    return 'You have selected "{}"'.format(value)

app.layout = html.Div(children =
    [
        #Random HTML
        html.H1("HI"),
        html.P("asdfasdf"),
        html.A("HIHIHI", href="https://dash.plotly.com/dash-html-components/a"), 
        #The actual graph to display
        dcc.Graph(
            figure = fig
        ),
        html.Button('Sat', id = 'Sat'),
        html.Button('Sun', id = 'Sun')
        ])
suppress_callback_exceptions=True
#Running it
if __name__ == '__main__':
    app.run_server(debug=True)