""" Functions used on home page """
import pandas as pd
import plotly.express as px

from pages.functions.common_elements import important_skills


def generate_bar_chart(df_sel):
    """ bar chart top 15 most commonly mentioned skills """
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    total_len = len(df_sel)
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
    df_skill['percent_dec'] = 100*df_skill['count']/total_len
    df_skill['percent'] = df_skill['percent_dec'].round(1).astype(str) + '%'
    df_skill['total'] = df_skill.groupby('skill')['count'].transform('sum')
    df_skill = df_skill.loc[df_skill['total'] > 0]
    df_skill = df_skill.sort_values(['total', 'skill'])[-30:]
    fig = px.bar(df_skill,
                 x='percent_dec',
                 y='skill',
                 color='mandatory',
                 category_orders={"mandatory": ["mandatory", "advantage"],
                                  },
                 hover_name = "skill",
                 hover_data = {'skill': False,
                               'percent_dec': False,
                               'count': True,
                               'mandatory':True,
                               'percent': True
                               }
                 )
    fig.update_layout(
        title='Top 15 Most Commonly Mentioned Skills',#<br>'
                #'<sup>, blue bar for mandatory skills,
                # red - for those marked as an advantage.</sup>',
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False
    )
    return fig

def generate_line_chart(df_sel):
    """ line chart new vacancies per week """
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_dates = df_sel.loc[df_sel['first_online'] > '2024-01-14']
    df_dates['week_num'] = df_dates['first_online'].dt.strftime('%U').astype(int)
    df_dates.loc[df_dates['first_online'].dt.year == 2025, 'week_num'] += 52
    df_dates.loc[df_dates['first_online'].dt.year == 2026, 'week_num'] += 104
    df_dates = df_dates.groupby('week_num').agg(
        jobs_count = ("url", "nunique"),
        last_day_of_the_week = ("first_online", "max")
    )

    fig = px.line(df_dates,
                  x="last_day_of_the_week",
                  y="jobs_count",
                  )

    fig.update_layout(
        title='New Vacancies per Week',
        yaxis_title=None,
        xaxis_title=None
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%Y-%m-%d")
    return fig

def generate_line_chart_m(df_sel):
    """ line chart new vacancies per week """
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_dates = df_sel.loc[df_sel['first_online'] > '2024-01-31']
    df_dates['month_num'] = df_dates['first_online'].dt.strftime('%m').astype(int)
    df_dates.loc[df_dates['first_online'].dt.year == 2025, 'month_num'] += 12
    df_dates.loc[df_dates['first_online'].dt.year == 2025, 'month_num'] += 24
    df_dates = df_dates.groupby('month_num').agg(
        jobs_count = ("url", "nunique"),
        month = ("first_online", "min")
    )
    df_dates['month'] = df_dates['month'].dt.strftime('%b-%Y')

    fig = px.line(df_dates,
                  x="month",
                  y="jobs_count",
                  )

    fig.update_layout(
        title='New Vacancies per Month',
        yaxis_title=None,
        xaxis_title=None
    )
    return fig

def generate_single_bar_en(df_sel):
    """ single bar chart counting vacancies mentioning English language """
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
    """ single bar chart counting vacancies mentioning Hebrew language """
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
    """ single bar chart counting vacancies mentioning a degree """
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
    """ single bar chart counting vacancies of recruiter companies """
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_sel['recr'] = 'Recruiter Company'
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
    """ pie chart for cloud skills """
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
    """ pie chart for visualization skills """
    df_sel = df_sel.loc[df_sel['is_unique_text'] > 0]
    df_pie = df_sel.groupby('viz_tools', as_index=False).agg(jobs_count = ("url", "nunique"))
    fig = px.pie(df_pie,
                 values='jobs_count',
                 names='viz_tools',
                 title='Visualization Tools',
                 hole=.5
                 )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def generate_pie_district(df_sel):
    """ pie chart for job locations by district """
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
    """ bar chart for largest employer companies """
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
