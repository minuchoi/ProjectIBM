import dash
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
from page1 import page1, page1_testing
from page2 import page2
import csv
import re
from datetime import datetime

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("Cement", className="display-4"),
        html.Hr(),
        html.P(
            "Welcome to the Dashboard!", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/page-1", id="page-1-link"),
                dbc.NavLink("Table", href="/page-2", id="page-2-link"),
                dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page1()
    elif pathname == "/page-2":
        return page2(df=pd.read_csv('deliveries.csv'))
    elif pathname == "/page-3":
        return "Page 3"
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    [Output(component_id='page_output', component_property='children'),
     Output(component_id='card_title_1', component_property='children'),
     Output(component_id='card_title_2', component_property='children'),
     Output(component_id='card_title_3', component_property='children'),
     Output(component_id='card_title_4', component_property='children'),],
    [Input(component_id='date-picker-single', component_property='date')]
)
def testing_date(date):
    df = pd.read_csv('deliveries.csv')

    date = datetime.strptime(re.split('T| ', date)[0], '%Y-%m-%d')
    date_string = date.strftime('%Y-%m-%d')

    chosen_date = df.Date == date_string

    safe_loads = df.Effectiveness == "Safe"
    warning_loads = df.Effectiveness == "Warning"
    danger_loads = df.Effectiveness == "Danger"

    cement = df.LoadType == "Cement"
    tarmac = df.LoadType == "Tarmac"

    filter1 = chosen_date & safe_loads
    filter2 = chosen_date & warning_loads
    filter3 = chosen_date & danger_loads
    filter4 = chosen_date & cement
    filter5 = chosen_date & tarmac

    deliveries_today = len(df[chosen_date].index)
    number_of_safe = len(df[filter1].index)
    number_of_warning = len(df[filter2].index)
    number_of_danger = len(df[filter3].index)
    number_of_cement = len(df[filter4].index)
    number_of_tarmac = len(df[filter5].index)
    times = df[chosen_date]

    values = [date, deliveries_today, number_of_safe, number_of_warning, number_of_danger, number_of_tarmac, number_of_cement, times]

    return page1_testing(values), f"{deliveries_today}", f"{number_of_safe}", f"{number_of_warning}", f"{number_of_danger}"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8888, debug=True)
