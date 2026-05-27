import customtkinter as ctk
import tkinter.messagebox as messagebox
from clima_interfaz import VentanaClima
from servicios import mostras_seguimiento
from DB_traker_clima import editar_seguimiento

class VentanaMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Menu")
        self.geometry("600x400")

        #CLIMA
        self.clima_lbl = ctk.CTkLabel(self, text="Clima", font=("Roboto", 15, "bold"))
        self.clima_lbl.pack(pady=20)

        self.clima_btn = ctk.CTkButton(self, text="Entrar", command=self.clima)
        self.clima_btn.pack(pady=10)

        #Ciudades Seguidas
        self.seguidas_lbl = ctk.CTkLabel(self, text="Ciudades en seguimiento", font=("Roboto", 15, "bold"))
        self.seguidas_lbl.pack(pady=10)

        self.seguidas_btn = ctk.CTkButton(self, text="Entrar", command=VentanaSeguidas)
        self.seguidas_btn.pack(pady=10)

    def clima(self):
        self.withdraw()
        ventana_hija = VentanaClima(self)

class VentanaSeguidas(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Seguimiento")
        self.geometry("600x400")

        #TITULO
        self.segui_lbl = ctk.CTkLabel(self, text="Ciudades en seguimiento", font=("Roboto", 15, "bold"))
        self.segui_lbl.pack(pady=10)

        #FRAME
        self.scroll_segui = ctk.CTkScrollableFrame(self, width=550, height=350)
        self.scroll_segui.pack(padx=10, pady=10, fill="both", expand=True)

        self,self.cargar_seguidas()

    def cargar_seguidas(self):
        ciudades = mostras_seguimiento()

        seguidas_reciente = ciudades[::-1]

        for i, entrada in enumerate(seguidas_reciente):
            numero = len(ciudades) - 1

            fila = ctk.CTkFrame(self.scroll_segui, fg_color="transparent")
            fila.pack(fill="x", pady=2)

            lbl_num = ctk.CTkLabel(fila, text=f"[{numero:03d}]", font=("Consolas", 12), text_color="#5dade2")
            lbl_num.pack(side="left", padx=5)

            lbl_text = ctk.CTkLabel(fila, text=f"| Ciudad: {entrada.ciudad} | Pais: {entrada.pais} | Hora: {entrada.hora} |" )
            lbl_text.pack(side="left",padx=5)

            btn_editar = ctk.CTkButton(fila, text="Editar", command= lambda id_ciudad=entrada.id : VentanaEditar(id=id_ciudad))
            btn_editar.pack(side="left", padx=5)

class VentanaEditar(ctk.CTkToplevel):
    def __init__(self,id):
        super().__init__()

        self.title("Editar")
        self.geometry("300x200")

        #Ciudad
        self.ciudad_lbl = ctk.CTkLabel(self, text="Nombre ciudad")
        self.ciudad_lbl.pack(pady=10)

        self.ciudad_entrada = ctk.CTkEntry(self, placeholder_text="Nombre(Opcional)", width=200)
        self.ciudad_entrada.pack(pady=10)

        #Hora
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
        self.btn_editar = ctk.CTkButton(self, text="Editar", command= lambda id_ciudad= id :self.editar(id=id_ciudad))
        self.btn_editar.pack(pady=10)

    def editar(self,id):
        ciudad = self.ciudad_entrada.get()
        hora = f"{self.combo_hora.get()}:{self.combo_minutos.get()}"
        editar_nombre = False

        if ciudad == "" and hora == "00:00":
            messagebox.showerror("Editar","Debe de rellenar al menos una opción")
            return
        elif hora == "00:00":
            hora = None

        if ciudad != "":
            confirmacion = messagebox.askyesno("Editar","Advertencia: Al editar el nombre de una ciudad se eliminaran los resgistro posteriores de esta, ¿desea continuar?")
            if confirmacion == False:
                self.destroy()
                return
            else:
                editar_nombre = True
                editar_seguimiento(id=id,
                                    editar_nombre=editar_nombre,
                                    nombre=ciudad,
                                    hora=hora)
        else:
            editar_seguimiento(id=id,
                                editar_nombre=editar_seguimiento,
                                nombre=None,
                                hora=hora)
        
        messagebox.showinfo("Editar",f"Ciudad {ciudad} editada correctamente")
        self.destroy()





if __name__ == "__main__":
    menu = VentanaMenu()
    menu.mainloop()