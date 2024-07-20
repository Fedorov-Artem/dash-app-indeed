import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_bootstrap_templates

from dash.dependencies import Input, Output
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


all_types_options = [{"label": "Data Science Jobs", "value": "type_ds"},
                     {"label": "Data Analyst Jobs", "value": "type_da"},
                     {"label": "Data Engineer Jobs", "value": "type_de"},]


#def generate_bar_charts(df_all, df_sel):
def generate_bar_chart(df_sel):
    important_skills = ['AI', 'AWS', 'Apache Airflow', 'Apache Spark', 'Azure', 'Big Data', 'Business Analysis',
                        'Business Intelligence', 'Cloud', 'Computer Vision', 'Data Pipelines', 'Data WareHousing', 'Deep Learning',
                        'ETL', 'GCP', 'Kubernetes', 'Looker', 'MS Excel', 'MS Power BI', 'Natural Language Processing', 'NoSQL',
                        'Machine Learning', 'Pandas', 'SQL', 'Tableau', 'Programing Language', 'Python', 'Java', 'Scala', 'R']

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
    df_skill = df_skill.sort_values('total', ascending=False)[:30]

    # fig = make_subplots(rows=1, cols=4, shared_yaxes=True)
    fig = px.bar(df_skill,
                 x='count',
                 y='skill',
                 color='mandatory',
                 category_orders={"mandatory": ["mandatory", "advantage"],
                                  #"smoker": ["Yes", "No"],
                                  #"sex": ["Male", "Female"]
                                  },
                 #orientation='h',
                 #custom_data=[color_col, 'size'],
                 )
    fig.update_layout(
        title='Top 15 skills',
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False
    )
    return fig

def generate_line_chart(df_sel):
    df_sel['first_online'] = pd.to_datetime(df_sel['first_online'])
    df_sel['week_num'] = df_sel['first_online'].dt.isocalendar().week
    df_dates = df_sel.groupby('week_num', as_index=False).agg({"url":"nunique"})
    df_dates = df_dates.loc[df_dates['week_num'] > 3]

    fig = px.line(df_dates,
                  x="week_num",
                  y="url",
                  #color='country'
                  )

    fig.update_layout(
        title='New Vacancies per Week',
        yaxis_title='total_jobs'
    )
    return fig

def generate_pie_cloud(df_sel):
    df_pie = df_sel.groupby('cloud_skills', as_index=False).agg({"url":"count"})
    fig = px.pie(df_pie,
                 values='url',
                 names='cloud_skills',
                 title='Cloud Skills',
                 hole=.5
                 )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def generate_pie_district(df_sel):
    df_pie = df_sel.groupby('district', as_index=False).agg({"url":"count"})
    fig = px.pie(df_pie,
                 values='url',
                 names='district',
                 title='Vacancies by District',
                 hole=.5
                 )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

fig_bar = generate_bar_chart(df)
fig_line = generate_line_chart(df)
fig_pie_district = generate_pie_district(df)
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
                        dbc.Row(
                            # className="row",
                            children=[
                                html.P(id='exp-text')
                            ]),
                        dbc.Row(
                            #className="row",
                            children=[
                                dbc.Col([dcc.Graph(id="bar_chart", figure=fig_bar)], width=8),
                                dbc.Col([dcc.Graph(id="pie_district", figure=fig_pie_district)], width=4),
                            ]),
                        dbc.Row(
                            #className="row",
                            children=[
                                html.Div([dcc.Graph(id="line_chart", figure=fig_line)])
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

    selected_jobs_string = "Vacancies Selected: {:,d}".format(
        len(df_selected) )

    exp_text = f"average min experience {df_selected['min_experience'].mean():.2f} years"

    return selected_jobs_string, fig_bar, fig_line, fig_pie_cloud, exp_text


if __name__ == '__main__':
    app.run_server()