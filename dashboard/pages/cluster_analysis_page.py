import dash
import os
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path="/")

BASIC_PATH = "data/cluster_analysis"
cluster_analysis_names = os.listdir(f"{BASIC_PATH}")

print(f"cluster_analysis_names { cluster_analysis_names}")
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


def read_data(cluster_num, params):
    path = f"data/cluster_analysis/{params}"
    station_dataset = "data/station_data_selected.csv"
    labels_dataset = f"{path}/labels_{cluster_num}.csv"
    print(f"labels_dataset {labels_dataset}")
    df_labels = pd.read_csv(f"{labels_dataset}", encoding="utf-8")
    df = pd.read_csv(f"{station_dataset}", encoding="utf-8")
    X = pd.concat([df, df_labels.loc[:, "0"]], axis=1)

    return X


@callback(
    Output("cluster_graph", "figure"),
    [Input("dropdown_cluster_num", "value"), Input("dropdown_cluster_params", "value")],
)
def cluster_graph_visualization(cluster_num, params):

    X = read_data(cluster_num, params)
    clusters_data = []
    for _, item in X.iterrows():
        try:
            clusters_data.append(
                [item["Name"], item["0"], item["Latitude"], item["Longitude"]],
            )
        except KeyError as e:
            print(e)

    geo_df = pd.DataFrame(
        clusters_data, columns=["Name", "Label", "Latitude", "Longitude"]
    )
    geo_df.to_csv("test.csv")
    fig = go.Figure(
        data=go.Scattergeo(
            lon=geo_df["Longitude"].values,
            lat=geo_df["Latitude"].values,
            text=geo_df["Name"].values,
            mode="markers",
            marker_color=geo_df["Label"].values,
        )
    )

    fig.update_layout(geo_scope="usa", margin=dict(l=10, r=10, t=10, b=10))
    return fig


def build_cluster_graph(cluster_num, cluster_param):
    return dcc.Graph(
        figure=cluster_graph_visualization(
            params=cluster_param, cluster_num=cluster_num
        ),
        id="cluster_graph",
    )


@callback(
    Output("cluster_table", "children"),
    [Input("dropdown_cluster_num", "value"), Input("dropdown_cluster_params", "value")],
)
def build_table(cluster_num, params):
    X = read_data(cluster_num, params)
    keys = [key[0] for key in X[["0"]].value_counts().keys().to_list()]
    values = X[["0"]].value_counts().to_list()
    table_header = [html.Thead(html.Tr([html.Th("Label"), html.Th("Count")]))]
    rows = []
    for key, value in zip(keys, values):
        rows.append(html.Tr([html.Td(key), html.Td(value)]))
    table_body = [html.Tbody(rows)]
    return table_header + table_body


def build_dropdown(cluster_num, cluster_param):
    return [
        dcc.Dropdown(
            options=cluster_analysis_names[:-4],
            value=cluster_param,
            id="dropdown_cluster_params",
            style={"width": "100%", "margin-right": "20px"},
        ),
        dcc.Dropdown(
            options=[i + 1 for i in range(9)],
            value=cluster_num,
            id="dropdown_cluster_num",
            style={"width": "100%"},
        ),
    ]


def build_cluster_section(cluster_num, cluster_param):

    X = read_data(cluster_num, cluster_param)
    print(X[["0"]].value_counts())
    section = [
        html.Div(
            id="cluster_dropdowns",
            children=[
                build_dropdown(cluster_num, cluster_param)[0],
                build_dropdown(cluster_num, cluster_param)[1],
            ],
            style=DROPDOWNS_DIV_STYLE,
        ),
        build_cluster_graph(cluster_num, cluster_param),
        dbc.Table(
            build_table(cluster_num, cluster_param),
            id="cluster_table",
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            dark=True,
        ),
    ]
    return section


def layout(velocity=None, **other_unknown_query_strings):
    return html.Div(
        children=[
            html.H1("Cluster analysis"),
            html.Div(
                children=[
                    html.Div(
                        id="cluster_div",
                        children=build_cluster_section(
                            cluster_num=4, cluster_param="temp"
                        ),
                        style={"height": "100%"},
                    ),
                ],
            ),
        ],
        style=CONTENT_STYLE,
    )
