
from persistencia.conexion import abrir_conexion
from dominio.usuario import Usuario


class UsuarioDAO:

    @staticmethod
    def hay_usuarios():
        conexion = abrir_conexion()

        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM usuario LIMIT 1")

            return cursor.fetchone() is not None

        finally:
            conexion.close()

    @staticmethod
    def guardar(usuario, sal, clave_hash, empleado_id=None, rol="empleado"):
        rol = Usuario.validar_rol(rol)
        conexion = abrir_conexion()

        try:
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO usuario "
                "(nombre_usuario, sal, clave_hash, empleado_id, rol) "
                "VALUES (%s, %s, %s, %s, %s)",
                (usuario, sal, clave_hash, empleado_id, rol)
            )

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()

    @staticmethod
    def buscar(usuario):
        conexion = abrir_conexion()

        try:
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT id, nombre_usuario, sal, clave_hash, empleado_id, rol "
                "FROM usuario WHERE nombre_usuario = %s",
                (usuario,)
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Usuario(
                id=fila[0],
                nombre_usuario=fila[1],
                sal=fila[2],
                password_hash=fila[3],
                empleado_id=fila[4],
                rol=fila[5],
            )

        finally:
            conexion.close()

    @staticmethod
    def buscar_por_id(id_usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre_usuario, sal, clave_hash, empleado_id, rol "
                "FROM usuario WHERE id = %s",
                (id_usuario,),
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Usuario(
                id=fila[0], nombre_usuario=fila[1], sal=fila[2],
                password_hash=fila[3], empleado_id=fila[4], rol=fila[5],
            )

        finally:
            conexion.close()
