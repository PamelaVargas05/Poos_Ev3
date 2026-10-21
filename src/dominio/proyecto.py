from datetime import date


class Proyecto:
    def __init__(
        self,
        nombre: str,
        descripcion: str = "",
        fecha_inicio: str | None = None,
        activo: bool = True,
        id: int | None = None,
    ):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del proyecto es obligatorio.")
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion.strip()
        self.fecha_inicio = fecha_inicio or date.today().isoformat()
        self.activo = bool(activo)


    def asignar_empleado(self, empleado) -> bool:
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def __str__(self) -> str:
        estado = "Activo" if self.activo else "Inactivo"
        return f"Proyecto(id={self.id}, nombre='{self.nombre}', estado={estado})"
