import csv
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
        id='date-picker-single',
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
            dbc.Col(pie_chart(['Tarmac', 'Cement'], data[5:], ['red', 'blue'], "Types of Loads"), md=6),
            dbc.Col(
                pie_chart(['Safe', 'Warning', 'Danger'], data[2:5], ['green', 'yellow', 'red'], "Load Effectiveness"),
                md=6),
        ]
    )
    return row


def bar_chart(data):
    times = data[7]

    times_list = times['Time'].tolist()

    dict_of_hours = {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0,
        "13": 0,
        "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0
    }

    for values in times_list:
        hour = values.rsplit(":")
        dict_of_hours[hour[0]] += 1

    x = ['0:00-0:59', '1:00-1:59', '2:00-2:59', '3:00-3:59', '4:00-4:59', '5:00-5:59', '6:00-6:59', '7:00-7:59', '8:00-8:59', '9:00-9:59', '10:00-10:59', '11:00-11:59', '12:00-12:59', '13:00-13:59', '14:00-14:59', '15:00-15:59', '16:00-16:59', '17:00-17:59', '18:00-18:59', '19:00-19:59', '20:00-20:59', '21:00-21:59', '22:00-22:59', '23:00-23:59']

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


def page1():
    testing = datetime.today()
    contents = html.Div(
        [
            title(testing),
            html.Hr(),
            cards()
        ], id='page_output'
    )
    return contents


def page1_testing(data):
    selected_date = data[0]
    contents = html.Div(
        [
            title(selected_date),
            html.Hr(),
            cards(),
            pie_charts(data),
            bar_chart(data)
        ],
        style=CONTENT_STYLE
    )
    return contents
