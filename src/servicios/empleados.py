from persistencia.empleado_dao import EmpleadoDAO
from servicios.permisos import exigir_admin, exigir_sesion


def listar_empleados(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()


def buscar_empleado(sesion, id_empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(id_empleado)


def insertar_empleado(sesion, empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.insertar(empleado)


def actualizar_empleado(sesion, empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.actualizar(empleado)


def eliminar_empleado(sesion, id_empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.eliminar(id_empleado)


def consultar_datos_propios(sesion):
    exigir_sesion(sesion)
    empleado_id = sesion.get("empleado_id")
    if empleado_id is None:
        raise PermissionError("La cuenta no está asociada a un empleado.")
    return EmpleadoDAO.buscar_por_id(empleado_id)


def actualizar_datos_propios(sesion, nombre, correo):
    empleado = consultar_datos_propios(sesion)
    if empleado is None:
        raise PermissionError("La cuenta no está asociada a un empleado.")
    empleado.nombre = empleado.validar_nombre(nombre)
    empleado.cambiar_correo(correo)
    return EmpleadoDAO.actualizar(empleado)
