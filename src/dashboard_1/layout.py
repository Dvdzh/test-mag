# src/app/layout.py
from dash import html, dcc, dash_table
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State


# x = np.linspace(0, 10, 100)
# y = np.sin(x)

df = pd.DataFrame([
    {'name': 'John', 'value': 10, 'description': 'Description 1', 'date': '2021-01-01'},
    {'name': 'Jane', 'value': 20, 'description': 'Description 2', 'date': '2021-01-02'},
    {'name': 'Jim', 'value': 30, 'description': 'Description 3', 'date': '2021-01-03'},
    {'name': 'Jill', 'value': 40, 'description': 'Description 4', 'date': '2021-01-04'},
    {'name': 'Jack', 'value': 50, 'description': 'Description 5', 'date': '2021-01-05'},
])

def create_layout(df_table,
                  df_daily_bar,
                  df_monthly_bar,
                  node_list,
                  start_date = '2024-01-01',
                  end_date = '2024-02-01'):


    # random dataframe
    left_panel = html.Div(
        [
            html.Div(
                [
                    html.H1('Most Congested Paths',
                        style={
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'color': '#2c3e50',
                            'margin': '0',
                            'padding': '20px 0',
                        }
                    ),
                ],
                style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'width': '100%',
                }
            ),
            html.Div(
                [
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=start_date,
                        end_date=end_date,
                        style={
                            'backgroundColor': '#ffffff',
                            'border': '1px solid #e2e8f0',
                            'borderRadius': '6px',
                            'fontSize': '14px',
                            'zIndex': '100',
                        },
                        calendar_orientation='horizontal',
                        display_format='YYYY-MM-DD',
                        month_format='MMMM YYYY',
                        clearable=True,
                        with_portal=True,
                        updatemode='bothdates',
                        start_date_placeholder_text='Start Date',
                        end_date_placeholder_text='End Date',
                    ),
                    dcc.Dropdown(
                        id='limit-dropdown',
                        options=[
                            {'label': '10 résultats', 'value': 10},
                            {'label': '20 résultats', 'value': 20},
                            {'label': '50 résultats', 'value': 50}
                        ],
                        value=20,  # valeur par défaut
                        style={
                            'width': '150px',
                            'marginLeft': '15px',
                            'marginRight': '15px',
                        },
                        clearable=False,
                    ),
                    html.Button(
                        [
                            html.I(className="fas fa-sync-alt", style={'marginRight': '8px'}),
                            'Refresh'
                        ],
                        id='refresh-button',
                        n_clicks=0,
                        style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'padding': '10px 20px',
                            'backgroundColor': '#3498db',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '8px',
                            'cursor': 'pointer',
                            'transition': 'all 0.3s ease',
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'boxShadow': '0 2px 4px rgba(52, 152, 219, 0.3)',
                            'width': '120px',
                            'height': '40px',
                        }
                    ),
                ],
                style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'padding': '15px 20px',
                    # 'borderBottom': '1px solid #eef2f7',
                    'width': '100%',
                    'borderRadius': '8px',
                    'marginBottom': '15px',
                    # 'backgroundColor': '#ffffff',
                    # 'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.1)',
                }
            ),
            dash_table.DataTable(
                id='left-panel-table',
                columns=[
                    {'name': col, 'id': col} for col in df_table.columns
                ],
                data=df_table.to_dict('records'),
                style_table={
                    'overflowX': 'auto',
                },
                style_header={
                    'backgroundColor': '#f8fafc',
                    'fontWeight': 'bold',
                    'border': '1px solid #eef2f7',
                    'textAlign': 'left',
                    'padding': '12px 15px',
                    'fontSize': '14px',
                },
                style_cell={
                    'padding': '12px 15px',
                    'textAlign': 'left',
                    'fontFamily': 'system-ui, -apple-system, sans-serif',
                    'fontSize': '13px',
                    'border': '1px solid #eef2f7'
                },
                style_data={
                    'backgroundColor': 'white',
                    'color': '#2c3e50',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f8fafc',
                    },
                    {
                        'if': {'state': 'selected'},
                        'backgroundColor': '#e3f2fd',
                        'border': '1px solid #2196f3',
                    },
                ],
                row_selectable='multi',
                selected_rows=[],
                style_as_list_view=True,
                editable=True,
            ),
        ],
        style={
            'borderRadius': '8px',
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            'display': 'flex',
            'flexDirection': 'column',
            'flex': '2',
            'backgroundColor': 'white',
            'overflow': 'hidden',
            'border': '1px solid #eef2f7',
            'margin': '10px',
            'padding': '20px',
        }
    )
    
    right_panel = html.Div(
        [
            # html.H1('Right Panel'),
            html.Div(
                [
                # html.H1('Graph 1'),
                dcc.Graph(
                    id='right-panel-graph-1',
                    figure=go.Figure(
                        data=go.Bar(
                            x=df_monthly_bar['Date'],
                            y=df_monthly_bar['Congestion'],
                            name='Congestion mensuelle'
                        ),
                        layout=go.Layout(
                            xaxis_title='Date',
                            yaxis_title='Congestion',
                            autosize=True,
                            margin=dict(l=50, r=50, t=50, b=50),
                            clickmode='event+select',
                        )
                    ),
                    config={'displayModeBar': True}
                )
            ],
            style={
                'width': '100%',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
            }
            ),
            html.Div(
                [
                    # html.H1('Graph 2'),
                    dcc.Graph(id='right-panel-graph-2',
                        figure=go.Figure(
                            data=go.Bar(x=df_daily_bar['Date'], y=df_daily_bar['Congestion']),
                                    layout=go.Layout(
                                        xaxis_title='X',
                                        yaxis_title='Y',
                                        autosize=True,
                                        margin=dict(l=50, r=50, t=50, b=50),
                                    )),
                        style={
                        'width': '100%',
                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                    }
                )
            ],
            style={
                'width': '100%',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
            }
            )
        ],
        style={
            # 'backgroundColor': 'red',
            'padding': '10px',
            'margin': '10px',
            'borderRadius': '4px',
            'width': '100%',
            'display': 'flex',
            'flex': '3',
            'flexDirection': 'column',
            'justifyContent': 'center',
            'alignItems': 'center',
        })

    search_div = html.Div(
        [
            # Premier div pour les contrôles de recherche
            html.Div([
                dcc.Dropdown(
                    id='search-dropdown-source',
                    options=[{'label': node, 'value': node} for node in node_list],
                    placeholder='Select a node',
                    clearable=True,
                    searchable=True,
                    value=node_list[4] if node_list else None,
                    style={
                        'width': '100%',
                    }
                ),
                dcc.Dropdown(
                    id='search-dropdown-sink',
                    options=[{'label': node, 'value': node} for node in node_list],
                    placeholder='Select a node',
                    clearable=True,
                    searchable=True,
                    value=node_list[3] if len(node_list) > 1 else node_list[0] if node_list else None,
                    style={
                        'width': '100%',
                    }
                ),
                html.Button(
                    'Search',
                    id='search-button',
                    n_clicks=0,
                    style={
                        'height': '38px',
                        'borderRadius': '4px',
                        'border': '1px solid #ccc',
                        'backgroundColor': '#ffffff',
                        'cursor': 'pointer',
                        'width': '100%',
                    }
                ),
            ],
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'center',
                'alignItems': 'center',
                'gap': '10px',
                'marginBottom': '15px',
            }),

            # Nouveau div pour les boutons de chemins
            html.Div(
                id='path-buttons-container',
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'flexWrap': 'wrap',
                    'gap': '10px',
                    'padding': '10px',
                    'borderTop': '1px solid #eef2f7',
                    'marginTop': '10px',
                }
            ),
        ],
        style={
            'margin': '20px',
            'padding': '15px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
            'display': 'flex',
            'flexDirection': 'column',
            'backgroundColor': 'white',
            'borderRadius': '8px',
        }
    )

    bottom_panel = html.Div(
        [
            left_panel,
            right_panel
        ],
        style={
            'flex': 1,
            'display': 'flex',
            'flexDirection': 'row',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
        }
    )

    return html.Div([
        search_div,
        bottom_panel
    ],
    style={
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100vh',
        }
    )



if __name__ == '__main__':
    simple_layout = create_layout(x, y, df)
    # print(simple_layout)