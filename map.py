import plotly.express as px
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from interface import getDataframe

app = dash.Dash(__name__)

#indexList = [
    #"5d4d6c49-9969-47dd-8f95-f6eb1a423b29",
#]

indexList = [
    "a279b738-bee5-4dce-aaeb-9ba4a7381439",
    "63bb641a-086e-4144-ae87-2f80122d4a72",
    "8cc7a92e-a568-4584-974a-0f9de97d64c7",
    "1adf12ae-f6da-41f0-8bcd-db59250a2643",
    "3a3517c9-a5c3-4727-a4dd-e38e2b9b77e3",
]

#df = getDataframe(indexList)
#df.to_csv("testing.csv")
df = pd.read_csv("testing.csv")
df = df.sort_values(by= "timestamp")

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

onlyfirst = df.groupby("sensor_id").first().reset_index()
print(onlyfirst.iloc[0]["sensor_id"])

print(onlyfirst.head(10))



app.layout = html.Div([
    html.H1("MAPIOTA", style={'text-align': 'center'}),

    dcc.Dropdown(id="select",
                 options=[
                     {"label": "temperature", "value": "temperature"},
                     {"label": "pressure", "value": "pressure"},
                     {"label": "lux", "value": "lux"},
                     {"label": "humidity", "value": "humidity"},
                     ],
                 multi=False,
                 value="temperature",
                 style={'width': "60%"}
                 ),

    html.Div(id='output', children=[]),
    html.Br(),

    dcc.Graph(id='map', figure={})
])

click = None 

def generateFig(option):
    """Generates a ScatterMapbox for the given option"""

    # if node wasn't clicked yet
    if click == None:



        fig = px.scatter_mapbox(df, 
                            lon = onlyfirst['longitude'],
                            lat = onlyfirst['latitude'],
                            zoom = 13,
                            color = onlyfirst[option],
                            size = onlyfirst['pressure'],
                            width = 1200,
                            height = 900,
                            color_continuous_scale = 'temps'
                            )

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0, "t":50, "l":0, "b":10})
    
    # if node was clicked
    else:
        id = click['points'][0]['pointNumber']
        fig = px.scatter(
            df[df["sensor_id"] == onlyfirst.iloc[id]["sensor_id"]], 
            x="timestamp", 
            y=option, 
            color='humidity',
            color_continuous_scale='blues',
            trendline="lowess",
            trendline_options=dict(frac=0.1)
            )
    
    return fig

@app.callback(
    [
        Output(component_id='output', component_property='children'),
        Output(component_id='map', component_property='figure')
    ],
    [
        Input(component_id='select', component_property='value'),
        Input('map', 'clickData'),
    ]
)
def update_graph(select, clickData):
    global click
    if not (clickData == None):
        click = clickData


    fig = generateFig(select)


    return None, fig

if __name__ == '__main__':
    app.run_server(debug=True)