from dataclasses import dataclass, field
from datetime import date, datetime
import math


@dataclass(frozen=True)
class Indicador:
    fecha: date
    valor: float
    unidad: str
    codigo: str = "dolar"
    fuente: str = "mindicador.cl"
    verificado_en: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not isinstance(self.codigo, str) or not self.codigo.strip():
            raise ValueError("El código del indicador es obligatorio.")
        if not isinstance(self.fuente, str) or not self.fuente.strip():
            raise ValueError("La fuente del indicador es obligatoria.")
        if not isinstance(self.fecha, date):
            raise TypeError("La fecha del indicador debe ser una fecha válida.")
        if isinstance(self.valor, bool) or not isinstance(self.valor, (int, float)):
            raise TypeError("El valor del indicador debe ser numérico.")
        if not math.isfinite(float(self.valor)) or self.valor <= 0:
            raise ValueError("El valor del indicador debe ser finito y mayor que cero.")
        if not isinstance(self.unidad, str) or not self.unidad.strip():
            raise ValueError("La unidad del indicador es obligatoria.")
        if not isinstance(self.verificado_en, datetime):
            raise TypeError("La fecha de verificación debe ser válida.")
