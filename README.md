# EcoTech EV3

Proyecto individual de Programación Orientada a Objetos Seguro, basado en
EcoTech EV2 y desarrollado con Python y MariaDB.

Incluye:

- Validaciones de empleados con reintentos y control de correos duplicados.
- Persistencia mediante DAO y transacciones.
- Semillas idempotentes para 5 departamentos y 20 empleados.
- Documentación de instalación, ejecución y evidencias.

## Inicio rápido

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\main.py
```

Configura las credenciales locales en `.env` usando `.env.example`. Ese
archivo no se versiona.

## Documentación

Consulta [`docs/README.md`](docs/README.md) para la configuración de MariaDB,
las validaciones y las instrucciones de semillas. Las decisiones técnicas y
el uso revisado de IA están documentados en [`USODEIA.md`](USODEIA.md).
