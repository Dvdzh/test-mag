from dash import Dash, html, dcc, callback, Output, Input, State
import dash
import pandas as pd
import sqlite3
import numpy as np
import json
from dash.dependencies import ALL
import time
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from layout import create_layout
# from query import get_nodes_pair_congestion_table, get_nodes_pair_congestion_daily_bar, get_nodes_pair_congestion_monthly_bar
import query

# Configuration du thème personnalisé (repris du dashboard 2)
CUSTOM_THEME = dbc.themes.BOOTSTRAP

app = Dash(
    __name__,
    external_stylesheets=[
        CUSTOM_THEME,
        "https://fonts.googleapis.com/css2?family=Helvetica:wght@400;600&display=swap"
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Dashboard Congestion"}
    ]
)

# Configuration des styles globaux (repris du dashboard 2)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard Congestion</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="/assets/styles.css">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Chargement des données initiales
df_table = query.get_nodes_pair_congestion_table(start_date='2024-09-01', end_date='2024-09-30', limit=20)
node_list = query.get_nodes_list()
df_daily_bar = query.get_nodes_pair_congestion_daily_bar(start_date='2024-01-01', end_date='2024-01-31', node_source='AECC_CSWS', node_sink='AECC_CSWS')
df_monthly_bar = query.get_nodes_pair_congestion_monthly_bar(node_source='AECC_CSWS', node_sink='AECC_CSWS')

pair_list = [
    ["BEP_M_TS_NPPD", "BEPM_TS_NPPD"],
    ["CSWCOMANCHE1", "CSWSOUTHWESTERN2"],
    ["CSWS.TNSK.GREENCNTY2", "CANADIAN_HILLS_2"],
    ["OMPA_PONCATY_1_3", "CSWS.7CBY.7CBYWIND"],
    ["AECC_FITZHUGH", "AECC_ELKINS"],
    ["BRAZ", "CSWATTISON1"],
    ["SEILKCPS.COMANCHE", "CANADIAN_HILLS_2"],
    ["CSWS.TNSK.GREENCNTY2", "CSWKNXOLEES"]
]
app.layout = create_layout(df_table, df_daily_bar, df_monthly_bar, node_list)

@app.callback(
    [
        Output('right-panel-graph-1', 'figure', allow_duplicate=True),
        Output('path-buttons-container', 'children', allow_duplicate=True)
    ],
    Input('search-button', 'n_clicks'),
    [
        State('search-dropdown-source', 'value'),
        State('search-dropdown-sink', 'value'),
        State('right-panel-graph-1', 'figure'),
        State('path-buttons-container', 'children')
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)
def update_search_bar(nclicks, source_value, sink_value, existing_figure, existing_buttons):
    if nclicks == 0:
        return existing_figure, existing_buttons

    # Récupérer les données et mettre à jour le graphique
    df = query.get_nodes_pair_congestion_monthly_bar(source_value, sink_value)
    
    if existing_figure is None:
        fig = go.Figure()
    else:
        fig = go.Figure(existing_figure)

    # Générer une couleur aléatoire
    color = f'rgb({np.random.randint(0,255)}, {np.random.randint(0,255)}, {np.random.randint(0,255)})'
    
    fig.add_trace(
        go.Bar(
            name=f'{source_value} -> {sink_value}',
            x=df['Date'],
            y=df['Congestion'],
            marker_color=color
        )
    )

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

    # Créer un conteneur pour le bouton et la croix
    button_container = html.Div([
        # Bouton principal
        html.Button(
            f'{source_value} -> {sink_value}',
            id={'type': 'path-button', 'index': nclicks},
            style={
                'padding': '8px 16px',
                'backgroundColor': color,
                'color': 'white',
                'border': 'none',
                'borderRadius': '6px 0 0 6px',  # Arrondi uniquement à gauche
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': '500',
                'transition': 'opacity 0.3s ease',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                'marginRight': '0',
            }
        ),
        # Bouton de suppression (croix)
        html.Button(
            '×',  # Symbole croix
            id={'type': 'delete-button', 'index': nclicks},
            style={
                'padding': '8px 12px',
                'backgroundColor': color,
                'color': 'white',
                'border': 'none',
                'borderRadius': '0 6px 6px 0',  # Arrondi uniquement à droite
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': 'bold',
                'transition': 'opacity 0.3s ease',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                'marginLeft': '1px',
                'opacity': '0.8',
                'hover': {
                    'opacity': '1'
                }
            }
        )
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'center',
    })

    # Ajouter le nouveau conteneur à la liste existante
    if existing_buttons is None:
        buttons = [button_container]
    else:
        buttons = existing_buttons + [button_container]

    return fig, buttons

# Callback pour gérer la suppression des boutons
@app.callback(
    [
        Output('right-panel-graph-1', 'figure', allow_duplicate=True),
        Output('path-buttons-container', 'children', allow_duplicate=True)
    ],
    Input({'type': 'delete-button', 'index': ALL}, 'n_clicks'),
    [
        State('right-panel-graph-1', 'figure'),
        State('path-buttons-container', 'children')
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)
def handle_delete_button_click(n_clicks, figure, buttons):

    # print("\n")
    # for button in buttons:
    #     button_id = button['props']['children'][0]['props']['id']['index']
    #     croix_id = button['props']['children'][1]['props']['id']['index']

    #     print(button_id)
    #     print(croix_id)

    if not any(n_clicks) or figure is None:
        return dash.no_update, dash.no_update

    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update

    # Récupérer l'index du bouton cliqué
    # print("\n")
    # print(ctx.triggered[0]['prop_id'])  
    button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
    clicked_index = button_id['index']

    # Créer une nouvelle figure sans la trace supprimée
    fig = go.Figure(figure)
    fig.data = tuple(trace for i, trace in enumerate(fig.data) if i != clicked_index)

    # Mettre à jour la liste des boutons
    updated_buttons = [button for i, button in enumerate(buttons) if i != clicked_index]

    # Mettre à jour les indices des boutons restants
    for i, button in enumerate(updated_buttons):
        # print(button)
        button['props']['children'][0]['props']['id']['index'] = i  # Mettre à jour l'index du bouton principal
        button['props']['children'][1]['props']['id']['index'] = i  # Mettre à jour l'index du bouton de suppression


    return fig, updated_buttons

@app.callback(
    [
        Output('right-panel-graph-1', 'figure', allow_duplicate=True),
        Output('path-buttons-container', 'children', allow_duplicate=True)
    ],
    [Input('left-panel-table', 'selected_rows')],
    [
        State('left-panel-table', 'data'),
        State('right-panel-graph-1', 'figure'),
        State('path-buttons-container', 'children')
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)
def update_graph_from_table(selected_rows, table_data, existing_figure, existing_buttons):
    # print(selected_rows)
    if not selected_rows:
        return dash.no_update, dash.no_update
    
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update
    
    # Récupérer la dernière ligne sélectionnée
    latest_selected = selected_rows[-1]
    row_data = table_data[latest_selected]
    # print("\n")
    # print(row_data)
    # Extraire les nœuds source et destination
    source_node = row_data['Node1']
    sink_node = row_data['Node2']

    # Récupérer les données pour le graphique
    df = query.get_nodes_pair_congestion_monthly_bar(source_node, sink_node)
    
    if existing_figure is None:
        fig = go.Figure()
    else:
        fig = go.Figure(existing_figure)

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Congestion',
        margin=dict(l=50, r=50, t=50, b=50),
    )

    # Générer une couleur aléatoire
    color = f'rgb({np.random.randint(0,255)}, {np.random.randint(0,255)}, {np.random.randint(0,255)})'
    
    # Ajouter la nouvelle trace
    fig.add_trace(
        go.Bar(
            name=f'{source_node} -> {sink_node}',
            x=df['Date'],
            y=df['Congestion'],
            marker_color=color
        )
    )

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

    # Créer un nouveau bouton pour le chemin
    button_container = html.Div([
        html.Button(
            f'{source_node} -> {sink_node}',
            id={'type': 'path-button', 'index': len(fig.data) - 1},
            style={
                'padding': '8px 16px',
                'backgroundColor': color,
                'color': 'white',
                'border': 'none',
                'borderRadius': '6px 0 0 6px',
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': '500',
                'transition': 'opacity 0.3s ease',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                'marginRight': '0',
            }
        ),
        html.Button(
            '×',
            id={'type': 'delete-button', 'index': len(fig.data) - 1},
            style={
                'padding': '8px 12px',
                'backgroundColor': color,
                'color': 'white',
                'border': 'none',
                'borderRadius': '0 6px 6px 0',
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': 'bold',
                'transition': 'opacity 0.3s ease',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                'marginLeft': '1px',
                'opacity': '0.8',
            }
        )
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'center',
    })

    # Ajouter le nouveau bouton à la liste existante
    if existing_buttons is None:
        buttons = [button_container]
    else:
        buttons = existing_buttons + [button_container]

    return fig, buttons

# Callback pour gérer les clics sur les boutons
@app.callback(
    [
        Output('right-panel-graph-1', 'figure', allow_duplicate=True),
        Output('path-buttons-container', 'children', allow_duplicate=True)
    ],
    Input({'type': 'path-button', 'index': ALL}, 'n_clicks'),
    [
        State('right-panel-graph-1', 'figure'),
        State('path-buttons-container', 'children')
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)
def handle_path_button_click(n_clicks, figure, buttons):
    if not any(n_clicks) or figure is None:
        return dash.no_update, dash.no_update

    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update

    button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
    clicked_index = button_id['index']

    # Mettre à jour la visibilité de la trace correspondante
    fig = go.Figure(figure)
    fig.data[clicked_index].visible = not fig.data[clicked_index].visible

    # Mettre à jour la liste des boutons
    updated_buttons = [button for i, button in enumerate(buttons) if i != clicked_index]

    # Mettre à jour les indices des boutons restants
    for i, button in enumerate(updated_buttons):
        button['props']['children'][0]['id']['index'] = i  # Mettre à jour l'index du bouton principal
        button['props']['children'][1]['id']['index'] = i  # Mettre à jour l'index du bouton de suppression

    # print(buttons)
    return fig, buttons

# update table from datepicker date
@app.callback(
    Output('left-panel-table', 'data', allow_duplicate=True),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'),
    State('limit-dropdown', 'value'),
    Input('refresh-button', 'n_clicks'),
    prevent_initial_call=True
)
def update_table(start_date, end_date, limit, n_clicks):
    # print("\n")
    # print(start_date, end_date, limit)
    start_time = time.time()
    if n_clicks == 0:
        return df_table.to_dict('records')
    df = query.get_nodes_pair_congestion_table(start_date, end_date, limit=limit)
    # print(df.head())
    # print(df.tail())
    # print("finished")
    end_time = time.time()
    # print(f"Time taken: {end_time - start_time} seconds")

    return df.to_dict('records')

@app.callback(
    Output('right-panel-graph-2', 'figure', allow_duplicate=True),  
    Input('right-panel-graph-1', 'clickData'),
    State('right-panel-graph-1', 'figure'),
    State('right-panel-graph-2', 'figure'),
    prevent_initial_call=True
)
def handle_bar_click(click_data, figure, existing_figure):
    if click_data is None:
        return existing_figure

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

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Congestion',
        margin=dict(l=50, r=50, t=50, b=50),
    )   

    mois = start_date.strftime('%B')

    # Configuration du graphique journalier
    fig.update_layout(
        xaxis=dict(
            title='',
            type='date',
            tickformat='%d %b',  # Format jour mois
            tickangle=-45,
            showgrid=True,
            gridcolor='#e0e0e0'
        ),
        yaxis=dict(
            title='Congestion',
            showgrid=True,
            gridcolor='#e0e0e0'
        ),
        title=f'{source} -> {sink}, {mois}',
        title_font_size=15,
        # title position
        title_x=0.5,
        title_y=0.9,
        margin=dict(l=50, r=50, t=40, b=70),
        plot_bgcolor='white',
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
