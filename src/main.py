from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
import sqlite3
import numpy as np

import plotly.graph_objects as go
from layout import create_layout
# from query import get_nodes_pair_congestion_table, get_nodes_pair_congestion_daily_bar, get_nodes_pair_congestion_monthly_bar
import query

app = Dash(__name__)

df_table = query.get_nodes_pair_congestion_table(limit=20)
node_list = query.get_nodes_list()
df_daily_bar = query.get_nodes_pair_congestion_daily_bar(start_date='2024-01-01', end_date='2024-01-31', node_source='AECC_CSWS', node_sink='AECC_CSWS')
df_monthly_bar = query.get_nodes_pair_congestion_monthly_bar(node_source='AECC_CSWS', node_sink='AECC_CSWS')

app.layout = create_layout(df_table, df_daily_bar, df_monthly_bar, node_list)

# @app.callback(
#     Output('left-panel-table', 'data'),
#     [Input('right-panel-graph-1', 'clickData')]
# )
# def update_table(clickData):
#     df = get_nodes_pair_congestion_table(limit=20)
#     return df.to_dict('records')

# df = query.get_nodes_pair_congestion_monthly_bar()

# @app.callback(
#     Output('right-panel-graph-1', 'figure'),
#     [Input('right-panel-graph-1', 'clickData')]
# )
# def update_graph(clickData):
#     fig = go.Figure()
#     fig.add_trace(go.Bar(x=df['Date'], y=df['Congestion']))
#     return fig

# df = query.get_nodes_pair_congestion_daily_bar(start_date='2024-01-01', end_date='2024-01-31')
# @app.callback(
#     Output('right-panel-graph-2', 'figure'),
#     [Input('right-panel-graph-2', 'clickData')]
# )
# def update_graph(clickData):
#     fig = go.Figure()
#     fig.add_trace(go.Bar(x=df['Date'], y=df['Congestion']))
#     return fig

@app.callback(
    Output('right-panel-graph-1', 'figure'),
    Input('search-button', 'n_clicks'),
    State('search-dropdown-source', 'value'),
    State('search-dropdown-sink', 'value'),
    State('right-panel-graph-1', 'figure'),
    allow_duplicate=True,
    prevent_initial_call=True
)
def update_search_bar(nclicks, source_value, sink_value, existing_figure):
    if nclicks == 0:
        return existing_figure
    # print(nclicks, source_value, sink_value)

    # Récupérer les nouvelles données
    df = query.get_nodes_pair_congestion_monthly_bar(source_value, sink_value)
    # print(df.head())

    # Créer ou récupérer la figure existante
    if existing_figure is None:
        fig = go.Figure()
    else:
        fig = go.Figure(existing_figure)

    fig.add_trace(
        go.Bar(
            name=f'{source_value} -> {sink_value}',
            x=df['Date'],  
            y=df['Congestion'], 
            marker_color=f'rgb({np.random.randint(0,255)}, {np.random.randint(0,255)}, {np.random.randint(0,255)})'
        )
    )

    # Mettre à jour la mise en page
    fig.update_layout(
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis_title='',
        yaxis_title='Congestion',
        margin=dict(l=50, r=50, t=50, b=50),
    )

    return fig

@app.callback(
    Output('right-panel-graph-2', 'figure'),  # ou tout autre output que vous souhaitez mettre à jour
    Input('right-panel-graph-1', 'clickData'),
    State('right-panel-graph-1', 'figure'),
    State('right-panel-graph-2', 'figure')
)
def handle_bar_click(click_data, figure, existing_figure):
    if click_data is None:
        return existing_figure
    
    # # Extraction des données du clic
    # clicked_x = point_data['x']  # Le mois cliqué
    # clicked_y = point_data['y']  # La valeur de congestion
    # curve_name = point_data['curveNumber']  # L'index de la série de données
    
    # print(f"Mois cliqué: {clicked_x}")
    # print(f"Valeur: {clicked_y}")
    # print(f"Série: {figure['data'][curve_name]['name']}")
    # print(figure['data'][curve_name]['name'].split(' -> '))
    start_date = pd.to_datetime(click_data['points'][0]['x'])
    end_date = start_date + pd.DateOffset(months=1)
    curveNumber = click_data['points'][0]['curveNumber']
    nodes = figure['data'][curveNumber]['name'].split(' -> ')

    source = nodes[0]
    sink = nodes[1]

    # print(source, sink)
    # print(start_date, end_date)

    # retrouver la couleur du plot 
    color = figure['data'][curveNumber]['marker']['color']
    # print(color)

    df = query.get_nodes_pair_congestion_daily_bar(source, sink, start_date, end_date)
    # print(df.head())
    # print(df.tail())

    fig = go.Figure(go.Bar(x=df['Date'], y=df['Congestion'], marker_color=color))
    return fig

# callback tableau recuperer nom Node 1 et Node 2
# et rajouter bar plot dans right panel graph 1 
@app.callback(
    Output('right-panel-graph-1', 'figure'),
    Input('left-panel-table', 'selected_rows'),
    State('right-panel-graph-1', 'figure'),
    allow_duplicate=True,
    prevent_initial_call=True
)
def update_graph(selected_rows, existing_figure):
    print(selected_rows)
    return existing_figure

    

if __name__ == '__main__':
    app.run_server(debug=True)  