import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image
import io
import requests
from datetime import datetime
import webbrowser
from DB_traker_clima import crear_tablas
from servicios import consulta, seguimiento_cuidad

crear_tablas()

class VentanaClima(ctk.CTkToplevel):
    def __init__(self,menu_principal):
        super().__init__()
        self.title("Clima")
        self.geometry("600x400")

        self.menu_principal = menu_principal

        #CONSULTA
        self.ciudad = ctk.CTkEntry(self, placeholder_text="Nombre de la ciudad...", width=200)
        self.ciudad.pack(pady=10)

        self.btn_consulta = ctk.CTkButton(self, text="Consultar", width=50, command= lambda: self.ejecutar_consulta())
        self.btn_consulta.pack(pady=10)

        #SEGIMIENTO
        self.segi_lbl = ctk.CTkLabel(self,text="Hora Seguimiento",font=("Roboto", 15, "bold"))
        self.segi_lbl.pack(pady=10)

        #HORA
        self.frame_tiempo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tiempo.pack(pady=10)

        horas_validas = [f"{i:02d}" for i in range(24)]
        self.combo_hora = ctk.CTkOptionMenu(self.frame_tiempo, values=horas_validas, width=70)
        self.combo_hora.pack(side="left", padx=5)

        self.lbl_puntos = ctk.CTkLabel(self.frame_tiempo, text=":", font=("Roboto", 20))
        self.lbl_puntos.pack(side="left")

        minutos_validos = [f"{i:02d}" for i in range(60)]
        self.combo_minutos = ctk.CTkOptionMenu(self.frame_tiempo, values=minutos_validos, width=70)
        self.combo_minutos.pack(side="left", padx=5)

        #BOTON
        self.btn_seguir = ctk.CTkButton(self, text="Seguir", width=50, command= lambda: self.ejecutar_seguimiento())
        self.btn_seguir.pack(pady=10)

        #Info
        self.info_lbl = ctk.CTkLabel(self, text="", text_color="Red",font=("Roboto", 15))
        self.info_lbl.pack(pady=20)

        #volver al menu
        self.btn_volver = ctk.CTkButton(self, text="Volver al menu", command=self.volver_al_menu )
        self.btn_volver.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.volver_al_menu)
    def volver_al_menu(self):
        self.menu_principal.deiconify()
        self.destroy()


    def ejecutar_consulta(self):
        ciudad = self.ciudad.get()
        clima = consulta(ciudad=ciudad)
        if not ciudad:
            self.info_lbl.configure(text="Error: Debe de colocar alguna ciudad antes de hacer la petición")
            return
        elif clima is None:
            self.info_lbl.configure(text="Error: Ciudad no encontrada o Conexión a internet fallida")
            return
        self.ventanaconsulta = VentanaConsulta(datos=clima)

    def ejecutar_seguimiento(self):
        ciudad = self.ciudad.get()
        if not ciudad:
            self.info_lbl.configure(text="Error: Debe de colocar alguna ciudad antes de hacer la petición")
            return
        hora = f"{self.combo_hora.get()}:{self.combo_minutos.get()}"
        estado = seguimiento_cuidad(ciudad_s=ciudad,hora=hora)

        if estado == "Repetida":
            self.info_lbl.configure(text="Error: Ciudad repetida en la lista de seguimiento")
            return
        elif estado == "No encontrada":
            self.info_lbl.configure(text="Error: Ciudad no encontrada o Conexión a internet fallida")
            return
        elif estado == "Completo":
            self.info_lbl.configure(text="Ciudad añadida correctamente",text_color="green")

class VentanaConsulta(ctk.CTkToplevel):
    def __init__(self,datos):
        super().__init__()

        self.title("Consulta")
        self.geometry("400x350")

        #SALIDA CONSULTA
        self.salida_lbl = ctk.CTkLabel(self, text="", font=("Roboto", 12, "bold"))
        self.salida_lbl.pack(pady=20)

        #IMAGEN
        self.clima_visual = ctk.CTkLabel(self,text="")
        self.clima_visual.pack(pady=10)

        #DATOS
        self.salida_lbl.configure(text=f"| Pais: {datos["Pais"]} | Temperatura: {datos["Temperatura"]} | {datos["Descripción"]} |")

        icon = datos["icon"]
        url_icon = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        respuesta = requests.get(url_icon)

        imagen = io.BytesIO(respuesta.content)

        self.img_clima = ctk.CTkImage(
            light_image=Image.open(imagen),
            dark_image=Image.open(imagen),
            size=(100, 100)
        )

        self.clima_visual.configure(image=self.img_clima, text="")

        self.info_btn = ctk.CTkButton(self, text="Mas información", command= lambda :self.mostrar_informacion(datos))
        self.info_btn.pack(pady=10)

        self.map_btn = ctk.CTkButton(self, text="MAPA", command= lambda :self.mostar_ubi(datos))
        self.map_btn.pack(pady=10)

    def mostar_ubi(self,datos):

        lat = datos["lat"]
        lon = datos["lon"]
        url_mapa = f"https://www.google.com/maps/@{lat},{lon},12z"

        webbrowser.open(url_mapa)

    def mostrar_informacion(self,datos):

        hora_amanecer = datetime.fromtimestamp(datos["Amanecer"]).strftime("%H:%M")
        hora_atardecer = datetime.fromtimestamp(datos["Atardecer"]).strftime("%H:%M")


        text_info = (
            f"Ciudad: {datos["Ciudad"]}    "
            f"Pais: {datos["Pais"]}    "
            f"Temperatura: {datos["Temperatura"]}    "
            f"Sensaciones: {datos["Sensación"]}    "
            f"Humedad: {datos["Humedad"]}    "
            f"Descripción: {datos["Descripción"]}    "
            f"Velocidad: {datos["Velocidad"]}    "
            f"Presión: {datos["Presión"]}hPa    "
            f"Visibilidad: {datos["Visibilidad"]}km    "
            f"Amanecer:  {hora_amanecer}    "
            f"Atardecer: {hora_atardecer}    "
        )

        messagebox.showinfo("Información", text_info)