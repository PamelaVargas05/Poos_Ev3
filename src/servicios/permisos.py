def exigir_sesion(sesion):
    if not isinstance(sesion, dict) or not sesion.get("id"):
        raise PermissionError("Debe iniciar sesión para realizar esta acción.")
    return sesion


def exigir_admin(sesion):
    exigir_sesion(sesion)
    if str(sesion.get("rol", "")).lower() != "admin":
        raise PermissionError("Esta acción requiere permisos de administrador.")
    return sesion
