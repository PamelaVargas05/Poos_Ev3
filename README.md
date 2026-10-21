# EcoTech EV3

Proyecto individual, basado en
EcoTech EV2 y desarrollado con Python y MariaDB.

Incluye:

- Validaciones de empleados con reintentos y control de correos duplicados.
- Validadores públicos con límites compatibles con MariaDB y UML actualizado.
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

Las Actividades 1 y 2 de la Unidad 3 están implementadas. La opción 5 del
menú consulta el dólar observado en `mindicador.cl` mediante HTTPS, valida el
JSON y muestra el valor más reciente por fecha. La consulta no almacena datos
en MariaDB.
