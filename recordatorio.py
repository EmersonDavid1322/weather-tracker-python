import requests
from storage import cargar_historial
from clima import *
import os
from config_datos import WEBHOOK_URL
from datetime import datetime
os.chdir("/home/emersondavid/Documentos/P/Phyton/Programa_De_Practica/Proyectos/traker_clima")

def enviar_discord():
    mensajes = []
    hora_actual = datetime.now().strftime("%H:%M")
    consultas, seg_cuidades = cargar_historial()
    for consulta in seg_cuidades:
        if hora_actual == consulta["Hora"]:
            nombre = consulta["Ciudad"]
            datos_clima = obtener_clima(nombre)
            if datos_clima is None:
                mensajes.append(f"⚠️ Error al intentar obtener el clima de la ciudad {nombre}")
            else:
                clima_actual = extraer_clima(datos_clima)
                mensajes.append(f"🌤 {clima_actual['Ciudad']}, {clima_actual['Pais']} - {clima_actual['Temperatura']}°C ,Sensación: {clima_actual['Sensación']}, {clima_actual['Humedad']},{clima_actual['Descripción']},")
    if mensajes:
        mensaje_texto = "El tiempo:\n" + "\n".join(mensajes)
        try:
            requests.post(WEBHOOK_URL, json={"content": mensaje_texto})
        except:
            print("Error al enviar mensaje a Discord")
if __name__ == "__main__":
    enviar_discord()
