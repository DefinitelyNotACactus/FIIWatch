from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context, register_page

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime as dt

import treasury as tr

from util import get_delta, indicator_delta

register_page(
    __name__,
    title="FII Watch | Tesouro Direto",
    description="Informações sobre Títulos Públicos",
    path="/pages/treasury_dashboard",
)

register_page(
    __name__,
    title="FII Watch | Tesouro Direto",
    description="Informações sobre Títulos Públicos",
    path="/",
)

def treasury_indicator(kind, treasury_dict):
	children = []
	for year in treasury_dict.keys():
		children.append(
			html.Div(children=[
				html.P('20{}'.format(year)),
				indicator_delta(treasury_dict[year].iloc[-1]['Taxa Compra Manhã'] * 100, treasury_dict[year].iloc[-2]['Taxa Compra Manhã'] * 100, kind_delta='absolute', suffix='%'),
				indicator_delta(treasury_dict[year].iloc[-1]['PU Compra Manhã'], treasury_dict[year].iloc[-2]['PU Compra Manhã'], prefix='R$'),
			], className='column treasury', id='{}-20{}'.format(kind, year)),
		)
	return html.Div(children=children, className='row')

def plot_yield_curve(ntnf, previous=14):
	current_date, previous_date = tr.NTNF_LAST_UPDATE, str(tr.NTNF_DICT[tr.NTNF.sheet_names[0][-2:]].index[-previous]).split(' ')[0]
	x, y, y_previous = np.zeros(len(ntnf)), np.zeros(len(ntnf)), np.zeros(len(ntnf))
	for i, year in enumerate(ntnf.keys()):
		x[i] = int('20{}'.format(year))
		y[i] = float(ntnf[year].iloc[-1]['Taxa Compra Manhã']) * 100
		y_previous[i] = float(ntnf[year].iloc[-previous]['Taxa Compra Manhã']) * 100

	fig = go.Figure()
	fig.update_layout(margin=dict(l=16, r=16, t=16, b=16), 
		xaxis=dict(title='Vencimento', tickmode='array', tickvals=x, showgrid=False, zeroline=False), 
		yaxis=dict(title='Taxa', showticklabels=False, showgrid=False, zeroline=False),
		plot_bgcolor="rgba(203, 203, 212, .3)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="DIN Alternate",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1)
        )

	fig.add_trace(go.Scatter(x=x, y=y, name='Curva de Juros em {}'.format(current_date), line_shape='spline',
			mode='lines+text', text=['{:.2f}%'.format(value) for value in y],  textposition='top center'))
	fig.add_trace(go.Scatter(x=x, y=y_previous, name='Curva de Juros em {}'.format(previous_date), line_shape='spline',
				mode='lines+text', text=['{:.2f}%'.format(value) for value in y_previous],  textposition='top center'))
	return fig

layout = html.Div(children=[
	html.Header(children=[
			html.H1('FII Watch'),
			html.Div(children=[
				html.Button('Tesouro', className='basic-button selected'),
				dcc.Link('FIIs', href='/pages/fii_dashboard', className='basic-button'),
				dcc.Link('Info', href='/pages/info_dashboard/KNIP11', className='basic-button'),
			], style={'height': '100%'}),		
		]),
	html.Div(children=[
			html.Div(children=[
				html.Div(id='ref-data', style={'display': 'none'}),
				html.H4('Tesouro Selic'),
				html.P('Data referência: {}'.format(tr.LFT_LAST_UPDATE)),
				treasury_indicator('lft', tr.LFT_DICT),
				html.H4('Tesouro IPCA+'),
				html.P('Data referência: {}'.format(tr.NTNB_LAST_UPDATE)),
				treasury_indicator('ntnb', tr.NTNB_DICT),
				html.H4('Tesouro Pré-fixado'),
				html.P('Data referência: {}'.format(tr.NTNF_LAST_UPDATE)),
				treasury_indicator('ntnf', tr.NTNF_DICT),
				html.H4('Curva de Juros'),
				html.Div(children=[
					dcc.Graph(id='yield-curve', config={'displayModeBar': False}, figure=plot_yield_curve(tr.NTNF_DICT)),
					], className='column', style={"marginLeft": "0", "position": "relative"}),
				html.Div(id='test-div'),
			], className='column', id='treasury-div'),
		], className='main-div'),
		#dcc.Graph(id="scatter", config={"displayModeBar": False}, figure=plot_tree_map(ifix))
	html.Footer(children=[
			html.H4('Todas as informações apresentadas por este aplicativo possuem carater informativo e provêm de fontes públicas. O FII Watch não se responsabiliza pelas decisões e caminhos tomados pelo usuário a partir da análise das informações apresentadas.'),
	]),])
