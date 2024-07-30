import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_bootstrap_templates
from datetime import date

#import dash_leaflet as dl
#import dash_leaflet.express as dlx

import plotly.express as px
#from plotly import graph_objs as go
#from plotly.tools import make_subplots
#from plotly.subplots import make_subplots
#from datetime import datetime as dt

#dbc_css = "./assets/css/bootstrap.min.css"
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
#dbc_css = "dbc.min.css"


dash_bootstrap_templates.load_figure_template('sandstone')

app = dash.Dash(
    __name__, #meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.SANDSTONE, dbc_css]
)
app.title = "Data Jobs 2024"
server = app.server

df = pd.read_csv('to_analysis_indeed.csv')
df['first_online'] = pd.to_datetime(df['first_online'])
pd.options.mode.chained_assignment = None


all_types_options = [{"label": "Data Science Jobs", "value": "type_ds"},
                     {"label": "Data Analyst Jobs", "value": "type_da"},
                     {"label": "Data Engineer Jobs", "value": "type_de"},
                     {"label": "BI Jobs", "value": "type_bi"},
                     {"label": "AI/ML Jobs", "value": "type_aiml"},]


def generate_bar_chart(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    important_skills = ['A/B Testing', 'AI', 'AWS', 'Apache Airflow', 'Apache Kafka', 'Apache Spark', 'Azure', 'Big Data',
                        'Computer Vision', 'Data Pipelines', 'Data Modeling', 'Data WareHousing', 'Deep Learning', 'Docker',
                        'ETL', 'Financial Analysis', 'GCP', 'Kubernetes', 'Looker', 'MS Excel', 'MS Power BI',
                        'Natural Language Processing', 'NoSQL', 'Machine Learning', 'Pandas', 'PyTorch',
                        'Snowflake', 'SQL', 'Tableau', 'TensorFlow', 'Programing Language', 'Python', 'Java', 'Scala', 'R']
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
    df_skill = df_skill.sort_values(['total', 'skill'], ascending=False)[:30]
    #print(df_skill)

    fig = px.bar(df_skill,
                 x='count',
                 y='skill',
                 color='mandatory',
                 category_orders={"mandatory": ["mandatory", "advantage"],
                                  },
                 )
    fig.update_layout(
        title='Top 15 skills',
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False
    )
    return fig

def generate_line_chart(df_sel):
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_sel['week_num'] = df_sel['first_online'].dt.isocalendar().week
    df_dates = df_sel.loc[df_sel['first_online'] > '2024-01-14']
    df_dates = df_dates.groupby('week_num', as_index=False).agg(jobs_count = ("url", "nunique"))

    fig = px.line(df_dates,
                  x="week_num",
                  y="jobs_count",
                  #color='country'
                  )

    fig.update_layout(
        title='New Vacancies per Week',
        yaxis_title='total_jobs'
    )
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
    fig.update_layout(margin={"t": 0, "b": 0})
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
    fig.update_layout(margin={"t": 0, "b": 0})
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
    fig.update_layout(margin={"t": 0, "b": 0})
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

fig_bar = generate_bar_chart(df)
fig_line = generate_line_chart(df)
fig_pie_district = generate_pie_district(df)
fig_en = generate_single_bar_en(df)
fig_he = generate_single_bar_he(df)
fig_edu = generate_single_bar_degree(df)
#fig_pie_cloud = generate_pie_cloud(df)

# Layout of Dash App
app.layout = html.Div(
    children=[
        dbc.Row([html.H2("Data Jobs 2024"),]),
        dbc.Row(
            #className="row",
            children=[
                # Column for user controls
                dbc.Col(
                    children=[
                        #dbc.Card([
                            html.P("""Select Job Type."""),
                            # Change to side-by-side for mobile layout
                            html.Div(
                                #className="row",
                                children=[
                                    html.Div(
                                        children=[
                                            # Dropdown for job type
                                            dcc.Dropdown(
                                                id="job-type",
                                                options=df['job_type'].unique(),
                                                value=[],
                                                multi=True,
                                                className='dbc'
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        #className="div-for-dropdown",
                                        children=[
                                            # Checkboxes for data professions
                                            dcc.Checklist(
                                                id="all-types",
                                                options=all_types_options,
                                                value=[],
                                                className='dbc'
                                            ),
                                        ],
                                    ),
                                    html.Div([
                                        dcc.DatePickerRange(
                                            id='time-period',
                                            min_date_allowed=date(2024, 1, 11),
                                            max_date_allowed=max(df['first_online']),
                                            #initial_visible_month=date(2017, 8, 5),
                                            #end_date=date(2017, 8, 25)
                                            ),
                                    ]),
                                ],
                            ),
                            html.Br(),
                            html.P("Total Vacancies: " + str(len(df))),
                            html.P(id="total-vacancies")
                        #]),
                    ], width=2
                ),
                # Column for app graphs and plots
                dbc.Col(
                    #className="eight columns div-for-charts bg-grey",
                    children=[
                        #dbc.Row(
                        #    # className="row",
                        #    children=[
                        #
                        #    ]),
                        dbc.Row(
                            #className="row",
                            children=[
                                dbc.Col([dcc.Graph(id="bar_chart", figure=fig_bar)], width=8),
                                dbc.Col([dcc.Graph(id="pie_district", figure=fig_pie_district)], width=4),
                            ]),
                        dbc.Row(
                            #className="row",
                            children=[
                                dbc.Col(html.Div([dcc.Graph(id="line_chart", figure=fig_line)]), width=8),
                                dbc.Col([
                                    dbc.Card([
                                        html.P(id='exp-text'),
                                        dcc.Graph(id="single_bar_en", figure=fig_en),
                                        dcc.Graph(id="single_bar_he", figure=fig_he),
                                        dcc.Graph(id="single_bar_degree", figure=fig_edu)
                                    ])
                                ], width=4)
                            ])
                    ], width=10

                ),
            ],
        ),

    ], className='dbc'
)


#Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("total-vacancies", "children"),
    Output("bar_chart", "figure"),
    Output("line_chart", "figure"),
    Output("pie_district", "figure"),
    Output("exp-text", "children"),
    Output("single_bar_en", "figure"),
    Output("single_bar_he", "figure"),
    Output("single_bar_degree", "figure"),
    [
        Input("job-type", "value"),
        Input("all-types", "value")
    ],
)
def filter_df(job_type, all_types):
    df_selected = df.copy()

    if len(job_type)  > 0:
        df_selected = df_selected.loc[df_selected['job_type'].isin(job_type)]

    if len(all_types) > 0:
        df_selected['total'] = df_selected[all_types].sum(axis=1)
        df_selected = df_selected.loc[df_selected['total'] > 0]

    fig_bar = generate_bar_chart(df_selected)
    fig_line = generate_line_chart(df_selected)
    fig_pie_cloud = generate_pie_district(df_selected)
    fig_en = generate_single_bar_en(df_selected)
    fig_he = generate_single_bar_he(df_selected)
    fig_edu = generate_single_bar_degree(df_selected)

    selected_jobs_string = "Vacancies Selected: {:,d}".format(
        len(df_selected) )

    exp_text = f"average min experience {df_selected['min_experience'].mean():.2f} years"

    return selected_jobs_string, fig_bar, fig_line, fig_pie_cloud, exp_text, fig_en, fig_he, fig_edu


if __name__ == '__main__':
    app.run_server()