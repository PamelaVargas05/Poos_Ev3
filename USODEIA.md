# Uso de IA en el proyecto EcoTech EV3


## Mejoras en las validaciones

Revisé las validaciones de nombre y correo de la clase `Empleado`.

Se mantuvieron los límites de caracteres y se utilizó la función `pedir_dato()`
para que el usuario pueda corregir información incorrecta sin comenzar
nuevamente el registro.

También revisé el UML y comprobé las validaciones con nombres vacíos, correos
incorrectos y datos válidos.

Se conservaron las clases, la herencia y las funcionalidades anteriores del
programa.

## Base de datos y semillas

Se mantuvo MariaDB como base de datos del proyecto y se continuaron utilizando
los DAO para guardar y consultar información.

Se utilizó `semilla_bd.py` para registrar cinco departamentos y veinte
empleados ficticios. Antes de insertar, el programa comprueba si los registros
ya existen. Esto permite ejecutar la semilla varias veces sin duplicar los
datos.

**Resultados de las pruebas:**

- En la primera ejecución se crearon 5 departamentos y 19 empleados nuevos,
  quedando 20 empleados en total.
- En la segunda ejecución no se crearon empleados adicionales ni se
  actualizaron registros.
- Los 20 correos son únicos.
- Cada departamento tiene 4 empleados.

También se reutilizó el registro existente de Ana Torres y se le asignó un
departamento, sin crear otro empleado con el mismo correo.

## Consulta del dólar mediante API

Se incorporó una nueva opción al menú de EcoTech para consultar el dólar
observado desde `mindicador.cl`.

Para esto se utilizó la librería `requests`. El programa obtiene una respuesta
JSON, revisa los datos y muestra el valor del dólar, la fecha y su fuente.

Se realizaron pruebas para comprobar que el programa pudiera manejar errores
de conexión, respuestas inválidas y listas de datos vacías.

En una prueba real se obtuvo un valor de **978,56 CLP por USD**, correspondiente
al 21 de octubre de 2026.

## Decisiones y comprobaciones

Decidí mantener la estructura original del proyecto, separar la consulta de la
API del menú y reutilizar los DAO existentes.

También se mantuvieron las restricciones de la base de datos para evitar
información duplicada. No se utilizaron `DROP`, `DELETE` ni `TRUNCATE` durante
las pruebas de las semillas.

Las mejoras se comprobaron mediante pruebas de validación, ejecución del
programa, consultas de solo lectura a MariaDB y pruebas de errores de la API.

El proyecto quedó documentado y los avances fueron publicados en mi
repositorio de GitHub.
