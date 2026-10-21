from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion


class EmpleadoDAO:
    @staticmethod
    def _valores_subtipo(empleado):
        return (
            getattr(empleado, "bono_anual", 0.0),
            getattr(empleado, "tarifa_hora", 0.0),
        )

    @staticmethod
    def _fila_a_empleado(fila):
        if not fila:
            return None
        return Empleado(
            id=fila[0],
            nombre=fila[1],
            correo=fila[2],
            telefono=fila[3],
            fecha_inicio=fila[4],
            salario_base=fila[5],
            tipo=fila[6],
            bono_anual=fila[7],
            tarifa_hora=fila[8],
            departamento_id=fila[9],
        )

    @staticmethod
    def insertar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            bono, tarifa = EmpleadoDAO._valores_subtipo(empleado)

            tipo = getattr(empleado, "TIPO", getattr(empleado, "tipo", "GENERAL"))
            telefono = getattr(empleado, "telefono", None)
            fecha_inicio = getattr(empleado, "fecha_inicio", None)
            salario_base = getattr(empleado, "salario_base", 0.0)
            departamento_id = getattr(empleado, "departamento_id", None)

            sql = f"""
                INSERT INTO empleado
                (nombre, correo, telefono, fecha_inicio, salario_base, tipo,
                bono_anual, tarifa_hora, departamento_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    empleado.nombre,
                    empleado.correo,
                    telefono,
                    fecha_inicio,
                    salario_base,
                    tipo,
                    bono,
                    tarifa,
                    departamento_id,
                ),
            )
            empleado.id = cursor.lastrowid
            conexion.commit()
            return empleado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            sql = f"""
                SELECT id, nombre, correo, telefono, fecha_inicio, salario_base,
                    tipo, bono_anual, tarifa_hora, departamento_id
                FROM empleado
                WHERE id = %s
            """
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
            return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_correo(correo):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            sql = f"""
                SELECT id, nombre, correo, telefono, fecha_inicio, salario_base,
                tipo, bono_anual, tarifa_hora, departamento_id
                FROM empleado
                WHERE correo = %s
            """
            cursor.execute(sql, (correo.strip().lower(),))
            fila = cursor.fetchone()
            return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)
        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            sql = """
                SELECT id, nombre, correo, telefono, fecha_inicio, salario_base,
                tipo, bono_anual, tarifa_hora, departamento_id
                FROM empleado
                ORDER BY id
            """
            cursor.execute(sql)
            filas = cursor.fetchall()
            return [EmpleadoDAO._fila_a_empleado(f) for f in filas]
        finally:
            conexion.close()

    @staticmethod
    def actualizar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            bono, tarifa = EmpleadoDAO._valores_subtipo(empleado)

            tipo = getattr(empleado, "TIPO", getattr(empleado, "tipo", "GENERAL"))
            telefono = getattr(empleado, "telefono", None)
            fecha_inicio = getattr(empleado, "fecha_inicio", None)
            salario_base = getattr(empleado, "salario_base", 0.0)
            departamento_id = getattr(empleado, "departamento_id", None)

            sql = """
                UPDATE empleado
                SET nombre = %s, correo = %s, telefono = %s, fecha_inicio = %s,
                    salario_base = %s, tipo = %s, bono_anual = %s,
                    tarifa_hora = %s, departamento_id = %s
                WHERE id = %s
            """
            cursor.execute(
                sql,
                (
                    empleado.nombre,
                    empleado.correo,
                    telefono,
                    fecha_inicio,
                    salario_base,
                    tipo,
                    bono,
                    tarifa,
                    departamento_id,
                    empleado.id,
                ),
            )
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
    def eliminar(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            sql = "DELETE FROM empleado WHERE id = %s"
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()
