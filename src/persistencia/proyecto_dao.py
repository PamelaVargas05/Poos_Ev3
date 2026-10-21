from dominio.proyecto import Proyecto
from persistencia.conexion import abrir_conexion


class ProyectoDAO:
    @staticmethod
    def _fila_a_proyecto(fila):
        return Proyecto(id=fila[0], nombre=fila[1], descripcion=fila[2] or "", fecha_inicio=str(fila[3]), activo=bool(fila[4]))

    @staticmethod
    def insertar(proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO proyecto (nombre,descripcion,fecha_inicio,activo) VALUES (%s,%s,%s,%s)",
                (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, int(proyecto.activo)),
            )
            proyecto.id = cursor.lastrowid
            conexion.commit()
            return proyecto
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_id(id_proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id,nombre,descripcion,fecha_inicio,activo FROM proyecto WHERE id=%s", (id_proyecto,))
            fila = cursor.fetchone()
            return None if fila is None else ProyectoDAO._fila_a_proyecto(fila)
        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id,nombre,descripcion,fecha_inicio,activo FROM proyecto ORDER BY id")
            return [ProyectoDAO._fila_a_proyecto(f) for f in cursor.fetchall()]
        finally:
            conexion.close()

    @staticmethod
    def actualizar(proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE proyecto SET nombre=%s,descripcion=%s,fecha_inicio=%s,activo=%s WHERE id=%s",
                (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, int(proyecto.activo), proyecto.id),
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
    def eliminar(id_proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM proyecto WHERE id=%s", (id_proyecto,))
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
    def asignar_empleado(id_proyecto, id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO proyecto_empleado (proyecto_id,empleado_id) VALUES (%s,%s)",
                (id_proyecto, id_empleado),
            )
            conexion.commit()
            return True
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def listar_empleados(id_proyecto):
        from persistencia.empleado_dao import EmpleadoDAO
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                f"""
                SELECT e.id,e.nombre,e.correo,e.telefono,e.fecha_inicio,e.salario_base,
                    e.tipo,e.bono_anual,e.tarifa_hora,e.departamento_id
                FROM empleado e
                INNER JOIN proyecto_empleado pe ON pe.empleado_id=e.id
                WHERE pe.proyecto_id=%s
                ORDER BY e.id
                """,
                (id_proyecto,),
            )
            return [EmpleadoDAO._fila_a_empleado(f) for f in cursor.fetchall()]
        finally:
            conexion.close()
