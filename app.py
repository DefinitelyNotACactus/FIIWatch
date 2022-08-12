from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime as dt

import treasury as tr

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "FII Watch"

server = app.server

fii_table = pd.read_csv('tabela_fiis.csv', index_col=0)
ifix = fii_table[fii_table['IFIX - Participação Percentual'] > 0]

def get_delta(current, previous, kind='relative'):
	if kind == 'relative': return current/previous - 1
	else: return current-previous

def indicator_delta(current, previous, kind_delta='relative', prefix='', suffix=''):
	if current > previous:
		return html.P([
				html.Span('{}{:.2f}{} '.format(prefix, current, suffix)),
				html.Span('▲ {:.2f}'.format(current-previous), style={'color': 'green'})
			])
	elif current < previous:
		return html.P([
			html.Span('{}{:.2f}{} '.format(prefix, current, suffix)),
			html.Span('▼ {:.2f}'.format(current-previous), style={'color': 'red'})
			])
	else:
		return html.P([
			html.Span('{}{:.2f}{} = 0'.format(prefix, current, suffix)),
			])

def treasury_indicator(treasury_dict):
	children = []
	for year in treasury_dict.keys():
		children.append(
			html.Div(children=[
				html.P('20{}'.format(year)),
				indicator_delta(treasury_dict[year].iloc[-1]['Taxa Compra Manhã'] * 100, treasury_dict[year].iloc[-2]['Taxa Compra Manhã'] * 100, suffix='%'),
				indicator_delta(treasury_dict[year].iloc[-1]['PU Compra Manhã'], treasury_dict[year].iloc[-2]['PU Compra Manhã'], prefix='R$'),
			], className='column treasury'),
		)
	return html.Div(children=children, className='row')

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
			html.H4('Tesouro Selic'),
			html.P('Data referência: {}'.format(tr.LFT_LAST_UPDATE)),
			treasury_indicator(tr.LFT_DICT),
			html.H4('Tesouro IPCA+'),
			html.P('Data referência: {}'.format(tr.NTNB_LAST_UPDATE)),
			treasury_indicator(tr.NTNB_DICT),
			html.H4('Tesouro Pré-fixado'),
			html.P('Data referência: {}'.format(tr.NTNF_LAST_UPDATE)),
			treasury_indicator(tr.NTNF_DICT),
		], className='column'),
		#dcc.Graph(id="scatter", config={"displayModeBar": False}, figure=plot_tree_map(ifix))
	], className='main-div')

if __name__ == '__main__':
    app.run_server(debug=True)