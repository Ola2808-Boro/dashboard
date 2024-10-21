import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/15_days")

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "display": "flex",
    "flex-direction": "column",
}

DROPDOWNS_DIV_STYLE = {
    "display": "flex",
    "flex-direction": "row",
    "width": "100%",
    "height": "20%",
    "justify-content": "space-between",
}


BASIC_PATH = "C:/Users/BorowsAl/Desktop/dash app/data/cluster_data_test"


def read_data(case, num):
    temp_path = f"{BASIC_PATH}/{case.replace(' ','_').lower()}.csv"
    print(temp_path)
    df = pd.read_csv(temp_path)
    if "lowest" in case:
        df = df.tail(num)
    else:
        df = df.head(num)
    return df


def build_dropdown(case, num):
    return [
        dcc.Dropdown(
            options=["The lowest temp", "The hightest temp"],
            value=case,
            id="dropdown_case",
            style={"width": "100%", "margin-right": "20px"},
        ),
        dcc.Dropdown(
            options=[i + 1 for i in range(15)],
            value=num,
            id="dropdown_num",
            style={"width": "100%"},
        ),
    ]


@callback(
    Output("figures", "children"),
    [Input("dropdown_case", "value"), Input("dropdown_num", "value")],
)
def draw_graphs(case, num):
    print(f"Read {case} {num}")
    df = read_data(case, num)
    figures = []
    for idx, (_, item) in enumerate(df.iterrows()):
        item.drop("Total", inplace=True)
        fig = px.line(item, title=f"{case}: {idx+1}")
        figures.append(dcc.Graph(figure=fig, id=f"{case}_{idx}"))

    return html.Div(children=figures, id="figures")


def build_cluster_section(case, num):
    print(f"Case {case} num {num}")
    section = [
        html.Div(
            id="cluster_dropdowns",
            children=[
                build_dropdown(case, num)[0],
                build_dropdown(case, num)[1],
            ],
            style=DROPDOWNS_DIV_STYLE,
        ),
        draw_graphs(case, num),
    ]
    return section


def layout(velocity=None, **other_unknown_query_strings):
    return html.Div(
        children=[
            html.H1("The lowest/hightest temp analysis"),
            html.Div(
                children=[
                    html.Div(
                        id="cluster_div",
                        children=build_cluster_section(case="The hightest temp", num=5),
                    ),
                ],
            ),
        ],
        style=CONTENT_STYLE,
    )
