from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context, register_page

import pandas as pd
import numpy as np
import requests
import json

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime as dt

from app import app
from util import get_delta, indicator_delta

import fii

#dash.register_page(__name__)

def yield_indicator(df):
	children = []
	for ticker in df.sort_values(by=['IPCA', 'CDI'], ascending=False)['Ticker'].unique():
		price = fii.market_price(ticker)
		previous = fii.market_previous(ticker)

		prefix = 'CDI+'
		if df.loc[df['Ticker'] == ticker, 'CDI'].isna().any(): prefix = 'IPCA+'

		spread = fii.YIELD_REGR[ticker].predict(np.array(price).reshape(-1, 1))[0]
		children.append(
			html.Div(children=[
				html.P(ticker),
				html.P([
					html.Span('{} {:.2f}%'.format(prefix, spread)),
				]),
				indicator_delta(price, previous, prefix='R$'),
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
			dcc.Link('Tesouro', href='/pages/treasury_dashbord', className='basic-button'),
			html.Button('FIIs', className='basic-button selected')		
		]),
	html.Div(children=[
			html.Div(children=[
				html.Div(id='ref-data', style={'display': 'none'}),
				html.H4('Kinea'),
				html.P('Data referência: {}'.format(fii.YIELD['Ref'].values[0])),
				yield_indicator(fii.YIELD),
			], className='column', id='treasury-div'),
		], className='main-div'),
		#dcc.Graph(id="scatter", config={"displayModeBar": False}, figure=plot_tree_map(ifix))
	html.Footer(children=[
			html.H4('Todas as informações apresentadas por este aplicativo possuem carater informativo e provêm de fontes públicas. O FII Watch não se responsabiliza pelas decisões e caminhos tomados pelo usuário a partir da análise das informações apresentadas.'),
	]),])
