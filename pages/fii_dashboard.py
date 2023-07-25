from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

from datetime import datetime as dt

import treasury as tr

from app import app
from util import get_delta, indicator_delta

def init_regressor(ticker, df):
	regr = LinearRegression()
	if df.loc[df['Ticker'] == ticker, 'CDI'].isna().any():
		regr.fit(df.loc[df['Ticker'] == ticker, 'Valor'].values.reshape(-1, 1), 
        	df.loc[df['Ticker'] == ticker, 'IPCA'].values)
	else:
		regr.fit(df.loc[df['Ticker'] == ticker, 'Valor'].values.reshape(-1, 1), 
        	df.loc[df['Ticker'] == ticker, 'CDI'].values)

	return regr

#fii_table = pd.read_csv('tabela_fiis.csv', index_col=0)
#ifix = fii_table[fii_table['IFIX - Participação Percentual'] > 0]
yield_df = pd.read_csv('data/yield.csv', index_col=0) 
regr = {ticker: init_regressor(ticker, yield_df) for ticker in yield_df['Ticker'].unique()}


split_date = lambda x : [int(s) for s in x.split('-')]

def treasury_indicator(treasury_dict):
	children = []
	for year in treasury_dict.keys():
		children.append(
			html.Div(children=[
				html.P('20{}'.format(year)),
				indicator_delta(treasury_dict[year].iloc[-1]['Taxa Compra Manhã'] * 100, treasury_dict[year].iloc[-2]['Taxa Compra Manhã'] * 100, kind_delta='absolute', suffix='%'),
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

layout = html.Div(children=[
	html.Header(children=[
			html.H1('FII Watch'),
			dcc.Link('Tesouro', href='pages/treasury_dashbord', className='basic-button'),
			html.Button('FIIs', className='basic-button selected')		
		]),
	html.Div(children=[
			html.Div(children=[
				html.Div(id='ref-data', style={'display': 'none'}),
				html.H4('Kinea'),
				html.P('Data referência: {}'.format(tr.LFT_LAST_UPDATE)),
				treasury_indicator(tr.LFT_DICT),
			], className='column', id='treasury-div'),
		], className='main-div'),
		#dcc.Graph(id="scatter", config={"displayModeBar": False}, figure=plot_tree_map(ifix))
	html.Footer(children=[
			html.H4('Todas as informações apresentadas por este aplicativo possuem carater informativo e provêm de fontes públicas. O FII Watch não se responsabiliza pelas decisões e caminhos tomados pelo usuário a partir da análise das informações apresentadas.'),
	]),])
