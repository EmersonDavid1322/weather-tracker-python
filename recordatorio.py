import requests
from DB_traker_clima import cargar_ciudad_Clima
from clima import obtener_clima, extraer_clima
from config import WEBHOOK_URL
from datetime import datetime

def enviar_discord():
    mensajes = []
    hora_actual = datetime.now().strftime("%H:%M")
    consultas, seg_cuidades = cargar_ciudad_Clima()
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
