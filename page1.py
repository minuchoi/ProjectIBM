import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime
import pandas as pd

df = pd.read_csv('deliveries.csv')

CONTENT_STYLE = {
    "margin-left": "5%",
    "margin-right": "5%",
    "padding": "2rem 1rem",
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

TEXT_STYLE = {
    'textAlign': 'right',
    'color': '#191970'
}

TEXT_STYLE_LEFT = {
    'textAlign': 'left',
    'color': '#191970'
}


def current_date(date):
    day = int(date.strftime('%d'))

    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    present_day = date.strftime(f'%A %d{suffix} %Y')

    return present_day


def date_picker(selected_date):
    date_selector = html.Div(dcc.DatePickerSingle(
        id='date-picker',
        date=selected_date,
        display_format="DD/MM/YYYY "
    ))
    return date_selector


def pie_chart(labels, values, colours, title):
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=[i for i in values],
                                 textinfo='label+percent',
                                 pull=[0, 0, 0.2, 0],
                                 marker=dict(colors=colours),
                                 title=title)])
    graph = dcc.Graph(id='pie_chart', figure=fig)

    return graph


def title(date):
    row = dbc.Row(
        [
            dbc.Col(
                ["Date Selector:", date_picker(date)], style=TEXT_STYLE_LEFT
            ),
            dbc.Col(
                html.H2(current_date(date), style=TEXT_STYLE)
            )
        ]
    )
    return row


def cards():
    row = dbc.Row([
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4(id='card_title_1', className='card-title', style=CARD_TEXT_STYLE),
                            html.P(id='card_text_1', children=['Today\'s Deliveries'], style=CARD_TEXT_STYLE),
                            dbc.Button("View", color="primary", block=True, id="deliveries-button")
                        ]
                    )
                ]
            ),
            md=3
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4(id='card_title_2', className='card-title', style=CARD_TEXT_STYLE),
                            html.P('Safe Loads.', style=CARD_TEXT_STYLE),
                            dbc.Button("View", color="primary", block=True, id='safe-button')
                        ]
                    ),
                ]

            ),
            md=3
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4(id='card_title_3', className='card-title', style=CARD_TEXT_STYLE),
                            html.P('Unlikely Loads', style=CARD_TEXT_STYLE),
                            dbc.Button("View", color="primary", block=True, id='warning-button')
                        ]
                    ),
                ]

            ),
            md=3
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4(id='card_title_4', className='card-title', style=CARD_TEXT_STYLE),
                            html.P('Loads in Danger', style=CARD_TEXT_STYLE),
                            dbc.Button("View", color="primary", block=True, id='danger-button')
                        ]
                    ),
                ]
            ),
            md=3
        )
    ])
    return row


def pie_charts(data):
    row = dbc.Row(
        [
            dbc.Col(pie_chart(['Asphalt', 'Cement'], data[5:], ['red', 'blue'], "Types of Loads"), md=6),
            dbc.Col(
                pie_chart(['Safe', 'Warning', 'Danger'], data[2:5], ['green', 'yellow', 'red'], "Load Effectiveness"),
                md=6),
        ]
    )
    return row


def bar_chart(data):
    times = data[7]

    times_list = times['Time'].tolist()

    dict_of_hours = {str(i): 0 for i in range(24)}

    for values in times_list:
        hour = values.rsplit(":")
        dict_of_hours[hour[0]] += 1

    x = [f"{hour}:00-{hour}:59" for hour in range(24)]

    y = [i for i in dict_of_hours.values()]

    fig = go.Figure(
        data=[go.Bar(
            x=x, y=y,
            textposition='auto',

        )])
    fig.update_layout(
        title='Delivery Times',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Quantity',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(
            title='Time',
            titlefont_size=16,
            tickfont_size=14,
        )

    )

    graph = dcc.Graph(id='bar_graph', figure=fig)

    row = dbc.Row(
        dbc.Col(graph, md=12)
    )

    return row


def page1_template():
    contents = html.Div(
        [
            title(datetime.today()),
            html.Hr(),
            cards(),
            html.Div(id='table-output', children="")
        ], id='page_output'
    )
    return contents


def page1_load(data):
    selected_date = data[0]
    contents = html.Div(
        [
            title(selected_date),
            html.Hr(),
            cards(),
            pie_charts(data),
            bar_chart(data),
            html.Div(id='table-output', children="")
        ]
    )
    return contents


