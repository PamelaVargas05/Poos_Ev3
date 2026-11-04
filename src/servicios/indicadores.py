from dataclasses import dataclass

import pymysql
import requests

from dominio.indicador import Indicador
from persistencia.indicador_dao import IndicadorDAO
from servicios.indicadores_api import consultar_dolar as consultar_api
from servicios.permisos import exigir_sesion


@dataclass(frozen=True)
class ResultadoIndicador:
    indicador: Indicador | None
    origen: str
    persistido: bool
    mensaje: str


def consultar_dolar(sesion):
    exigir_sesion(sesion)
    try:
        indicador = consultar_api()
    except (requests.RequestException, ValueError) as exc:
        respaldo = IndicadorDAO.buscar_ultimo()
        if respaldo is None:
            return ResultadoIndicador(
                indicador=None,
                origen="sin respaldo",
                persistido=False,
                mensaje=f"No hay datos disponibles. Motivo de la API: {exc}",
            )
        return ResultadoIndicador(
            indicador=respaldo,
            origen="respaldo local",
            persistido=True,
            mensaje=(
                "La API no está disponible. Se muestra el último dato guardado "
                f"({respaldo.fecha.isoformat()}) y no se presenta como actualizado."
            ),
        )

    try:
        IndicadorDAO.guardar_o_actualizar(indicador)
    except pymysql.MySQLError:
        return ResultadoIndicador(
            indicador=indicador,
            origen="API",
            persistido=False,
            mensaje="El dato se obtuvo de la API, pero no quedó persistido en MariaDB.",
        )
    return ResultadoIndicador(
        indicador=indicador,
        origen="API",
        persistido=True,
        mensaje="Dato obtenido de la API y guardado en MariaDB.",
    )


def listar_historial(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()
