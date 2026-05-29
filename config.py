import json
import sys
import os

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
else:
    ruta_base = os.path.dirname(os.path.abspath(__file__))

CAPERTA_DATA = os.path.join(ruta_base, "data")
os.makedirs(CAPERTA_DATA, exist_ok=True)

RUTA_CONFIG = os.path.join(CAPERTA_DATA, "config.json")

def guardar_configuraciones(api):

    with open(RUTA_CONFIG, "w", encoding="utf-8") as f:
        json.dump(api, f, indent=4, ensure_ascii=False)

def cargar_configutaciones():
    try:

        with open(RUTA_CONFIG, "r", encoding="utf-8") as f:
            api = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Eror cargando datos: {e}")

        api = ""

    return api
