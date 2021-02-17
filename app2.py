#importing all the required libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import time
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dayGetter import get_day

pio.templates.default = 'plotly_dark'

# Starting the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title="Dashboard"

# Reading data from csv file
df = pd.read_csv("data/Walmart_Shawnessy/test1.csv")
df2 = pd.read_csv("data/Walmart_Shawnessy/test2.csv")

#Live Counter of most up-to-date Data
counter = 'Live People Counter'

day = get_day()[0]

app.layout = html.Div(
    children = [
        html.Div([
            html.Div(id = "title"),
            html.H1(counter)   #display counter
        ]),
        html.P("Please pick the day that you want to view data for, using drop-down menu. Stay safe!"),  #short message
        html.Title("Dashboard"),
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
                {"label": "Friday", "value": "Friday"}
            ],
            multi = True,         #enables multiple graphs to be displayed
            style = {'background-color': '#000', 'color': '#000'},
            value = day,   #default value
            placeholder = "Select a Day",
            searchable = False,
            clearable = False,
        )]),
        html.Div([
         dcc.Graph(id='ourGraph',
         )]), #output for the callback

        html.Div([
            dcc.Slider(
                id = "weekGetter",
                min = 1,
                max = 2,
                value = 1,
                marks={
                    1: {'label': 'Previous Week', 'style': {'color': '#fff'}},
                    2: {'label': 'Current Week', 'style': {'color': '#fff'}}
                }
            )
        ])
    ]
)

@app.callback(
    Output('ourGraph', 'figure'),   #output changes to figure
    Input('daySelector', 'value'),   #input that is connected to the id and value
    Input('weekGetter', 'value')
)
def update_graph(day, week):
    #value = day
    if len(day) == 0:
        day = "None"
    if week == 1:
        fig = px.line(df, x = "Time of Day", y = day, title="Number of People in Building at Different Times") # X-axis of graph is Time of Day from csv file, and the y-axis is the day(s) that are selected
    if week == 2:
        fig = px.line(df2, x = "Time of Day", y = day, title="Number of People in Different at Different Times")
    fig.update_layout(yaxis_title = "Number of People")
    fig.update_layout(legend_title="Day of Week")
    return fig

# Running it
if __name__ == "__main__":
    app.run_server(debug=True)