from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context

from app import app
from pages import fii_dashboard, treasury_dashboard, info_dashboard

import fii

info_tickers_path = [
    f"/pages/info_dashboard/{symbol.lower()}" for symbol in fii.SYMBOLS
]

app.layout = html.Div(children=[
        dcc.Location(id="url", refresh=False), 
        html.Div(id="page-content"),
    ]
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    print(pathname)
    if pathname == "/pages/treasury_dashboard":
        return treasury_dashboard.layout
    elif pathname == "/pages/fii_dashboard":
        return fii_dashboard.layout
    elif pathname == "/pages/info_dashboard":
        return info_dashboard.get_layout()
    elif pathname in info_tickers_path:
        return info_dashboard.get_layout(pathname.split('/')[-1].upper())
    else:
        return treasury_dashboard.layout

if __name__ == "__main__":
    #app.run_server(host="0.0.0.0", debug=False)
    app.run_server(host="127.0.0.1", debug=True)
