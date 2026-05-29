from plyer import notification
import subprocess
import os
import sys
import time
from datetime import datetime
from DB_traker_clima import cargar_ciudad_Clima, eliminar_ciudad
from servicios import seguimiento_cuidad

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RUTA_SONIDO = os.path.join(BASE_DIR, "notificacion", "noti_clima.mp3")
RUTA_ICONO = os.path.join(BASE_DIR, "icon.png")

def notificar_clima(titulo, mensaje):
    if os.path.exists(RUTA_SONIDO):
        subprocess.Popen(["pw-play", RUTA_SONIDO])
    else:
        print(f"Advertencia: No se encontró el sonido en {RUTA_SONIDO}")
        
    notification.notify(
        title=f" {titulo} ",
        message=mensaje,
        app_name='Traker Clima',
        app_icon=RUTA_ICONO if os.path.exists(RUTA_ICONO) else None,
        timeout=10
    )

def enviar_notificacion():
    _ , seguimiento = cargar_ciudad_Clima()

    hora = datetime.now().strftime("%H:%M")

    for ciudad in seguimiento:
        if ciudad.hora == hora:
            estado, clima = seguimiento_cuidad(ciudad.ciudad, ciudad.hora)

            if estado == "No encontrada":
                print("Error en la recibida de información")
                notificar_clima(titulo="Error",mensaje=f"Ha ocurrido un error la ciudad {ciudad.ciudad} no existe o a ocurrido un error de red")
            elif estado == "Completo":
                print("Intento de notificación")
                eliminar_ciudad(ciudad)
                notificar_clima(
                    titulo=f"{clima.ciudad} | {clima.descripcion}",
                    mensaje=(
                        f"🌡️ {clima.temperatura}°C\n"
                        f"💧 Humedad: {clima.humedad}%"
                    )
                )

def daemon_clima():
    print("Notificador iniciado...")

    while True:
        enviar_notificacion()

        time.sleep(40)

if __name__ == "__main__":
    daemon_clima()
