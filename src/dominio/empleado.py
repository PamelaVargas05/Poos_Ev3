from datetime import date


class Empleado:
    """Clase base del dominio EcoTech. No conoce SQL ni detalles de persistencia."""

    TIPO = "BASE"

    def __init__(
        self,
        nombre: str,
        correo: str,
        telefono: str = "",
        fecha_inicio: str | None = None,
        salario_base: float = 0.0,
        tipo: str = "BASE",
        bono_anual: float = 0.0,
        tarifa_hora: float = 0.0,
        departamento_id: int | None = None,
        id: int | None = None,
    ):
        self.id = id
        self.nombre = self._validar_nombre(nombre)
        self._correo = self._validar_correo(correo)
        self.telefono = (telefono or "").strip()
        self.fecha_inicio = fecha_inicio or date.today().isoformat()
        self.salario_base = self._validar_salario(salario_base)
        self.tipo = tipo or self.TIPO
        self.bono_anual = self._validar_salario(bono_anual)
        self.tarifa_hora = self._validar_salario(tarifa_hora)
        self.departamento_id = departamento_id

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        nombre = (nombre or "").strip()
        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        return nombre

    @staticmethod
    def _validar_correo(correo: str) -> str:
        correo = (correo or "").strip().lower()
        if "@" not in correo or "." not in correo.split("@")[-1]:
            raise ValueError("El correo debe tener un formato válido (ejemplo: usuario@dominio.com).")
        return correo

    @staticmethod
    def _validar_salario(valor: float) -> float:
        try:
            valor = float(valor)
        except (TypeError, ValueError) as exc:
            raise ValueError("El salario/monto debe ser numérico.") from exc
        if valor < 0:
            raise ValueError("El monto no puede ser negativo.")
        return valor

    @property
    def correo(self) -> str:
        return self._correo

    def cambiar_correo(self, nuevo_correo: str) -> None:
        self._correo = self._validar_correo(nuevo_correo)

    def calcular_salario(self) -> float:
        return self.salario_base

    def obtener_detalles(self) -> str:
        depto_str = f"ID {self.departamento_id}" if self.departamento_id else "Sin asignar"
        return (
            f"[{self.id or 'Nuevo'}] {self.nombre} | Correo: {self.correo} | "
            f"Tipo: {self.tipo} | Depto: {depto_str}"
        )

    def __str__(self) -> str:
        return self.obtener_detalles()


class EmpleadoPlanta(Empleado):
    TIPO = "PLANTA"

    def __init__(self, *args, bono_anual: float = 0.0, **kwargs):
        kwargs["tipo"] = "PLANTA"
        kwargs["bono_anual"] = bono_anual
        super().__init__(*args, **kwargs)

    def calcular_salario(self) -> float:
        return self.salario_base + (self.bono_anual / 12)


class EmpleadoContrata(Empleado):
    TIPO = "CONTRATA"

    def __init__(self, *args, tarifa_hora: float = 0.0, **kwargs):
        kwargs["tipo"] = "CONTRATA"
        kwargs["tarifa_hora"] = tarifa_hora
        super().__init__(*args, **kwargs)

    def calcular_salario(self) -> float:
        return self.salario_base
