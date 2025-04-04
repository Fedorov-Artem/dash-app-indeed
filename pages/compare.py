import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from datetime import date
from pages.functions.generate_charts import df, all_types_options, important_skills, create_ban_card

import plotly.express as px
from dateutil.relativedelta import relativedelta
import datetime

from plotly import graph_objs as go
#from plotly.tools import make_subplots
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/compare', title='Data Jobs in Israel 2024-2025')


def bar_chart_skills(df_sel,
                     text_all='All Vacancies',
                     text_recent='Recent Vacancies',
                     time_period=6):
    def get_top_skills(df_sel_filtered):
        skill_count = []
        for skill in important_skills:
            if skill in df_sel:
                total_skills = len(df_sel_filtered.loc[df_sel_filtered[skill] > 0])
                skill_count.append([skill, total_skills])
            else:
                print(skill + '!!!')

        df_skill = pd.DataFrame(skill_count, columns=['skill', 'count'])
        df_skill = df_skill.sort_values('count')[-15:]
        return list(df_skill['skill'])

    def generate_bar(df_to_agg, top_skills, legend):
        skill_count = []
        for skill in top_skills:
            if skill in df_to_agg:
                total_skills = len(df_to_agg.loc[df_to_agg[skill] > 0])
                skill_count.append([skill, total_skills])
            else:
                print(skill + '!!!')

        df_skill = pd.DataFrame(skill_count, columns=['skill', 'count'])
        df_skill['percent'] = 100*df_skill['count'] / len(df_to_agg)
        g_bar = go.Bar(
            x=df_skill['percent'],
            y=df_skill['skill'] ,
            name=legend,
            orientation='h',
            #marker_color=color,
            customdata = df_skill['count'],
            hovertemplate= '<b>%{y}</b><br>' +
                               'percent: %{x:.2f}%<br>' +
                               'absolute: %{customdata}<extra></extra>'
            )
        return g_bar


    df_sel_filtered = df_sel.loc[df_sel['is_unique_text'] > 0].copy()
    top_skills = get_top_skills(df_sel_filtered)
    last_include = df_sel_filtered['first_online'].max() - relativedelta(months=time_period)
    fig = go.Figure()
    fig.add_trace(generate_bar(df_sel_filtered, top_skills, text_all))
    fig.add_trace(generate_bar(df_sel_filtered.loc[df_sel_filtered['first_online'] >= last_include], top_skills, text_recent))
    fig.update_layout(title="Top 15 Skills - Comparison")
    return fig


def bar_chart_compare(df_sel, title, agg_column,
                      remove_nonunique=True,
                      time_period=6):
    def generate_bar(df_to_agg, legend, agg_column):
        df_to_agg = pd.DataFrame(df_to_agg[agg_column].value_counts()).reset_index()
        total_val = df_to_agg['count'].sum()
        df_to_agg['percent'] = 100*df_to_agg['count'] / total_val
        g_bar = go.Bar(
            x=df_to_agg[agg_column],
            y=df_to_agg['percent'] ,
            name=legend,
            customdata = df_to_agg['count'],
            hovertemplate= '<b>%{x}</b><br>' +
                               'percent: %{y:.2f}%<br>' +
                               'absolute: %{customdata}<extra></extra>'
            )
        return g_bar

    if remove_nonunique:
        df_sel_filtered = df_sel.loc[df_sel['is_unique_text'] > 0].copy()
    else:
        df_sel_filtered = df_sel.copy()
    last_include = df_sel_filtered['first_online'].max() - relativedelta(months=time_period)
    fig = go.Figure()
    fig.add_trace(generate_bar(df_sel_filtered, 'All Vacancies', agg_column))
    fig.add_trace(generate_bar(df_sel_filtered.loc[df_sel_filtered['first_online'] >= last_include],
                               'Recent Vacancies', agg_column))
    fig.update_layout(title=title)
    return fig


layout = dbc.Row(
    children = [
        # Column for user controls
        dbc.Col(html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Br(),
                                dbc.Label("Select Job Type", html_for="job-type"),
                                # Dropdown for job type
                                dcc.Dropdown(
                                    id="job-type-comp",
                                    options=df['job_type'].unique(),
                                    value=[],
                                    multi=True,
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                # Checkboxes for data professions
                                dbc.Checklist(
                                    id="all-types-comp",
                                    options=all_types_options,
                                    value=[],
                                    ),
                            ]
                        ),
                        html.Div([
                            dcc.DatePickerRange(
                                id='time-period-comp',
                                min_date_allowed=str(min(df['first_online']).date()),
                                max_date_allowed=str(max(df['first_online']).date()),
                                start_date=str(min(df['first_online']).date()),
                                end_date=str(max(df['first_online']).date()),
                            ),
                        ]),
                    ],
                ),
                html.Br(),
                html.Div([
                    dbc.Label("Select Comparison Period", html_for="comparison-period"),
                    dbc.RadioItems(
                        id="comparison-period",
                        options=[{'label':'Three months', 'value': 3},
                                 {'label':'Six months', 'value': 6}],
                        value=6,
                    ),
                ]),
                html.Br(),
                html.P(f"Last Update: {df['first_online'].max():%m.%d.%Y}"),
                html.P("Total Vacancies: {:,d}".format(len(df))),
                #html.P(id="total-vacancies"),
                html.P(id='exp-text')
            ], style={"padding-left" : "4px"},
        ), style = {"position": "fixed", "background-color": "#f8f9fa", "top": "4rem", "bottom":0, "width":"20rem"}
        ),
        # Column for app graphs and plots
        dbc.Col([
            dbc.Row([
                create_ban_card("Vacancies Selected: ", "total-vacancies-comp"),
                create_ban_card("Recent Vacancies: ", "vacancies-compared"),
                create_ban_card("Av per week: ", "vacancies-per-week"),
                create_ban_card("Av per week recent: ", "vacancies-per-week-compared")
            ], style = {"text-align": "center"}),
            dbc.Row(
                [dcc.Graph(id="bar-chart-comp")]
            ),
            dbc.Row([dbc.Col([
                    dcc.Graph(id="cloud-comp")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="viz-comp")
                ], width=6),
            ]),
            dbc.Row([dbc.Col([
                dcc.Graph(id="districts-comp")
            ], width=6),
                dbc.Col([
                    dcc.Graph(id="recr-comp")
                ], width=6),
            ])
        ], style = {"margin-left": "21rem"}),
    ], className='dbc'
)


@dash.callback(
    Output("total-vacancies-comp", "children"),
    Output("vacancies-compared", "children"),
    Output("vacancies-per-week", "children"),
    Output("vacancies-per-week-compared", "children"),
    Output("bar-chart-comp", "figure"),
    Output("cloud-comp", "figure"),
    Output("viz-comp", "figure"),
    Output("districts-comp", "figure"),
    Output("recr-comp", "figure"),
    [
        Input("job-type-comp", "value"),
        Input("all-types-comp", "value"),
        Input("time-period-comp", "start_date"),
        Input("time-period-comp", "end_date"),
        Input("comparison-period", "value")
    ],
)
def filter_df(job_type, all_types, start_date, end_date, comparison_period):
    df_selected = df.copy()

    if len(job_type)  > 0:
        df_selected = df_selected.loc[df_selected['job_type'].isin(job_type)]

    if len(all_types) > 0:
        df_selected['total'] = df_selected[all_types].sum(axis=1)
        df_selected = df_selected.loc[df_selected['total'] > 0]

    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)

    df_selected = df_selected.loc[(df_selected['first_online'].dt.date >= start_date) & (df_selected['first_online'].dt.date <= end_date)]

    comparison_earliest = df_selected['first_online'].max() - relativedelta(months=comparison_period)

    days_diff_all = df_selected['first_online'].max() - df_selected['first_online'].min()
    days_diff_all = days_diff_all.days

    days_diff_recent = df_selected['first_online'].max() - comparison_earliest
    days_diff_recent = days_diff_recent.days
    count_without_old = len(df_selected.loc[df_selected['first_online'].notnull()])
    count_recent = len(df_selected.loc[df_selected['first_online'] >= comparison_earliest])

    selected_jobs_string = "{:,d}".format(len(df_selected))
    compared_jobs_string = "{:,d}".format(len(df_selected.loc[df_selected['first_online'] >= comparison_earliest]))
    per_week = "{:.2f}".format(7*count_without_old/days_diff_all)
    per_week_compared = "{:.2f}".format(7*count_recent/days_diff_recent)

    fig_bar = bar_chart_skills(df_selected, time_period=comparison_period)
    fig_cloud = bar_chart_compare(df_selected, time_period=comparison_period,
                                title='Cloud Skills - Comparison', agg_column='cloud_skills')
    fig_viz = bar_chart_compare(df_selected, time_period=comparison_period,
                                 title='Visualization Skills - Comparison', agg_column='viz_tools')
    fig_distr = bar_chart_compare(df_selected, time_period=comparison_period,
                                 title='Districts - Comparison', agg_column='district', remove_nonunique=False)
    fig_recr = bar_chart_compare(df_selected, time_period=comparison_period,
                                 title='Direct Employers - Comparison', agg_column='is_direct', remove_nonunique=False)

    return selected_jobs_string, compared_jobs_string, per_week, per_week_compared, fig_bar, fig_cloud,\
        fig_viz, fig_distr, fig_recr
