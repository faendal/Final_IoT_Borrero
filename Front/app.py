import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Inicializamos la aplicación de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la aplicación
app.layout = html.Div(
    [
        # Título
        html.Div(
            children=[html.H1("Sistema de Monitoreo - Temperatura y Humedad de una Planta")],
            style={"textAlign": "center", "padding": "10px"},
        ),
        # Imágenes de la planta
        html.Div(
            children=[
                html.Img(
                    src="assets/succulent1.jpg",
                    style={"width": "200px", "margin": "10px"},
                ),
                html.Img(
                    src="assets/succulent2.jpg",
                    style={"width": "200px", "margin": "10px"},
                ),
            ],
            style={"textAlign": "center"},
        ),
        # Navbar
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Temperatura", href="/temperature")),
                dbc.NavItem(dbc.NavLink("Humedad del aire", href="/humidity_air")),
                dbc.NavItem(dbc.NavLink("Humedad de la tierra", href="/humidity_soil")),
            ],
            brand="Escoge una gráfica",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        # Contenedor para las gráficas
        html.Div(id="page-content", style={"padding": "20px"}),
    ]
)


# Callbacks para cambiar de gráficas según el navbar
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/temperature":
        return html.Iframe(
            src="http://localhost:3000/d/temperature-chart",
            style={"width": "100%", "height": "400px"},
        )
    elif pathname == "/humidity_air":
        return html.Iframe(
            src="http://localhost:3000/d/humidity-air-chart",
            style={"width": "100%", "height": "400px"},
        )
    elif pathname == "/humidity_soil":
        return html.Iframe(
            src="http://localhost:3000/d/humidity-soil-chart",
            style={"width": "100%", "height": "400px"},
        )
    else:
        return html.P("Selecciona una gráfica del menú.")


# Iniciar el servidor de Dash
if __name__ == "__main__":
    app.run_server(debug=True)
