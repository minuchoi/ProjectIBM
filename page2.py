import urllib.request
import json
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import datetime
import pandas as pd
import dash_table as dt

token = "pk.eyJ1IjoibWludXRvciIsImEiOiJja2NvdnlwMWMwMnlyMnpsZ3JsM3BrdGs2In0.XD4skMgplLoswXjrGbbQ-g"


def get_location(postcode):
    url = 'https://api.postcodes.io/postcodes/' + str(postcode)
    with urllib.request.urlopen(url) as response:
        testing = json.load(response)
        results = [i[1] for i in testing['result'].items()]
        long = results[6]
        lat = results[7]

    return lat, long, postcode


# http://postcodes.io/

def map_locations(home, dest):
    initial_lat, initial_lon, home_postcode = get_location(home)
    final_lat, final_lon, dest_postcode = get_location(dest)
    return initial_lat, initial_lon, final_lat, final_lon, home_postcode, dest_postcode


def get_route(home, dest):
    initial_lat, initial_lon, final_lat, final_lon, home_postcode, dest_postcode = map_locations(home, dest)

    mapurl = 'https://api.mapbox.com/directions/v5/mapbox/driving-traffic/' + str(initial_lon) + ',' + str(
        initial_lat) + ';' + str(final_lon) + ',' + str(
        final_lat) + '?geometries=geojson&access_token=pk.eyJ1IjoibWludXRvciIsImEiOiJja2NvdnlwMWMwMnlyMnpsZ3JsM3BrdGs2In0.XD4skMgplLoswXjrGbbQ-g'

    lons = []
    lats = []
    destination_names = []

    with urllib.request.urlopen(mapurl) as response:
        map_js = json.load(response)
        for keys in map_js['routes']:
            for name, value in keys.items():
                if name == 'geometry':
                    for each_name, each_value in value.items():
                        if each_name == 'coordinates':
                            for eachloc in each_value:
                                lons.append(eachloc[0])
                                lats.append(eachloc[1])
            for name, value in keys.items():
                if name == "duration":
                    duration = value
        destination = map_js['waypoints']
        counter = 0
        for waypoints in destination:
            for item in waypoints.items():
                if item[0] == 'name':
                    if item[1] != "":
                        destination_names.append(item[1])
                        counter += 1
                    elif counter == 0:
                        destination_names.append(home_postcode)
                        counter += 1
                    else:
                        destination_names.append(dest_postcode)

    return lats, lons, mapurl, duration, destination_names


def plot_map(home, dest, eff):
    lats, lons, map_url, duration, destination_names = get_route(home, dest)

    colour = ""

    if eff == 'Safe':
        colour += 'green'
    elif eff == 'Warning':
        colour += 'orange'
    else:
        colour += 'red'

    eta = str(datetime.timedelta(seconds=int(duration)))

    mid_lat = (max(lats) + min(lats)) / 2
    mid_lons = (max(lons) + min(lons)) / 2

    graph = go.Figure(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='lines',
        line=dict(width=2, color=colour),
        marker=dict(
            size=5,
        ),
        text='{} to {}, ETA: {}'.format(str(destination_names[0]).title(), str(destination_names[1]).title(),
                                        str(eta).title()),
        hoverinfo='text'
    ))

    graph.update()

    graph.update_layout(mapbox_style="streets",
                        mapbox_accesstoken=token,
                        mapbox_zoom=11.5,
                        mapbox_center=dict(lat=mid_lat, lon=mid_lons))
    graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    map_display = html.Div([
        html.Div(dcc.Graph(figure=graph))
    ])
    return map_display


def page2(df):
    table = html.Div([
        html.Div(
            dt.DataTable(
                id='delivery-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                row_selectable='single',
                selected_rows=[],
                filter_action='native',
                page_size=15,
                data=df.to_dict('records'),
                sort_action='native',
                style_cell={
                    'min-width': '50px'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                css=[
                    {'selector': '.row-1', 'rule': 'min-height: 500px;'}
                ]
            ), className="six columns"),
        html.Br(),
        html.Br(),
        html.Div(id='my-output'),

    ])
    return table
