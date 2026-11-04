import sys
from datetime import date
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import pymysql
import requests

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from dominio.indicador import Indicador
from servicios import indicadores
from servicios.indicadores_api import validar_respuesta_dolar
from servicios.registros import registrar_registro_propio


class Clase6Tests(TestCase):
    def setUp(self):
        self.sesion = {"id": 1, "rol": "empleado", "empleado_id": 7}
        self.indicador = Indicador(date(2026, 11, 4), 951.25, "Pesos")

    def test_deserializa_y_selecciona_fecha_mas_reciente(self):
        respuesta = {
            "codigo": "dolar",
            "unidad_medida": "Pesos",
            "serie": [
                {"fecha": "2026-11-03", "valor": 950},
                {"fecha": "2026-11-04", "valor": 951.25},
            ],
        }
        resultado = validar_respuesta_dolar(respuesta)
        self.assertEqual(resultado.fecha, date(2026, 11, 4))
        self.assertEqual(resultado.codigo, "dolar")

    def test_rechaza_valor_no_positivo(self):
        respuesta = {
            "codigo": "dolar",
            "unidad_medida": "Pesos",
            "serie": [{"fecha": "2026-11-04", "valor": 0}],
        }
        with self.assertRaises(ValueError):
            validar_respuesta_dolar(respuesta)

    def test_usa_respaldo_local_si_falla_api(self):
        with patch.object(
            indicadores, "consultar_api", side_effect=requests.Timeout("offline")
        ), patch.object(
            indicadores.IndicadorDAO, "buscar_ultimo", return_value=self.indicador
        ):
            resultado = indicadores.consultar_dolar(self.sesion)
        self.assertEqual(resultado.origen, "respaldo local")
        self.assertEqual(resultado.indicador.fecha, date(2026, 11, 4))

    def test_informa_dato_no_persistido(self):
        with patch.object(
            indicadores, "consultar_api", return_value=self.indicador
        ), patch.object(
            indicadores.IndicadorDAO,
            "guardar_o_actualizar",
            side_effect=pymysql.MySQLError("database down"),
        ):
            resultado = indicadores.consultar_dolar(self.sesion)
        self.assertFalse(resultado.persistido)
        self.assertIs(resultado.indicador, self.indicador)

    def test_exige_sesion_para_indicador(self):
        with self.assertRaises(PermissionError):
            indicadores.consultar_dolar(None)

    def test_rechaza_registro_en_proyecto_no_asignado(self):
        with patch(
            "servicios.registros.ProyectoDAO.buscar_por_id", return_value=object()
        ), patch(
            "servicios.registros.ProyectoDAO.empleado_asignado", return_value=False
        ):
            with self.assertRaises(PermissionError):
                registrar_registro_propio(
                    self.sesion, 9, "2026-11-04", 2, "tarea"
                )


if __name__ == "__main__":
    import unittest

    unittest.main()
