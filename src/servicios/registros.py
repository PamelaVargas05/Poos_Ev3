from datetime import date

from dominio.registro_tiempo import RegistroTiempo
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.proyecto_dao import ProyectoDAO
from servicios.permisos import exigir_admin, exigir_sesion


def listar_registros(sesion):
    exigir_admin(sesion)
    return RegistroTiempoDAO.listar()


def total_horas_por_proyecto(sesion, proyecto_id):
    exigir_admin(sesion)
    return RegistroTiempoDAO.horas_por_proyecto(proyecto_id)


def buscar_registro(sesion, registro_id):
    exigir_admin(sesion)
    return RegistroTiempoDAO.buscar_por_id(registro_id)


def listar_registros_propios(sesion):
    exigir_sesion(sesion)
    empleado_id = sesion.get("empleado_id")
    if empleado_id is None:
        raise PermissionError("La cuenta no está asociada a un empleado.")
    return RegistroTiempoDAO.listar_por_empleado(empleado_id)


def registrar_registro_propio(sesion, proyecto_id, fecha, horas, descripcion):
    exigir_sesion(sesion)
    empleado_id = sesion.get("empleado_id")
    if empleado_id is None:
        raise PermissionError("La cuenta no está asociada a un empleado.")
    if ProyectoDAO.buscar_por_id(proyecto_id) is None:
        raise ValueError("El proyecto indicado no existe.")
    if not ProyectoDAO.empleado_asignado(proyecto_id, empleado_id):
        raise PermissionError("Solo puedes registrar horas en proyectos asignados a tu cuenta.")
    if fecha:
        try:
            date.fromisoformat(fecha)
        except ValueError as exc:
            raise ValueError("La fecha debe tener formato AAAA-MM-DD.") from exc
    registro = RegistroTiempo(
        empleado_id=empleado_id,
        proyecto_id=proyecto_id,
        fecha=fecha or None,
        horas=horas,
        descripcion=descripcion,
    )
    return RegistroTiempoDAO.insertar(registro)


def insertar_registro(sesion, registro):
    exigir_admin(sesion)
    return RegistroTiempoDAO.insertar(registro)


def actualizar_registro(sesion, registro):
    exigir_admin(sesion)
    return RegistroTiempoDAO.actualizar(registro)


def eliminar_registro(sesion, id_registro):
    exigir_admin(sesion)
    return RegistroTiempoDAO.eliminar(id_registro)
