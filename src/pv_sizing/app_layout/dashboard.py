from pv_sizing.dimension.pv import PVProduction
import datetime
import pandas as pd

from pv_sizing.utils.pv_utils import init_inv

from pv_sizing.app_layout.applayout import app
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
from plotly.subplots import make_subplots

import numpy as np

from applayout import app
from parsedata import parse_data


@app.callback(
[Output(component_id='PV', component_property='figure')],
[Input('upload-data', 'contents'),
Input('upload-data', 'filename'),
Input(component_id='num_panels', component_property='value'),
Input(component_id='panel_price', component_property='value'),
Input(component_id='inverter_price', component_property='value'),
Input(component_id='addition_cost', component_property='value'),
Input(component_id='instalation_cost_perc', component_property='value'),
Input(component_id='select_tnoct', component_property='value'),
Input(component_id='panel_power', component_property='value'),
Input(component_id='gamma', component_property='value'),
])
def interactive_plot(contents, filename, num_panel, panel_price, inverter_price, additional_cost, installation_cost_perc,
                     tnoct, panel_power, gamma):
    fig = make_subplots(rows=2, cols=1, horizontal_spacing = 1)
    if contents:
        dfs = []
        for c, f in zip(contents, filename):
            df = parse_data(c, f)
            df = df.set_index(df.columns[0], drop=True)
            dfs.append(df)

        for df in dfs:
            if 'Gb(i)' in df.columns:
                irr_data = df
            else:
                load_data = df

        pv = PVProduction(irr_data=irr_data, load=load_data, tnoct=tnoct, gamma=gamma, panel_power=panel_power, num_panel=num_panel)

        initial_investment = init_inv(num_panel=num_panel, price_panel=panel_price,
                                        additional_cost=additional_cost, installation_cost_perc=installation_cost_perc,
                                        price_inverter=inverter_price)

        cashflow, van, tir = pv.economic_analysis(initial_investment)

        fig.add_trace(
            go.Scatter(x = pv.myload_yearly.index, y = pv.myload_yearly.AE_kWh, name = 'Load'),
            row=1, col=1
        )

        fig.add_trace(go.Scatter(x = pv.myload_yearly.index, y = pv.myprod_yearly.kWh, name= 'PV production'),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(x=cashflow.index.values, y=cashflow['Accumulated cashflow'], name = 'Accumulated cashflow'),
            row=2, col=1
        )

        fig.update_xaxes(title_text="Time [h]", row=1, col=1)
        fig.update_yaxes(title_text="Energy [kWh]", row=1, col=1)

        fig.update_xaxes(title_text="Time [years]", row=2, col=1)
        fig.update_yaxes(title_text="Money [€]", row=2, col=1)

        fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1))

        fig.update_layout(
        paper_bgcolor="#f8f9fa"
        )

    return [fig]

if __name__ == "__main__":
    app.run_server(debug=True)