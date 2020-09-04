import dash
import dash_auth
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
from page1 import page1, page1_testing
from page2 import delivery_table, plot_map
from sidebar import *
import re
from datetime import datetime


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

df = pd.read_csv('deliveries.csv')

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 3)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/page-{i}" for i in range(1, 3)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page1()
    elif pathname == "/page-2":
        return delivery_table(df)

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
     Output(component_id='card_title_4', component_property='children'),
     Output('container-button-timestamp', 'children')],
    [Input(component_id='date-picker-single', component_property='date'),
     Input('deliveries-button', 'n_clicks'),
     Input('safe-button', 'n_clicks'),
     Input('warning-button', 'n_clicks'),
     Input('danger-button', 'n_clicks')]
)
def date_input(date, btn1, btn2, btn3, btn4):
    date = datetime.strptime(re.split('T| ', date)[0], '%Y-%m-%d')
    date_string = date.strftime('%Y-%m-%d')

    chosen_date = df.Date == date_string

    safe_loads = df.Effectiveness == "Safe"
    warning_loads = df.Effectiveness == "Warning"
    danger_loads = df.Effectiveness == "Danger"

    cement = df.LoadType == "Cement"
    tarmac = df.LoadType == "Asphalt"

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

    values = [date, deliveries_today, number_of_safe, number_of_warning, number_of_danger, number_of_tarmac,
              number_of_cement, times]

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'deliveries-button' in changed_id:
        msg = delivery_table(df[chosen_date])
    elif 'safe-button' in changed_id:
        msg = delivery_table(df[filter1])
    elif 'warning-button' in changed_id:
        msg = delivery_table(df[filter2])
    elif 'danger-button' in changed_id:
        msg = delivery_table(df[filter3])
    else:
        msg = ''

    return page1_testing(values), f"{deliveries_today}", f"{number_of_safe}", f"{number_of_warning}", f"{number_of_danger}", html.Div(msg)


@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input('delivery-table', 'selected_rows'),
     Input('delivery-table', 'data')]
)
def plot_selected_map(input_value, data):
    if not input_value:
        pass
    else:
        filtered_df = pd.DataFrame(data)
        starting_location = filtered_df.iloc[input_value, 5].values
        destination = filtered_df.iloc[input_value, 6].values
        effectiveness = filtered_df.iloc[input_value, 7].values
        return plot_map(starting_location[0], destination[0], effectiveness)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=80, debug=True)
