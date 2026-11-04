from datetime import date, datetime
import math

import requests

from dominio.indicador import Indicador

URL_DOLAR = "https://mindicador.cl/api/dolar"
TIMEOUT_CONEXION = 5
TIMEOUT_LECTURA = 15


IndicadorDolar = Indicador
FUENTE_DOLAR = "mindicador.cl"


def _parsear_fecha(valor):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError("Cada registro debe incluir una fecha válida.")
    texto = valor.strip()
    try:
        return datetime.fromisoformat(texto.replace("Z", "+00:00")).date()
    except ValueError as exc:
        raise ValueError("Cada registro debe incluir una fecha válida.") from exc


def validar_respuesta_dolar(respuesta):
    if not isinstance(respuesta, dict):
        raise ValueError("La respuesta de indicadores debe ser un objeto JSON.")
    if respuesta.get("codigo") != "dolar":
        raise ValueError("La respuesta no corresponde al indicador dólar.")
    if respuesta.get("unidad_medida") != "Pesos":
        raise ValueError("La unidad del indicador debe ser Pesos.")

    serie = respuesta.get("serie")
    if not isinstance(serie, list) or not serie:
        raise ValueError("La respuesta no contiene una serie de datos.")

    registros = []
    for registro in serie:
        if not isinstance(registro, dict):
            raise ValueError("Cada registro de la serie debe ser un objeto JSON.")
        fecha = _parsear_fecha(registro.get("fecha"))
        valor = registro.get("valor")
        if isinstance(valor, bool):
            raise ValueError("El valor del dólar debe ser numérico.")
        try:
            valor = float(valor)
        except (TypeError, ValueError) as exc:
            raise ValueError("El valor del dólar debe ser numérico.") from exc
        if not math.isfinite(valor) or valor <= 0:
            raise ValueError("El valor del dólar debe ser finito y mayor que cero.")
        registros.append(
            Indicador(
                codigo="dolar",
                fuente=FUENTE_DOLAR,
                fecha=fecha,
                valor=valor,
                unidad="Pesos",
                verificado_en=datetime.now(),
            )
        )

    return max(registros, key=lambda indicador: indicador.fecha)


def consultar_dolar():
    respuesta = requests.get(
        URL_DOLAR,
        timeout=(TIMEOUT_CONEXION, TIMEOUT_LECTURA),
    )
    respuesta.raise_for_status()
    try:
        datos = respuesta.json()
    except ValueError as exc:
        raise ValueError("El servicio devolvió un JSON inválido.") from exc
    return validar_respuesta_dolar(datos)
