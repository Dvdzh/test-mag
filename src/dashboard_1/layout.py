# src/app/layout.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import query

TEMPLATE = 'plotly_white'

# Définition des styles (repris du dashboard 2)
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

TITLE_STYLE = {
    "font-family": "Helvetica, Arial, sans-serif",
    "font-weight": "bold",
    "font-size": "2.5rem",
    "color": "#2c3e50",
    "margin-bottom": "1rem"
}

SUBTITLE_STYLE = {
    "font-family": "Helvetica, Arial, sans-serif",
    "font-size": "1.2rem",
    "color": "#7f8c8d",
    "line-height": "1.5"
}

BUTTON_STYLE = {
    "font-family": "Helvetica, Arial, sans-serif",
    "font-weight": "600",
    "margin-right": "10px",
    "background-color": "#2c3e50",
    "border": "none"
}

SECTION_HEADER_STYLE = {
    "fontSize": "1.2rem",
    "color": "#2c3e50",
    "fontWeight": "500",
    "marginBottom": "20px",
    "padding": "10px",
    "backgroundColor": "#f8f9fa",
    "borderRadius": "5px",
    "borderLeft": "4px solid #3498db"
}


def create_layout(df_table,
                  df_daily_bar,
                  df_monthly_bar,
                  node_list,
                  start_date = '2024-01-01',
                  end_date = '2024-02-01'):

    # Préparons les données initiales pour les graphiques
    # Prenons les 3 premières paires de nœuds du tableau pour le graphique mensuel
    top_pairs = df_table.head(3)
    
    # Créons une figure initiale pour le graphique mensuel avec ces 3 paires
    fig_monthly = go.Figure()
    
    # Couleurs pour les différentes paires
    colors = ['rgb(55, 83, 109)', 'rgb(26, 118, 255)', 'rgb(220, 20, 60)']
    
    # Préparons les boutons initiaux
    initial_buttons = []
    
    # Ajoutons les 3 premières paires au graphique mensuel
    for i, row in enumerate(top_pairs.itertuples()):
        # Récupérer les données mensuelles pour cette paire
        monthly_data = query.get_nodes_pair_congestion_monthly_bar(row.Node1, row.Node2)
        
        # Conversion explicite des dates
        monthly_data['Date'] = pd.to_datetime(monthly_data['Date'])
        
        # Ajoutons cette paire au graphique
        fig_monthly.add_trace(
            go.Bar(
                name=f'{row.Node1} -> {row.Node2}',
                x=monthly_data['Date'],
                y=monthly_data['Congestion'],
                marker_color=colors[i % len(colors)]
            )
        )
        
        # Créons un bouton pour cette paire
        button_container = html.Div([
            # Bouton principal
            html.Button(
                f'{row.Node1} -> {row.Node2}',
                id={'type': 'path-button', 'index': i},
                style={
                    'padding': '8px 16px',
                    'backgroundColor': colors[i % len(colors)],
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
                id={'type': 'delete-button', 'index': i},
                style={
                    'padding': '8px 12px',
                    'backgroundColor': colors[i % len(colors)],
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
                }
            )
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'center',
        })
        
        initial_buttons.append(button_container)
    
    # Configuration du graphique mensuel
    fig_monthly.update_layout(
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            title='',
            type='date',  # Spécifier le type d'axe comme date
            tickformat='%b %Y',  # Format des dates (mois année)
            tickangle=-45,  # Rotation des étiquettes
            tickmode='auto',
            nticks=12,  # Nombre de graduations souhaitées
            showgrid=True,
            gridcolor='#e0e0e0'
        ),
        yaxis=dict(
            title='Congestion',
            showgrid=True,
            gridcolor='#e0e0e0'
        ),
        margin=dict(l=50, r=50, t=50, b=70),  # Marge inférieure augmentée pour les dates
        plot_bgcolor='white',
    )
    
    # Pour le graphique journalier, prenons les données de la première paire
    # et affichons les données du premier mois disponible
    print("\n", node_list)
    source, sink = node_list[40], node_list[51]
    daily_data = query.get_nodes_pair_congestion_daily_bar(source, sink, "2024-06-01", "2024-06-30")
    fig_daily = go.Figure(
        go.Bar(
            x=daily_data['Date'],
            y=daily_data['Congestion'],
            marker_color=colors[0]
        )
    )
    
    mois = pd.to_datetime(start_date).strftime('%B')
    fig_daily.update_layout(
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

    return html.Div([
        # En-tête avec navigation (reprenant le style du dashboard 2)
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("HOME", id="home-button", style=BUTTON_STYLE, className="mr-1"),
                    dbc.Button("PATHS", id="section1-button", style=BUTTON_STYLE, className="mr-1"),
                    dbc.Button("CONSTRAINTS", id="section2-button", style=BUTTON_STYLE, className="mr-1"),
                ]), 
                width=4
            ),
            dbc.Col(width=7),
        ], justify='center', style={"padding": "1rem 0 0.5rem 0"}),  # Réduction du padding
        
        # Contenu principal
        html.Div([
            # Titre et description
            dbc.Row([
                dbc.Col(html.H1("Congestion Dashboard", style=TITLE_STYLE), width=9),
                dbc.Col(width=2),
            ], justify='center'),
            
            dbc.Row([
                dbc.Col(
                    html.Div(
                        "Visualisation des congestions entre les nœuds du réseau.",
                        style=SUBTITLE_STYLE
                    ), 
                    width=9
                ),
                dbc.Col(width=2)
            ], justify='center'),
            
            html.Br(),
            
            # Barre de recherche déplacée ici, entre le titre et les tableaux
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Div("Recherche de congestion par paire de nœuds", style=SECTION_HEADER_STYLE),
                        dbc.Row([
                            dbc.Col(
                                dcc.Dropdown(
                                    id='search-dropdown-source',
                                    options=[{'label': node, 'value': node} for node in node_list],
                                    placeholder="Source",
                                    style={"marginBottom": "10px", "width": "100%"}
                                ),
                                width=5
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='search-dropdown-sink',
                                    options=[{'label': node, 'value': node} for node in node_list],
                                    placeholder="Destination",
                                    style={"marginBottom": "10px", "width": "100%"}
                                ),
                                width=5
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Search",
                                    id="search-button",
                                    style=BUTTON_STYLE,
                                    className="mr-1"
                                ),
                                width=2
                            )
                        ]),
                    ]),
                    width=12
                )
            ], style={"marginBottom": "20px"}),
            
            # Conteneur pour les boutons de chemins actifs
            dbc.Row([
                dbc.Col(
                    html.Div(
                        id='path-buttons-container',
                        children=initial_buttons,
                        style={
                            'display': 'flex',
                            'flexWrap': 'wrap',
                            'gap': '8px',
                            'marginBottom': '20px'
                        }
                    ),
                    width=12
                )
            ]),
            
            # Panneau de recherche et sélection
            dbc.Row([
                # Panneau de gauche (table)
                dbc.Col(
                    html.Div([
                        html.Div("Top congestions par paires de nœuds", style=SECTION_HEADER_STYLE),
                        dbc.Row([
                            dbc.Col(
                                dcc.DatePickerRange(
                                    id='date-picker-range',
                                    start_date='2024-09-01',
                                    end_date='2024-09-30',
                                    display_format='YYYY-MM-DD',
                                    style={"marginBottom": "10px", "width": "100%"}
                                ),
                                width=8
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='limit-dropdown',
                                    options=[
                                        {'label': '10', 'value': 10},
                                        {'label': '20', 'value': 20},
                                        {'label': '50', 'value': 50},
                                        {'label': '100', 'value': 100}
                                    ],
                                    value=20,
                                    style={"marginBottom": "10px", "width": "100%"}
                                ),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Refresh",
                                    id="refresh-button",
                                    style=BUTTON_STYLE,
                                    className="mr-1"
                                ),
                                width=2
                            )
                        ]),
                        dash_table.DataTable(
                            id='left-panel-table',
                            columns=[
                                {"name": "Source", "id": "Node1"},
                                {"name": "Sink", "id": "Node2"},
                                {"name": "Congestion", "id": "Congestion"}
                            ],
                            data=df_table.to_dict('records'),
                            style_table={
                                'height': '50hv',
                                'overflowY': 'auto',
                                'border': '1px solid #e0e0e0',
                                'borderRadius': '5px'
                            },
                            style_header={
                                'backgroundColor': '#2c3e50',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'textAlign': 'center'
                            },
                            style_cell={
                                'padding': '10px',
                                'textAlign': 'left',
                                'fontFamily': 'Helvetica, Arial, sans-serif'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#f8f9fa'
                                },
                                {
                                    'if': {'state': 'selected'},
                                    'backgroundColor': '#3498db50',
                                    'border': '1px solid #3498db'
                                }
                            ],
                            row_selectable='multi'
                        )
                    ]),
                    width=6
                ),
                
                # Panneau de droite (graphiques)
                dbc.Col(
                    html.Div([
                        # Graphique de congestion mensuelle
                        html.Div([
                            html.Div("Visualisation des congestions mensuelles et journalières", style=SECTION_HEADER_STYLE),
                            dcc.Graph(
                                id='right-panel-graph-1',
                                figure=fig_monthly,
                                config={'displayModeBar': False},
                                style={"height": "450px"}
                            )
                        ]),
                        
                        # Graphique de congestion journalière
                        html.Div([
                            # html.Div("Congestion journalière (cliquer sur un mois ci-dessus)", style=SECTION_HEADER_STYLE),
                            dcc.Graph(
                                id='right-panel-graph-2',
                                figure=fig_daily,
                                config={'displayModeBar': False},
                                style={"height": "450px"}
                            )
                        ])
                    ]),
                    width=6
                )
            ], justify='center'),
            
            html.Br(),
        ], style=CONTENT_STYLE)
    ])

if __name__ == '__main__':
    simple_layout = create_layout(x, y, df)
    # print(simple_layout)