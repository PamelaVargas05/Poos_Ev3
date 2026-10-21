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
