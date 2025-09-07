"""  This is the about page of the dash application """
import dash
from dash import html
import dash_bootstrap_components as dbc

# Define dash app page
dash.register_page(__name__, path='/about')

all_texts = [
    "Data for this dashboard was gathered from indeed biweekly starting from 11.01.2024.",
    "Required skills and experience where extracted from vacancy descriptions using Gemini."
]

# Page layout
layout = dbc.Row(
    children = [
        dbc.Col(children=[],
         style = {"position": "fixed", "background-color": "#f8f9fa",
                  "top": "4rem", "bottom":0, "width":"20rem"}),
        dbc.Col(
            children=[
                html.Br(),
                html.P(all_texts[0]),
                html.P(all_texts[1]),
                html.P([
                    html.Span("Written by "),
                    html.A("Artem Fedorov", href='mailto:artem.v.fedorov@gmail.com'),
                    html.Span(".")
                ])
            ], style = {"margin-left": "21rem"}
        ),
    ], className='dbc'
)
