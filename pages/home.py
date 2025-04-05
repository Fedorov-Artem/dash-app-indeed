import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from datetime import date
from dateutil.relativedelta import relativedelta
from pages.functions.generate_charts import job_type, data_professions, time_period


#import dash_leaflet as dl
#import dash_leaflet.express as dlx
import plotly.express as px
import sys
sys.path.append('/functions')
from pages.functions import generate_charts as gen_charts

dash.register_page(__name__, path='/', title='Data Jobs in Israel 2024-2025')

pd.options.mode.chained_assignment =  None

df = gen_charts.df
all_types_options = gen_charts.all_types_options

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

layout = dbc.Row(
    children = [
        # Column for user controls
        dbc.Col(html.Div(
            children=[
                html.Div(
                    children=[
                        job_type,
                        data_professions,
                        html.Br(),
                        time_period
                    ],
                ),
                html.Br(),
            ], style={"padding-left" : "4px"},
        ), style = {"position": "fixed", "background-color": "#f8f9fa", "top": "4rem", "bottom":0, "width":"20rem"}
        ),
        # Column for app graphs and plots
        dbc.Col(
            children=[
                dbc.Row([
                    gen_charts.create_ban_card("Last Update:", f"{df['first_online'].max():%m.%d.%Y}", True),
                    gen_charts.create_ban_card("Total Vacancies: ", "{:,d}".format(len(df)), True),
                    gen_charts.create_ban_card("Vacancies Selected: ", "total-vacancies"),
                    gen_charts.create_ban_card("Mean required experience: ", "exp-text")
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

# Update date-picker
@dash.callback(
    Output("time-period", "start_date"),
    Output("time-period", "end_date"),
    Output("time-period", "disabled"),
    [
        Input("time-period-radio", "value"),
    ],
)
def filter_df(radio_value):
    if radio_value > 0:
        last_include = df['first_online'].max() - relativedelta(months=radio_value)
        return last_include.date(), df['first_online'].max().date(), True
    if radio_value == 0:
        return df['first_online'].min().date(), df['first_online'].max().date(), True
    return df['first_online'].min().date(), df['first_online'].max().date(), False

# Update Map Graph based on date-picker, selected data on histogram and location dropdown
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
    df_selected = df.copy()

    if len(job_type)  > 0:
        df_selected = df_selected.loc[df_selected['job_type'].isin(job_type)]

    if len(all_types) > 0:
        df_selected['total'] = df_selected[all_types].sum(axis=1)
        df_selected = df_selected.loc[df_selected['total'] > 0]

    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)

    df_selected = df_selected.loc[
        (df_selected['first_online'].dt.date >= start_date) & (df_selected['first_online'].dt.date <= end_date)]

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
