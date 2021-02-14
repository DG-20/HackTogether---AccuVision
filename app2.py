import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import time
import datetime
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import date

# Started the app
app = dash.Dash(__name__)

# Reading data
df = pd.read_csv("data/test.csv")

counter = 'Live Person Counter'

app.layout = html.Div(
    children = [
        html.H1(counter),
        html.P("Please pick the day that you want to view data for using the Slider feature, stay safe!"),
        #html.A("HIHIHI", href="https://dash.plotly.com/dash-html-components/a"),
        html.Div([
        dcc.Dropdown(
            id="daySelector",
            options=[
                {"label": "Saturday", "value": "Saturday"},
                {"label": "Sunday", "value": "Sunday"},
                {"label": "Monday", "value": "Monday"},
                {"label": "Tuesday", "value": "Tuesday"},
                {"label": "Wednesday", "value": "Wednesday"},
                {"label": "Thursday", "value": "Thursday"},
                {"label": "Friday", "value": "Friday"},
            ],
            multi=True,
            value="Saturday",
        )]),
        html.Div([
         dcc.Graph(id='ourGraph')])
    ]
)

@app.callback(
    Output('ourGraph', 'figure'),
    Input('daySelector', 'value')
)
def update_graph(day):
    value = day
    fig = px.line(df, x = "Time of Day", y = day, title="Number of People in Store at Different Times")
    return fig

# Running it
if __name__ == "__main__":
    app.run_server(debug=True)