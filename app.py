from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "FII Watch"

server = app.server

fii_table = pd.read_csv('tabela_fiis.csv', index_col=0)
ifix = fii_table[fii_table['IFIX - Participação Percentual'] > 0]

def plot_tree_map(data):
	fig = px.treemap(data, path=['Categoria', 'Código Negociação'], 
                 values='IFIX - Participação Percentual', 
                 color='Variação no Dia', color_continuous_scale=px.colors.diverging.RdYlGn)

	fig.data[0].customdata = fig.data[0].marker.colors
	fig.data[0].texttemplate = "<b>%{label}</b><br>%{customdata:.2f}%<br>"
	fig.update_layout(height=720)
	return fig

app.layout = html.Div(children=[
		html.Div(children=[
			dcc.Graph(id="scatter", config={"displayModeBar": False}, figure=plot_tree_map(ifix)),
		], className='graph-container'),
	], className='main-div')

if __name__ == '__main__':
    app.run_server(debug=True)