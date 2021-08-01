import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import webbrowser
import plotly.graph_objs as go
import pandas_datareader as web
from datetime import datetime
import pandas as pd

app = dash.Dash()
server = app.server
nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)

options = [{'label': str(nsdq.loc[i]['Name']) + ' ' +
            str(i), 'value': str(i)} for i in nsdq.index]
app.layout = html.Div(
    [
        html.H1('Stock Ticker Dashboard', style={
            'text-align': 'center', 'font-weight': 'bold', 'background': '#0000CD', 'color': 'rgb(173, 216, 230)', 'padding': 20}),
        html.Div([html.Div([html.H3('Select Ticker'),
                            dcc.Dropdown(id='DropDown', options=options, multi=True)],
                           style={'verticalAlign': 'top', 'width': '30%'}),
                  html.Div([html.H3('Select start and end date'),
                            dcc.DatePickerRange(id='date-picker',
                                                min_date_allowed=datetime(
                                                    2018, 1, 1),
                                                max_date_allowed=datetime.today(),
                                                start_date=datetime(
                                                    2019, 1, 1),
                                                end_date=datetime.today())
                            ], style={'marginLeft': '30px'}),
                  html.Div([html.Button(id='button',
                                        n_clicks=0,
                                        children='Submit',
                                        style={'marginLeft': '30px', 'fontSize': '25px', 'marginTop': '45%'})
                            ],
                           style={'display': 'inline-block'}
                           )
                  ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
        html.Br(),
        dcc.Graph(id='Graph')
    ],
    style={'font-family': 'Arial, Roboto, sans-serif'}
)


@app.callback(Output('Graph', 'figure'),
              [Input('button', 'n_clicks')],
              [
              State('DropDown', 'value'),
              State('date-picker', 'start_date'),
              State('date-picker', 'end_date')
              ]
              )
def update_graph(n_clicks, value, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    if value is None or len(value) == 0:
        pass
    else:
        for tic in value:
            df = web.DataReader(tic, "stooq", start, end)
            traces.append({'x': df.index, 'y': df['Close'], 'name': tic})

        fig = {'data': traces,
               'layout': {'title': str(tic)}}
        return fig
    return {'data': [], 'layout': {}}


if __name__ == '__main__':
    app.run_server()