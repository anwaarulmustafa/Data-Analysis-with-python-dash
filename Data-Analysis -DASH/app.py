# ____________________________________________________________________
#------basic dash imports 
from dash import Dash, Input, Output, State, dcc, dash_table, html

#------importing required libraries & packages
import dash_bootstrap_components as dbc
import dash_cytoscape as cy
import pandas as pd
from collections import OrderedDict

#------imports related to exception-handling
import traceback
import sys

#-----importing parser-functions for filers-data 
from parser import *

#____________________________________________________________________


try:
    #---------initializing dash-application---------------
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    # -----------------internal-STYLE-properties-------------------
    SIDEBAR_STYLE = {
        "width": "13%",
        "height": "85vh",
        "min-height": "475px",
        "max-height": "475px",
        "float": "left",
        "background-color": "#f8f9fa",
    }

    SELECT_CASE = {
        "width": "100px",
        "max-height": "1vh",
    }

    TOOLBAR_STYLE = {
        "height": "12vh",
        "width": "87%",
        "min-height": "70px",
        "float": "right",
        "background-color": "#f8f9fa",
        "border-bottom": "2px solid black",
    }

    CANVAS_AREA = {
        "height": "88vh",
        "min-height": "400px",
        "width": "87%",
        "float": "right",
        "overflow": "hidden",
        "position": "relative",
        "background-color": "#f8f9fa",
    }

    # -------global Options for Components---------
    caseIds = [
        {"label": "CDR 221", "value": "CDR 221"},
        {"label": "CDR 222", "value": "CDR 222"},
        {"label": "CDR 223", "value": "CDR 223"},
    ]

    comuncationTypes = [
        {"label": "Call", "value": "call"},
        {"label": "SMS", "value": "sms"},
    ]

    #-----------TBC 
    dict = graphInfo = {"aParties": "100", "bParties": "200"}

    #-----------TBC
    NODES = [
        {
            "data": {"id": short, "label": label},
            "position": {"x": 20 * lat, "y": -20 * long},
        }
        for short, label, long, lat in (
            ("la", "Los Angeles", 34.03, -118.25),
            ("nyc", "New York", 40.71, -74),
            ("to", "Toronto", 43.65, -79.38),
            ("mtl", "Montreal", 45.50, -73.57),
            ("van", "Vancouver", 49.28, -123.12),
            ("chi", "Chicago", 41.88, -87.63),
            ("bos", "Boston", 42.36, -71.06),
            ("hou", "Houston", 29.76, -95.37),
        )
    ]
    #-----------TBC
    EDGES = [
        {"data": {"source": source, "target": target}}
        for source, target in (
            ("van", "la"),
            ("la", "chi"),
            ("hou", "chi"),
            ("to", "mtl"),
            ("mtl", "bos"),
            ("nyc", "bos"),
            ("to", "hou"),
            ("to", "nyc"),
            ("la", "nyc"),
            ("nyc", "bos"),
        )
    ]
    #-----------TBC
    ELEMENTS = NODES + EDGES

    #-----------TBC
    
    data = OrderedDict(
        [
            ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
            ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
            ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
            ("Humidity", [10, 20, 30, 40, 50, 60]),
            ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
        ]
    )

    df = pd.DataFrame(data)
    # --------------------------------Side-bar component-----------------------------
    side_bar = html.Div(
        [
            # ______  graph Information panel
            html.Div(
                [
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.CardBody(
                                            [
                                                html.H6(
                                                    "Graph Info",
                                                    className="card-title mt-0",
                                                ),
                                                html.P(
                                                    "A-parties: "
                                                    + graphInfo["aParties"],
                                                    className="card-text my-1",
                                                ),
                                                html.P(
                                                    "B-parties: "
                                                    + graphInfo["bParties"],
                                                    className="card-text",
                                                ),
                                                html.Small(
                                                    "Last updated: seconds ago",
                                                    className="card-text text-muted",
                                                ),
                                            ],
                                            className="pt-0",
                                        ),
                                        className="col-md",
                                    ),
                                ],
                                className="g-0 d-flex align-items-center",
                            )
                        ],
                        className="my-1 shadow bg-white rounded-10",
                        style={"maxWidth": "250px"},
                    ),
                ],
            ),
            dbc.Card(
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(
                            # ______  case-selection menu
                            html.Div(
                                [
                                    html.Label("Select Case Id:"),
                                    dcc.Dropdown(
                                        caseIds,
                                        [],
                                        id="case-id-input",
                                        multi=True,
                                        clearable=False,
                                        placeholder="Select Case",
                                        className="m-2 col-lg-9",
                                    ),
                                    dbc.Button("View case details", id="open-dismiss"),
                                ],
                                className=SELECT_CASE,
                            ),
                        ),
                        dbc.ListGroupItem(
                            [
                                dbc.FormFloating(
                                    [
                                        dbc.Input(
                                            id="start-time-range",
                                            type="datetime-local",
                                            value="2022-01-18T00:00",
                                        ),
                                        dbc.Label("start range"),
                                    ]
                                ),
                                dbc.FormFloating(
                                    [
                                        dbc.Input(
                                            id="end-time-range",
                                            type="datetime-local",
                                            value="2022-01-18T04:00",
                                        ),
                                        dbc.Label("end range"),
                                    ],
                                    className="py-0 my-2",
                                ),
                            ],
                            className="col-lg-9",
                        ),
                        # ______comunicatin-type  input
                        dbc.ListGroupItem(
                            html.Div(
                                [
                                    dcc.Checklist(
                                        comuncationTypes,
                                        ["call", "sms"],
                                        id="communication-type",
                                        className="p-2 m-1",
                                    ),
                                    html.Div([
                                        html.Label("Call Duration: "),
                                    dbc.ListGroup(
                                        [
                                            # _____call duration lower-limit
                                            dbc.ListGroupItem(
                                                [
                                                    dbc.Input(
                                                        id="start-call-duration",
                                                        type="number",
                                                        min=0,
                                                        max=1000,
                                                        step=1,
                                                        value=0,
                                                    )
                                                ],
                                                className="p-0",
                                            ),
                                            # _____call duration upper-limit
                                            dbc.ListGroupItem(
                                                [
                                                    dbc.Input(
                                                        id="end-call-duration",
                                                        type="number",
                                                        min=0,
                                                        max=1000,
                                                        step=1,
                                                        value=1,
                                                    ),
                                                ],
                                                className="p-0",
                                            ),
                                        ],
                                        className="list-group-horizontal m-2 col-lg-9",
                                    ),
                                    # _____No of calls
                                    html.Label("No of calls:"),
                                    dbc.ListGroupItem(
                                        [
                                            dbc.Input(
                                                id="no-of-calls",
                                                type="number",
                                                min=1,
                                                max=10000,
                                                step=1,
                                                value=1,
                                                
                                            ),
                                        ],
                                        className="list-group-horizontal m-2 col-lg-9",
                                    ),
                                    ],style={"display": "None"},id="display_handler"),
                                    
                                ],
                                style={"display": "block"},
                            ),
                        ),
                        dbc.ListGroupItem(
                            # -----------call duration input
                            # -----------communication direction
                            dcc.Dropdown(
                                ["Incoming", "Outgoing", "Incoming/Outgoing"],
                                "Incoming/Outgoing",
                                id="call-direction",
                                # multi=True,
                                clearable=False,
                                placeholder="None",
                                className="m-2 col-lg-9",
                            ),
                        ),
                        dbc.Button("Get Data", id="get-data", n_clicks=0),
                    ],
                    flush=True,
                ),
                style={"width": "100%"},
                className="mb-5 my-1  shadow p-1 mb-5 bg-white rounded",
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    # ------------------------------Analysis component-------------------------------
    tool_bar = html.Nav(
        [
            html.Div(
                [
                    html.Ul(
                        [
                            html.Li(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Img(
                                                                src="assets/images/community.png",
                                                                style={
                                                                    "width": "60px",
                                                                    "height": "60px",
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-front",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P(
                                                                "Community Detection",
                                                                style={
                                                                    "font-size": "12px"
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-back py-3",
                                                    ),
                                                ],
                                                className="flip-box-inner",
                                            )
                                        ],
                                        className="flip-box",
                                    ),
                                ],
                                className="nav-item mx-1 py-2",
                            ),
                            html.Li(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Img(
                                                                src="assets/images/closeness.png",
                                                                style={
                                                                    "width": "60px",
                                                                    "height": "60px",
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-front",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P(
                                                                "Closeness Centrality",
                                                                style={
                                                                    "font-size": "12px"
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-back py-3",
                                                    ),
                                                ],
                                                className="flip-box-inner",
                                            )
                                        ],
                                        className="flip-box",
                                    ),
                                ],
                                className="nav-item mx-1 py-2",
                            ),
                            html.Li(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Img(
                                                                src="assets/images/betweeness.png",
                                                                style={
                                                                    "width": "60px",
                                                                    "height": "60px",
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-front",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P(
                                                                "Betweeness Centrality",
                                                                style={
                                                                    "font-size": "12px"
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-back py-3",
                                                    ),
                                                ],
                                                className="flip-box-inner",
                                            )
                                        ],
                                        className="flip-box",
                                    ),
                                ],
                                className="nav-item mx-1 py-2",
                            ),
                            html.Li(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Img(
                                                                src="assets/images/degree.png",
                                                                style={
                                                                    "width": "60px",
                                                                    "height": "60px",
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-front",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P(
                                                                "Degree Centrality",
                                                                style={
                                                                    "font-size": "12px"
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-back py-3",
                                                    ),
                                                ],
                                                className="flip-box-inner",
                                            )
                                        ],
                                        className="flip-box",
                                    ),
                                ],
                                className="nav-item mx-1 py-2",
                            ),
                            html.Li(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Img(
                                                                src="assets/images/clustering.png",
                                                                style={
                                                                    "width": "60px",
                                                                    "height": "60px",
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-front",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P(
                                                                "Clustering",
                                                                style={
                                                                    "font-size": "12px"
                                                                },
                                                            )
                                                        ],
                                                        className="flip-box-back py-3",
                                                    ),
                                                ],
                                                className="flip-box-inner",
                                            )
                                        ],
                                        className="flip-box",
                                    ),
                                ],
                                className="nav-item mx-1 py-2",
                            ),
                        ],
                        className="nav",
                    ),
                    html.Ul(
                        [
                            dbc.Button(
                                "🔍", color="light", className="py-0 my-3 display-3"
                            ),
                            dcc.Dropdown(
                                id="dropdown-update-layout",
                                value="grid",
                                placeholder="Select Layout",
                                clearable=False,
                                options=[
                                    {"label": name.capitalize(), "value": name}
                                    for name in [
                                        "grid",
                                        "random",
                                        "circle",
                                        "cose",
                                        "concentric",
                                    ]
                                ],
                                style={"width": "80px"},
                                className="py-0 my-3",
                            ),
                        ],
                        style={"margin-left": "auto"},
                        className="nav",
                    ),
                ],
                className="container-fluid d-flex",
            ),
        ],
        className="nav-header navbar-light",
        style=TOOLBAR_STYLE,
    )

    # ----------Cytoscape component----------
    canvas_area = html.Div(
        [
            cy.Cytoscape(
                id="cytoscape-update-layout",
                layout={"name": "grid"},
                style={"width": "100%", "height": "450px"},
                elements=ELEMENTS,
            ),
        ],
        style=CANVAS_AREA,
    )
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("case ids "), close_button=False),
                    dbc.ModalBody(
                        dash_table.DataTable(
                            data=df.to_dict("records"),
                            columns=[{"id": c, "name": c} for c in df.columns],
                            row_selectable="multi",
                        )
                    ),
                    dbc.ModalFooter([dbc.Button("Cancel", id="close-dismiss"),dbc.Button("Add", id="close-dismis")]),
                ],
                id="modal-dismiss",
                scrollable=True,
                is_open=False,
                backdrop='static'
            ),
        ],
    )
    # _______registering layout components of application
    app.layout = html.Div([side_bar, tool_bar, canvas_area, modal])

    # # ______init-callBack for fetching case-details
    # @app.callback(Output(), Input())
    # def foo():
    #     return data

    # _____modal-callBack for viewing case-details
    @app.callback(
        Output("modal-dismiss", "is_open"),
        [Input("open-dismiss", "n_clicks"), Input("close-dismiss", "n_clicks")],
        [State("modal-dismiss", "is_open")],
    )
    def toggle_modal(n_open, n_close, is_open):
        if n_open or n_close:
            return not is_open
        return is_open
    
    @app.callback(
        Output("display_handler", "display"),
        [Input("communication-type", "value")],
    )
    def display_call_properties (input):
        if input[0] =="call"

    #______Get-data callBack on Filters input
    @app.callback(
        Output("get-data", "color"),
        Input("get-data", "n_clicks"),
        State("case-id-input", "value"),
        State("start-time-range", "value"),
        State("end-time-range", "value"),
        State("communication-type", "value"),
        State("start-call-duration", "value"),
        State("end-call-duration", "value"),
        State("no-of-calls", "value"),
        State("call-direction", "value"),
    )
    def update_layout(
        n_clicks, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8
    ):
        if n_clicks != 0:
            data = {
                "case_id": input_1,
                "start_date_time": parseDateTime(input_2, input_3)[0],
                "end_date_time": parseDateTime(input_2, input_3)[1],
                "call": communicationType(input_4)["call"],
                "sms": communicationType(input_4)["sms"],
                "start_call_duration": input_5,
                "end_call_duration": input_6,
                "no_of_calls": input_7,
                "incoming": callDirection(input_8)["incoming"],
                "outgoing": callDirection(input_8)["outgoing"],
            }
            print(input_1,input_2,input_3,input_4,input_5,input_5,input_6,input_7,input_8)
            # variable= get-data function()

            return "dark"
        # get_data(data)
        return "primary"
    #_____Chained callBack for analysis trigger
    @app.callback(
        Output("end-call-duration", "value"),
        Input("dropdown-update-layout", "value"),
    )
    def abc(value):
        return f"1234"
    
    # _____Cytoscape-CallBack for updating cy-Layout
    @app.callback(
        Output("cytoscape-update-layout", "layout"),
        Input("dropdown-update-layout", "value"),
    )
    def update_layout(layout):
        return {"name": layout, "animate": True}

    

    if __name__ == "__main__":
        app.run_server(debug=True, dev_tools_props_check=False)

except Exception as e:
    traceback.print_exc(file=sys.stdout)
    print(e)
