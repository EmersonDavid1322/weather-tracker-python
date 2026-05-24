import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image
import io
import requests
from datetime import datetime
import webbrowser
from DB_traker_clima import crear_tablas
from main_menu import consulta

crear_tablas()

class VentanaMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Clima")
        self.geometry("600x400")

        #CONSULTA
        self.consulta_lbl = ctk.CTkLabel(self, text="Consulta", font=("Roboto", 15, "bold"))
        self.consulta_lbl.pack(pady=5)

        self.consulta = ctk.CTkEntry(self, placeholder_text="Nombre de la ciudad...", width=200)
        self.consulta.pack(pady=10)

        self.btn_consulta = ctk.CTkButton(self, text="Listo", width=50, command= lambda: self.ejecutar_consulta())
        self.btn_consulta.pack(pady=10)


    def ejecutar_consulta(self):
        ciudad = self.consulta.get()
        clima = consulta(ciudad=ciudad)
        if not ciudad:
            messagebox.showerror("Consulta", "Debe de colocar alguna ciudad antes de hacer la petición")
            return
        elif clima is None:
            messagebox.showerror("Consulta", "Ciudad no encontrada")
            return
        self.ventanaconsulta = VentanaConsulta(datos=clima)



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


if __name__ == "__main__":
    ventana = VentanaMenu()
    ventana.mainloop()