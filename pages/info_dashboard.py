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

layout = html.Div(children=[
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
				html.H3('FUMO11', id='ticker'),
				html.P('Fumo investimentos imobiliários', id='name')
			]),
		html.Div(children=[
			html.H3('R$ 99,99', id='current-price'),
			html.P('▲ 0,10%', id='price-change'),
			]),
		], className='main-div info', id='top-info'),
	# BASIC DATA
	html.Div(children=[
		html.Div(children=[
				html.H4('Segmento'),
				html.H3('Recebíveis imobiliários', id='fund-class'),
			], className='info-div'),
		html.Div(children=[
				html.H4('DY 12M'),
				html.H3('12,02%', id='dy'),
			], className='info-div'),
		html.Div(children=[
				html.H4('Último rendimento'),
				html.H3('R$ 1,00', id='latest-dividend'),
			], className='info-div'),
		html.Div(children=[
				html.H4('Min. 52 Sem.'),
				html.H3('R$ 88,00', id='min-52wk'),
			], className='info-div'),
		html.Div(children=[
				html.H4('Valor Patrimonial'),
				html.H3('R$ 95,00', id='pv-value'),
			], className='info-div'),
		html.Div(children=[
				html.H4('P/VP'),
				html.H3('1,05', id='pv-mv'),
			], className='info-div'),
		html.Div(children=[
				html.H4('Retorno 12M'),
				html.H3('-10,98%', id='1y-return'),
			], className='info-div'),
		html.Div(children=[
				html.H4('Retorno 1M'),
				html.H3('-2,32%', id='1m-return'),
			], className='info-div'),
		], className='main-div info', id='basic-info'),
	html.Footer(children=[
			html.H4('Todas as informações apresentadas por este aplicativo possuem carater informativo e provêm de fontes públicas. O FII Watch não se responsabiliza pelas decisões e caminhos tomados pelo usuário a partir da análise das informações apresentadas.'),
	]),])
