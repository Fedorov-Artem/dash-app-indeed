import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from datetime import date

#import dash_leaflet as dl
#import dash_leaflet.express as dlx

import plotly.express as px
dash.register_page(__name__, path='/', title='Data Jobs in Israel 2024')


df = pd.read_csv('to_analysis_indeed.csv')
df['first_online'] = pd.to_datetime(df['first_online'])
df['last_online'] = pd.to_datetime(df['last_online'])
df['day_diff'] = (df['last_online'] - df['first_online']).dt.days
pd.options.mode.chained_assignment =  None


all_types_options = [{"label": "Data Science Jobs", "value": "type_ds"},
                     {"label": "Data Analyst Jobs", "value": "type_da"},
                     {"label": "Data Engineer Jobs", "value": "type_de"},
                     {"label": "BI Jobs", "value": "type_bi"},
                     {"label": "AI/ML Jobs", "value": "type_aiml"},]


def generate_bar_chart(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    important_skills = ['A/B Testing', 'AI', 'AWS', 'Apache Airflow', 'Apache Kafka', 'Apache Spark', 'Azure', 'Big Data',
                        'Computer Vision', 'Data Pipelines', 'Data Modeling', 'Data WareHousing', 'Data Visualization',
                        'Deep Learning', 'Docker', 'ETL', 'Financial Analysis', 'GCP', 'Hadoop', 'Kubernetes', 'Looker',
                        'MS Excel', 'MS Power BI', 'Natural Language Processing', 'NoSQL', 'Machine Learning', 'Pandas',
                        'PyTorch', 'Snowflake', 'SQL', 'Tableau', 'TensorFlow', 'Programing Language', 'Python', 'Java',
                        'Scala', 'R']
    skill_count = []
    for skill in important_skills:
        if skill in df_sel:
            advantage = len(df_sel.loc[df_sel[skill] == 1])
            mandatory = len(df_sel.loc[df_sel[skill] > 1])
            skill_count.append([skill, advantage, 'advantage'])
            skill_count.append([skill, mandatory, 'mandatory'])
        else:
            print(skill + '!!!')

    df_skill = pd.DataFrame(skill_count, columns=['skill', 'count', 'mandatory'])
    df_skill['total'] = df_skill.groupby('skill')['count'].transform('sum')
    df_skill = df_skill.loc[df_skill['total'] > 0]
    df_skill = df_skill.sort_values(['total', 'skill'])[-30:]
    fig = px.bar(df_skill,
                 x='count',
                 y='skill',
                 color='mandatory',
                 category_orders={"mandatory": ["mandatory", "advantage"],
                                  },
                 )
    fig.update_layout(
        title='Top 15 Skills <br>'
              '<sup>Most commonly mentioned skills, blue bar for mandatory skills, red - for those marked as an advantage.</sup>',
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False
    )
    return fig

def generate_line_chart(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_dates = df_sel.loc[df_sel['first_online'] > '2024-01-14']
    df_dates['week_num'] = df_dates['first_online'].dt.strftime('%U').astype(int)
    df_dates = df_dates.groupby('week_num').agg(
        jobs_count = ("url", "nunique"),
        month_of_last_day = ("first_online", "max")
    )

    fig = px.line(df_dates,
                  x="month_of_last_day",
                  y="jobs_count",
                  )

    fig.update_layout(
        title='New Vacancies per Week',
        yaxis_title=None,
        xaxis_title=None
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b")
    return fig

def generate_single_bar_en(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_sel['English'] = 0
    df_sel.loc[df_sel['languages'].str.contains('English', na=False), 'English'] = 1
    df_sel['x'] = 'English'
    fig = px.histogram(df_sel,
                       y='x',
                       color='English',
                       barnorm='percent',
                       height=75,
                       category_orders={"English": [0, 1]},
                       )
    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False,
    )
    fig.update_xaxes(visible=False)
    fig.update_layout(margin={"t": 0, "b": 0, "r": 0})
    return fig

def generate_single_bar_he(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_sel['Hebrew'] = 0
    df_sel.loc[df_sel['languages'].str.contains('Hebrew', na=False), 'Hebrew'] = 1
    df_sel['x'] = 'Hebrew'
    fig = px.histogram(df_sel,
                       y='x',
                       color='Hebrew',
                       barnorm='percent',
                       height=75,
                       category_orders={"Hebrew": [0, 1]}
                       )
    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False,
    )
    fig.update_xaxes(visible=False)
    fig.update_layout(margin={"t": 0, "b": 0, "r": 0})
    return fig

def generate_single_bar_degree(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_sel['edu'] = 'No Degree Requirements'
    df_sel.loc[df_sel['education'].str.contains('Ph.D.', na=False), 'edu'] = 'Ph.D.'
    df_sel.loc[df_sel['education'].str.contains('MBA', na=False), 'edu'] = 'MBA'
    df_sel.loc[df_sel['education'].str.contains('M.Sc.', na=False), 'edu'] = 'M.Sc.'
    df_sel.loc[df_sel['education'].str.contains('B.Sc.', na=False), 'edu'] = 'B.Sc.'
    df_sel['x'] = 'Degree'
    fig = px.histogram(df_sel,
                       y='x',
                       color='edu',
                       barnorm='percent',
                       height=75,
                       category_orders={"edu": ['No Degree Requirements', 'B.Sc.', 'M.Sc.', 'MBA', 'Ph.D.']}
                       )
    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False,
    )
    fig.update_xaxes(visible=False)
    fig.update_layout(margin={"t": 0, "b": 0, "r": 0})
    return fig

def generate_single_bar_recruter(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_sel['recr'] = 'Recruter Company'
    df_sel.loc[df_sel['is_direct'] == 1, 'recr'] = 'Direct Employer'
    df_sel['x'] = 'Is Direct'
    fig = px.histogram(df_sel,
                       y='x',
                       color='recr',
                       barnorm='percent',
                       height=75,
                       )
    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False,
    )
    fig.update_xaxes(visible=False)
    fig.update_layout(margin={"t": 0, "b": 0, "r": 0})
    return fig

def generate_pie_cloud(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_pie = df_sel.groupby('cloud_skills', as_index=False).agg(jobs_count = ("url", "nunique"))
    fig = px.pie(df_pie,
                 values='jobs_count',
                 names='cloud_skills',
                 title='Cloud Skills',
                 hole=.5
                 )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def generate_pie_viz(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_pie = df_sel.groupby('viz_tools', as_index=False).agg(jobs_count = ("url", "nunique"))
    fig = px.pie(df_pie,
                 values='jobs_count',
                 names='viz_tools',
                 title='Viz Tools',
                 hole=.5
                 )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def generate_pie_district(df_sel):
    df_pie = df_sel.groupby('district', as_index=False).agg(jobs_count = ("url", "nunique"))
    fig = px.pie(df_pie,
                 values='jobs_count',
                 names='district',
                 title='Vacancies by District',
                 hole=.5
                 )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def generate_bar_chart_companies(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_sel = df_sel.loc[df_sel['is_direct'] > 0]
    df_emp = df_sel['company'].value_counts()[:15].reset_index().sort_values('count')
    fig = px.bar(df_emp,
                 x='count',
                 y='company',
                 )
    fig.update_layout(
        title='Top 15 Direct Employers',
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False
    )
    return fig

fig_bar = generate_bar_chart(df)
fig_line = generate_line_chart(df)
fig_pie_district = generate_pie_district(df)
fig_en = generate_single_bar_en(df)
fig_he = generate_single_bar_he(df)
fig_edu = generate_single_bar_degree(df)
fig_recr = generate_single_bar_recruter(df)
#fig_pie_cloud = generate_pie_cloud(df)
fig_pie_viz = generate_pie_viz(df)
fig_bar_companies = generate_bar_chart_companies(df)

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
                                dbc.Label("Select Job Type", html_for="dropdown"),
                                # Dropdown for job type
                                dcc.Dropdown(
                                    id="job-type",
                                    options=df['job_type'].unique(),
                                    value=[],
                                    multi=True,
                                ),
                            ], className='mb-4'
                        ),
                        html.Div(
                            children=[
                                # Checkboxes for data professions
                                dbc.Checklist(
                                    id="all-types",
                                    options=all_types_options,
                                    value=[],
                                    ),
                            ], className='mb-4'
                        ),
                        html.Div([
                            dcc.DatePickerRange(
                                id='time-period',
                                min_date_allowed=str(min(df['first_online']).date()),
                                max_date_allowed=str(max(df['first_online']).date()),
                                start_date=str(min(df['first_online']).date()),
                                end_date=str(max(df['first_online']).date()),
                            ),
                            dbc.Checklist(
                                id="include-older",
                                options=['include older'],
                                value=['include older'],
                            ),
                        ], className='mb-4'),
                    ],
                ),
                html.Br(),
                html.P(f"Last Update: {df['first_online'].max():%m.%d.%Y}"),
                html.P("Total Vacancies: {:,d}".format(len(df))),
                html.P(id="total-vacancies"),
                html.P(id='exp-text')
            ], style={"padding-left" : "4px"},
        ), style = {"position": "fixed", "background-color": "#f8f9fa", "top": "4rem", "bottom":0, "width":"20rem"}
        ),
        # Column for app graphs and plots
        dbc.Col(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col([dcc.Graph(id="bar_chart", figure=fig_bar)], width=8),
                        dbc.Col([dbc.Card([
                            html.H6("Language/Degree Requirements, Employer type", className="card-title"),
                            dcc.Graph(id="single_bar_en", figure=fig_en, config= {'displayModeBar': False}),
                            dcc.Graph(id="single_bar_he", figure=fig_he, config= {'displayModeBar': False}),
                            dcc.Graph(id="single_bar_degree", figure=fig_edu, config= {'displayModeBar': False}),
                            dcc.Graph(id="single_bar_recr", figure=fig_recr, config= {'displayModeBar': False}),
                        ], style = {"top": "1rem"})], width=4),
                    ]),
                dbc.Row(
                    children=[
                        dbc.Col(html.Div([dcc.Graph(id="line_chart", figure=fig_line)]), width=8),
                        dbc.Col([dcc.Graph(id="pie_district", figure=fig_pie_district)], width=4)
                    ]),
                dbc.Row(
                    children=[
                        dbc.Col(html.Div([dcc.Graph(id="bar_companies", figure=fig_bar_companies)]), width=8),
                        dbc.Col([
                            dbc.Col([dcc.Graph(id="pie_viz", figure=fig_pie_viz)]),
                        ], width=4)
                ]),
            ], style = {"margin-left": "21rem"}
        ),
    ], className='dbc'
)

#Update Map Graph based on date-picker, selected data on histogram and location dropdown
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
        Input("time-period", "end_date"),
        Input("include-older", "value")
    ],
)
def filter_df(job_type, all_types, start_date, end_date, include_older):
    df_selected = df.copy()

    if len(job_type)  > 0:
        df_selected = df_selected.loc[df_selected['job_type'].isin(job_type)]

    if len(all_types) > 0:
        df_selected['total'] = df_selected[all_types].sum(axis=1)
        df_selected = df_selected.loc[df_selected['total'] > 0]

    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)

    if len(include_older) > 0:
        df_selected = df_selected.loc[((df_selected['first_online'].dt.date >= start_date) & (df_selected['first_online'].dt.date <= end_date)) |
        df_selected['first_online'].isnull()]
    else:
        df_selected = df_selected.loc[(df_selected['first_online'].dt.date >= start_date) & (df_selected['first_online'].dt.date <= end_date)]

    fig_bar = generate_bar_chart(df_selected)
    fig_line = generate_line_chart(df_selected)
    fig_pie_cloud = generate_pie_district(df_selected)
    fig_en = generate_single_bar_en(df_selected)
    fig_he = generate_single_bar_he(df_selected)
    fig_edu = generate_single_bar_degree(df_selected)
    fig_recr = generate_single_bar_recruter(df_selected)
    fig_bar_companies = generate_bar_chart_companies(df_selected)
    fig_pie_viz = generate_pie_viz(df_selected)

    selected_jobs_string = "Vacancies Selected: {:,d}".format(
        len(df_selected) )

    exp_text = f"Mean required experience: {df_selected['min_experience'].mean():.2f} years"

    return selected_jobs_string, fig_bar, fig_line, fig_pie_cloud, exp_text, fig_en, fig_he, fig_edu, fig_recr,\
           fig_bar_companies, fig_pie_viz
