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

def seguimiento_cuidad():
    consultas, seg_ciudades = cargar_ciudad_Clima()
    ciudad_s = input("Introduzca la cuidad: ")
    for ciudad in seg_ciudades:
        if ciudad.ciudad == ciudad_s:
            print("Esta cuidad ya esta en la lista de seguimiento")
            return
        
    datos = obtener_clima(ciudad_s)
    if datos is None:
        print("Ciudad no encontrada")
    else:
        hora = input("ingrese la hora para notificar el seguimiento en formato HH:MM ")
        if len(hora) == 5 and hora[2] == ":":
            partes = hora.split(":")
            if partes[0].isdigit() and partes[1].isdigit():
                if int(partes[0]) <= 23 and int(partes[1]) <= 59:
                    informacion = extraer_clima(datos)
                    informacion["Hora"] = hora

                    id = 0
                    tipo = "Seguimiento"
                    print(informacion)

                    clima = CiudadClima(id=id, tipo=tipo, datos=informacion)
                    guardar_ciudad_clima(clima)
                    print("Se añadio la cuidad a la lista de seguimiento")
                else:
                    print("Hora incorrecta")
        else:
            print("Formato incorrecto")

def mostras_seguimiento():
    consultas, seg_ciudades = cargar_ciudad_Clima()
    if len(seg_ciudades) == 0:
        confirmacion = input("No hay ciudades en seguimiento, ¿desea añadir una? (S/N): ").lower()
        if confirmacion in ("s","si"):
            seguimiento_cuidad()
            return
    else:
        for ciudad in seg_ciudades:
            print(f"| Ciudad: {ciudad.ciudad} | Pais: {ciudad.pais} | Temperatura: {ciudad.temperatura} |")

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

def eliminar():
    consultas, seg_ciudades = cargar_ciudad_Clima()
    ciudad_eliminar = input("Introduzca el nombre de la cuidad que no desea seguir: ").title()
    for ciudad in seg_ciudades:
        if ciudad.ciudad == ciudad_eliminar:
            eliminar_ciudad(informacion=ciudad)
            print("Se elimino el seguimiento de: ",ciudad)
            return
    print("No se encontro la cuidad")


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