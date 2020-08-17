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


def load_type_pie():
    file = open('deliveries.csv')

    csv_file = csv.reader(file)

    labels = ['Tarmac', 'Cement']
    tarmac_no = 0
    cement_no = 0

    for value in csv_file:
        if value[2] == 'Tarmac':
            tarmac_no += 1
        elif value[2] == 'Cement':
            cement_no += 1
        else:
            pass

    values = [tarmac_no, cement_no]

    colours = ['red', 'blue']

    return pie_chart(labels, values, colours, "Types of Loads")


def load_effectiveness_pie():
    file = open('deliveries.csv')

    csv_file = csv.reader(file)

    labels = ['Danger', 'Warning', 'Safe']
    safe_no = 0
    warning_no = 0
    danger_no = 0

    for value in csv_file:
        if value[6] == 'Safe':
            safe_no += 1
        elif value[6] == 'Warning':
            warning_no += 1
        elif value[6] == 'Danger':
            danger_no += 1
        else:
            pass

    colours = ['red', 'yellow', 'green']

    values = [danger_no, warning_no, safe_no]

    return pie_chart(labels, values, colours, "Load Effectiveness")


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
                            html.H4(id='card_title_1', children=['Card Title 1'], className='card-title',
                                    style=CARD_TEXT_STYLE),
                            html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
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
                            html.H4('Card Title 2', className='card-title', style=CARD_TEXT_STYLE),
                            html.P('Sample text.', style=CARD_TEXT_STYLE),
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
                            html.H4('Card Title 3', className='card-title', style=CARD_TEXT_STYLE),
                            html.P('Sample text.', style=CARD_TEXT_STYLE),
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
                            html.H4('Card Title 4', className='card-title', style=CARD_TEXT_STYLE),
                            html.P('Sample text.', style=CARD_TEXT_STYLE),
                        ]
                    ),
                ]
            ),
            md=3
        )
    ])
    return row


def graphs_testing():
    row = dbc.Row(
        [
            dbc.Col(load_type_pie(), md=6),
            dbc.Col(load_effectiveness_pie(), md=6)
        ]
    )
    return row


def page1():
    testing = datetime.today()
    contents = html.Div(
        [
            title(testing),
            html.Hr(),
            cards(),
            graphs_testing(),
            html.Div(id='testing_output', children=f'{testing}'),
        ], id='page_output',
        style=CONTENT_STYLE
    )
    return contents


def page1_testing(selected_date):
    contents = html.Div(
        [
            title(selected_date),
            html.Hr(),
            cards(),
            graphs_testing(),
            html.Div(id='testing_output2', children=f'{selected_date}'),
        ], id='page_output2',
        style=CONTENT_STYLE
    )
    return contents
