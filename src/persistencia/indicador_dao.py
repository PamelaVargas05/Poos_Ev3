from dominio.indicador import Indicador
from persistencia.conexion import abrir_conexion


class IndicadorDAO:
    @staticmethod
    def _fila_a_indicador(fila):
        return Indicador(
            codigo=fila[2],
            fuente=fila[1],
            fecha=fila[3],
            valor=float(fila[4]),
            unidad=fila[5],
            verificado_en=fila[6],
        )

    @staticmethod
    def guardar_o_actualizar(indicador):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                INSERT INTO indicador_api
                    (fuente, codigo, fecha, valor, unidad, verificado_en)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    valor = VALUES(valor),
                    unidad = VALUES(unidad),
                    verificado_en = VALUES(verificado_en)
                """,
                (
                    indicador.fuente,
                    indicador.codigo,
                    indicador.fecha,
                    indicador.valor,
                    indicador.unidad,
                    indicador.verificado_en,
                ),
            )
            conexion.commit()
            return indicador
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT id, fuente, codigo, fecha, valor, unidad, verificado_en
                FROM indicador_api
                WHERE codigo = %s
                ORDER BY fecha DESC, verificado_en DESC, id DESC
                """,
                ("dolar",),
            )
            return [IndicadorDAO._fila_a_indicador(fila) for fila in cursor.fetchall()]
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_ultimo():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT id, fuente, codigo, fecha, valor, unidad, verificado_en
                FROM indicador_api
                WHERE codigo = %s
                ORDER BY fecha DESC, verificado_en DESC, id DESC
                LIMIT 1
                """,
                ("dolar",),
            )
            fila = cursor.fetchone()
            return None if fila is None else IndicadorDAO._fila_a_indicador(fila)
        finally:
            if conexion:
                conexion.close()
