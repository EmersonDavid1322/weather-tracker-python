from clima import *  
from storage import *
consultas, seg_cuidades = cargar_historial()

def main_menu():
    while True:
        try:
            print("1) Ver clima de alguna cuidad")
            print("2) añadir seguimiento de una cuidad")
            print("3) Ver cuidades en seguimiento")
            print("4) Editar Hora de seguimiento")
            print("5) Eliminar cuidad en seguimiento")
            print("6) ver histrial de consultas")
            print("7) salir")
            opcion = int(input("Seleccione una opción: "))
            return opcion
        except ValueError:
            print("Seleccione una opción valida")

def clima_cuidad(consultas, seg_cuidades):
    cuidad = input("Introduzca la cuidad: ")
    datos = obtener_clima(cuidad)
    if datos is None:
        print("Ciudad no encontrada")
    else:
        informacion = extraer_clima(datos)
        print(informacion)
        consultas.append(informacion)
        guardar_consulta(consultas,seg_cuidades)

def seguimiento_cuidad(consultas,seg_cuidades):
    ciudad_s = input("Introduzca la cuidad: ")
    for ciudad in seg_cuidades:
        if ciudad["Ciudad"] == ciudad_s:
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
                    seg_cuidades.append(informacion)
                    guardar_consulta(consultas,seg_cuidades)
                    print("Se añadio la cuidad a la lista de seguimiento")
                else:
                    print("Hora incorrecta")
        else:
            print("Formato incorrecto")

def mostras_seguimiento(seg_cuidades):
    if len(seg_cuidades) == 0:
        confirmacion = input("No hay ciudades en seguimiento, ¿desea añadir una? (S/N): ").lower()
        if confirmacion in ("s","si"):
            seguimiento_cuidad(seg_cuidades)
            return
    else:
        print(seg_cuidades)

def editar(seg_cuidades,consultas):
    ciudad_e = input("Introduzca la ciudad que quieres editar: ")
    for ciudad in seg_cuidades:
        if ciudad["Ciudad"] == ciudad_e:
            print(ciudad_e)
            hora = input("ingrese la hora para notificar el seguimiento en formato HH:MM ")
            if len(hora) == 5 and hora[2] == ":":
                partes = hora.split(":")
                if partes[0].isdigit() and partes[1].isdigit():
                    if int(partes[0]) <= 23 and int(partes[1]) <= 59:
                        ciudad["Hora"] = hora
                        guardar_consulta(seg_cuidades,consultas)
                        print(f"Se a editado la ciudad: {ciudad_e} a nuevo horario de {hora}")
                        return
                    else:
                        print("Hora incorrecta")
    print("Ciudad no encontrada")

def eliminar(consultas,seg_cuidades):
    ciudad_eliminar = input("Introduzca el nombre de la cuidad que no desea seguir: ").title()
    for ciudad in seg_cuidades:
        if ciudad["Ciudad"] == ciudad_eliminar:
            print("Se elimino el seguimiento de: ",ciudad)
            seg_cuidades.remove(ciudad)
            guardar_consulta(consultas,seg_cuidades)
            return
    print("No se encontro la cuidad")


def historial_consultas(consultas):
    if len(consultas) == 0:
            confirmacion = input("NO hay consultas registradas, ¿desea hacer una? (S/N): ").lower()
            if confirmacion in ("s","si"):
                clima_cuidad(consultas)
    else:
        for consulta in consultas:
            print(consulta)
    print("\n Ha consultado un total de: ", len(consultas),"veces")
    

if __name__ == "__main__":
    while True:
        opcion = main_menu()
        if opcion == 1:
            clima_cuidad(consultas,seg_cuidades)
        elif opcion == 2:
            seguimiento_cuidad(consultas,seg_cuidades)
        elif opcion == 3:
            mostras_seguimiento(seg_cuidades)
        elif opcion == 4:
            editar(seg_cuidades,consultas)
        elif opcion == 5:
            eliminar(consultas,seg_cuidades)
        elif opcion == 6:
            historial_consultas(consultas)
        elif opcion == 7:
            confirmacion = input("¿Seguro que desea salir? (S/N): ").lower()
            if confirmacion in ("s","si"):
                break
        else:
            print("Valor no valido")