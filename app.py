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

# Setting the template for the graph to a pre-defined plotly theme.
pio.templates.default = 'plotly_dark'

# Starting the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Title for the website.
app.title = "AccuVision"

bestTime = ""
bestDay = ""
currentCount = ""

# Reading data from Google Sheets using Pandas through URLs as CSV files and storing as data frames.
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
week1 = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1hgcC3dLOoQFVB5-EbkkKNQlFo5GQrcCFzzOsmUSUSWY/export?format=csv", index_col=None)

# Approximate areas of buildings obtained through Google Maps measuring app.
WalShaw_Area = 14519
CostcoHeritage_Area = 13576
YMCAShaw_Area = 6028

# Using dayGetter.py to obtain the day of the week.
day = get_day()[0]

# This is where the HTML5 is incorporated through the .layout backbone of plotly.
app.layout = html.Div(
    children=[
        html.Div([
            # Logo and title.
            html.Div(id="title"),
            html.Img(src="assets/Accuvision_Logo_v3.png",
                     height="70", width="220.925"),
            html.H1("AccuVision")

        ]),
        #Introductory message.
        html.H4("""     In these times of uncertainty during the COVID-19 pandemic, the necessity for limiting public contact is greater than ever. 
                    In order to assist you with doing so, AccuVision provides real-time data about the number of people within an establishment at 
                    any given point over the course of the current and past week. We hope AccuVision helps you stay safe in these unprecedented times.""",
                    title='Introduction to AccuVision',
                className='text_area'),

        html.Div(children=[
            html.Div([

                # Dropdown to select from the establishment that user would like to view data for.
                dcc.Dropdown(
                    id="buildingSelector",
                    options=[
                        {"label": "Costco Heritage", "value": "Costco-Heritage"},
                        {"label": "Walmart Shawnessy",
                            "value": "Walmart-Shawnessy"},
                        {"label": "YMCA Shawnessy", "value": "YMCA-Shawnessy"}
                    ],
                    placeholder="Select a Building",
                    clearable=False,
                    className='dropdown',
                    searchable=False,
                    # Default selected establishment in this code is YMCA-Shawnessy (customizable).
                    value = "YMCA-Shawnessy"
                ),

                # Dropdown to select the day of the week as another required filter.
                dcc.Dropdown(
                    # id that will link dropdown menu to input for callbacks.
                    id="daySelector",  
                    # Creating labels and values for the labels that are linked to the csv file.
                    options=[  
                        {"label": "Saturday", "value": "Saturday"},
                        {"label": "Sunday", "value": "Sunday"},
                        {"label": "Monday", "value": "Monday"},
                        {"label": "Tuesday", "value": "Tuesday"},
                        {"label": "Wednesday", "value": "Wednesday"},
                        {"label": "Thursday", "value": "Thursday"},
                        {"label": "Friday", "value": "Friday"}
                    ],
                    # Enables multiple graphs to be displayed and overlayed for better comparison.
                    multi=True,
                    # Default value is set to the current day of the week.
                    value=day,  
                    placeholder="Select a Day",
                    searchable=False,
                    clearable=True,
                    className='dropdown',
                ),

                # Slider for selecting which week's information is to be viewed. For demo purposes, both weeks are pre-filled,
                # however upon deployment, the weekly information will be filled as time progresses.
                dcc.Slider(id="weekGetter",
                           min=1,
                           max=2,
                           # Default value is set to display previous week information.
                           value=1,
                           marks={
                               1: {'label': 'Previous Week', 'style': {'color': '#fff'}},
                               2: {'label': 'Current Week', 'style': {'color': '#fff'}},
                           },
                           className='slider',
                           )
            ], className="left_side"),

            # Div element for the graph. The id is used as output in the callback according to the filters selected.
            html.Div([
                dcc.Graph(id='ourGraph'),  
            ], className="right_side"),
        ], className="side_by_side"),

        # The div element which contains the general information displayed based on the filters selected
        html.Div(children = [
        html.Div([
            html.P(id="generalInfo", children=True),
        ], className = 'left_side2'),
        html.Div([
            html.Div([
            html.H5('From:', title='Range (From)', className='from'),
            html.H5('To:', title='Range (To)', className='to'),
            ], className = 'FromToTitle'),
            dcc.RangeSlider(
            min = 6,
            max = 23,
            value=[6, 23],
            marks={
                6: {'label': '6:00',},
                7: {'label': '7:00',},
                8: {'label': '8:00',},
                9: {'label': '9:00',},
                10: {'label': '10:00',},
                11: {'label': '11:00',},
                12: {'label': '12:00',},
                13: {'label': '13:00',},
                14: {'label': '14:00',},
                15: {'label': '15:00',},
                16: {'label': '16:00',},
                17: {'label': '17:00',},
                18: {'label': '18:00',},
                19: {'label': '19:00',},
                20: {'label': '20:00',},
                21: {'label': '21:00',},
                22: {'label': '22:00',},
                23: {'label': '23:00',},
                },
            ),
            html.H4('Enter a range Above in the slider using a 24-hour clock time to find the best day to go', className = 'rangeText'),
        ], className = "right_side2"),
        ], className = 'side_by_side2'),

    ],
    # Added styling to be able to display side by side for a better user experience.
    id="mainContainer", style={"display": "flex", "flex-direction": "column"})

# First callback. This is to display the graph based on the inputs selected.
@app.callback(
    Output('ourGraph', 'figure'),  
    Input('daySelector', 'value'),
    Input('weekGetter', 'value'),
    Input('buildingSelector', 'value')
)
def update_graph(day, week, building):
    # Changing the CSV based on the building selected.
    sheetToReadFrom_Previous = WalShaw_Previous
    sheetToReadFrom_Current = WalShaw_Current
    if building == "Costco-Heritage":
        sheetToReadFrom_Previous = CostcoHeritage_Previous
        sheetToReadFrom_Current = CostcoHeritage_Current
    elif building == "YMCA-Shawnessy":
        sheetToReadFrom_Previous = YMCAShaw_Previous
        sheetToReadFrom_Current = YMCAShaw_Current

    # If nothing is selected, don't display anything.
    if len(day) == 0:
        day = "None"

    # X-axis of graph is Time of Day from csv file, and the y-axis is the day(s) that are selected.
    if week == 1:
        fig = px.line(sheetToReadFrom_Previous, x="Time of Day", y=day,
                      title="Number of People in Building at Different Times")
    if week == 2:
        fig = px.line(sheetToReadFrom_Current, x="Time of Day", y=day,
                      title="Number of People in Building at Different Times")

    # Updating y-axis title and the legend title.
    fig.update_layout(yaxis_title="Number of People")
    fig.update_layout(legend_title="Day of Week")
    return fig

    # Second callback to the paragraph tag where the output is dependent of the filters chosen by the user.
@app.callback(
    Output('generalInfo', 'children'),
    Input('daySelector', 'value'),
    Input('buildingSelector', 'value')
)
def update_info(day, building):
    daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    buildingArea = WalShaw_Area
    #Determining which Google Sheets to read from based on the input of the building
    #With Walmart-Shawnessy as the current default.
    sheetToReadFrom_Previous = YMCAShaw_Previous                  #WalShaw_Previous
    if building == "Costco-Heritage":
        sheetToReadFrom_Previous = CostcoHeritage_Previous
        buildingArea = CostcoHeritage_Area
    elif building == "YMCA-Shawnessy":
        sheetToReadFrom_Previous = YMCAShaw_Previous
        buildingArea = YMCAShaw_Area
    oneDay = True
    if len(day) != 1:
        oneDay = False
    if isinstance(day, str) == True:
        oneDay = True
    if oneDay == False:
        return "Select a day to display general information about it."
    else:
        #This returns a string which provides the user the day in the previous week which contained the least number of people in total.
        indexOfSuggestedDay = dayWithLeast(day, building, sheetToReadFrom_Previous)
        liveCounter = displayLiveCounter(day, building, sheetToReadFrom_Previous)
        return f"""
        According to last week's data, the day with the least number of visitors in {building} was: {daysOfWeek[indexOfSuggestedDay]}.
            \nThis is {displayLiveCounter(day, building, sheetToReadFrom_Previous)}. The live visitor per building area for {building}
            is: {buildingArea/liveCounter:.0f} m²/people."""


def dayWithLeast(day, building, sheetToReadFrom_Previous):
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

def displayLiveCounter(day, building, sheetToReadFrom_Previous):
    #Finding the total number of lines so as to read the most recent counter value
    lastLine = len(sheetToReadFrom_Previous)

    #Based on the day, get the column number to read from a specific cell
    if day == "Monday":
        dayIndex = 1
    elif day == "Tuesday":
        dayIndex = 2
    elif day == "Wednesday":
        dayIndex = 3
    elif day == "Thursday":
        dayIndex = 4
    elif day == "Friday":
        dayIndex = 5
    elif day == "Saturday":
        dayIndex = 6
    elif day == "Sunday":
        dayIndex = 7
    else:
        dayIndex = 8
    #Returning the most recent counter value
    return sheetToReadFrom_Previous.iloc[1046 - 1, dayIndex]


# Running it
if __name__ == "__main__":
    app.run_server(debug=True)
