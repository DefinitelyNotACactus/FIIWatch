from dash import html

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

def price_delta(delta):
	if delta > 0:
		return html.P('▲ {:.2f}%'.format(delta), style={'color': 'green'})
	elif delta < 0:
		return html.P('▼ {:.2f}%'.format(delta), style={'color': 'red'})
	else:
		return html.P('= 0%'.format(delta))