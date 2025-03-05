from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import layout 
import query
import sqlite3

# Configuration du thème personnalisé
CUSTOM_THEME = dbc.themes.BOOTSTRAP

app = Dash(
    __name__,
    external_stylesheets=[
        CUSTOM_THEME,
        "https://fonts.googleapis.com/css2?family=Helvetica:wght@400;600&display=swap"
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Dashboard Énergétique"}
    ]
)

# Configuration des styles globaux
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard Énergétique</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: Helvetica, Arial, sans-serif;
                background-color: #f8f9fa;
                color: #2c3e50;
            }
            .dash-dropdown .Select-control {
                border-radius: 4px;
                border: 1px solid #e0e0e0;
            }
            .dash-dropdown .Select-menu-outer {
                border-radius: 0 0 4px 4px;
            }
        </style>
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

query.init_conn_memory()
constraint_name_primaire = query.get_constraint_name_list()

app.layout = layout.create_layout(constraint_name_primaire)

# main-graph-dropdown1 -> main-graph-dropdown2
@app.callback(
    [Output('main-graph-dropdown2', 'options'),
     Output('main-graph-dropdown2', 'value')],
    [Input('main-graph-dropdown1', 'value')]
)
def update_dropdown2(value):
    constraint_name_suppl = query.get_constraint_name_suppl_list(value) 
    return constraint_name_suppl, constraint_name_suppl[0]['value']

# main-graph-dropdown2 -> main-graph-figure
@app.callback(
    [Output('main-graph', 'figure')],
    [Input('main-graph-dropdown2', 'value')],
    [State('main-graph-dropdown1', 'value')]
)
def update_figure(value, value_primaire):
    if value is None or value_primaire is None:
        return [go.Figure()]
    
    fig = query.get_constraint_shadow_figure(value_primaire, value)

    fig.update_layout(
        title=f"{value_primaire} - {value}",
        xaxis_title="Date",
        yaxis_title="Shadow Price"
    )

    return [fig]

# graph2-dropdown -> graph2
@app.callback(
    [Output('graph2', 'figure')],
    [Input('graph2-dropdown', 'value')]
)
def update_figure2(value):
    fig = query.get_constraing_figure_2(value)
    return [fig]

# graph1-dropdown -> graph1
@app.callback(
    [Output('graph1', 'figure')],
    [Input('graph1-dropdown', 'value')]
)
def update_figure3(values):
    print(values)
    fig = query.get_constraint_figure_3(values)
    return [fig]

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8060)