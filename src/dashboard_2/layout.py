# src/app/layout.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

TEMPLATE = 'plotly_white'

# Définition des styles
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

def create_layout(
        constraint_name_primaire
):
    return html.Div([
        # En-tête avec navigation
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("HOME", id="home-button", style=BUTTON_STYLE, className="mr-1"),
                    dbc.Button("SECTION 1", id="section1-button", style=BUTTON_STYLE, className="mr-1"),
                    dbc.Button("SECTION 2", id="section2-button", style=BUTTON_STYLE, className="mr-1"),
                ]), 
                width=4
            ),
            dbc.Col(width=7),
        ], justify='center', style={"padding": "2rem 0"}),
        
        html.Br(),
        
        # Contenu principal
        html.Div([
            # Titre et description
            dbc.Row([
                dbc.Col(html.H1("Constraint Dashboard", style=TITLE_STYLE), width=9),
                dbc.Col(width=2),
            ], justify='center'),
            
            dbc.Row([
                dbc.Col(
                    html.Div(
                        "Données qui sont dans les tables BINDING_CONSTRAINTS_HOURLY, BINDING_CONSTRAINTS_DAILY ou BINDING_CONSTRAINTS_MONTHLY.",
                        style=SUBTITLE_STYLE
                    ), 
                    width=9
                ),
                dbc.Col(width=2)
            ], justify='center'),
            
            html.Br(),
            
            
            # Grand graphique principal
            dbc.Row([
                dbc.Col(
                    html.Div([
                        # Texte explicatif
                        html.Div(
                            "Lecture des données mensuelles des contraintes",
                            style={
                                "fontSize": "1.2rem",
                                "color": "#2c3e50",
                                "fontWeight": "500",
                                "marginBottom": "20px",
                                "padding": "10px",
                                "backgroundColor": "#f8f9fa",
                                "borderRadius": "5px",
                                "borderLeft": "4px solid #3498db"
                            }
                        ),
                        # Dropdowns en ligne
                        dbc.Row([
                            dbc.Col(
                                dcc.Dropdown(
                                    id='main-graph-dropdown1',
                                    options=constraint_name_primaire,
                                    value='global',
                                    style={"marginBottom": "20px"}
                                ),
                                width=6
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='main-graph-dropdown2',
                                    options=[
                                        {'label': 'Shadow Price', 'value': 'shadow_price'},
                                        {'label': 'Fréquence', 'value': 'frequency'},
                                        {'label': 'Limite', 'value': 'limit'}
                                    ],
                                    value='shadow_price',
                                    style={"marginBottom": "20px"}
                                ),
                                width=6
                            ),
                        ]),
                        dcc.Graph(
                            id='main-graph',
                            config={'displayModeBar': False},
                            style={"height": "400px"}  # Hauteur fixe pour le grand graphique
                        )
                    ]),
                    width=12
                ),
            ], justify='center', style={"marginBottom": "2rem"}),
            
            # Section des trois graphiques
            dbc.Row([
                # Premier graphique
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            id='graph1-dropdown',
                            options=[
                                {'label': 'MA', 'value': 'MA'},
                                {'label': 'FG', 'value': 'FG'},
                                {'label': 'MCE', 'value': 'MCE'}
                            ],
                            multi=True,
                            style={"marginBottom": "20px"}
                        ),
                        dcc.Graph(
                            id='graph1',
                            config={'displayModeBar': False},
                            style={"height": "400px"}  # Hauteur fixe pour les petits graphiques
                        )
                    ]), 
                    width=6
                ),
                # Deuxième graphique
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            id='graph2-dropdown',
                            options=[
                                {'label': 'True', 'value': True},
                                {'label': 'False', 'value': False}
                            ],
                            value=False,
                            style={"marginBottom": "20px"}
                        ),
                        dcc.Graph(
                            id='graph2',
                            config={'displayModeBar': False},
                            style={"height": "400px"}
                        )
                    ]),
                    width=6
                )
            ], justify='center'),
            
            html.Br(),
        ], style=CONTENT_STYLE)
    ])
