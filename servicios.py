from clima import obtener_clima, extraer_clima
from DB_traker_clima import guardar_ciudad_clima,cargar_ciudad_Clima,eliminar_ciudad
from clases import CiudadClima
from datetime import datetime

def consulta(ciudad):
    print(ciudad)
    datos = obtener_clima(ciudad)

    if datos is None:
        print("Ciudad no encontrada")
    else:
        informacion = extraer_clima(datos)
        fecha_consulta = datetime.now()
        hora_actual = fecha_consulta.strftime("%H:%M")
        fecha_actual = fecha_consulta.strftime("%d/%m/%Y")

        informacion["Hora_Consulta"] = hora_actual
        informacion["Fecha_Consulta"] = fecha_actual
        print(informacion)

        id = 0
        tipo = "Consulta"
        clima = CiudadClima(id=id, tipo=tipo, datos=informacion)

        guardar_ciudad_clima(clima)
        return informacion

def seguimiento_cuidad(ciudad_s,hora):
    consultas, seg_ciudades = cargar_ciudad_Clima()
    estado = None

    datos = obtener_clima(ciudad_s)
    if datos is None:
        estado = "No encontrada"
        clima = None
        return estado, clima
    else:
        informacion = extraer_clima(datos)
        informacion["Hora"] = hora

        id = 0
        tipo = "Seguimiento"


        clima = CiudadClima(id=id, tipo=tipo, datos=informacion)
        guardar_ciudad_clima(clima)
        estado =  "Completo"
        return estado, clima

def mostras_seguimiento():
    _ , seg_ciudades = cargar_ciudad_Clima()
    seguimiento_lista = []
    for ciudad in seg_ciudades:
        seguimiento_lista.append(ciudad)
        print(f"| Ciudad: {ciudad.ciudad} | Pais: {ciudad.pais} | Hora: {ciudad.hora} |")

    return seguimiento_lista

def editar():
    consutlas, seg_ciudades = cargar_ciudad_Clima()
    ciudad_e = input("Introduzca la ciudad que quieres editar: ")
    for ciudad in seg_ciudades:
        if ciudad.ciudad == ciudad_e:
            hora = input("ingrese la hora para notificar el seguimiento en formato HH:MM ")
            if len(hora) == 5 and hora[2] == ":":
                partes = hora.split(":")
                if partes[0].isdigit() and partes[1].isdigit():
                    if int(partes[0]) <= 23 and int(partes[1]) <= 59:
                        ciudad.hora = hora
                        eliminar_ciudad(informacion=ciudad)
                        guardar_ciudad_clima(informacion=ciudad)
                        print(f"Se a editado la ciudad: {ciudad_e} a nuevo horario de {hora}")
                        return
                    else:
                        print("Hora incorrecta")
    print("Ciudad no encontrada")


def historial_consultas():
    consultas, seg_ciudades = cargar_ciudad_Clima()
    if len(consultas) == 0:
            confirmacion = input("NO hay consultas registradas, ¿desea hacer una? (S/N): ").lower()
            if confirmacion in ("s","si"):
                consulta()
    else:
        for consulta in consultas:
            print(f"| Ciudad: {consulta.ciudad} | Pais: {consulta.pais} | Temperatura: {consulta.temperatura} |")
            print("\n Ha consultado un total de: ", len(consultas),"veces")