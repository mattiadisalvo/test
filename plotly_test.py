import plotly.graph_objs as go
import os
import pandas as pd
import dash
# from dash import dcc
# from dash import html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# os.chdir('/Users/mattiadisalvo/Documents/RES/EUROSTAT/data/tot')
df = pd.read_csv('migr_resfirst_tot.csv')

app = dash.Dash()

year_options = []
for year in df['year'].unique():
    year_options.append({'label' :str(year), 'value':year})

value_options = [{'label': 'Total', 'value': 'PERMITS'}]
value_options.append({'label':'Work', 'value': 'PERM_WORK'})
value_options.append({'label':'Family reunification', 'value': 'PERM_FAM'})
value_options.append({'label':'Protection', 'value': 'PERM_OTHER'})
value_options.append({'label':'Education', 'value': 'PERM_EDU'})

colors = {
    'background': '#ffffff',
    'text': '#000000'
}

app.layout = html.Div([

            html.H1(
                    children='First time residence permits',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

            html.Div(
                    children='Use the filters below to change year and country of origin, as well '
                             'as reason for issuing a permit'
                             ,
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

            html.P(),

            html.Div([
                # dcc.Dropdown(id='filter_type',
                #              options=[{'label': i, 'value':i} for i in df['variable'].unique()],
                #              value='PERMITS'),

                html.Div([
                    html.Label(['Choose/type reason for permit'], style={'font-weight': 'bold',
                                                                         "text-align": "center",
                                                                         "margin": "auto"}),
                    dcc.Dropdown(id='filter_type',
                                 options=value_options,
                                 value='PERMITS',
                                 style={'width': '55%',
                                        'verticalAlign': "middle",
                                        "margin": "auto"
                                        },
                                 className='justify-content-center'
                                 ),
                    html.P()

                ], style={'width': '33%', 'display': 'inline-block',
                          "text-align": "center"
                          }
                ),

                html.Div([
                    html.Label(['Choose/type country of origin'],
                               style={'font-weight': 'bold', "text-align": "center",  "margin": "auto"}),
                    dcc.Dropdown(id='filter_cit',
                                 options=[{'label': i, 'value': i} for i in df['cit_label'].unique()],
                                 value='Total',
                                 style={'width': '55%',
                                        'verticalAlign': "middle",
                                        "margin": "auto"
                                        }
                                 ),
                    html.P()
                ], style={'width': '33%', 'display': 'inline-block', "text-align": "center"}
                    ),

                html.Div([
                    html.Label(['Choose/type year'], style={'font-weight': 'bold', "text-align": "center", "margin": "auto"}),
                    dcc.Dropdown(id='filter_year',
                                 options=year_options,
                                 value=df['year'].min(),
                                 style={'width': '55%',
                                        'verticalAlign': "middle",
                                        "margin": "auto"
                                        }

                                 )
                ], style={'width': '33%', 'display': 'inline-block',
                          "text-align": "center"
                          }
                   ),
            ], className='justify-content-center'),

    html.Div(
    dcc.Graph(id='feature-graphic',
              style={'width':'75%',
                     'margin':'auto'})
    )
],  className='justify-content-center')

eu_ms = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES',
        'FI', 'FR', 'HR', 'HU', 'IE', 'IT',
       'LT', 'LU', 'LV', 'MT', 'NL',  'PL', 'PT', 'RO', 'SE',
       'SI', 'SK']

@app.callback(Output('feature-graphic', 'figure') ,
              [Input('filter_type','value'),
               Input('filter_cit','value'),
               Input('filter_year','value')
               ])

def update_graph(filter_type, filter_cit, filter_year):
    df_filter = df.loc[
                       (df['cit_label'] == filter_cit) &
                       (df['year'] == filter_year) &
                       (df['variable'] == filter_type) &
                       (df['geo'].isin(eu_ms))]
    return {'data': [go.Bar(x=df_filter['geo'],
                            y=df_filter['value'], name='bar'
                            )],
            'layout': go.Layout(title='First time residence permits',
                                #xaxis={'categoryorder': 'total descending'}
            )

            }

if __name__ == '__main__':
    app.run_server()
