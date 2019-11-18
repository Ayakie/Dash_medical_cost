import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objs as go
import pandas as pd
from dash_table.Format import Format, Scheme, Symbol
from dash.dependencies import Input, Output
import time

external_stylesheets = [
    dbc.themes.FLATLY
]

common_style = {
    'position': 'relative',
    'text-align': 'center',
    'margin': '0 auto'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# データ読み込み、欠損値のある行は削除
# ダウンロードページ：https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00450032&tstat=000001020931&cycle=8&tclass1=000001133083&tclass2=000001133084&stat_infid=000031861532
# https://www.mhlw.go.jp/toukei/saikin/hw/k-iryohi/17/index.html

df_iryouhi_year = pd.read_excel('data/h2901.xls').dropna(thresh=3)

# 必要な列の選択
df_iryouhi_year = df_iryouhi_year.iloc[3:, [2,3,5,7,9,11,12,13]]
df_iryouhi_year.columns = ['年次','医療費計(億円)', '一人当たり医療費(千円)', '国内総生産(GDP)(億円)', '国民所得(NI)(億円)', 'GDPに対する比率(%)', 'NIに対する比率(%)', '総人口(千人)']
df_iryouhi_year['年次'] = range(1954, 2018)

app.layout = html.Div(
    children=[
        html.H1('Dash Visualization: Medical Cost in Japan'),
        html.Div(
            className='container',
            children=[
                dash_table.DataTable(
                    id='table',
                    style_table={
                        'maxHeight': '300',
                        'overflowX': 'scroll'
                    },
                    fixed_rows={'headers': True, 'data': 0},
                    columns=[{'name': i, 'id': i} for i in df_iryouhi_year.columns],
                    data=df_iryouhi_year.to_dict('records')
                )
            ]
        ),
        html.Div(
            className='container',
            children=[
                html.H5('Select two data to visualize',
                        style={'margin-top': '3%'}),
                html.Div(
                    className='d-flex justify-content-center',
                    children=[
                        dcc.Dropdown(
                            id='select-item1',
                            value='医療費計(億円)',
                            options=[{'label': i, 'value': i} for i in df_iryouhi_year.columns[1:]],
                            style={'width': '80%', 'margin': '0 auto'}
                        ),
                        dcc.Dropdown(
                            id='select-item2',
                            value='GDPに対する比率(%)',
                            options=[{'label': i, 'value': i} for i in df_iryouhi_year.columns[1:]],
                            style={'width': '80%', 'margin': '0 auto'}
                        )
                ]),
                html.Div(
                    dcc.Loading(
                        id='loading-1',
                        children=[
                            dcc.Graph(
                                id='output-graph'
                            )
                        ],
                        type='graph' # 'graph', 'cube', 'circle', 'dot'

                    )
                ),
                html.Br(),
                html.Br()
            ]
        )


    ],
    style=common_style
)

@app.callback(
    Output('output-graph', 'figure'),
    [Input('select-item1', 'value'),
     Input('select-item2', 'value')]
)
def input_triggers_spineer(select_value_1, select_value_2):
    time.sleep(1)

    return {
        'data': [go.Bar(
            x = df_iryouhi_year['年次'],
            y = df_iryouhi_year[select_value_1],
            name=select_value_1
        ),
            go.Scatter(
                x = df_iryouhi_year['年次'],
                y = df_iryouhi_year[select_value_2],
                mode='lines',
                line={'width': 3},
                name=select_value_2,
                yaxis='y2'
            )
        ],

        'layout': go.Layout(
            xaxis={'title': '年次'},
            yaxis={'title': select_value_1},
            yaxis2 = {
                'title': select_value_2,
                'side':'right',
                'overlaying': 'y' # これがないと表示されない
            }

        ),
    }

if __name__=='__main__':
    app.run_server(debug=True)