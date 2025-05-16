# This is the main page of the dash application
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from datetime import date
from pages.functions.common_elements import df, important_skills, create_ban_card
from pages.functions.common_elements import job_type_compare, data_professions_compare, time_period_compare

from dateutil.relativedelta import relativedelta
from datetime import datetime

from plotly import graph_objs as go

# Define dash app page
dash.register_page(__name__, path='/compare', title='Data Jobs in Israel 2024-2025')

def bar_chart_skills(df_sel,
                     text_all='All Vacancies',
                     text_recent='Recent Vacancies',
                     time_period=6):
    ''' bar chart to compare top 15 most commonly mentioned skills between different time periods '''
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
    ''' function used to visualize multiple comparisons between different time periods '''
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
                html.Div([
                    # user controls similar to those used on main page
                    job_type_compare,
                    data_professions_compare,
                    html.Br(),
                    time_period_compare
                ]),
                html.Br(),
                # select comparison period
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
                # print some stats
                html.P(f"Last Update: {df['first_online'].max():%d %b %Y}"),
                html.P("Total Vacancies: {:,d}".format(len(df))),
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
                    dcc.Graph(id="seniority-comp")
                ], width=6),
            ])
        ], style = {"margin-left": "21rem"}),
    ], className='dbc'
)

@dash.callback(
    Output("time-period-all", "start_date"),
    Output("time-period-all", "end_date"),
    Output("time-period-all", "disabled"),
    [
        Input("time-period-all-radio", "value"),
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
    Output("total-vacancies-comp", "children"),
    Output("vacancies-compared", "children"),
    Output("vacancies-per-week", "children"),
    Output("vacancies-per-week-compared", "children"),
    Output("bar-chart-comp", "figure"),
    Output("cloud-comp", "figure"),
    Output("viz-comp", "figure"),
    Output("districts-comp", "figure"),
    Output("seniority-comp", "figure"),
    [
        Input("job-type-comp", "value"),
        Input("all-types-comp", "value"),
        Input("time-period-all", "start_date"),
        Input("time-period-all", "end_date"),
        Input("comparison-period", "value")
    ],
)
def filter_df(job_type, all_types, start_date, end_date, comparison_period):
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
    df_selected = df_selected.loc[(df_selected['first_online'].dt.date >= start_date) & (df_selected['first_online'].dt.date <= end_date)]

    # format dates for comparison period
    comparison_earliest = df_selected['first_online'].max() - relativedelta(months=comparison_period)
    all_earliest = max(start_date,
                       datetime.strptime('10-01-2024', '%d-%m-%Y').date())
    days_diff_all = df_selected['first_online'].dt.date.max() - all_earliest
    days_diff_all = days_diff_all.days

    days_diff_recent = df_selected['first_online'].max() - comparison_earliest
    days_diff_recent = days_diff_recent.days
    count_without_old = len(df_selected.loc[df_selected['first_online'].dt.date > all_earliest])
    count_recent = len(df_selected.loc[df_selected['first_online'] >= comparison_earliest])

    # strings for BANs
    selected_jobs_string = "{:,d}".format(len(df_selected))
    compared_jobs_string = "{:,d}".format(len(df_selected.loc[df_selected['first_online'] >= comparison_earliest]))
    per_week = "{:.2f}".format(7*count_without_old/days_diff_all)
    per_week_compared = "{:.2f}".format(7*count_recent/days_diff_recent)

    # plotly visualisations
    fig_bar = bar_chart_skills(df_selected, time_period=comparison_period)
    fig_cloud = bar_chart_compare(df_selected, time_period=comparison_period,
                                title='Cloud Skills - Comparison', agg_column='cloud_skills')
    fig_viz = bar_chart_compare(df_selected, time_period=comparison_period,
                                 title='Visualization Skills - Comparison', agg_column='viz_tools')
    fig_distr = bar_chart_compare(df_selected, time_period=comparison_period,
                                 title='Districts - Comparison', agg_column='district', remove_nonunique=False)
    fig_sen = bar_chart_compare(df_selected, time_period=comparison_period,
                                 title='Seniority levels - Comparison', agg_column='job_type')
    return selected_jobs_string, compared_jobs_string, per_week, per_week_compared, fig_bar, fig_cloud,\
        fig_viz, fig_distr, fig_sen
