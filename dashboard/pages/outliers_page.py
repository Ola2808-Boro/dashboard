import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import re
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/outliers")

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


BASIC_PATH = "https://raw.githubusercontent.com/Ola2808-Boro/dashboard/refs/heads/main/data/cluster_data_test"
# https://raw.githubusercontent.com/Ola2808-Boro/dashboard/refs/heads/main/data/cluster_data_test/all%20params/9/Cluster_1/10/data_daily_spring.csv


def read_data():
    df = pd.read_csv(f"{BASIC_PATH}/anomalies.csv")
    return df


def build_dropdown(feature, cluster, season):
    df = read_data()
    features_unique = df["features"].unique()
    cluster_unique = df["cluster"].unique()
    season_unique = df["season"].unique()
    return [
        dcc.Dropdown(
            options=features_unique,
            value=feature,
            id="dropdown_features_anomalies",
            style={"width": "100%", "margin-right": "20px"},
        ),
        dcc.Dropdown(
            options=cluster_unique,
            value=cluster,
            id="dropdown_cluster_anomalies",
            style={"width": "100%", "margin-right": "20px"},
        ),
        dcc.Dropdown(
            options=season_unique,
            value=season,
            id="dropdown_season_anomalies",
            style={"width": "100%", "margin-right": "20px"},
        ),
    ]


@callback(
    Output("figures_anomalies", "children"),
    [
        Input("dropdown_features_anomalies", "value"),
        Input("dropdown_cluster_anomalies", "value"),
        Input("dropdown_season_anomalies", "value"),
    ],
)
def draw_graphs(feature, cluster, season):

    df_anomalies = read_data()
    indexes = df_anomalies.loc[
        (df_anomalies["features"] == feature)
        & (df_anomalies["cluster"] == cluster)
        & (df_anomalies["season"] == season)
    ]["indexes"]
    print(f"Build again {indexes}")
    df = pd.read_csv(
        f"{BASIC_PATH}/{feature.replace(' ','%20')}/9/Cluster_{cluster}/anomalies_{season}.csv"
    )
    print(df.head())
    print(
        f"Outliers {BASIC_PATH}/{feature.replace(' ','%20')}/9/Cluster_{cluster}/anomalies_{season}.csv"
    )
    figures = []
    indexes_iter = (
        indexes if isinstance(indexes, int) else re.findall(r"\d", str(indexes))
    )
    for idx in indexes_iter:
        # print(f"Idx : {idx}")
        # print(df.iloc[:, int(idx)])
        fig = px.line(
            df.iloc[:, int(idx)],
        )
        figures.append(
            dcc.Graph(figure=fig, id=f"{feature}_{season}_{cluster}_{str(idx)}")
        )

    return html.Div(children=figures, id="figures_anomalies")


def build_cluster_section(feature, cluster, season):
    print("Build outliers")
    section = [
        html.Div(
            id="cluster_dropdowns_anomalies",
            children=[
                build_dropdown(feature, cluster, season)[0],
                build_dropdown(feature, cluster, season)[1],
                build_dropdown(feature, cluster, season)[2],
            ],
            style=DROPDOWNS_DIV_STYLE,
        ),
        draw_graphs(feature, cluster, season),
    ]
    return section


def layout(velocity=None, **other_unknown_query_strings):
    df = read_data()
    features = df["features"].unique()
    cluster = df["cluster"].unique()
    season = df["season"].unique()
    return html.Div(
        children=[
            html.H1("Outliers analysis"),
            html.Div(
                children=[
                    html.Div(
                        id="cluster_div_anomalies",
                        children=build_cluster_section(
                            feature=features[0],
                            cluster=cluster[0],
                            season=season[0],
                        ),
                    ),
                ],
            ),
        ],
        style=CONTENT_STYLE,
    )
