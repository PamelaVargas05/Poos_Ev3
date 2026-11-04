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

Las Actividades 1 y 2 de la Unidad 3 están implementadas. La aplicación consulta el dólar observado en `mindicador.cl` mediante HTTPS,
valida y deserializa el JSON en `Indicador`, y lo persiste en MariaDB mediante
`IndicadorDAO`. El historial se ordena por fecha descendente y utiliza
exclusivamente MariaDB. Si la API falla se muestra el último respaldo local
con su fecha y origen; nunca se presenta como actualizado. Si falla el guardado
se informa que el dato se obtuvo, pero no quedó persistido.

## Unidad 3, Clase 6

La arquitectura conserva las capas `dominio`, `servicios`, `persistencia` y
`main`. `exigir_sesion()` protege las operaciones autenticadas y
`exigir_admin()` limita la administración. Administradores gestionan
empleados, cuentas, departamentos, proyectos, asignaciones y registros;
empleados solo modifican su propio perfil, consultan sus proyectos y registros,
registran horas en proyectos asignados y consultan indicadores.

El submenú administrativo de proyectos permite listar proyectos, consultar
empleados, asignar sin duplicar, revisar asignaciones y quitar una asignación.
Una asignación no se retira si ya tiene registros laborales, evitando dejar
historiales inconsistentes. El empleado consulta únicamente sus asignaciones y
el servicio obtiene su identidad desde la sesión.

El administrador también dispone de `7. Mi perfil`, con consulta y edición
limitada a su nombre y correo. El perfil se resuelve usando el
`empleado_id` de la sesión, por lo que no permite cambiar rol, contraseña,
identificador ni relaciones laborales. El empleado conserva la misma
restricción sobre sus propios datos.

`indicador_api` tiene una restricción única por `(fuente, codigo, fecha)` y el
DAO usa `INSERT ... ON DUPLICATE KEY UPDATE`, por lo que repetir una consulta
actualiza la observación sin duplicarla y una fecha nueva conserva historial.
La tabla se crea de forma idempotente junto con las tablas existentes, sin
borrar datos.

La mejora de seguridad incorporada con apoyo de IA es la autorización por
asignación: antes de insertar horas se verifica en `proyecto_empleado` que el
empleado de la sesión esté asignado al proyecto. El `empleado_id` nunca se
recibe desde la entrada del empleado.

Para la demostración reproducible se deben ejecutar validaciones unitarias
simuladas de JSON, timeout, HTTP, respaldo con y sin datos y guardado mockeado;
la creación de tablas, el UPSERT y el historial deben comprobarse contra una
instancia MariaDB configurada en `.env`. No se modifican credenciales ni
cuentas existentes.

La suite no destructiva incluida en `tests/test_clase6.py` se ejecuta con:

```powershell
$env:PYTHONPATH = "$PWD\src"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

El UML actualizado debe reflejar `Indicador` (`codigo`, `fuente`, `fecha`,
`valor`, `unidad`, `verificado_en`), `IndicadorDAO`, `ProyectoDAO`,
`proyecto_empleado`, `RegistroTiempo` y las operaciones de servicios
`consultar_dolar`, `listar_historial` y `registrar_registro_propio`, además de
las relaciones Usuario--Empleado, Proyecto--Empleado y
RegistroTiempo--Empleado/Proyecto.
