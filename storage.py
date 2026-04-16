import json 

def guardar_consulta(consultas,seg_cuidades):
    with open("clima.json","w") as f:
        json.dump(consultas,f)
    
    with open("seguimiento_cuidades.json","w") as f:
        json.dump(seg_cuidades,f)


def cargar_historial():
    try:
        with open("clima.json", "r") as f:
            consultas = json.load(f)
        with open("seguimiento_cuidades.json", "r") as f:
            seg_cuidades = json.load(f)
            return consultas,seg_cuidades
    except FileNotFoundError:
        return [], []