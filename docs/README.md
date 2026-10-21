# EcoTech

Aplicación de gestión de empleados, departamentos, proyectos y horas
trabajadas, organizada en capas de dominio y persistencia.

## Requisitos

- Python 3.10 o superior.
- Dependencias de `requirements.txt`.
- Una instancia MariaDB/MySQL configurada mediante `.env`.

Instalación:

```powershell
python -m pip install -r requirements.txt
```

## Configuración

Copia `.env.example` como `.env` y ajusta la configuración de la base de
datos. `.env` es local y no debe versionarse.

MariaDB/MySQL es el único motor utilizado:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3307
DB_NAME=ecotech_ev3
DB_USER=root
DB_PASSWORD=
```

## Ejecución

Desde la raíz del proyecto:

```powershell
python src/main.py
```

El menú permite administrar departamentos, empleados, proyectos y registros
de tiempo, incluyendo búsquedas, actualizaciones, eliminaciones y asignación
de empleados a proyectos.

## Semillas de prueba

La semilla carga datos ficticios idempotentes en `ecotech_ev3`. No elimina
registros y consulta los departamentos por nombre y los empleados por correo
antes de insertar. Las restricciones `UNIQUE` de la base de datos ofrecen una
protección adicional.

Los cinco departamentos son:

1. Desarrollo de Software
2. Recursos Humanos
3. Finanzas
4. Marketing
5. Soporte Técnico

Se definen veinte empleados, cuatro por departamento. Ana Torres
(`ana.torres.ev3@example.com`) forma parte de la definición y se reutiliza si
ya existe. La opción `--asignar-ana` autoriza actualizar únicamente su
departamento cuando todavía está sin asignar.

Desde PowerShell, en la raíz del repositorio:

```powershell
$env:PYTHONPATH = "$PWD\src"
.\.venv\Scripts\python.exe -m persistencia.semilla_bd --asignar-ana
```

La primera ejecución realizada produjo:

| Resultado | Cantidad |
|---|---:|
| Departamentos creados | 5 |
| Empleados nuevos | 19 |
| Empleados existentes reutilizados | 1 |
| Empleados actualizados | 1 |
| Empleados totales | 20 |

La segunda ejecución produjo 0 nuevos empleados, 20 empleados existentes y
0 actualizaciones. En ambas comprobaciones se obtuvieron 5 departamentos,
20 empleados, 20 correos únicos y 4 empleados por departamento. Ana Torres
apareció una sola vez.

## Estructura

- `src/dominio`: entidades y reglas de negocio.
- `src/persistencia`: conexión, creación de tablas, semillas y DAO parametrizados.
- `src/main.py`: menú interactivo y validaciones de entrada.
- `docs/uml_empleado_validaciones.mmd`: diagrama Mermaid adicional de `Empleado`.

## Actividad 1: validaciones y UML

`Empleado` define `MIN_NOMBRE=2`, `MAX_NOMBRE=100`, `MIN_CORREO=6` y
`MAX_CORREO=150`. El límite del nombre es menor que `VARCHAR(120)` y el del
correo coincide con `VARCHAR(150)`, por lo que no fue necesario modificar la
base de datos. `validar_nombre()` y `validar_correo()` son métodos públicos de
clase; el constructor y `cambiar_correo()` los reutilizan. El correo exige
exactamente un `@`, un dominio con punto y rechaza puntos consecutivos en el
dominio.

`main.py` incorpora `pedir_dato(mensaje, validador)`, que reintenta ante
`TypeError` y `ValueError`. El registro usa esta función para nombre y correo,
y mantiene la consulta de duplicados mediante `EmpleadoDAO`. La actualización
de correo también reintenta sin reiniciar el formulario del empleado.

### Pruebas de la guía

Las pruebas se ejecutaron con el intérprete de `.venv`, sin conexión a
MariaDB, sin ejecutar semillas y sin insertar empleados:

| Caso | Resultado esperado | Resultado obtenido |
|---|---|---|
| Nombre vacío | Rechazo | Rechazado |
| Nombre de un carácter | Rechazo | Rechazado |
| Nombre de 101 caracteres | Rechazo | Rechazado |
| Nombre con espacios externos | Aceptar normalizado | Aceptado como `Ana Torres` |
| Correo sin `@` | Rechazo | Rechazado |
| Correo con doble punto en dominio | Rechazo | Rechazado |
| Nombre `None` | Rechazo por tipo | Rechazado con `TypeError` |
| Constructor con dato inválido | Rechazo | Rechazado |
| Corrección de correo | Reintentar sin reconstruir empleado | Comprobado |
| `pedir_dato` | Reintentar ante error | Comprobado con entradas simuladas |

También se comprobó la compilación de todos los módulos de `src` con
`compileall`. Las 20 definiciones de correo de la semilla cumplen el mínimo de
6 caracteres. Una lectura de MariaDB confirmó que los 20 empleados existentes
también cumplen la regla. No se ejecutaron semillas ni escrituras.

## Actividad 2: HTTP, JSON y dólar observado

Se agregó `requests` a `requirements.txt` y se instaló en `.venv`. El módulo
[`src/servicios/indicadores_api.py`](../src/servicios/indicadores_api.py)
consulta `https://mindicador.cl/api/dolar` con `timeout=(3, 5)`,
verificación TLS predeterminada y `raise_for_status()`. La función no imprime,
no ejecuta SQL y devuelve la fecha, valor y unidad del registro más reciente
después de validar todos los registros de `serie`.

La validación exige un objeto JSON, `codigo=dolar`, `unidad_medida=Pesos`, una
serie no vacía, fechas ISO válidas y valores numéricos finitos mayores que
cero. Se selecciona el registro con fecha máxima; no se presupone que el
primer registro sea el más reciente.

El menú principal conserva las opciones anteriores y agrega:

```text
5. Consultar dólar observado
```

Los errores de red, timeout, HTTP, JSON inválido, serie vacía y datos
inconsistentes se muestran como mensajes claros sin traceback ni cierre de la
aplicación.

### Pruebas de la Actividad 2

| Tipo | Caso | Resultado |
|---|---|---|
| Real | GET HTTPS a mindicador.cl | Exitoso |
| Real | Valor obtenido | `978.56 CLP por USD` |
| Real | Fecha obtenida | `2026-10-21` |
| Real | Fuente | `mindicador.cl` |
| Simulada | Serie vacía | Rechazada |
| Simulada | Valor cero | Rechazado |
| Simulada | Fecha inválida | Rechazada |
| Simulada | Unidad incorrecta | Rechazada |
| Simulada | JSON inválido | Capturado como error de validación |
| Simulada | Error HTTP | Propagado para manejo del menú |
| Simulada | Timeout/problema de red | Propagado para manejo del menú |

La importación de `requests` fue comprobada en `.venv` con la versión
instalada. No se usó `verify=False`, no se agregaron credenciales y el dólar
no se guardó en MariaDB.
