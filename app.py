# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
<<<<<<< HEAD
import plotly.express as px
import pandas as pd
from my_special import fig1
from my_special import fig22
from my_special import conversion_rate
import dash_daq as daq
import my_special
from my_special import available_indicators
from my_special import df_to_use
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
=======

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
>>>>>>> parent of 538b0ad (simple)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#1d492b',x
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


app.layout = html.Div(
    [

        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            "Montant devis fait",
                            className="first",
                        ),
                        html.Br(),
                        html.Label('Multi-Select Dropdown'),
                        dcc.Dropdown(
                            id='xaxis-column',
                            options=[{'label': i, 'value': i}
                                     for i in available_indicators],
                            value='ACCEPTED'
                        ),
                        dcc.Graph(id='graph_changing'),

                    ]
                ),
            ],
            className="something",
        ),

        html.Div(
            [
                html.H6(
                    "Share of leads received in number",
                    className="first",

                ),
                dcc.Graph(
                    id="graph-11",
                    figure=my_special.fig11,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [
                html.H6(
                    "Share of leads received in amount",
                    className="first",

                ),
                dcc.Graph(
                    id="graph-12",
                    figure=my_special.fig12,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),


        html.Div(
            [
                html.H6(
                    "Share of ACCEPTED leads received in amount",
                    className="first",

                ),
                dcc.Graph(
                    id="graph-13",
                    figure=my_special.fig13,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [
                html.H6(
                    "Share of leads & status per month",
                    className="first",

                ),
                dcc.Graph(
                    id="graph-14",
                    figure=my_special.fig14,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [
                html.H6(
                    "Area graph of revenue ACCEPTED",
                    className="first",

                ),
                dcc.Graph(
                    id="graph-15",
                    figure=my_special.fig15,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [
                html.H6(
                    "Stacked Area graph of revenue ACCEPTED",
                    className="first",

                ),
                dcc.Graph(
                    id="graph-16",
                    figure=my_special.fig16,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [
                html.H6(
                    "Montant devis fait",
                    className="first",

                ),
                dcc.Graph(
                    id="graph-31",
                    figure=my_special.fig22,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),


        html.Div(
            [
                html.Div(
                    html.H6(
                        "Share of accepted lead per source",
                        className="first",
                    ),
                ),
                dcc.Graph(
                    id="graph-32",
                    figure=my_special.fig3,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [
                html.Div(
                    html.H6(
                        "Share of accepted lead per service",
                        className="first",
                    ),
                ),
                dcc.Graph(
                    id="graph-4",
                    figure=my_special.fig4,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [
                html.Div(
                    html.H6(
                        "Share of source for total leads",
                        className="first",
                    ),
                ),
                dcc.Graph(
                    id="graph-5",
                    figure=my_special.fig5,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [
                html.P(
                    "There what we want to see the cumulative amounts of devis signed to see the growth of the CA over the year."
                ),
                html.Div(
                    html.H6(
                        "Number of leads per cantons",
                        className="first",
                    ),
                ),
                dcc.Graph(
                    id="graph-6",
                    figure=my_special.fig6,
                    config={"displayModeBar": False},
                ),
            ],
            className="more",
        ),

        html.Div(
            [html.H6(
                "Conversion rate",
                className="first"),
                html.Div(
                    [
                        html.H6(
                            "Accepted rate",
                            className="first",
                        ),
                        daq.LEDDisplay(
                            id="operator-led",
                            value=conversion_rate,
                            color="#92e0d3",
                            backgroundColor="#1e2130",
                        ),
                    ],
                    className="something",
            ),
                html.Div(
                    [
                        html.H6(
                            "Potential conversion rate",
                            className="first",
                        ),
                        daq.LEDDisplay(
                            id="operator-led2",
                            value=my_special.potential_conversion_rate,
                            color="#92e0d3",
                            backgroundColor="#1e2130",
                        ),
                    ],
                    className="something",
            ),
            ],
            className="more",
        ),


    ],
    className="sub_page",
)


@ app.callback(
    Output('graph_changing', 'figure'),
    Input('xaxis-column', 'value'))
def update_figure(selected_status):
    filtered_df2 = df_to_use[df_to_use.STATUS_DEVIS == selected_status]

    fig2 = px.line(filtered_df2, x=filtered_df2['DATE_DEVIS'],
                   y=filtered_df2['Cumulative_per_serv'],
                   color=filtered_df2['SERVICE'],
                   # possibility to make the line more flexible
                   line_shape='spline')

    fig2.update_layout(transition_duration=500)

<<<<<<< HEAD
    return fig2
=======
app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value'),
        html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])
>>>>>>> parent of 538b0ad (simple)


if __name__ == '__main__':
    app.run_server(debug=True)
