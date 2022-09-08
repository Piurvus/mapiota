import plotly.express as px
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = px.data.carshare()



app.layout = html.Div([
    html.H1("TITLE", style={'text-align': 'center'}),

    dcc.Dropdown(id="select",
                 options=[
                     {"label": "temperature", "value": 0},
                     {"label": "pressure", "value": 1},
                     ],
                 multi=False,
                 value=0,
                 style={'width': "60%"}
                 ),

    html.Div(id='output', children=[]),
    html.Br(),

    dcc.Graph(id='map', figure={})
])
@app.callback(
    [Output(component_id='output', component_property='children'),
     Output(component_id='map', component_property='figure')],
    [Input(component_id='select', component_property='value'), Input('map', 'clickData')]
)
def update_graph(option_slctd, clickData):
    
    # initiate sending data
    print(clickData)

    fig = px.scatter_mapbox(df, 
                        lon = df['centroid_lon'],
                        lat = df['centroid_lat'],
                        zoom = 10,
                        color = df['peak_hour'],
                        size = df['car_hours'],
                        width = 1200,
                        height = 900,
                        title = "blub")

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0, "t":50, "l":0, "b":10})

    return None, fig

if __name__ == '__main__':
    app.run_server(debug=True)