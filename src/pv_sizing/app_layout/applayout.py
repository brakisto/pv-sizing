from dash import Dash, dcc, html, Input, Output
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "overflow": "scroll",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "15rem",
    "margin-right": "0rem",
    "padding": "5rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div([
    html.H4("Select parameters", className="display-4"),
    html.Hr(),

    html.P('Number of panels',style={'display':'inline-block','margin-right':20}),
    dcc.Input(id="num_panels", type="number", placeholder="Numer of panels", value = 1, style={'width':'90%', 'marginRight':'10px', 'display':'inline-block'},
                 ),

    html.Hr(),

    html.P('Panel price',style={'display':'inline-block','margin-right':20}),
    dcc.Input(id="panel_price", type="number", placeholder="Panel price", value = 260 ,style={'width':'90%','marginRight':'10px', 'display':'inline-block'}
                 ),

    html.Hr(),
    
    html.P('Inverter price',style={'display':'inline-block','margin-right':20}),
    dcc.Input(id="inverter_price", type="number", placeholder="Inverter price", value = 1300 ,style={'width':'90%','marginRight':'10px', 'display':'inline-block'}
                 ),
        
    html.Hr(),

    html.P('Additional cost',style={'display':'inline-block','margin-right':20}),
    dcc.Input(id="addition_cost", type="number", placeholder="Additional price", value = 500 ,style={'width':'90%','marginRight':'10px', 'display':'inline-block'}
                 ),

    html.Hr(),

    html.P('Installation cost percantage',style={'display':'inline-block','margin-right':20}),
    dcc.Input(id="instalation_cost_perc", type="number", placeholder="Instalation percentage cost", value = 0.15 ,style={'width':'90%','marginRight':'10px', 'display':'inline-block'}
                 ),

    html.Hr(),

    html.P('Panel power',style={'display':'inline-block','margin-right':20}),
    dcc.Input(id="panel_power", type="number", placeholder="Instalation percentage cost", value = 450 ,style={'width':'90%','marginRight':'10px', 'display':'inline-block'}
                 ),

    html.Hr(),

    html.P('Gamma',style={'display':'inline-block','margin-right':20}),
    dcc.Input(id="gamma", type="number", placeholder="Instalation percentage cost", value = -0.36 ,style={'width':'90%','marginRight':'10px', 'display':'inline-block'}
                 ),

    html.Hr(),

    html.P('TNOC [ºC]',style={'display':'inline-block','margin-right':20}),
    dcc.Input(id="select_tnoct", type="number", placeholder="TNOCT [ºC]", value = 42 ,style={'width':'90%','marginRight':'10px', 'display':'inline-block'}
                 )],
                 
    style=SIDEBAR_STYLE,
)

# App layout
app.layout = html.Div([

    html.H1("Photovoltaic production", style={'text-align': 'center'}),

    html.Div([
    dcc.Graph(id='PV', figure={})
    ]),
    html.Br(), 
    sidebar
],
    style = CONTENT_STYLE)