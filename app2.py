# importing all the required libraries
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
app.title = "AccuVision"
bestTime = ""
bestDay = ""
currentCount = ""

# Reading data from csv file
WalShaw_Current = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1F-fvele1EorJJ6Vdm8T5gG3lOP_hapmwyIoXEZIeZ6A/export?gid=496819679&format=csv", index_col=None)
WalShaw_Previous = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1ii_78RxFOF98gipDtC_31VMzUhAfYvOd69R1a3f098A/export?gid=688427654&format=csv",  index_col=None)
CostcoHeritage_Current = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1Fh37SZr6vFYi-1GGrdAsSrYB8Vv1VGhKWJUeyp981zA/export?gid=1224033525&format=csv", index_col=None)
CostcoHeritage_Previous = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1dB_NgzL0c5qBn1A3y2rPkRcBDTfSYofg6F0BuZ8eFsk/export?gid=583703077&format=csv", index_col=None)
YMCAShaw_Previous = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1agLC1TUQz2N_9vle5FXpVZ5lAieVDgidTVmqKw4JbZk/export?gid=1278973156&format=csv", index_col=None)
YMCAShaw_Current = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1SQOCXvnZUW74ES4R-37HorE3A2_-hnrxnvjq_A1fLK4/export?gid=1144356892&format=csv", index_col=None)

# Live Counter of most up-to-date Data

day = get_day()[0]

app.layout = html.Div(
    children=[
        html.Div([
            html.Div(id="title"),
            html.Img(src="assets/Accuvision_Logo_v3.png",
                     height="70", width="220.925"),  # display counter
            html.H1("AccuVision")

        ]),
        # short message
        html.P(
            "Please pick the day that you want to view data for, using drop-down menu. Stay safe!"),
        html.Title("Dashboard"),
        html.H4('   In these times of uncertainty during the COVID-19 pandemic, the necessity for limiting public contact is greater than ever. In order to assist you with doing so, AccuVision provides real-time data about the number of people within an establishment at any given point over the course of the current and past week. We hope AccuVision helps you stay safe in these unprecedented times.', title='Introduction to AccuVision',
                className='text_area'),
        html.Div(children=[
            html.Div([
                dcc.Dropdown(
                    id="buildingSelector",
                    options=[
                        {"label": "Costco Heritage", "value": "Costco_Heritage"},
                        {"label": "Walmart Shawnessy",
                            "value": "Walmart_Shawnessy"},
                        {"label": "YMCA Shawnessy", "value": "YMCA_Shawnessy"}
                    ],
                    placeholder="Select a Building",
                    clearable=False,
                    className='dropdown',
                    searchable=False,
                ),

                dcc.Dropdown(
                    id="daySelector",  # id that will link dropdown menu to input for callback
                    options=[  # creating labels and values for the labels that are linked to the csv file
                        {"label": "Saturday", "value": "Saturday"},
                        {"label": "Sunday", "value": "Sunday"},
                        {"label": "Monday", "value": "Monday"},
                        {"label": "Tuesday", "value": "Tuesday"},
                        {"label": "Wednesday", "value": "Wednesday"},
                        {"label": "Thursday", "value": "Thursday"},
                        {"label": "Friday", "value": "Friday"}
                    ],
                    multi=True,  # enables multiple graphs to be displayed
                    value=day,  # default value
                    placeholder="Select a Day",
                    searchable=False,
                    clearable=True,
                    className='dropdown',
                ),

                dcc.Slider(id="weekGetter",
                           min=1,
                           max=2,
                           value=1,
                           marks={
                               1: {'label': 'Previous Week', 'style': {'color': '#fff'}},
                               2: {'label': 'Current Week', 'style': {'color': '#fff'}},
                           },
                           className='slider',
                           )
            ], className="left_side"),

            html.Div([
                dcc.Graph(id='ourGraph',
                          ),  # output for the callback
            ], className="right_side"),
        ], className="side_by_side"),
        html.Div([
            html.P(id="generalInfo", children=True)
        ])
    ],
    id="mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(
    Output('ourGraph', 'figure'),  # output changes to figure
    # input that is connected to the id and value
    Input('daySelector', 'value'),
    Input('weekGetter', 'value'),
    Input('buildingSelector', 'value')
)
def update_graph(day, week, building):
    sheetToReadFrom_Previous = WalShaw_Previous
    sheetToReadFrom_Current = WalShaw_Current
    if building == "Costco_Heritage":
        sheetToReadFrom_Previous = CostcoHeritage_Previous
        sheetToReadFrom_Current = CostcoHeritage_Current
    elif building == "YMCA_Shawnessy":
        sheetToReadFrom_Previous = YMCAShaw_Previous
        sheetToReadFrom_Current = YMCAShaw_Current

    if len(day) == 0:
        day = "None"
    if week == 1:
        # X-axis of graph is Time of Day from csv file, and the y-axis is the day(s) that are selected
        fig = px.line(sheetToReadFrom_Previous, x="Time of Day", y=day,
                      title="Number of People in Building at Different Times")
    if week == 2:
        fig = px.line(sheetToReadFrom_Current, x="Time of Day", y=day,
                      title="Number of People in Building at Different Times")
    fig.update_layout(yaxis_title="Number of People")
    fig.update_layout(legend_title="Day of Week")
    return fig


@app.callback(
    Output('generalInfo', 'children'),
    Input('daySelector', 'value'),
    Input('buildingSelector', 'value')
)
def update_info(day, building):
    oneDay = True
    if len(day) != 1:
        oneDay = False
    if isinstance(day, str) == True:
        oneDay = True
    if oneDay == False:
        return "Select a day to display general information about it."
    else:
        leastpeople = besDay(day, building)
        return f"The best day to go is:, with {leastpeople} people"


def besDay(day, building):
    sheetToReadFrom_Previous = WalShaw_Previous
    if building == "Costco_Heritage":
        sheetToReadFrom_Previous = CostcoHeritage_Previous
    elif building == "YMCA_Shawnessy":
        sheetToReadFrom_Previous = YMCAShaw_Previous
    prevmon = sheetToReadFrom_Previous['Monday'].sum()
    prevtue = sheetToReadFrom_Previous['Tuesday'].sum()
    prevwed = sheetToReadFrom_Previous['Wednesday'].sum()
    prevthu = sheetToReadFrom_Previous['Thursday'].sum()
    prevfri = sheetToReadFrom_Previous['Friday'].sum()
    prevsat = sheetToReadFrom_Previous['Saturday'].sum()
    prevsun = sheetToReadFrom_Previous['Sunday'].sum()
    bigday = (prevmon, prevtue, prevwed, prevthu, prevfri, prevsat, prevsun)
    dayIndex = bigday.index(min(bigday))
    return dayIndex


# Running it
if __name__ == "__main__":
    app.run_server(debug=True)
