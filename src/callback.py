import pandas as pd
import sqlite3

conn_memory = sqlite3.connect('memory.db')
def apply_filters(date_debut, date_fin, max_rows):
    query = f"SELECT * FROM NODES_CONGESTION_DAILY \
        WHERE Date >= '{date_debut}' AND Date <= '{date_fin}' \
        ORDER BY Congestion DESC \
        LIMIT {max_rows};"
    return query

def update_table(date_debut, date_fin, max_rows):
    query = apply_filters(date_debut, date_fin, max_rows)
    df = pd.read_sql_query(query, conn_memory)
    return df.to_dict('records')

