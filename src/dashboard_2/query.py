from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
import sqlite3

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def connect_to_db():
    conn = sqlite3.connect('data/database.db')
    conn_memory = sqlite3.connect(':memory:')
    return conn, conn_memory

def get_constraint_name_list():
    conn, conn_memory = connect_to_db()
    query = f'SELECT DISTINCT "Constraint Name" \
        FROM BINDING_CONSTRAINTS_HOURLY;'
    df = pd.read_sql_query(query, conn)['Constraint Name'].tolist()
    df_dict = [{'label': name, 'value': name} for name in df]
    return df_dict

def get_constraint_name_suppl_list(constraint_name):
    conn, conn_memory = connect_to_db()
    query = f'SELECT DISTINCT "Monitored Facility" || "Contingent Facility" as "Constraint Name" \
        FROM BINDING_CONSTRAINTS_HOURLY \
        WHERE "Constraint Name" = "{constraint_name}";'
    df = pd.read_sql_query(query, conn)['Constraint Name'].tolist()
    df_dict = [{'label': name, 'value': name} for name in df]   
    if df_dict == []:
        return [{'label': 'Aucune contrainte supplémentaire', 'value': 'Aucune contrainte supplémentaire'}]
    return df_dict

def init_conn_memory():
    conn, conn_memory = connect_to_db()
    print('Initialisation de la base de données en mémoire...')

    query = f'SELECT Interval, "Constraint Name" || " - " || "Monitored Facility" || "Contingent Facility" as "Constraint Name", "Constraint Type", "Shadow Price"\
        FROM BINDING_CONSTRAINTS_HOURLY;'
    df = pd.read_sql_query(query, conn)
    df.to_sql('BINDING_CONSTRAINTS_HOURLY', conn_memory, if_exists='replace', index=False)

    query = f'SELECT Interval, "Constraint Name" || " - " || "Monitored Facility" || "Contingent Facility" as "Constraint Name", "Constraint Type", \
            "Shadow Price", "Contigency Name" \
            FROM BINDING_CONSTRAINTS_HOURLY;'
    df = pd.read_sql_query(query, conn, parse_dates=['Interval'])
    df['Interval'] = pd.to_datetime(df['Interval']) - pd.Timedelta(minutes=30)
    df['Interval'] = pd.to_datetime(df['Interval'].dt.strftime('%Y-%m-%d'))
    df.to_sql('BINDING_CONSTRAINTS_DAILY', conn_memory, if_exists='replace', index=False)

    query = f'SELECT Interval, "Constraint Name" || " - " || "Monitored Facility" || "Contingent Facility" as "Constraint Name", "Constraint Type", \
            "Shadow Price", "Contigency Name" \
            FROM BINDING_CONSTRAINTS_HOURLY;'
    df = pd.read_sql_query(query, conn, parse_dates=['Interval'])
    df['Interval'] = df['Interval'].dt.strftime('%Y-%m')
    df.to_sql('BINDING_CONSTRAINTS_MONTHLY', conn_memory, if_exists='replace', index=False)

    return conn_memory

def get_constraint_shadow_figure(constraint_name_primaire, constraint_name_suppl):
    conn, conn_memory = connect_to_db()
    constraint_name = constraint_name_primaire + ' - ' + constraint_name_suppl

    query = f'SELECT Interval, "Constraint Name" || " - " || "Monitored Facility" || "Contingent Facility" as "Constraint Name", "Constraint Type", \
            "Shadow Price", "Contigency Name" \
            FROM BINDING_CONSTRAINTS_HOURLY;'
    df = pd.read_sql_query(query, conn, parse_dates=['Interval'])
    df['Interval'] = df['Interval'].dt.strftime('%Y-%m')
    df.to_sql('BINDING_CONSTRAINTS_MONTHLY', conn_memory, if_exists='replace', index=False)

    query = f'SELECT * \
        FROM BINDING_CONSTRAINTS_MONTHLY \
        WHERE "Constraint Name" = "{constraint_name}"'
    df = pd.read_sql_query(query, conn_memory)
    df = df.groupby('Interval')['Shadow Price'].sum().reset_index()

    fig = go.Figure()   

    fig.add_trace(
        go.Bar(
            x=df['Interval'],
            y=df['Shadow Price'],
            hovertemplate="%{x}<br>%{y}<extra></extra>",
            marker_color=['#e74c3c' if val == 1 else '#95a5a6' for val in df['Shadow Price']],
            name=''
        )
    )
    return fig

def get_constraing_figure_2(ascending):

    conn_memory = init_conn_memory()

    query = f'SELECT Interval, "Constraint Name", "Constraint Type", "Shadow Price"\
        FROM BINDING_CONSTRAINTS_HOURLY;'
    df = pd.read_sql_query(query, conn_memory, parse_dates=['Interval'])
    df['Shadow Price'] = df['Shadow Price'].astype(float)
    df['Shadow Price'] = df.apply(lambda row: 1 if row['Shadow Price'] != 0 else 0, axis=1)
    df['Interval'] = pd.to_datetime(df['Interval']).dt.strftime('%Y-%m')
    df = df.groupby(['Constraint Name'])['Shadow Price'].sum().reset_index()
    df = df.sort_values(by='Shadow Price', ascending=ascending)
    df = df.head(100)
    df['hover_text'] = df['Constraint Name'] + '\n' + df['Shadow Price'].astype(str)
    # bar plot 
    fig = go.Figure()   

    fig.add_trace(
        go.Bar(
            x=df['Constraint Name'],
            y=df['Shadow Price'],
            hovertemplate="%{x}<br>%{y} jours<extra></extra>",
            marker_color=['#e74c3c' if val == 1 else '#95a5a6' for val in df['Shadow Price']],
            name=''
        )
    )
    # hiding x axis
    fig.update_layout(xaxis_visible=False)

    # y axis : Compteur jour 
    fig.update_layout(yaxis_title='Compteur jour',
                    xaxis_title='',
                    )
    
    return fig

def get_constraint_figure_3(constraint_types):
    print(constraint_types)
    conn_memory = init_conn_memory()

    query = f'SELECT * \
            FROM BINDING_CONSTRAINTS_HOURLY \
            WHERE '
    query += ' or '.join([f'"Constraint Type" == "{constraint_type}"' for constraint_type in constraint_types])
    query += ' ORDER BY "Shadow Price" DESC LIMIT 100'
    df = pd.read_sql_query(query, conn_memory)
    print(df)
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df['Shadow Price'],
            y=df['Constraint Name'],
            # bar width
            width=5,
        )
    )

    # hide y axis
    fig.update_layout(yaxis_visible=False)

    return fig