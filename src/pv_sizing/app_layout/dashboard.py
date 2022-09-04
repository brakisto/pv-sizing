from pv_sizing.dimension.pv import PVProduction

from pv_sizing.utils.load_example import example_irr, example_load
from pv_sizing.utils.pv_utils import init_inv

from pv_sizing.app_layout.applayout import app
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
from plotly.subplots import make_subplots


@app.callback(
[Output(component_id='PV', component_property='figure')],
[Input(component_id='num_panels', component_property='value'),
Input(component_id='panel_price', component_property='value'),
Input(component_id='inverter_price', component_property='value'),
Input(component_id='addition_cost', component_property='value'),
Input(component_id='instalation_cost_perc', component_property='value'),
Input(component_id='select_tnoct', component_property='value'),
Input(component_id='panel_power', component_property='value'),
Input(component_id='gamma', component_property='value')])
def interactive_plot(num_panel = 2, panel_price = 260, inverter_price = 1300, additional_cost = 500, installation_cost_perc = 0.15,
                     tnoct = 42, panel_power = 450, gamma = -0.36):

    pv = PVProduction(irr_data=example_irr, load=example_load, tnoct=tnoct, gamma=gamma, panel_power=panel_power, num_panel=num_panel)

    initial_investment = init_inv(num_panel=num_panel, price_panel=panel_price,
                                    additional_cost=additional_cost, installation_cost_perc=installation_cost_perc,
                                    price_inverter=inverter_price)

    cashflow, van, tir = pv.economic_analysis(initial_investment)

    fig = make_subplots(rows=2, cols=1, horizontal_spacing = 1)

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