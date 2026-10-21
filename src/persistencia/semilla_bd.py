import argparse

from dominio.departamento import Departamento
from dominio.empleado import Empleado, EmpleadoContrata, EmpleadoPlanta
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO


DEPARTAMENTOS = (
    "Desarrollo de Software",
    "Recursos Humanos",
    "Finanzas",
    "Marketing",
    "Soporte Técnico",
)

EMPLEADOS = (
    {
        "nombre": "Ana Torres",
        "correo": "ana.torres.ev3@example.com",
        "telefono": "+56911111111",
        "fecha_inicio": "2024-03-01",
        "salario_base": 234,
        "tipo": "BASE",
        "departamento": "Desarrollo de Software",
    },
    {
        "nombre": "Carlos Soto",
        "correo": "carlos.soto.ev3@example.com",
        "telefono": "+56911111112",
        "fecha_inicio": "2024-03-04",
        "salario_base": 950000,
        "tipo": "PLANTA",
        "bono_anual": 1200000,
        "departamento": "Desarrollo de Software",
    },
    {
        "nombre": "Beatriz Rojas",
        "correo": "beatriz.rojas.ev3@example.com",
        "telefono": "+56911111113",
        "fecha_inicio": "2024-03-11",
        "salario_base": 780000,
        "tipo": "CONTRATA",
        "tarifa_hora": 6500,
        "departamento": "Desarrollo de Software",
    },
    {
        "nombre": "Diego Fuentes",
        "correo": "diego.fuentes.ev3@example.com",
        "telefono": "+56911111114",
        "fecha_inicio": "2024-03-18",
        "salario_base": 880000,
        "tipo": "BASE",
        "departamento": "Desarrollo de Software",
    },
    {
        "nombre": "Elena Morales",
        "correo": "elena.morales.ev3@example.com",
        "telefono": "+56922222221",
        "fecha_inicio": "2024-04-01",
        "salario_base": 820000,
        "tipo": "PLANTA",
        "bono_anual": 900000,
        "departamento": "Recursos Humanos",
    },
    {
        "nombre": "Felipe Vargas",
        "correo": "felipe.vargas.ev3@example.com",
        "telefono": "+56922222222",
        "fecha_inicio": "2024-04-08",
        "salario_base": 700000,
        "tipo": "CONTRATA",
        "tarifa_hora": 5800,
        "departamento": "Recursos Humanos",
    },
    {
        "nombre": "Gabriela Silva",
        "correo": "gabriela.silva.ev3@example.com",
        "telefono": "+56922222223",
        "fecha_inicio": "2024-04-15",
        "salario_base": 760000,
        "tipo": "BASE",
        "departamento": "Recursos Humanos",
    },
    {
        "nombre": "Hugo Paredes",
        "correo": "hugo.paredes.ev3@example.com",
        "telefono": "+56922222224",
        "fecha_inicio": "2024-04-22",
        "salario_base": 740000,
        "tipo": "BASE",
        "departamento": "Recursos Humanos",
    },
    {
        "nombre": "Isabel Reyes",
        "correo": "isabel.reyes.ev3@example.com",
        "telefono": "+56933333331",
        "fecha_inicio": "2024-05-01",
        "salario_base": 1050000,
        "tipo": "PLANTA",
        "bono_anual": 1500000,
        "departamento": "Finanzas",
    },
    {
        "nombre": "Javier Castro",
        "correo": "javier.castro.ev3@example.com",
        "telefono": "+56933333332",
        "fecha_inicio": "2024-05-06",
        "salario_base": 900000,
        "tipo": "BASE",
        "departamento": "Finanzas",
    },
    {
        "nombre": "Karen Molina",
        "correo": "karen.molina.ev3@example.com",
        "telefono": "+56933333333",
        "fecha_inicio": "2024-05-13",
        "salario_base": 830000,
        "tipo": "CONTRATA",
        "tarifa_hora": 7000,
        "departamento": "Finanzas",
    },
    {
        "nombre": "Luis Navarro",
        "correo": "luis.navarro.ev3@example.com",
        "telefono": "+56933333334",
        "fecha_inicio": "2024-05-20",
        "salario_base": 790000,
        "tipo": "BASE",
        "departamento": "Finanzas",
    },
    {
        "nombre": "Marcela Espinoza",
        "correo": "marcela.espinoza.ev3@example.com",
        "telefono": "+56944444441",
        "fecha_inicio": "2024-06-03",
        "salario_base": 810000,
        "tipo": "PLANTA",
        "bono_anual": 1000000,
        "departamento": "Marketing",
    },
    {
        "nombre": "Nicolás Bravo",
        "correo": "nicolas.bravo.ev3@example.com",
        "telefono": "+56944444442",
        "fecha_inicio": "2024-06-10",
        "salario_base": 730000,
        "tipo": "CONTRATA",
        "tarifa_hora": 6000,
        "departamento": "Marketing",
    },
    {
        "nombre": "Olivia Carmona",
        "correo": "olivia.carmona.ev3@example.com",
        "telefono": "+56944444443",
        "fecha_inicio": "2024-06-17",
        "salario_base": 770000,
        "tipo": "BASE",
        "departamento": "Marketing",
    },
    {
        "nombre": "Pablo Araya",
        "correo": "pablo.araya.ev3@example.com",
        "telefono": "+56944444444",
        "fecha_inicio": "2024-06-24",
        "salario_base": 750000,
        "tipo": "BASE",
        "departamento": "Marketing",
    },
    {
        "nombre": "Rosa Cisternas",
        "correo": "rosa.cisternas.ev3@example.com",
        "telefono": "+56955555551",
        "fecha_inicio": "2024-07-01",
        "salario_base": 800000,
        "tipo": "PLANTA",
        "bono_anual": 800000,
        "departamento": "Soporte Técnico",
    },
    {
        "nombre": "Sebastián Leiva",
        "correo": "sebastian.leiva.ev3@example.com",
        "telefono": "+56955555552",
        "fecha_inicio": "2024-07-08",
        "salario_base": 720000,
        "tipo": "CONTRATA",
        "tarifa_hora": 5900,
        "departamento": "Soporte Técnico",
    },
    {
        "nombre": "Tamara Núñez",
        "correo": "tamara.nunez.ev3@example.com",
        "telefono": "+56955555553",
        "fecha_inicio": "2024-07-15",
        "salario_base": 760000,
        "tipo": "BASE",
        "departamento": "Soporte Técnico",
    },
    {
        "nombre": "Walter Muñoz",
        "correo": "walter.munoz.ev3@example.com",
        "telefono": "+56955555554",
        "fecha_inicio": "2024-07-22",
        "salario_base": 740000,
        "tipo": "BASE",
        "departamento": "Soporte Técnico",
    },
)


def cargar_departamentos():
    existentes = {departamento.nombre: departamento for departamento in DepartamentoDAO.listar()}
    departamentos = {}
    for nombre in DEPARTAMENTOS:
        departamento = existentes.get(nombre)
        if departamento is None:
            departamento = DepartamentoDAO.insertar(Departamento(nombre))
            print(f"Departamento creado: {nombre} (ID {departamento.id}).")
        else:
            print(f"Departamento existente: {nombre} (ID {departamento.id}).")
        departamentos[nombre] = departamento
    return departamentos


def crear_empleado(definicion, departamento_id):
    datos = {
        "nombre": definicion["nombre"],
        "correo": definicion["correo"],
        "telefono": definicion["telefono"],
        "fecha_inicio": definicion["fecha_inicio"],
        "salario_base": definicion["salario_base"],
        "departamento_id": departamento_id,
    }
    if definicion["tipo"] == "PLANTA":
        return EmpleadoPlanta(**datos, bono_anual=definicion["bono_anual"])
    if definicion["tipo"] == "CONTRATA":
        return EmpleadoContrata(**datos, tarifa_hora=definicion["tarifa_hora"])
    return Empleado(**datos)


def cargar_empleados(departamentos, asignar_ana=False):
    resultados = {"creados": 0, "existentes": 0, "actualizados": 0}
    for definicion in EMPLEADOS:
        departamento_id = departamentos[definicion["departamento"]].id
        empleado = EmpleadoDAO.buscar_por_correo(definicion["correo"])
        if empleado is not None:
            resultados["existentes"] += 1
            if (
                definicion["correo"] == "ana.torres.ev3@example.com"
                and empleado.departamento_id is None
                and asignar_ana
            ):
                empleado.departamento_id = departamento_id
                EmpleadoDAO.actualizar(empleado)
                resultados["actualizados"] += 1
                print(
                    f"Empleado existente actualizado: {empleado.nombre} "
                    f"(ID {empleado.id}, departamento {definicion['departamento']})."
                )
            else:
                print(f"Empleado existente: {empleado.nombre} (ID {empleado.id}).")
            continue

        empleado = EmpleadoDAO.insertar(crear_empleado(definicion, departamento_id))
        resultados["creados"] += 1
        print(f"Empleado creado: {empleado.nombre} (ID {empleado.id}).")
    return resultados


def cargar_semilla(asignar_ana=False):
    departamentos = cargar_departamentos()
    resultados = cargar_empleados(departamentos, asignar_ana=asignar_ana)
    print(
        "Resumen: "
        f"{resultados['creados']} creados, "
        f"{resultados['existentes']} existentes, "
        f"{resultados['actualizados']} actualizados."
    )


def main():
    parser = argparse.ArgumentParser(description="Carga semillas idempotentes de EcoTech.")
    parser.add_argument(
        "--asignar-ana",
        action="store_true",
        help="Asigna Ana Torres a Desarrollo de Software si existe sin departamento.",
    )
    args = parser.parse_args()
    cargar_semilla(asignar_ana=args.asignar_ana)


if __name__ == "__main__":
    main()
