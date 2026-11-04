from persistencia.crear_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from dominio.departamento import Departamento
from dominio.empleado import Empleado, EmpleadoPlanta, EmpleadoContrata
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo
from servicios.indicadores import consultar_dolar, listar_historial
import requests
import pymysql
from getpass import getpass

from persistencia.usuario_dao import UsuarioDAO
from servicios.empleados import (
    actualizar_datos_propios,
    consultar_datos_propios,
)
from servicios.permisos import exigir_admin, exigir_sesion
from servicios.proyectos import (
    asignar_empleado,
    listar_empleados_asignados,
    listar_empleados_disponibles,
    listar_proyectos,
    listar_proyectos_propios,
    quitar_asignacion,
)
from servicios.registros import (
    actualizar_registro,
    buscar_registro,
    eliminar_registro,
    insertar_registro,
    listar_registros,
    listar_registros_propios,
    registrar_registro_propio,
    total_horas_por_proyecto,
)
from seguridad.autenticacion import (
    validar_usuario,
    validar_clave,
    crear_hash,
    verificar_clave,
)


def pedir_entero(mensaje, permitir_vacio=False):
    while True:
        valor = input(mensaje).strip()
        if permitir_vacio and not valor:
            return None
        try:
            return int(valor)
        except ValueError:
            print("Debe ingresar un número entero válido.")


def pedir_float(mensaje, minimo=0.0, permitir_vacio=False):
    while True:
        valor = input(mensaje).strip()
        if permitir_vacio and not valor:
            return None
        try:
            numero = float(valor)
            if numero < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue
            return numero
        except ValueError:
            print("Debe ingresar un número válido.")


def pedir_dato(mensaje, validador):
    while True:
        try:
            return validador(input(mensaje))
        except (TypeError, ValueError) as exc:
            print(f"Dato inválido: {exc}")


def validar_correo_nuevo(correo):
    correo = Empleado.validar_correo(correo)
    if EmpleadoDAO.buscar_por_correo(correo) is not None:
        raise ValueError("Ese correo ya está registrado. Ingrese otro correo.")
    return correo


def validar_correo_actualizado(correo, id_empleado):
    correo = Empleado.validar_correo(correo)
    existente = EmpleadoDAO.buscar_por_correo(correo)
    if existente is not None and existente.id != id_empleado:
        raise ValueError("Ese correo ya está registrado. Ingrese otro correo.")
    return correo


def listar_departamentos():
    items = DepartamentoDAO.listar()
    if not items:
        print("No hay departamentos registrados.")
        return
    for item in items:
        print(item)


def mostrar_dolar_observado(sesion):
    try:
        resultado = consultar_dolar(sesion)
        if resultado.indicador is None:
            print(resultado.mensaje)
            return
        indicador = resultado.indicador
        print(
            f"{resultado.mensaje}\n"
            f"Dólar observado: ${indicador.valor:,.2f} {indicador.unidad} por USD | "
            f"Fecha: {indicador.fecha.isoformat()} | Origen: {resultado.origen}"
        )
    except (requests.RequestException, ValueError, PermissionError, pymysql.MySQLError) as exc:
        print(f"No fue posible consultar el dólar: {exc}")


def menu_indicadores(sesion):
    exigir_sesion(sesion)
    while True:
        print("\n--- INDICADORES ---")
        print("1. Consultar dólar actualizado")
        print("2. Ver historial del dólar")
        print("0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                mostrar_dolar_observado(sesion)
            elif opcion == "2":
                historial = listar_historial(sesion)
                if not historial:
                    print("Todavía no existen datos guardados.")
                for indicador in historial:
                    print(
                        f"Fecha: {indicador.fecha.isoformat()} | "
                        f"Valor: ${indicador.valor:,.2f} | "
                        f"Unidad: {indicador.unidad} | Fuente: {indicador.fuente}"
                    )
            elif opcion == "0":
                return
            else:
                print("Opción no válida.")
        except (pymysql.MySQLError, PermissionError, ValueError) as exc:
            print(f"No fue posible completar la operación: {exc}")


def menu_departamentos(sesion):
    exigir_admin(sesion)
    while True:
        print("\n--- DEPARTAMENTOS ---")
        print("1. Crear")
        print("2. Listar")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                dep = Departamento(input("Nombre: "))
                DepartamentoDAO.insertar(dep)
                print(f"Departamento creado con ID {dep.id}.")
            elif op == "2":
                listar_departamentos()
            elif op == "3":
                id_dep = pedir_entero("ID: ")
                dep = DepartamentoDAO.buscar_por_id(id_dep)
                if dep is None:
                    print("Departamento no encontrado.")
                    continue
                dep.nombre = input(f"Nuevo nombre [{dep.nombre}]: ").strip() or dep.nombre
                print("Actualizado." if DepartamentoDAO.actualizar(dep) else "Sin cambios.")
            elif op == "4":
                id_dep = pedir_entero("ID: ")
                print("Eliminado." if DepartamentoDAO.eliminar(id_dep) else "No encontrado.")
            elif op == "0":
                return
            else:
                print("Opción no válida.")
        except ValueError as exc:
            print(f"Error de validación: {exc}")
        except Exception as exc:
            print(f"Error de base de datos / sistema: {exc}")


def crear_empleado_desde_entrada():
    nombre = pedir_dato("Nombre: ", Empleado.validar_nombre)
    correo = pedir_dato("Correo: ", validar_correo_nuevo)
    telefono = input("Teléfono (opcional): ").strip()
    salario = pedir_float("Salario base: ", minimo=0)
    while True:
        dep_id = pedir_entero("ID departamento (Enter = sin departamento): ", permitir_vacio=True)
        if dep_id is None or DepartamentoDAO.buscar_por_id(dep_id) is not None:
            break
        print("El departamento indicado no existe. Ingrese un ID válido o deje el campo vacío.")
    tipo = input("Tipo [1=Base, 2=Planta, 3=Contrata]: ").strip()
    comunes = dict(nombre=nombre, correo=correo, telefono=telefono, salario_base=salario, departamento_id=dep_id)
    if tipo == "2":
        return EmpleadoPlanta(**comunes, bono_anual=pedir_float("Bono anual: ", minimo=0))
    if tipo == "3":
        return EmpleadoContrata(**comunes, tarifa_hora=pedir_float("Tarifa hora: ", minimo=0))
    return Empleado(**comunes)


def menu_empleados(sesion):
    exigir_admin(sesion)
    while True:
        print("\n--- EMPLEADOS ---")
        print("1. Registrar empleado")
        print("2. Listar empleados")
        print("3. Buscar por ID")
        print("4. Buscar por correo")
        print("5. Actualizar correo/departamento")
        print("6. Eliminar")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                emp = crear_empleado_desde_entrada()
                EmpleadoDAO.insertar(emp)
                print(f"Empleado registrado con éxito con ID {emp.id}.")
            elif op == "2":
                empleados = EmpleadoDAO.listar()
                if not empleados:
                    print("No hay empleados registrados.")
                for emp in empleados:
                    print(emp)
            elif op == "3":
                emp = EmpleadoDAO.buscar_por_id(pedir_entero("ID: "))
                print(emp if emp else "Empleado no encontrado.")
            elif op == "4":
                emp = EmpleadoDAO.buscar_por_correo(input("Correo: ").strip())
                print(emp if emp else "Empleado no encontrado.")
            elif op == "5":
                emp = EmpleadoDAO.buscar_por_id(pedir_entero("ID: "))
                if emp is None:
                    print("Empleado no encontrado.")
                    continue
                correo = pedir_dato(
                    f"Nuevo correo [{emp.correo}] (Enter = mantener): ",
                    lambda valor: (
                        emp.correo
                        if not valor.strip()
                        else validar_correo_actualizado(valor, emp.id)
                    ),
                )
                emp.cambiar_correo(correo)
                dep = pedir_entero("Nuevo ID departamento (Enter = mantener): ", permitir_vacio=True)
                if dep is not None:
                    emp.departamento_id = dep
                print("Actualizado correctamente." if EmpleadoDAO.actualizar(emp) else "Sin cambios.")
            elif op == "6":
                print("Eliminado correctamente." if EmpleadoDAO.eliminar(pedir_entero("ID: ")) else "Empleado no encontrado.")
            elif op == "0":
                return
            else:
                print("Opción no válida.")
        except ValueError as exc:
            print(f"Error de validación: {exc}")
        except Exception as exc:
            print(f"Error de base de datos / sistema: {exc}")


def menu_proyectos(sesion):
    exigir_admin(sesion)
    while True:
        print("\n--- PROYECTOS ---")
        print("1. Crear proyecto")
        print("2. Listar proyectos")
        print("3. Actualizar")
        print("4. Eliminar")
        print("5. Asignar empleado")
        print("6. Ver empleados asignados")
        print("7. Quitar asignación")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                p = Proyecto(nombre=input("Nombre: ").strip(), descripcion=input("Descripción: ").strip())
                ProyectoDAO.insertar(p)
                print(f"Proyecto creado con ID {p.id}.")
            elif op == "2":
                items = listar_proyectos(sesion)
                if not items:
                    print("No hay proyectos.")
                for item in items:
                    print(item)
            elif op == "3":
                p = ProyectoDAO.buscar_por_id(pedir_entero("ID: "))
                if not p:
                    print("Proyecto no encontrado.")
                    continue
                p.nombre = input(f"Nombre [{p.nombre}]: ").strip() or p.nombre
                p.descripcion = input(f"Descripción [{p.descripcion}]: ").strip() or p.descripcion
                print("Actualizado." if ProyectoDAO.actualizar(p) else "Sin cambios.")
            elif op == "4":
                print("Eliminado." if ProyectoDAO.eliminar(pedir_entero("ID: ")) else "No encontrado.")
            elif op == "5":
                proyecto_id = pedir_entero("ID proyecto: ")
                if ProyectoDAO.buscar_por_id(proyecto_id) is None:
                    print("Proyecto no encontrado.")
                    continue
                print("Empleados disponibles:")
                for empleado in listar_empleados_disponibles(sesion):
                    print(empleado)
                empleado_id = pedir_entero("ID empleado: ")
                if asignar_empleado(sesion, proyecto_id, empleado_id):
                    print("Empleado asignado al proyecto.")
                else:
                    print("El empleado ya estaba asignado a este proyecto.")
            elif op == "6":
                items = listar_empleados_asignados(sesion, pedir_entero("ID proyecto: "))
                if not items:
                    print("No hay empleados asignados.")
                for item in items:
                    print(item)
            elif op == "7":
                proyecto_id = pedir_entero("ID proyecto: ")
                items = listar_empleados_asignados(sesion, proyecto_id)
                if not items:
                    print("No hay empleados asignados.")
                    continue
                print("Empleados asignados:")
                for item in items:
                    print(item)
                empleado_id = pedir_entero("ID empleado a quitar: ")
                if quitar_asignacion(sesion, proyecto_id, empleado_id):
                    print("Asignación quitada.")
                else:
                    print("La asignación no existe.")
            elif op == "0":
                return
            else:
                print("Opción no válida.")
        except ValueError as exc:
            print(f"Error de validación: {exc}")
        except Exception as exc:
            print(f"Error de base de datos / sistema: {exc}")


def menu_registros(sesion):
    exigir_admin(sesion)
    while True:
        print("\n--- REGISTROS DE TIEMPO ---")
        print("1. Registrar horas")
        print("2. Listar")
        print("3. Actualizar")
        print("4. Eliminar")
        print("5. Total horas por proyecto")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                r = RegistroTiempo(
                    empleado_id=pedir_entero("ID empleado: "),
                    proyecto_id=pedir_entero("ID proyecto: "),
                    horas=pedir_float("Horas: ", minimo=0.01),
                    descripcion=input("Descripción tarea: ").strip(),
                )
                insertar_registro(sesion, r)
                print(f"Registro creado con ID {r.id}.")
            elif op == "2":
                items = listar_registros(sesion)
                if not items:
                    print("No hay registros.")
                for item in items:
                    print(item)
            elif op == "3":
                r = buscar_registro(sesion, pedir_entero("ID registro: "))
                if not r:
                    print("Registro no encontrado.")
                    continue
                horas = pedir_float(f"Nuevas horas [{r.horas}] (Enter = mantener): ", minimo=0.01, permitir_vacio=True)
                if horas is not None:
                    r.horas = horas
                desc = input(f"Descripción [{r.descripcion}]: ").strip()
                if desc:
                    r.descripcion = desc
                print("Actualizado." if actualizar_registro(sesion, r) else "Sin cambios.")
            elif op == "4":
                print(
                    "Eliminado."
                    if eliminar_registro(sesion, pedir_entero("ID: "))
                    else "No encontrado."
                )
            elif op == "5":
                id_p = pedir_entero("ID proyecto: ")
                print(f"Total de horas: {total_horas_por_proyecto(sesion, id_p):.2f}")
            elif op == "0":
                return
            else:
                print("Opción no válida.")
        except ValueError as exc:
            print(f"Error de validación: {exc}")
        except Exception as exc:
            print(f"Error de base de datos / sistema: {exc}")


def registrar_cuenta_empleado(sesion):
    exigir_admin(sesion)
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("No hay empleados registrados para asociar una cuenta.")
        return
    print("\n--- REGISTRAR CUENTA DE EMPLEADO ---")
    empleado_id = pedir_entero("ID del empleado: ")
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        print("Empleado no encontrado.")
        return
    usuario = validar_usuario(input("Nombre de usuario: "))
    if UsuarioDAO.buscar(usuario) is not None:
        print("Ese nombre de usuario ya existe.")
        return
    clave = validar_clave(getpass("Contraseña: "))
    if clave != getpass("Repita la contraseña: "):
        print("Las contraseñas no coinciden.")
        return
    sal, clave_hash = crear_hash(clave)
    UsuarioDAO.guardar(usuario, sal, clave_hash, empleado_id=empleado_id)
    print("Cuenta de empleado creada correctamente.")


def iniciar_sesion():
    """Exige credenciales válidas antes de acceder al menú principal."""
    print("\n===== ACCESO A ECOTECH =====")

    for _ in range(3):
        try:
            nombre = input("Usuario: ")
            clave = getpass("Contraseña: ")
        except EOFError:
            print("\nEntrada finalizada. Hasta luego.")
            return None

        try:
            usuario = validar_usuario(nombre)
        except ValueError:
            print("Usuario o contraseña incorrectos.")
            continue

        registro = UsuarioDAO.buscar(usuario)
        if registro is not None and verificar_clave(
            clave, registro.sal, registro.password_hash
        ):
            print("Acceso autorizado.")
            return {
                "id": registro.id,
                "empleado_id": registro.empleado_id,
                "nombre_usuario": registro.nombre_usuario,
                "rol": registro.rol,
            }

        print("Usuario o contraseña incorrectos.")

    print("Acceso bloqueado en esta ejecución: tres intentos fallidos.")
    return None


def menu_perfil(sesion):
    exigir_sesion(sesion)
    while True:
        print("\n--- MI PERFIL ---")
        print("1. Consultar mis datos")
        print("2. Modificar mi nombre y correo")
        print("3. Volver")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                empleado = consultar_datos_propios(sesion)
                print(empleado if empleado is not None else "La cuenta no está asociada a un empleado.")
            elif opcion == "2":
                empleado = consultar_datos_propios(sesion)
                if empleado is None:
                    print("La cuenta no está asociada a un empleado.")
                    continue
                nombre = input(
                    f"Nombre [{empleado.nombre}]: "
                ).strip() or empleado.nombre
                correo = input(
                    f"Correo [{empleado.correo}]: "
                ).strip() or empleado.correo
                actualizar_datos_propios(sesion, nombre, correo)
                print("Datos actualizados.")
            elif opcion == "3":
                return
            else:
                print("Opción no válida.")
        except (ValueError, PermissionError) as exc:
            print(f"Error: {exc}")


def menu_empleado(sesion):
    exigir_sesion(sesion)
    while True:
        print("\n--- MI CUENTA ---")
        print("1. Consultar mis datos")
        print("2. Modificar nombre y correo")
        print("3. Consultar mis registros")
        print("4. Consultar mis proyectos asignados")
        print("5. Registrar trabajo realizado")
        print("6. Indicadores y dólar")
        print("7. Cerrar sesión")
        print("8. Volver")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                print(consultar_datos_propios(sesion))
            elif opcion == "2":
                empleado = consultar_datos_propios(sesion)
                if empleado is None:
                    print("La cuenta no está asociada a un empleado.")
                    continue
                nombre = input(f"Nombre [{empleado.nombre}]: ").strip() or empleado.nombre
                correo = input(f"Correo [{empleado.correo}]: ").strip() or empleado.correo
                actualizar_datos_propios(sesion, nombre, correo)
                print("Datos actualizados.")
            elif opcion == "3":
                registros = listar_registros_propios(sesion)
                if not registros:
                    print("No tienes registros.")
                for registro in registros:
                    print(registro)
            elif opcion == "4":
                proyectos = listar_proyectos_propios(sesion)
                if not proyectos:
                    print("No tienes proyectos asignados.")
                    continue
                for proyecto in proyectos:
                    print(proyecto)
            elif opcion == "5":
                proyectos = listar_proyectos_propios(sesion)
                if not proyectos:
                    print("No tienes proyectos asignados para registrar trabajo.")
                    continue
                print("Proyectos asignados:")
                for proyecto in proyectos:
                    print(proyecto)
                proyecto_id = pedir_entero("ID proyecto: ")
                fecha = input(
                    "Fecha (AAAA-MM-DD, Enter = hoy): "
                ).strip()
                horas = pedir_float("Horas: ", minimo=0.01)
                descripcion = input("Descripción del trabajo: ").strip()
                registro = registrar_registro_propio(
                    sesion, proyecto_id, fecha, horas, descripcion
                )
                print(f"Trabajo registrado correctamente con ID {registro.id}.")
            elif opcion == "6":
                menu_indicadores(sesion)
            elif opcion == "7":
                return "logout"
            elif opcion == "8":
                return "back"
            else:
                print("Opción no válida.")
        except (ValueError, PermissionError) as exc:
            print(f"Error: {exc}")


def main():
    try:
        crear_tablas()
        print("OK: Base de datos conectada e inicializada correctamente.")
    except Exception as exc:
        print(f"ERROR AL CONECTAR/CREAR BASE DE DATOS: {exc}")
        print("Verifica tu archivo .env o que el servidor MariaDB/MySQL esté activo.")
        return

    while True:
        try:
            sesion = iniciar_sesion()
            if sesion is None:
                return
        except pymysql.MySQLError:
            print("No fue posible verificar las credenciales en MariaDB.")
            return

        cerrar_sesion = False
        print("\n========== ECOTECH ==========")
        while True:
            if sesion["rol"] == "admin":
                print("1. Empleados")
                print("2. Departamentos")
                print("3. Proyectos")
                print("4. Registros de tiempo")
                print("5. Registrar cuenta de empleado")
                print("6. Consultar dólar observado")
                print("7. Mi perfil")
                print("9. Cerrar sesión")
            else:
                print("1. Mi cuenta")
            print("0. Salir")
            opcion = input("Seleccione una opción: ").strip()
            if sesion["rol"] == "admin" and opcion == "1":
                menu_empleados(sesion)
            elif sesion["rol"] == "admin" and opcion == "2":
                menu_departamentos(sesion)
            elif sesion["rol"] == "admin" and opcion == "3":
                menu_proyectos(sesion)
            elif sesion["rol"] == "admin" and opcion == "4":
                menu_registros(sesion)
            elif sesion["rol"] == "admin" and opcion == "5":
                registrar_cuenta_empleado(sesion)
            elif sesion["rol"] == "admin" and opcion == "6":
                menu_indicadores(sesion)
            elif sesion["rol"] == "admin" and opcion == "7":
                menu_perfil(sesion)
            elif sesion["rol"] == "admin" and opcion == "9":
                print("Sesión cerrada.")
                cerrar_sesion = True
                break
            elif sesion["rol"] == "empleado" and opcion == "1":
                resultado = menu_empleado(sesion)
                if resultado == "logout":
                    print("Sesión cerrada.")
                    cerrar_sesion = True
                    break
            elif opcion == "0":
                print("Hasta luego.")
                return
            else:
                print("Opción no válida.")
        if not cerrar_sesion:
            return


if __name__ == "__main__":
    main()
