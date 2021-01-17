import dash 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.line(df, x="Fruit", y="Amount", title="Stuff")

app.layout = html.Div(children =
    [
        html.H1("HI"),
        html.P("asdfasdf"),
        html.A("HIHIHI", href="https://dash.plotly.com/dash-html-components/a"), 
        dcc.Graph(
            figure = fig
        )
        
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

