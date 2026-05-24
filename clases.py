class CiudadClima:
    def __init__(self, id, tipo, datos):
        self.id = id
        self.tipo = tipo
        self.ciudad = datos["Ciudad"]
        self.pais = datos["Pais"]
        self.temperatura = datos["Temperatura"]
        self.sensacion = datos["Sensación"]
        self.humedad = datos["Humedad"]
        self.descripcion = datos["Descripción"]
        self.velocidad = datos["Velocidad"]

        if tipo == "Consulta":
            self.hora_consulta = datos["Hora_Consulta"]
            self.fecha_consulta = datos["Fecha_Consulta"]
        else:
            self.hora = datos["Hora"]