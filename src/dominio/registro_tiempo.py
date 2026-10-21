from datetime import date


class RegistroTiempo:
    def __init__(
        self,
        empleado_id: int,
        proyecto_id: int,
        horas: float,
        descripcion: str,
        fecha: str | None = None,
        id: int | None = None,
    ):
        if not empleado_id or not proyecto_id:
            raise ValueError("Empleado y proyecto son obligatorios.")
        try:
            horas = float(horas)
        except (TypeError, ValueError) as exc:
            raise ValueError("Las horas deben ser numéricas.") from exc
        if horas <= 0 or horas > 24:
            raise ValueError("Las horas deben estar entre 0 y 24.")
        descripcion = descripcion.strip()
        if not descripcion:
            raise ValueError("La descripción de la tarea es obligatoria.")

        self.id = id
        self.empleado_id = int(empleado_id)
        self.proyecto_id = int(proyecto_id)
        self.fecha = fecha or date.today().isoformat()
        self.horas = horas
        self.descripcion = descripcion

    def validar_registro(self) -> bool:
        return 0 < self.horas <= 24 and bool(self.descripcion)

    def __str__(self) -> str:
        return (
            f"RegistroTiempo(id={self.id}, fecha={self.fecha}, horas={self.horas}, "
            f"empleado={self.empleado_id}, proyecto={self.proyecto_id})"
        )
