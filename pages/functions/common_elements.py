import pandas as pd
import numpy as np
from dash import dcc, html
import dash_bootstrap_components as dbc

df = pd.read_csv('../../to_analysis_indeed.csv')
df['first_online'] = pd.to_datetime(df['first_online'])
df['last_online'] = pd.to_datetime(df['last_online'])
df['day_diff'] = (df['last_online'] - df['first_online']).dt.days


all_types_options = [{"label": "Data Science Jobs", "value": "type_ds"},
                     {"label": "Data Analyst Jobs", "value": "type_da"},
                     {"label": "Data Engineer Jobs", "value": "type_de"},
                     {"label": "BI Jobs", "value": "type_bi"},
                     {"label": "AI/ML Jobs", "value": "type_aiml"},]

important_skills = ['A/B Testing', 'AI', 'AWS', 'Apache Airflow', 'Apache Kafka', 'Apache Spark',
                    'Apache Hadoop',
                    'Azure', 'Big Data', 'Computer Vision', 'Data Pipelines', 'Data Modeling',
                    'Data WareHousing',
                    'Data Visualization', 'Deep Learning', 'Docker', 'ETL', 'Financial Analysis', 'GCP',
                    'Kubernetes', 'Looker', 'MS Excel', 'MS Power BI', 'Natural Language Processing', 'NoSQL',
                    'Machine Learning', 'Pandas', 'PyTorch', 'Snowflake', 'SQL', 'Tableau', 'TensorFlow',
                    'Programing Language', 'Python', 'Java', 'Scala', 'R']

time_period_options_compare = [{'label': 'All time', 'value': 0},
                               {'label': 'Twelve months', 'value': 12},
                               {'label': 'Six months', 'value': 6},
                               {'label': 'Custom', 'value': -1}]

time_period_options = [{'label': 'All time', 'value': 0},
                       {'label': 'Six months', 'value': 6},
                       {'label': 'Three months', 'value': 3},
                       {'label': 'Custom', 'value': -1}]

def select_job_type(element_id):
    job_type_div = html.Div(
        children=[
            html.Br(),
            dbc.Label("Select Job Type", html_for=element_id),
            # Dropdown for job type
            dcc.Dropdown(
                id=element_id,
                options=df['job_type'].unique(),
                value=[],
                multi=True,
            ),
        ]
    )
    return job_type_div


job_type = select_job_type("job-type")
job_type_compare = select_job_type("job-type-comp")

def select_data_professions(element_id):
    data_professions_div = html.Div(
        children=[
            # Checkboxes for data professions
            dbc.Checklist(
                id=element_id,
                options=all_types_options,
                value=[],
            ),
        ]
    )
    return data_professions_div


data_professions = select_data_professions("all-types")
data_professions_compare = select_data_professions("all-types-comp")

def select_time_period(element_id_radio, element_id_datepicker, raio_dict):
    time_period_div = html.Div([
        dbc.Label("Select Time Period", html_for=element_id_radio),
        dbc.RadioItems(
            id=element_id_radio,
            options=raio_dict,
            value=0,
        ),
        dcc.DatePickerRange(
            id=element_id_datepicker,
            min_date_allowed=str(min(df['first_online']).date()),
            max_date_allowed=str(max(df['first_online']).date()),
            start_date=str(min(df['first_online']).date()),
            end_date=str(max(df['first_online']).date()),
        ),
    ])
    return time_period_div

time_period = select_time_period("time-period-radio",
                                        "time-period",
                                        time_period_options)
time_period_compare = select_time_period("time-period-all-radio",
                                        "time-period-all",
                                        time_period_options_compare)

def create_ban_card(desc_text, value_str, is_static=False):
    if is_static:
        big_string = html.P(value_str, style={"font-size": 24, "line-height": "1em"})
    else:
        big_string = html.P(id=value_str, style={"font-size": 24, "line-height": "1em"})
    ban_card = dbc.Col([
        dbc.Card([
            html.P(desc_text),
            big_string,
        ])
    ], width=3)
    return ban_card