## Uso de Inteligencia Artificial

Se utilizó IA como apoyo para revisar la estructura de los DAO,
manejo de excepciones y coherencia entre relaciones UML y base de datos.

Las sugerencias fueron revisadas y probadas antes de incorporarlas.

## Actividad 1 de Unidad 3

Se utilizó IA como apoyo para revisar las validaciones de `Empleado`, comparar
los límites con el esquema real de MariaDB y proponer una función reutilizable
de entrada en `main.py`. La decisión final fue conservar `VARCHAR(120)` para
nombre y `VARCHAR(150)` para correo sin modificar la base de datos, usando
límites de dominio de 100 y 150 caracteres respectivamente.

También se utilizó IA para estructurar el diagrama Mermaid adicional
[`docs/uml_empleado_validaciones.mmd`](docs/uml_empleado_validaciones.mmd),
sin reemplazar los diagramas de imagen existentes. La implementación fue
revisada con pruebas locales de validación, constructor, cambio de correo,
reintentos y compilación de `src`. No se ejecutaron semillas ni se insertaron
nuevos empleados.

## Adaptación de persistencia a MariaDB

Se utilizó IA como apoyo para revisar y adaptar la persistencia del proyecto.

El proyecto mantenía compatibilidad con SQLite y MariaDB, pero se decidió
mantener únicamente MariaDB debido al alcance trabajado en clases.

La IA fue utilizada para apoyar:
- la eliminación de referencias a SQLite;
- la revisión de la configuración de PyMySQL;
- el diagnóstico del error de clave foránea en `proyecto_empleado`;
- la verificación de compatibilidad entre claves primarias y foráneas;
- la revisión del orden de creación de tablas;
- la revisión de imports después de eliminar archivos `__init__.py`.

Los cambios fueron comprobados mediante ejecución del proyecto y revisión
de las tablas desde phpMyAdmin.

Ejemplo:
- Se aceptó el uso de try/except/finally y rollback en operaciones de escritura.
- Se mantuvo el patrón DAO trabajado en clases.
- No se incorporaron capas Service o Controller porque no corresponden
  al alcance trabajado en la unidad.

## Recomendación aplicada para las semillas de prueba

Se utilizó IA como apoyo para diseñar una semilla idempotente sin reemplazar
la arquitectura de la EV2. La recomendación técnica fue reutilizar
`DepartamentoDAO` y `EmpleadoDAO`, consultar departamentos por nombre y
empleados por correo antes de insertar, y dejar que las restricciones
`UNIQUE` de MariaDB actúen como protección adicional.

La propuesta fue revisada contra las clases reales `Departamento` y
`Empleado`, el esquema de `crear_bd.py` y la base `ecotech_ev3`. Se mantuvo
la separación entre dominio y persistencia: la semilla no agrega SQL a
`main.py` y usa los DAO existentes para escribir.

Ana Torres ya existía con el correo
`ana.torres.ev3@example.com`. Por eso se reutilizó su ID y se actualizó
únicamente su departamento desde `NULL` a Desarrollo de Software, con
autorización explícita. No se usaron IDs fijos para los departamentos.

## Evidencia verificada

La primera ejecución de
`.\.venv\Scripts\python.exe -m persistencia.semilla_bd --asignar-ana`
creó 5 departamentos y 19 empleados, reutilizó 1 empleado existente,
actualizó 1 registro y dejó 20 empleados totales.

La segunda ejecución detectó los 5 departamentos y los 20 empleados como
existentes: creó 0 empleados y actualizó 0 registros.

Las consultas posteriores en MariaDB 11.5.2 confirmaron en ambas ejecuciones:

- 5 departamentos.
- 20 empleados.
- 20 correos únicos.
- 4 empleados por departamento.
- Una sola fila para Ana Torres.
- Ningún empleado sin departamento después de la asignación autorizada.

No se utilizaron `DROP`, `DELETE` ni `TRUNCATE`.

## Actividad 2 de Unidad 3

Se utilizó IA como apoyo para separar la consulta HTTPS de la presentación
del menú, definir la validación defensiva de la respuesta JSON y preparar
pruebas simuladas de errores. La decisión fue crear
`src/servicios/indicadores_api.py`, sin agregar SQL ni persistencia del
indicador.

La implementación fue revisada contra los requisitos de la presentación:
`requests.get()` con `timeout=(3, 5)`, `raise_for_status()`, TLS habilitado
por defecto, validación de `codigo`, `unidad_medida`, `serie`, fechas y valores
finitos positivos. Para no asumir el orden de la API, se selecciona la fecha
más reciente después de validar todos los registros.

También se utilizó IA para revisar la integración mínima de la opción 5 del
menú y el manejo de errores sin traceback. Las pruebas reales y simuladas se
mantuvieron diferenciadas en la documentación. La consulta real realizada
devolvió `978.56` CLP por USD para `2026-10-21`, desde `mindicador.cl`.
La revisión de MariaDB fue de solo lectura: confirmó 20 empleados y no se
ejecutaron semillas ni se insertaron o modificaron registros.