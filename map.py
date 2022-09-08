import plotly.express as px
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from interface import getDataframe

app = dash.Dash(__name__)

indexList = [
    "5d4d6c49-9969-47dd-8f95-f6eb1a423b29",
]


#df = getDataframe(indexList)
df = pd.read_csv("testing.csv")

print(df.head(10))



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
    if click == None:
        fig = px.scatter_mapbox(df, 
                            lon = df['longitude'],
                            lat = df['latitude'],
                            zoom = 10,
                            color = df[option],
                            size = df['altitude'],
                            width = 1200,
                            height = 900,
                            )

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0, "t":50, "l":0, "b":10})
    else:
        print(click)
        fig = px.scatter(df, x="temperature", y="pressure", color='humidity')


    
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