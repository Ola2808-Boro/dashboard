import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, use_pages=True)
server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "display": "flex",
    "flex-direction": "column",
}

sidebar = html.Div(
    [
        html.H2("Analysis", style={"font-size": "30px"}),
        html.Hr(),
        # html.P("A simple sidebar layout with navigation links", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink(
                    "Cluster analysis",
                    href="/",
                    active=True,
                    style={
                        "text-decoration": "none",
                        "color": "black",
                        "font-weight": "bold",
                        "font-size": "20px",
                    },
                ),
                dbc.NavLink(
                    "Outliers",
                    href="/outliers",
                    style={
                        "text-decoration": "none",
                        "color": "black",
                        "font-weight": "bold",
                        "font-size": "20px",
                    },
                ),
                dbc.NavLink(
                    "The warmest/coldest days",
                    href="/15_days",
                    style={
                        "text-decoration": "none",
                        "color": "black",
                        "font-weight": "bold",
                        "font-size": "20px",
                    },
                ),
            ],
            vertical="md",
            pills=True,
            style={
                "display": "flex",
                "flex-direction": "column",
                "height": "20%",
                "justify-content": "space-around",
                "text-decoration": "none",
            },
        ),
    ],
    style=SIDEBAR_STYLE,
)


app.layout = html.Div([dcc.Location(id="url"), sidebar, dash.page_container])


if __name__ == "__main__":
    app.run_server()
