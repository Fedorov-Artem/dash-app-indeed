import dash
from dash import html#, dcc
import dash_bootstrap_components as dbc
#import dash_bootstrap_templates


dash.register_page(__name__, path='/about')

layout = dbc.Row(
    children = [
        dbc.Col(children=[],
         style = {"position": "fixed", "background-color": "#f8f9fa", "top": "4rem", "bottom":0, "width":"20rem"}),
        dbc.Col(
            children=[
                html.Br(),
                html.P("Data for this dashboard was gathered from indeed biweekly starting from 11.01.2024."),
                html.P("Required skills and experience where extracted from vacancy descriptions using Gemini."),
                html.P([
                    html.Span("Written by "),
                    html.A("Artem Fedorov", href='mailto:artem.v.fedorov@gmail.com'),
                    html.Span(".")
                ])
            ], style = {"margin-left": "21rem"}
        ),
    ], className='dbc'
)
