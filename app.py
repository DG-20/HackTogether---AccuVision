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

currentDate = date.today()
year = currentDate.year
month = currentDate.month
dayNumber = currentDate.day

def dayGet(day, month, year):
    daysINWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    #dayIndex is an object of datetime
    dayInd = datetime.date(year, month, day)
    # .weekday is a method of this object (returns a number)
    dayofweek = daysINWeek[dayInd.weekday()]
    return (dayofweek)

day = dayGet(dayNumber, month, year)

# Started the app
app = dash.Dash(__name__)


# Reading data
df = pd.read_csv("data/mon.csv")
df2 = pd.read_csv("data/tues.csv")

app.layout = html.Div(
    children=[
        # Random HTML
        html.H1("HI"),
        html.P("asdfasdf"),
        html.A("HIHIHI", href="https://dash.plotly.com/dash-html-components/a"),
        dcc.Dropdown(
            id="first-dropdown",
            options=[
                {"label": "Saturday", "value": "Sat"},
                {"label": "Sunday", "value": "Sun"},
                {"label": "Monday", "value": "Mon"},
                {"label": "Tuesday", "value": "Tues"},
                {"label": "Wednesay", "value": "Wed"},
                {"label": "Thursday", "value": "Thur"},
                {"label": "Friday", "value": "Fri"},
            ],
            multi=True,
            value="Sat",
        ),
        updatemenus=list([
    dict(
        buttons=list([
            dict(
                args=['type', 'surface'],
                label='3D Surface',
                method='restyle'
            ),
            dict(
                args=['type', 'heatmap'],
                label='Heatmap',
                method='restyle'
            )
        ]),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.1,
        xanchor = 'left',
        y = 1.1,
        yanchor = 'top'
    ),
])
layout['updatemenus'] = updatemenus
        html.H1(),
        html.Button("Saturday", id="btn-1", n_clicks=0),
        html.Button("Sunday", id="btn-2", n_clicks=0),
        html.Button("Monday", id="btn-3", n_clicks=0),
        html.Button("Tuesday", id="btn-4", n_clicks=0),
        html.Button("Wednesay", id="btn-5", n_clicks=0),
        html.Button("Thursday", id="btn-6", n_clicks=0),
        html.Button("Friday", id="btn-7", n_clicks=0),
        html.Div(id="button"),
        dcc.Markdown(
            """
                We can enter text here

                also insert hyperlinks to other [Websites](http://commonmark.org/help).

                Markdown is a simple way to write and format text.
                It includes a syntax for things like **bold text** and *italics*,
                [links](http://commonmark.org/help), inline `code` snippets, lists,
                quotes, and more.
                """
        ),
        dcc.DatePickerSingle(
            id="date-picker",
            date=date(year, month, dayNumber),
            # value = day,
        ),
        # The actual graph to display
        dcc.Graph(figure=px.line(df, x="Time of Day", y = "value", title="Stuff")),
        dcc.Graph(figure=px.line(df2, x="Time of Day", y = "value", title="Stuff2")),
        html.Div(id="test"),
    ]
)


@app.callback(
    Output("button", "children"),
    Input("btn-1", "n_clicks"),
    Input("btn-2", "n_clicks"),
    Input("btn-3", "n_clicks"),
    Input("btn-4", "n_clicks"),
    Input("btn-5", "n_clicks"),
    Input("btn-6", "n_clicks"),
    Input("btn-7", "n_clicks"),
)
def ifClicked(btn1, btn2, btn3, btn4, btn5, btn6, btn7):
    change_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "btn-1" in change_id:
        fig2 = px.line(df, x = "Time of Day", y = "Saturday", title = "Stuff")
    elif "btn-2" in change_id:
        message = "Button 2 was pressed"
    elif "btn-3" in change_id:
        message = "Button 3 was pressed"
    elif "btn-4" in change_id:
        message = "Button 4 was pressed"
    elif "btn-5" in change_id:
        message = "Button 5 was pressed"
    elif "btn-6" in change_id:
        message = "Button 6 was pressed"
    elif "btn-7" in change_id:
        message = "Button 7 was pressed"
    else:
        message = "Nothing was pressed"
    return html.Div(fig2)


@app.callback(
    Output(component_id="test", component_property="children"),
    Input(component_id="first-dropdown", component_property="value"),
)
def update_output_div(input_value):
    return "output {}".format(input_value)


# Running it
if __name__ == "__main__":
    app.run_server(debug=True)

# Creating figure
