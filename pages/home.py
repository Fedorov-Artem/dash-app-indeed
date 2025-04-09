# This is the main page of the dash application
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

from pages.functions.common_elements import job_type, data_professions, time_period
from pages.functions.common_elements import df, create_ban_card
from pages.functions import generate_charts as gen_charts

import sys
from datetime import date

from dateutil.relativedelta import relativedelta

# Define dash app page
sys.path.append('/functions')
dash.register_page(__name__, path='/', title='Data Jobs in Israel 2024-2025')
pd.options.mode.chained_assignment =  None

# All default visualizations are defined using functions from generate_charts.py
fig_bar = gen_charts.generate_bar_chart(df)
fig_line = gen_charts.generate_line_chart(df)
fig_pie_district = gen_charts.generate_pie_district(df)
fig_en = gen_charts.generate_single_bar_en(df)
fig_he = gen_charts.generate_single_bar_he(df)
fig_edu = gen_charts.generate_single_bar_degree(df)
fig_recr = gen_charts.generate_single_bar_recruter(df)
#fig_pie_cloud = generate_pie_cloud(df)
fig_pie_viz = gen_charts.generate_pie_viz(df)
fig_bar_companies = gen_charts.generate_bar_chart_companies(df)

# Page layout
layout = dbc.Row(
    children = [
        # Column for user controls
        dbc.Col(html.Div([
            html.Div(
                children=[
                    job_type,
                    data_professions,
                    html.Br(),
                    time_period
                ]),
                html.Br(),
            ], style={"padding-left" : "4px"},
        ), style = {"position": "fixed", "background-color": "#f8f9fa", "top": "4rem", "bottom":0, "width":"20rem"}
        ),
        # Column for app graphs and plots
        dbc.Col(
            children=[
                dbc.Row([
                    create_ban_card("Last Update:", f"{df['first_online'].max():%m.%d.%Y}", True),
                    create_ban_card("Total Vacancies: ", "{:,d}".format(len(df)), True),
                    create_ban_card("Vacancies Selected: ", "total-vacancies"),
                    create_ban_card("Mean required experience: ", "exp-text")
                ], style={"text-align": "center"}),
                dbc.Row(
                    children=[
                        dbc.Col([dcc.Graph(id="bar_chart", figure=fig_bar)], width=8),
                        dbc.Col([dcc.Graph(id="pie_district", figure=fig_pie_district)], width=4)
                    ]),
                dbc.Row(
                    children=[
                        dbc.Col(html.Div([dcc.Graph(id="line_chart", figure=fig_line)]), width=8),
                        dbc.Col([dbc.Card([
                            html.H6("Language/Degree Requirements, Employer type", className="card-title"),
                            dcc.Graph(id="single_bar_en", figure=fig_en, config={'displayModeBar': False}),
                            dcc.Graph(id="single_bar_he", figure=fig_he, config={'displayModeBar': False}),
                            dcc.Graph(id="single_bar_degree", figure=fig_edu, config={'displayModeBar': False}),
                            dcc.Graph(id="single_bar_recr", figure=fig_recr, config={'displayModeBar': False}),
                        ], style={"top": "1rem"})], width=4),
                    ]),
                dbc.Row(
                    children=[
                        dbc.Col(html.Div([dcc.Graph(id="bar_companies", figure=fig_bar_companies)]), width=8),
                        dbc.Col([dcc.Graph(id="pie_viz", figure=fig_pie_viz)], width=4)
                ]),
            ], style = {"margin-left": "21rem"}
        ),
    ], className='dbc'
)

@dash.callback(
    Output("time-period", "start_date"),
    Output("time-period", "end_date"),
    Output("time-period", "disabled"),
    [
        Input("time-period-radio", "value"),
    ],
)
def filter_df(radio_value):
    ''' updates datepicker based on selected radiobutton '''
    if radio_value > 0:
        last_include = df['first_online'].max() - relativedelta(months=radio_value)
        return last_include.date(), df['first_online'].max().date(), True
    if radio_value == 0:
        return df['first_online'].min().date(), df['first_online'].max().date(), True
    return df['first_online'].min().date(), df['first_online'].max().date(), False

@dash.callback(
    Output("total-vacancies", "children"),
    Output("bar_chart", "figure"),
    Output("line_chart", "figure"),
    Output("pie_district", "figure"),
    Output("exp-text", "children"),
    Output("single_bar_en", "figure"),
    Output("single_bar_he", "figure"),
    Output("single_bar_degree", "figure"),
    Output("single_bar_recr", "figure"),
    Output("bar_companies", "figure"),
    Output("pie_viz", "figure"),
    [
        Input("job-type", "value"),
        Input("all-types", "value"),
        Input("time-period", "start_date"),
        Input("time-period", "end_date")
    ],
)
def filter_df(job_type, all_types, start_date, end_date):
    ''' 1. filters main dataframe depending on user control values
        2. generates visualisations using filtered dataframe '''

    df_selected = df.copy()

    # filter by seniority level
    if len(job_type)  > 0:
        df_selected = df_selected.loc[df_selected['job_type'].isin(job_type)]

    # filter by profession
    if len(all_types) > 0:
        df_selected['total'] = df_selected[all_types].sum(axis=1)
        df_selected = df_selected.loc[df_selected['total'] > 0]

    # filter by publication date
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    df_selected = df_selected.loc[
        (df_selected['first_online'].dt.date >= start_date) & (df_selected['first_online'].dt.date <= end_date)]

    # generate visualisations
    fig_bar = gen_charts.generate_bar_chart(df_selected)
    fig_line = gen_charts.generate_line_chart(df_selected)
    fig_pie_cloud = gen_charts.generate_pie_district(df_selected)
    fig_en = gen_charts.generate_single_bar_en(df_selected)
    fig_he = gen_charts.generate_single_bar_he(df_selected)
    fig_edu = gen_charts.generate_single_bar_degree(df_selected)
    fig_recr = gen_charts.generate_single_bar_recruter(df_selected)
    fig_bar_companies = gen_charts.generate_bar_chart_companies(df_selected)
    fig_pie_viz = gen_charts.generate_pie_viz(df_selected)

    selected_jobs_string = "{:,d}".format( len(df_selected) )
    exp_text = f"{df_selected['min_experience'].mean():.2f} years"

    return selected_jobs_string, fig_bar, fig_line, fig_pie_cloud, exp_text, fig_en, fig_he, fig_edu, fig_recr,\
           fig_bar_companies, fig_pie_viz
