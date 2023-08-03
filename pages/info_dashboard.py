from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context, register_page

import pandas as pd
import numpy as np
import requests
import json

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime as dt

from app import app
from util import get_delta, indicator_delta, price_delta

import fii

#dash.register_page(__name__)

def get_layout(symbol='KNIP11'):
	return html.Div(children=[
			html.Header(children=[
					html.H1('FII Watch'),
					html.Div(children=[
						dcc.Link('Tesouro', href='/pages/treasury_dashbord', className='basic-button'),
						dcc.Link('FIIs', href='/pages/fii_dashboard', className='basic-button'),
						html.Button('Info', className='basic-button selected'),
					], style={'height': '100%'}),
				]),
			# TICKER, NAME & PRICE
			html.Div(children=[
				html.Div(children=[
						html.H3(symbol, id='ticker'),
						html.P(fii.INFO.loc[fii.INFO['symbol'] == symbol, 'longName'].values[0], id='name')
					]),
				html.Div(children=[
					html.H3(f"R$ {fii.INFO.loc[fii.INFO['symbol'] == symbol, 'regularMarketPrice'].values[0]: .2f}", id='current-price'),
					price_delta(fii.INFO.loc[fii.INFO['symbol'] == symbol, 'regularMarketChangePercent'].values[0]),
					]),
				], className='main-div info', id='top-info'),
			# BASIC DATA
			html.Div(children=[
				html.Div(children=[
						html.H4('Segmento'),
						html.H3('N/A', id='fund-class'),
					], className='info-div'),
				html.Div(children=[
						html.H4('DY 12M'),
						html.H3('N/A', id='dy'),
					], className='info-div'),
				html.Div(children=[
						html.H4('Último rendimento'),
						html.H3('N/A', id='latest-dividend'),
					], className='info-div'),
				html.Div(children=[
						html.H4('Min. 52 Sem.'),
						html.H3(f"R$ {fii.INFO.loc[fii.INFO['symbol'] == symbol, 'fiftyTwoWeekLow'].values[0]: .2f}", id='min-52wk'),
					], className='info-div'),
				html.Div(children=[
						html.H4('Valor Patrimonial'),
						html.H3('N/A', id='pv-value'),
					], className='info-div'),
				html.Div(children=[
						html.H4('P/VP'),
						html.H3('N/A', id='pv-mv'),
					], className='info-div'),
				html.Div(children=[
						html.H4('Retorno 12M'),
						html.H3('N/A', id='1y-return'),
					], className='info-div'),
				html.Div(children=[
						html.H4('Retorno 1M'),
						html.H3('N/A', id='1m-return'),
					], className='info-div'),
				], className='main-div info', id='basic-info'),
			html.Footer(children=[
					html.H4('Todas as informações apresentadas por este aplicativo possuem carater informativo e provêm de fontes públicas. O FII Watch não se responsabiliza pelas decisões e caminhos tomados pelo usuário a partir da análise das informações apresentadas.'),
			]),])