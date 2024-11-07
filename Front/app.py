import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from crate import client
import pandas as pd
import plotly.express as px

# Inicializamos la aplicación de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Constantes de Crate db
CRATE_HOST = "crate-db"
CRATE_PORT = "4200"


def obtener_datos(consulta):
    with client.connect(
        f"http://{CRATE_HOST}:{CRATE_PORT}", username="crate", error_trace=True
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        cursor.close()
    return pd.DataFrame(resultado, columns=columns)


# Activar la supresión de excepciones por callback
app.config.suppress_callback_exceptions = True

# Layout de la aplicación
app.layout = html.Div(
    [
        # Monitorización de la URL
        dcc.Location(id="url", refresh=False),
        # Título
        html.Div(
            children=[
                html.H1("Sistema de Monitoreo - Temperatura y Humedad de una Planta")
            ],
            style={"textAlign": "center", "padding": "10px"},
        ),
        html.Hr(),
        # Imágenes de la planta
        html.Div(
            children=[
                html.Img(
                    src="https://raw.githubusercontent.com/faendal/Final_IoT_Borrero/main/Imagenes/Suculenta1.jpeg",
                    style={"width": "200px", "margin": "10px"},
                ),
                html.Img(
                    src="https://raw.githubusercontent.com/faendal/Final_IoT_Borrero/main/Imagenes/Suculenta2.jpeg",
                    style={"width": "200px", "margin": "10px"},
                ),
            ],
            style={"textAlign": "center"},
        ),
        html.Hr(),
        # Navbar
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Temperatura", href="/temperatura")),
                dbc.NavItem(dbc.NavLink("Humedad del aire", href="/humedad_aire")),
                dbc.NavItem(
                    dbc.NavLink("Humedad de la tierra", href="/humedad_tierra")
                ),
            ],
            brand="Escoge una gráfica",
            brand_href="/",
            color="primary",
            dark=True,
        ),
        html.Hr(),
        # Filtro de tiempo
        html.Div(
            children=[
                html.Label("Seleccione el intervalo de tiempo que desea graficar: "),
                dcc.Dropdown(
                    id="time-interval",
                    options=[
                        {"label": "Últimos 5 minutos", "value": 5},
                        {"label": "Últimos 15 minutos", "value": 15},
                        {"label": "Últimos 30 minutos", "value": 30},
                        {"label": "Última hora", "value": 60},
                    ],
                    value=15,
                    clearable=False,
                ),
            ],
            style={"width": "500px", "margin": "0 auto", "padding": "10px"},
        ),
        html.Hr(),
        # Contenedor para las gráficas
        html.Div(id="page-content", style={"padding": "20px"}),
        html.Hr(),
        # Estado de la planta
        html.Div(id="latest-readings", style={"padding": "20px"}),
    ]
)


# Callbacks para cambiar de gráficas según el navbar
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"), Input("time-interval", "value")],
)
def display_page(pathname, intervalo):
    now = pd.Timestamp.now()
    tiempo_inicio = int((now - pd.Timedelta(minutes=intervalo)).timestamp() * 1000)
    if pathname == "/temperatura":
        df = obtener_datos(
            f'SELECT entity_id, time_index, temperatura FROM "doc"."etsensor_proyecto" WHERE time_index >= {tiempo_inicio} ORDER BY time_index DESC;'
        )
        df["time_index"] = pd.to_datetime(df["time_index"], unit="ms").dt.strftime(
            "%d/%m/%Y %H:%M"
        )
        df["time_index"] = df["time_index"].apply(
            lambda x: pd.to_datetime(x) - pd.Timedelta(hours=5)
        )
        df = df.sort_values(by="time_index")
        fig = px.line(
            df,
            x="time_index",
            y="temperatura",
            title="Temperatura",
            labels={"time_index": "Tiempo", "temperatura": "Temperatura (°C)"},
        )
        return dcc.Graph(figure=fig)
    elif pathname == "/humedad_aire":
        df = obtener_datos(
            f'SELECT entity_id, time_index, humedad_aire FROM "doc"."etsensor_proyecto" WHERE time_index >= {tiempo_inicio} ORDER BY time_index DESC;'
        )
        df["time_index"] = pd.to_datetime(df["time_index"], unit="ms").dt.strftime(
            "%d/%m/%Y %H:%M"
        )
        df["time_index"] = df["time_index"].apply(
            lambda x: pd.to_datetime(x) - pd.Timedelta(hours=5)
        )
        df = df.sort_values(by="time_index")
        fig = px.line(
            df,
            x="time_index",
            y="humedad_aire",
            title="Humedad del Aire",
            labels={"time_index": "Tiempo", "humedad_aire": "Humedad (%)"},
        )
        return dcc.Graph(figure=fig)
    elif pathname == "/humedad_tierra":
        df = obtener_datos(
            f'SELECT entity_id, time_index, humedad_tierra FROM "doc"."etsensor_proyecto" WHERE time_index >= {tiempo_inicio} ORDER BY time_index DESC;'
        )
        df["time_index"] = pd.to_datetime(df["time_index"], unit="ms").dt.strftime(
            "%d/%m/%Y %H:%M"
        )
        df["time_index"] = df["time_index"].apply(
            lambda x: pd.to_datetime(x) - pd.Timedelta(hours=5)
        )
        df = df.sort_values(by="time_index")
        fig = px.line(
            df,
            x="time_index",
            y="humedad_tierra",
            title="Humedad de la Tierra",
            labels={"time_index": "Tiempo", "humedad_tierra": "Humedad (%)"},
        )
        return dcc.Graph(figure=fig)
    else:
        return html.P("Selecciona una gráfica del menú.")


@app.callback(Output("latest-readings", "children"), [Input("time-interval", "value")])
def mostrar_ultimos_valores(intervalo):
    df = obtener_datos(
        'SELECT entity_id, time_index, temperatura, humedad_aire, humedad_tierra FROM "doc"."etsensor_proyecto" ORDER BY time_index DESC LIMIT 1;'
    )
    if not df.empty:
        last_temp = df["temperatura"].iloc[0]
        last_hum_ai = df["humedad_aire"].iloc[0]
        last_hum_ti = df["humedad_tierra"].iloc[0]
        if last_temp > 28:
            if last_hum_ai > 70:
                status_msg = "Alerta: Riesgo de hongos. Bajar la humedad"
            elif last_hum_ai < 50:
                status_msg = "Alerta: Riesgo de estrés hídrico. Regar planta"
            else:
                status_msg = "Condiciones normales"
        elif last_temp < 10:
            if last_hum_ai > 50:
                status_msg = (
                    "Alerta: Riesgo de quemadura por frío. Dar calor a la planta"
                )
            elif last_hum_ai < 10:
                status_msg = "Alerta: Riesgo de daño celular. Dar calor a la planta"
            else:
                status_msg = "Condiciones normales"
        else:
            status_msg = "Condiciones normales"
        return html.Div(
            [
                html.H4("Últimos valores registrados:"),
                html.P(f"Temperatura: {last_temp} °C"),
                html.P(f"Humedad del aire: {last_hum_ai} %"),
                html.P(f"Humedad de la tierra: {last_hum_ti} %"),
                html.Hr(),
                html.H5("Estado de la planta: "),
                html.P(
                    status_msg,
                    style={"color": "red" if "Alerta" in status_msg else "green"},
                ),
            ]
        )
    else:
        return html.P("No hay datos disponibles")


# Iniciar el servidor de Dash
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=80, debug=True)
