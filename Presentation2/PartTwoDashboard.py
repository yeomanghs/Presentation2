
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import json
from itertools import count


#snapshot html
snapShotHtml = "2021-02-05_SnapShotPrediction.html"

#Bootstrap themes
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "14rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
#         html.H2('Dashboard', className="display-4"),
        html.Hr(),
        html.P(
            "Part Two Dashboard", className = "lead"
              ),
        dbc.Nav(
            [
                dbc.NavLink("Business Problem", href="/page-1", id = "page-1-link"),
                dbc.NavLink("Objective", href="/page-2", id = "page-2-link"),
                dbc.NavLink("Stakeholders involved", href="/page-3", id = "page-3-link"),
                dbc.NavLink("Solution", href="/page-4", id = "page-4-link"),
                # dbc.NavLink("Involvement", href="/page-5", id = "page-5-link"),
                dbc.NavLink("Evaluation and validation", href="/page-5", id = "page-5-link"),
                dbc.NavLink("Business Outcome", href="/page-6", id = "page-6-link"),
            ],
            vertical = True,
            pills = True,
        ),
    ],
    style = SIDEBAR_STYLE,
)

#business problem
BpPage = html.P("We receive remittance history from money service providers \
                (money changing, remittance and wholesale currencies services) on daily basis.\
                Report from enforcement agency shows that informal tip-off from the providers is sometimes too late\
                or inefficient to identify and catch culprits using those channels to commit financial crimes.\
                A proactive approach is needed to flag suspicious customer and reduce reliance on one source of information.")

#objective
ObjectivePage = html.P("Train a machine with Machine Learning algorithm to identify suspicious customer in financial crime X\
                        based on remittance history")

#stakeholder involved
section1 = "Money Service Business Regulation Department"
S1point1 = "Mandate: Supervise and regulate money changing, remittance and wholesale currencies services for sake of financial stability"
S1point2 = "Own all data used and solution in the project"
S1point3 = "Commitment: One data analytic team - 1 manager and two analysts"
StakeholdersPage = html.Div(
                            [
                                html.H6("%s"%section1),
                                html.Div(
                                        [
                                html.Li("%s"%S1point1),
                                html.Li("%s"%S1point2),
                                html.Li("%s"%S1point3),
                                        ]
                                        )
                            ]
                            )

#solution
OverviewFlow = 'flowChart.png'
TechnicalFlow = "technicalFlow.png"
SolutionDetails = "solutionDetails.png"
SolutionPage = [
        html.Div(children = [
        dbc.Row(dbc.Col(html.Div("Please select phase"))),        
        dcc.Dropdown(
            id = 'solutionRound',
            options = [{'label': i, 'value': i} for i in ['Before working', 'Working', "Solution details"]],
            value = 'Solution details'
                    ),
        html.Div(id = "solution")
                            ])
            ]

#evaluation and validation
evaluationFlow = "evaluation.png"
EvaluationPage = [html.Img(
                        src = app.get_asset_url(evaluationFlow),
                        style={'height':'50%', 'width':'70%'}
                )]

#business outcome
BusinessOutcomePage = html.P("MSBR has a proactive measure to identify suspicious customers in financial crime X\
                              . The department is no longer to just rely on tip-off to tackle the crime X.")

snapShotPage = html.Div(
                        [
                        html.Iframe(src = app.get_asset_url(snapShotHtml),
                                className = "six columns",
                                style = {"height": "400px", "width": "100%"}),
                        ])

#2nd round
section1 = "Conclusion"
S1point1 = "For **precision**, **CRF outperforms** SpaCy significantly in both ORG and PERSON labels and,"\
            " hence CRF gains a slight advantage in F1 score"
S1point2 = "For **recall**, **SpaCy has an edge** over CRF in both ORG and PERSON labels"
S1point3 = "Same situation happens in named entities (wrong label)"

section2 = "Suggestion (Priority:Choice)"
S2point1 = "Correct labelling, Equally important to **reduce false positives** and **identify all positive cases**: CRF"
S2point2 = "Correct labelling, More important to **identify all positive cases** than to reduce false positives: SpaCy"
S2point3 = "Correct labelling, More important to **reduce false positives** than to identify all positive cases: CRF"
S2point4 = "Incorrect labelling is ok, Equally important to **reduce false positives** and **identify all positive cases** for all named entities: SpaCy"

conclusion2 =  html.Div(
                    [
                        html.H6("%s"%section1),
                        html.Br([]),
                        html.Div(
                            [
                                # html.Li("%s"%S1point1)),
                                # html.Li("%s"%S1point2),
                                # html.Li("%s"%S1point3),
                                dcc.Markdown('''
                                            * %s
                                            * %s
                                            * %s
                                            '''%(S1point1, S1point2, S1point3))
                            ],
                                ),
                        html.Br([]),
                        html.Br([]),
                        html.H6("%s"%section2),
                        html.Br([]),
                        html.Div(
                            [
                                # html.Li("%s"%S2point1),
                                # html.Li("%s"%S2point2),
                                # html.Li("%s"%S2point3),
                                # html.Li("%s"%S2point4),
                                dcc.Markdown('''
                                            * %s
                                            * %s
                                            * %s
                                            * %s
                                            '''%(S2point1, S2point2, S2point3, S2point4))
                            ],
                                )
                    ],
                    )

content = html.Div(id="page-content", style = CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id = "url"), sidebar, content])
                    
#callback on link
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 7)],
    [Input("url", "pathname")],
            )
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/page-{i}" for i in range(1, 7)]
                
#callback on page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return BpPage
    elif pathname == "/page-2":
        return ObjectivePage
    elif pathname == "/page-3":
        return StakeholdersPage
    elif pathname == "/page-4":
        return SolutionPage
    elif pathname == "/page-5":
        return EvaluationPage
    elif pathname == "/page-6":
        return BusinessOutcomePage
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
                        )

#callback on flow image
@app.callback([Output("solution", 'children')],
              [Input('solutionRound', 'value')])
def churnOutFlowGraph(value):
    if value == "Before working":
        return [html.Img(
                        src = app.get_asset_url(OverviewFlow),
                        style={'height':'50%', 'width':'70%'}
                        )]
    elif value == "Working":
        return [
                    html.Img(
                        src = app.get_asset_url(TechnicalFlow),
                        style={'height':'50%', 'width':'70%'}
                            ),
                ]
    elif value == "Solution details":     
        return [
                    html.Img(
                        src = app.get_asset_url(SolutionDetails),
                        style={'height':'50%', 'width':'70%'}
                            ),
                ]
           
if __name__ == '__main__':
    app.run_server(debug=True)
