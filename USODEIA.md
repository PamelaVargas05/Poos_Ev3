# Uso, evaluación y validación de herramientas de Inteligencia Artificial

## Herramienta y objetivo

Durante el desarrollo de EcoTech se utilizó GitHub Copilot como apoyo para
revisar código, analizar funcionalidades y proponer mejoras. Su uso no
reemplazó el diseño del proyecto ni la decisión del estudiante. Las
funcionalidades que ya existían se conservaron y se revisaron antes de
integrar cambios.

El objetivo fue mejorar la calidad del código sin romper la arquitectura
orientada a objetos ni la persistencia en MariaDB. La revisión se enfocó en
validaciones, seguridad, permisos, manejo de excepciones, consultas a la base
de datos y pruebas.

## Funcionalidades en las que prestó apoyo

El apoyo de Copilot se utilizó para revisar o proponer mejoras en:

- Validación de nombres y correos de `Empleado`.
- Reintentos de entrada mediante `pedir_dato()`.
- Consulta del dólar observado mediante una API HTTPS.
- Validación de la respuesta JSON y selección del registro más reciente.
- Manejo de errores de conexión, HTTP, datos inválidos y respaldo local.
- Roles de administrador y empleado, autenticación y permisos.
- Asociación entre usuarios y empleados.
- Autorización por asignación antes de registrar horas en un proyecto.
- Menú de perfil personal para el administrador.
- Reutilización de `consultar_datos_propios()` y
  `actualizar_datos_propios()`.

Los empleados, departamentos, proyectos, registros y DAO ya formaban parte de
la evolución anterior del proyecto. Por lo tanto, no se atribuye a Copilot la
creación completa de esas funcionalidades. La herramienta ayudó a revisarlas,
reforzarlas o integrarlas con los nuevos requerimientos.

## Mejoras en validaciones y persistencia

Se mantuvieron en `Empleado` los límites de nombre y correo compatibles con
MariaDB y con el UML. Las validaciones se reutilizan en el constructor y al
cambiar el correo. En el menú, `pedir_dato()` permite corregir un valor
inválido sin comenzar nuevamente el registro.

MariaDB se mantuvo como único motor de persistencia. Los DAO utilizan
consultas parametrizadas y transacciones para guardar, actualizar y eliminar
información. La semilla comprueba si departamentos y empleados ya existen
antes de insertarlos, evitando duplicados al ejecutarse más de una vez. Las
restricciones `UNIQUE` de la base de datos agregan una protección adicional.

En las comprobaciones documentadas de la semilla, la primera ejecución creó
5 departamentos y 19 empleados nuevos, reutilizando un empleado existente
para completar 20. La segunda ejecución no creó empleados adicionales. Se
comprobó que existieran 20 empleados, 20 correos únicos y 4 empleados por
departamento. Estas comprobaciones no utilizaron `DROP`, `DELETE` ni
`TRUNCATE`.

## Consulta del dólar

Se incorporó una opción para consultar el dólar observado desde
`mindicador.cl` mediante `requests`. La respuesta se valida antes de
convertirla en un objeto de dominio `Indicador`. Se exige una respuesta JSON
válida, el código esperado, la unidad correcta, una serie no vacía, fechas
válidas y valores positivos.

La consulta utiliza HTTPS, timeout y `raise_for_status()`. Si la API o la
persistencia fallan, el servicio informa la situación y puede utilizar el
último respaldo local sin presentarlo como un valor actualizado. El historial
se obtiene desde MariaDB.

En una comprobación real documentada se obtuvo un valor de **978,56 CLP por
USD**, correspondiente al 21 de octubre de 2026. También se realizaron
comprobaciones simuladas para respuestas inválidas, series vacías, errores HTTP
y timeout.

## Perfil del administrador y asociación con el empleado

El menú principal incorpora la opción `7. Mi perfil` para administradores. El
menú permite consultar los datos propios y modificar únicamente el nombre y el
correo. No permite cambiar el rol, la contraseña, el identificador ni las
relaciones laborales.

La funcionalidad reutiliza los servicios existentes
`consultar_datos_propios()` y `actualizar_datos_propios()`. Estos servicios
obtienen el empleado desde `empleado_id` incluido en la sesión, en lugar de
recibirlo desde la entrada del usuario. De esta forma, la consulta y la
actualización quedan limitadas a la identidad autenticada.

La asociación concreta del administrador se comprobó posteriormente en
MariaDB y no corresponde a una configuración inicial demostrada por el
repositorio. El usuario `admin_ecotech`, con ID 2, fue actualizado para tener
`empleado_id = 22`. La sentencia de actualización confirmó una fila
afectada. Después, un `SELECT` con `LEFT JOIN` permitió visualizar el nombre y
el correo del empleado asociado. Esta comprobación fue manual y se realizó
sobre la base de datos existente; no se modificó la lógica Python ni se
incorporaron credenciales al código.

## Recomendaciones aceptadas, adaptadas y no validadas

### Recomendaciones aceptadas

Se aceptaron las recomendaciones que eran compatibles con el diseño existente:

- Validar los datos en el dominio antes de persistirlos.
- Reutilizar servicios para las operaciones sobre los datos propios.
- Obtener `empleado_id` desde la sesión autenticada.
- Aplicar permisos en la capa de servicios y no solamente en el menú.
- Verificar la asignación del empleado antes de registrar horas.
- Utilizar consultas SQL parametrizadas.
- Mantener las contraseñas protegidas mediante hash y sal.
- Probar errores de API y persistencia mediante dependencias simuladas.

### Recomendaciones adaptadas

El perfil del administrador se adaptó al código existente en vez de crear una
lógica paralela. Se utilizó el mismo mecanismo de perfil del empleado y se
limitó la edición a nombre y correo. También se mantuvo la separación entre
menú, servicios, dominio y DAO para evitar que la interfaz ejecutara
directamente reglas de autorización o SQL.

### Recomendaciones no consideradas validadas

No se consideraron validadas las afirmaciones que no contaban con una prueba
correspondiente. En particular:

- No se afirma que todas las funcionalidades existentes hayan sido creadas
  por Copilot.
- No se afirma que el menú de perfil tenga cobertura automatizada completa.
- No se afirma que la asociación del administrador forme parte de la
  configuración inicial del repositorio; fue comprobada después directamente
  en MariaDB.
- No se afirma que todos los errores de actualización de correo duplicado
  tengan un mensaje específico, porque el caso depende también de la
  restricción `UNIQUE` y de la respuesta de MariaDB.

La decisión final de implementar, modificar o descartar cada recomendación
fue responsabilidad del estudiante, considerando el código existente y la
evidencia disponible.

## Criterios técnicos de validación

Las recomendaciones se evaluaron según los siguientes criterios:

- Coherencia con las clases de dominio y la arquitectura por capas.
- Encapsulamiento de atributos, especialmente el correo de `Empleado`.
- Validación de tipos, formatos, rangos y valores obligatorios.
- Identificación del usuario mediante la sesión y no mediante datos
  manipulables del formulario.
- Separación entre autenticación y autorización.
- Verificación de roles y asignaciones antes de ejecutar operaciones.
- Uso de consultas parametrizadas para evitar concatenar entradas en SQL.
- Uso de transacciones y restricciones de MariaDB para mantener consistencia.
- Manejo explícito de errores de validación, permisos, red y persistencia.
- Resultados de pruebas reproducibles, diferenciando pruebas simuladas,
  pruebas automatizadas y comprobaciones manuales.

## Pruebas y resultados comprobables

### Pruebas automatizadas existentes

La suite `tests/test_clase6.py` contiene seis pruebas automatizadas. Se
ejecutó con `unittest` y el resultado fue:

```text
Ran 6 tests in 0.006s
OK
```

Las seis pruebas comprueban:

1. Deserialización del JSON y selección de la fecha más reciente.
2. Rechazo de un valor del dólar igual a cero.
3. Uso del respaldo local cuando la API produce un timeout.
4. Información de dato no persistido cuando falla el guardado.
5. Exigencia de una sesión para consultar indicadores.
6. Rechazo de horas en un proyecto no asignado al empleado.

También se comprobó la compilación de los módulos Python de `src` y `tests`.
Estas pruebas no cubren directamente el menú de perfil ni la asociación del
administrador.

### Comprobaciones manuales

De forma separada, se realizaron comprobaciones manuales de:

- Navegación del menú `7. Mi perfil`.
- Consulta de los datos propios del administrador.
- Actualización manual de nombre y correo.
- Restricción de la edición a los campos permitidos.
- Actualización de `empleado_id` del usuario `admin_ecotech` en MariaDB.
- Confirmación de una fila afectada por la actualización.
- Consulta posterior mediante `SELECT` con `LEFT JOIN`.

Estas comprobaciones no deben presentarse como pruebas automatizadas. La
confirmación de MariaDB demuestra el estado de esa base de datos en el momento
de la revisión, pero no reemplaza una prueba automatizada ni modifica la
configuración inicial versionada.

## Relación con el criterio 2.1.5 de la ES2

El trabajo responde al criterio 2.1.5 porque el código sugerido o revisado
con apoyo de IA fue evaluado antes de aceptarse. La revisión consideró
seguridad, encapsulamiento, validación de datos, permisos, consultas
parametrizadas, manejo de excepciones y compatibilidad con la arquitectura
orientada a objetos.

La evidencia disponible permite distinguir lo que fue probado de lo que solo
fue revisado manualmente. Así, Copilot se utilizó como apoyo para detectar
necesidades y proponer alternativas, mientras que la decisión técnica final y
la responsabilidad por el código implementado correspondieron al estudiante.

## Conclusión

GitHub Copilot fue útil para revisar funcionalidades, detectar riesgos y
proponer mejoras relacionadas con seguridad, validaciones, permisos y
persistencia. Su aporte fue especialmente útil al integrar el perfil del
administrador con servicios que ya existían, evitando duplicar reglas de
acceso.

La herramienta no sustituyó la revisión técnica. Las recomendaciones se
aceptaron, adaptaron o descartaron según su compatibilidad con el proyecto y
según las pruebas disponibles. Las limitaciones pendientes quedan
identificadas para no presentar como automatizado o validado aquello que solo
fue comprobado manualmente.
