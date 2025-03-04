from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
import sqlite3

import plotly.express as px
import numpy as np
from datetime import datetime

def connect_to_db():
    # TODO @contextmanager
    conn = sqlite3.connect('data/database.db')
    conn_memory = sqlite3.connect(':memory:')
    return conn, conn_memory

def get_nodes_congestion_monthly(start_date, end_date, conn, conn_memory):

    if conn is None or conn_memory is None:
        conn, conn_memory = connect_to_db()

    query = f'SELECT * \
            FROM NODES_CONGESTION_MONTHLY \
        WHERE Date >= "{start_date}" AND Date <= "{end_date}" \
        ORDER BY Congestion DESC;'
    
    df = pd.read_sql_query(query, conn)
    df.to_sql('NODES_CONGESTION_DAILY', conn_memory, if_exists='replace', index=False)
    
    return df

def get_nodes_pair_congestion_table(start_date = '2024-01', 
                              end_date = '2024-02', 
                              limit = 100,
                              conn = None,
                              conn_memory = None):
    
    if conn is None or conn_memory is None:
        conn, conn_memory = connect_to_db()

    # get nodes congestion monthly
    get_nodes_congestion_monthly(start_date, end_date, conn, conn_memory)

    query = f'SELECT DISTINCT \
            a.Date as Date, \
            a.Node as Node1, \
            b.Node as Node2, \
            a.Congestion - b.Congestion as Congestion \
        FROM NODES_CONGESTION_DAILY a \
        CROSS JOIN NODES_CONGESTION_DAILY b \
        WHERE a.Node < b.Node OR a.Node > b.Node \
        ORDER BY Congestion \
        LIMIT {limit};'
    
    df = pd.read_sql_query(query, conn_memory)
    df.to_sql('NODES_PAIR_CONGESTION', conn_memory, if_exists='replace', index=False)

    return df

def get_nodes_pair_congestion_monthly_bar(node_source, node_sink, conn = None, conn_memory = None):
    if conn is None or conn_memory is None:
        conn, conn_memory = connect_to_db()

    # node_source = 'MPS.OSBORN'
    # node_sink = 'WAUE.BEPM.LRSE'

    query = f'SELECT * \
        FROM NODES_CONGESTION_MONTHLY\
        WHERE Node == "{node_source}" ;'
    df = pd.read_sql_query(query, conn)
    df.to_sql('NODES_CONGESTION_MONTHLY_BAR_SOURCE', conn_memory, if_exists='replace', index=False)

    query = f'SELECT * \
            FROM NODES_CONGESTION_MONTHLY\
            WHERE Node == "{node_sink}" ;'
    df = pd.read_sql_query(query, conn)
    df.to_sql('NODES_CONGESTION_MONTHLY_BAR_SINK', conn_memory, if_exists='replace', index=False)

    # TODO limit 
    limit = 100
    query = f'SELECT source.Date, source.Congestion - sink.Congestion as Congestion \
            FROM NODES_CONGESTION_MONTHLY_BAR_SOURCE as sink\
            FULL OUTER JOIN NODES_CONGESTION_MONTHLY_BAR_SINK as source \
            ON source.Date == sink.Date \
            ORDER BY source.Date;'
    df = pd.read_sql_query(query, conn_memory)
    df.to_sql('NODES_PAIR_CONGESTION_MONTHLY', conn_memory, if_exists='replace', index=False)

    return df

def get_nodes_pair_congestion_daily_bar(node_source, node_sink, start_date, end_date, conn = None, conn_memory = None):
    if conn is None or conn_memory is None:
        conn, conn_memory = connect_to_db()

    # start_date = '2024-01-01'
    # end_date = '2024-01-31'

    # node_source = 'MPS.OSBORN'
    # node_sink = 'WAUE.BEPM.LRSE'

    # node_a = 'WAUE.BEPM.LCS1'
    # node_b = 'MPS.OSBORN'

    query = f'SELECT * \
            FROM NODES_CONGESTION_DAILY\
            WHERE Node == "{node_source}" \
            AND Date >= "{start_date}" AND Date <= "{end_date}" ;'
    df = pd.read_sql_query(query, conn)
    df.to_sql('NODES_CONGESTION_DAILY_BAR_SOURCE', conn_memory, if_exists='replace', index=False)

    query = f'SELECT * \
            FROM NODES_CONGESTION_DAILY\
            WHERE Node == "{node_sink}" \
            AND Date >= "{start_date}" AND Date <= "{end_date}" ;'
    df = pd.read_sql_query(query, conn)
    df.to_sql('NODES_CONGESTION_DAILY_BAR_SINK', conn_memory, if_exists='replace', index=False)

    limit = 100
    query = f'SELECT source.Date, source.Congestion - sink.Congestion as Congestion \
            FROM NODES_CONGESTION_DAILY_BAR_SOURCE as sink\
            FULL OUTER JOIN NODES_CONGESTION_DAILY_BAR_SINK as source \
            ON source.Date == sink.Date \
            ORDER BY source.Date;'
    df = pd.read_sql_query(query, conn_memory)
    df.to_sql('NODES_PAIR_CONGESTION_DAILY', conn_memory, if_exists='replace', index=False)

    return df

def get_nodes_list(conn = None, conn_memory = None):
    if conn is None or conn_memory is None:
        conn, conn_memory = connect_to_db()

    query = f'SELECT DISTINCT Node \
        FROM NODES_CONGESTION_MONTHLY;'
    df = pd.read_sql_query(query, conn)
    # print(df)
    # df.to_sql('NODES_CONGESTION_MONTHLY_BAR_SOURCE', conn_memory, if_exists='replace', index=False)
    return df['Node'].tolist()