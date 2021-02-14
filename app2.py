#importing all the required libraries
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

# Starting the app
app = dash.Dash(__name__)

# Reading data from csv file
df = pd.read_csv("data/test.csv")

#Live Counter of most up-to-date Data
counter = 'Live People Counter'


app.layout = html.Div(
    children = [
        html.H1(counter),   #display counter
        html.P("Please pick the day that you want to view data for, using drop-down menu. Stay safe!"),  #short message
        html.Div([
        dcc.Dropdown(
            id="daySelector",    #id that will link dropdown menu to input for callback
            options=[            #creating labels and values for the labels that are linked to the csv file
                {"label": "Saturday", "value": "Saturday"},
                {"label": "Sunday", "value": "Sunday"},
                {"label": "Monday", "value": "Monday"},
                {"label": "Tuesday", "value": "Tuesday"},
                {"label": "Wednesday", "value": "Wednesday"},
                {"label": "Thursday", "value": "Thursday"},
                {"label": "Friday", "value": "Friday"},
            ],
            multi=True,         #enables multiple graphs to be displayed
            value="Saturday",   #default value
        )]),
        html.Div([
         dcc.Graph(id='ourGraph')]) #output for the callback
    ]
)

@app.callback(
    Output('ourGraph', 'figure'),   #output changes to figure
    Input('daySelector', 'value')   #input that is connected to the id and value
)
def update_graph(day):
    value = day
    fig = px.line(df, x = "Time of Day", y =day, title="Number of People in Store at Different Times") # X-axis of graph is Time of Day from csv file, and the y-axis is the day(s) that are selected
    return fig

# Running it
if __name__ == "__main__":
    app.run_server(debug=True)