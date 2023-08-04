from dash import html

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np

def get_delta(current, previous, kind='relative'):
	if kind == 'relative': return current/previous - 1
	else: return current-previous

def indicator_delta(current, previous, kind_delta='relative', prefix='', suffix=''):
	suffix_delta = '%'
	delta = current-previous
	if kind_delta == 'relative': delta = (current/previous - 1) * 100
	else: suffix_delta = ''
	if delta > 0:
		return html.P([
				html.Span('{}{:.2f}{}'.format(prefix, current, suffix)),
				html.Span('▲ {:.2f}{}'.format(delta, suffix_delta), style={'color': 'green'})
			])
	elif delta < 0:
		return html.P([
			html.Span('{}{:.2f}{}'.format(prefix, current, suffix)),
			html.Span('▼ {:.2f}{}'.format(delta, suffix_delta), style={'color': 'red'})
			])
	else:
		return html.P([
			html.Span('{}{:.2f}{} = 0{}'.format(prefix, current, suffix, suffix_delta)),
			])

def price_delta(delta, H3=False):
	if delta > 0:
		if H3 is False: return html.P('▲ {:.2f}%'.format(delta), style={'color': 'green'})
		else: return html.H3('▲ {:.2f}%'.format(delta), style={'color': 'green'})
	elif delta < 0:
		if H3 is False: return html.P('▼ {:.2f}%'.format(delta), style={'color': 'red'})
		else: return html.H3('▼ {:.2f}%'.format(delta), style={'color': 'red'})
	else:
		if H3 is False: return html.P('= 0%'.format(delta))
		else: return html.H3('= 0%'.format(delta))

def line_plot(data, x, y):
	# Create traces
	fig = go.Figure()
	fig.update_layout(margin=dict(l=16, r=16, t=16, b=16), 
		xaxis=dict(showgrid=True, zeroline=False, gridcolor="rgb(80, 80, 80)", griddash='dash'), 
		yaxis=dict(showgrid=True, zeroline=False, gridcolor="rgb(80, 80, 80)"), 
		plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="DIN Alternate",
        showlegend=False,
        )

	fig.add_trace(go.Scatter(x=data[x], y=data[y], mode='lines'))

	return fig