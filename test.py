import base64
import datetime
import io
import plotly.graph_objs as go

from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots

from src.pv_sizing.dimension.pv import PVProduction

import pandas as pd

from pv_sizing.utils.load_example import example_irr, example_load
from pv_sizing.utils.constants import fresnel_fixed
from pv_sizing.utils.pv_utils import init_inv

from pv_sizing.web_scrapping.electricity_price import ElectricityPrice

import pandas as pd


pv_costs = {"num_panel": 5,
            "price_panel": 260,
            "price_inverter" : 1300,
            "additional_cost" : 500,
            "installation_cost_perc" : 0.15}

initial_investment = init_inv(**pv_costs)

electricity_price = ElectricityPrice().extract_data()


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        dcc.Graph(id="Mygraph"),
        html.Div(id="output-data-upload"),
    ]
)


@app.callback(Output('Mygraph', 'figure'), [
Input('upload-data', 'contents'),
Input('upload-data', 'filename')
])
def update_graph(contents, filename):

    fig = make_subplots(rows=2, cols=1, horizontal_spacing = 1)
    
    if contents:
        dfs = []
        for c, f in zip(contents, filename):
            df = parse_data(c, f)
            df = df.set_index(df.columns[0], drop=True)
            dfs.append(df)

    
        pv = PVProduction(irr_data=dfs[1], load=dfs[0], tnoct=42, gamma=-0.36, 
                        panel_power=450, num_panel=5, fresnel_eff=fresnel_fixed)

        initial_investment = init_inv(num_panel=5, price_panel=260,
                                    additional_cost=500, installation_cost_perc=0.15,
                                    price_inverter=1000)

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

    return fig


def parse_data(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif "txt" or "tsv" in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return df

if __name__ == "__main__":
    app.run_server(debug=True)
