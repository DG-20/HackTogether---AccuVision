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
fig = px.line(df, x="Time of Day", y=" Sat", title="Stuff")


#Line graph object created
fig = px.line(df, x="Time of Day", y="Number of People Inside", title="Number of People Inside a Store at Different Times of Day" )
app.layout = html.Div(children =
    [
        #Random HTML
        html.H1("HI"),
        html.P("asdfasdf"),
        html.A("HIHIHI", href="https://dash.plotly.com/dash-html-components/a"), 
        #The actual graph to display
        dcc.Graph(
            figure = fig
        )
    ])

#Running it
if __name__ == '__main__':
    app.run_server(debug=True)

#Creating figure

fig = go.Figure()
#Adding surface trace
fig.add_trace(go.Surface(z= df.values.tolist(), colorscale = "tealgrn"))

#Update plot sizing

fig.update_layout(
    width = 800,
    height = 800,
    autosize = False,
    margin=dict(t=0, b=0, l=0, r=0),
    template = "gridon",
)

#Adding dropdown menu

fig.update_layout(
    updatemenus = [
        dict(
            buttons = list([
                dict(
                    args = ["type", ]
                )

                )
            ])
        )