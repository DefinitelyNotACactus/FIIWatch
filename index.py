from dash import Dash, html, register_page, page_registry, page_container

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
app.title = "FII Watch"

server = app.server

if __name__ == "__main__":
    #app.run_server(host="0.0.0.0", debug=False)
    app.run_server(host="127.0.0.1", debug=True)
