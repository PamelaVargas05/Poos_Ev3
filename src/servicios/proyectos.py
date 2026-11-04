from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from servicios.permisos import exigir_admin, exigir_sesion


def listar_proyectos(sesion):
    exigir_admin(sesion)
    return ProyectoDAO.listar()


def listar_empleados_disponibles(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()


def listar_empleados_asignados(sesion, proyecto_id):
    exigir_admin(sesion)
    _exigir_proyecto(proyecto_id)
    return ProyectoDAO.listar_empleados(proyecto_id)


def asignar_empleado(sesion, proyecto_id, empleado_id):
    exigir_admin(sesion)
    _exigir_proyecto(proyecto_id)
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("El empleado indicado no existe.")
    if ProyectoDAO.empleado_asignado(proyecto_id, empleado_id):
        return False
    ProyectoDAO.asignar_empleado(proyecto_id, empleado_id)
    return True


def quitar_asignacion(sesion, proyecto_id, empleado_id):
    exigir_admin(sesion)
    _exigir_proyecto(proyecto_id)
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("El empleado indicado no existe.")
    if not ProyectoDAO.empleado_asignado(proyecto_id, empleado_id):
        return False
    if ProyectoDAO.horas_registradas(proyecto_id, empleado_id) > 0:
        raise ValueError(
            "No se puede quitar la asignación porque existen registros laborales. "
            "Conserve la asignación para mantener el historial consistente."
        )
    return ProyectoDAO.quitar_empleado(proyecto_id, empleado_id)


def listar_proyectos_propios(sesion):
    exigir_sesion(sesion)
    empleado_id = sesion.get("empleado_id")
    if empleado_id is None:
        raise PermissionError("La cuenta no está asociada a un empleado.")
    return ProyectoDAO.listar_por_empleado(empleado_id)


def _exigir_proyecto(proyecto_id):
    if ProyectoDAO.buscar_por_id(proyecto_id) is None:
        raise ValueError("El proyecto indicado no existe.")
