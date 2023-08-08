from dash import html, dcc

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

def get_annot_template(annot):
	template = go.layout.Template()
	template.layout.annotations = [
	    dict(name="watermark", text=annot, opacity=0.1,
	        font=dict(color="black", size=100), xref="paper", yref="paper",
	        x=0.5, y=0.5, showarrow=False)
	    ]

	return template

def line_plot(data, x, y, figure=True, annot=None):
	# Create traces
	fig = go.Figure()
	if annot is not None: fig.update_layout(template=get_annot_template(annot))
	fig.update_layout(margin=dict(l=16, r=16, t=16, b=16), 
		xaxis=dict(showgrid=True, zeroline=False, gridcolor="rgb(80, 80, 80)", griddash='dash'), 
		yaxis=dict(showgrid=True, zeroline=False, gridcolor="rgb(80, 80, 80)"), 
		plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="DIN Alternate",
        showlegend=False,
        )

	fig.add_trace(go.Scatter(x=data[x], y=data[y], mode='lines'))

	if figure is True: return fig
	else: return dcc.Graph(figure=fig, className='chart')

def pie_plot(data, label, value, figure=True, annot=None):
	# Fake data
	#labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
	#values = [np.random.uniform(0, 1) for i in range(4)]

	#fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
	# Create traces
	fig = go.Figure()
	if annot is not None: fig.update_layout(template=get_annot_template(annot))
	fig.update_layout(margin=dict(l=16, r=16, t=16, b=16), 
		#xaxis=dict(showgrid=True, zeroline=False, gridcolor="rgb(80, 80, 80)", griddash='dash'), 
		#yaxis=dict(showgrid=True, zeroline=False, gridcolor="rgb(80, 80, 80)"), 
		plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="DIN Alternate",
        #showlegend=False,
        )

	fig.add_trace(go.Pie(labels=data[label].values, values=data[value].values))
	fig.update_traces(textposition='inside', textinfo='percent+label')

	if figure is True: return fig
	else: return dcc.Graph(figure=fig, className='chart')	