from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context, register_page, page_registry, page_container

#from util import line_plot

import fii

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
app.title = "FII Watch"

server = app.server

buttons = ["bt-quote", "bt-vp", "bt-holders", "bt-earnings", "bt-expenses", "bt-income", "bt-portfolio"]
bt_output_classname = [Output(bt, 'className') for bt in buttons]
bt_input_n_clicks = [Input(bt, 'n_clicks') for bt in buttons]

# Callback: button selected info page
@app.callback(bt_output_classname, bt_input_n_clicks)
def set_active_button(*args):
    ctx = callback_context
    
    if not ctx.triggered or not any(args): return ["basic-button" if x != 0 else "basic-button selected" for x in range(len(buttons))]

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    styles = ["basic-button" if button != button_id else "basic-button selected" for button in buttons]

    return styles

# Callback; update info chart
@app.callback(Output('chart-div', 'children'), bt_input_n_clicks + [Input("symbol-memory", "data")])
def update_info_chart(*args):
    ctx = callback_context
    
    if not ctx.triggered or not any(args): button_id = "bt-quote"
    else: button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "bt-quote": return fii.plot_quotes(args[-1])
    elif button_id == "bt-portfolio": return fii.plot_funds_portfolio(args[-1])
    else: return html.P(button_id)

if __name__ == "__main__":
    #app.run_server(host="0.0.0.0", debug=False)
    app.run_server(host="127.0.0.1", debug=True)