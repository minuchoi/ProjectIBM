import pandas as pd
import dash_html_components as html
import dash_table as dt


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
        html.Div(id='my-output'),

    ])
    return table
