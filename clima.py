import requests
from config_datos import API_KEY
def obtener_clima(ciudad):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        if datos["cod"] != 200:
            return None
        else:
            return datos
    except requests.exceptions.ConnectionError:
        print("Conexion fallida, verifique su internet")

def extraer_clima(datos):
    return {
        "Ciudad": datos["name"],
        "Pais": datos["sys"]["country"],
        "Temperatura": datos["main"]["temp"],
        "Sensación": datos["main"]["feels_like"],
        "Humedad": datos["main"]["humidity"],
        "Descripción": datos["weather"][0]["description"],
        "Velocidad": datos["wind"]["speed"]
    }
