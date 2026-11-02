class Usuario:
    ROLES_VALIDOS = ("admin", "empleado")

    def __init__(
        self,
        nombre_usuario: str = "",
        password_hash: str = "",
        empleado_id: int | None = None,
        rol: str = "empleado",
        id: int | None = None,
        sal: str = "",
    ):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.password_hash = password_hash
        self.empleado_id = empleado_id
        self.rol = self.validar_rol(rol)
        self.sal = sal

    @classmethod
    def validar_rol(cls, rol: str) -> str:
        if not isinstance(rol, str):
            raise TypeError("El rol debe ser texto.")
        rol = rol.strip().lower()
        if rol not in cls.ROLES_VALIDOS:
            raise ValueError("El rol debe ser 'admin' o 'empleado'.")
        return rol
