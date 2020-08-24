import dash_html_components as html
import dash_bootstrap_components as dbc

# the styles for the main content position it to the right of the sidebar and
# add some padding.

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

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