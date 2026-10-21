from dominio.departamento import Departamento
from persistencia.conexion import abrir_conexion


class DepartamentoDAO:
    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(id=fila[0], nombre=fila[1])

    @staticmethod
    def insertar(departamento):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO departamento (nombre) VALUES (%s)", (departamento.nombre,))
            departamento.id = cursor.lastrowid
            conexion.commit()
            return departamento
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_id(id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id,nombre FROM departamento WHERE id=%s", (id_departamento,))
            fila = cursor.fetchone()
            return None if fila is None else DepartamentoDAO._fila_a_departamento(fila)
        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id,nombre FROM departamento ORDER BY id")
            return [DepartamentoDAO._fila_a_departamento(f) for f in cursor.fetchall()]
        finally:
            conexion.close()

    @staticmethod
    def actualizar(departamento):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute("UPDATE departamento SET nombre=%s WHERE id=%s", (departamento.nombre, departamento.id))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_departamento):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM departamento WHERE id=%s", (id_departamento,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()
