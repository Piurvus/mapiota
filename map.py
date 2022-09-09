import plotly.express as px
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from interface import getDataframe

app = dash.Dash(__name__)

# all the sensors (necessary to retrieve the msgs)
indexList = [
    "a279b738-bee5-4dce-aaeb-9ba4a7381439",
    "63bb641a-086e-4144-ae87-2f80122d4a72",
    "8cc7a92e-a568-4584-974a-0f9de97d64c7",
    "1adf12ae-f6da-41f0-8bcd-db59250a2643",
    "3a3517c9-a5c3-4727-a4dd-e38e2b9b77e3",
    "5d4d6c49-9969-47dd-8f95-f6eb1a412939",
]

def prepareDFs():
    """returns the dataframe and the onlyfirst dataframe consisting of only one entry per sensor"""

    #df = getDataframe(indexList)
    #df.to_csv("testing.csv")
    df = pd.read_csv("testing.csv")
    df = df.sort_values(by= "timestamp")

    # convert timestamps to dates
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # only one entry per sensor
    onlyfirst = df.groupby("sensor_id").first().reset_index()
    return onlyfirst, df


# the web app
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
                 style={'width': "30%"}
                 ),

    html.Div(id='output', children=[]),
    html.Button('Reload', id='submit', n_clicks=0),
    html.Button('Back', id='back', n_clicks=0),
    html.Br(),

    dcc.Graph(id='map', figure={})
])

# nicely named variables for the button clicks and clicks on map
click = None 
clicked = 0
clickback = 0

def generateFig(option):
    """Generates a ScatterMapbox or scatterplot for the given option"""

    # if node wasn't clicked yet
    if click == None:
        fig = px.scatter_mapbox(onlyfirst, 
                            lon = 'longitude',
                            lat = 'latitude',
                            zoom = 13,
                            color = option,
                            size = option,
                            width = 2000,
                            height = 900,
                            color_continuous_scale = 'thermal',
                            title = option
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
            trendline_options=dict(frac=0.1),
            title = option
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
        Input('submit', 'n_clicks'),
        Input('back', 'n_clicks')
    ]
)
def update_graph(select, clickData, clicks, clickb):
    """the main update function"""
    # click on the map
    global click
    if not (clickData == None):
        click = clickData

    # click the reload button -> reload the map and the data
    global clicked
    if (clicked != clicks):
        global onlyfirst, df
        onlyfirst, df = prepareDFs()
        click = None
        clicked = clicks

    # click the back button -> go back to the map
    global clickback
    if (clickback != clickb):
        click = None
        clickback = clickb

    fig = generateFig(select)

    return None, fig

if __name__ == '__main__':
    global onlyfirst, df
    onlyfirst, df = prepareDFs()
    app.run_server(debug=True)