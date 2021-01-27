import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Started the app
app = dash.Dash(__name__)


# Reading data
df = pd.read_csv("data/test.csv")

# Line graph object created
fig = px.line(df, x="Time of Day", y=" Sat", title="Stuff")


app.layout = html.Div(
    children=[
        # Random HTML
        html.H1("HI"),
        html.P("asdfasdf"),
        html.A("HIHIHI", href="https://dash.plotly.com/dash-html-components/a"),


        dcc.Dropdown(
            id = "first-dropdown",
            options=[
                {"label": "Saturday", "value": "Sat"},
                {"label": "Sunday", "value": "Sun"},
                {"label": "Monday", "value": "Mon"},
                {"label": "Tuesday", "value": "Tues"},
                {"label": "Wednsay", "value": "Wed"},
                {"label": "Thursday", "value": "Thur"},
                {"label": "Friday", "value": "Fri"},
            ],
            value="Sat",
        ),

        # The actual graph to display
        dcc.Graph(figure=fig),
        html.Div(id='test')
    ]
)
@app.callback(
    Output(component_id='test', component_property='children'),
    Input(component_id='first-dropdown', component_property='value')

)
def update_output_div(input_value):
    return 'output {}'.format(input_value)


# Running it
if (__name__ == "__main__"):
    app.run_server(debug=True)

# Creating figure
