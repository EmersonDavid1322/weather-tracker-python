import sqlite3
import sys
import os
from clases import CiudadClima

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
else:
    ruta_base = os.path.dirname(os.path.abspath(__file__))

CARPETA_DATA = os.path.join(ruta_base, "data")
os.makedirs(CARPETA_DATA, exist_ok=True)

RUTA_DB = os.path.join(CARPETA_DATA, "traker.db")

def crear_tablas():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        ciudad TEXT NOT NULL,
        pais TEXT NOT NULL,
        temperatura TEXT NOT NULL,
        sensacion TEXT NOT NULL,
        humedad TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        velocidad TEXT NOT NULL,
        hora_consulta TEXT NOT NULL,
        fecha_consulta TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seguimiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    ciudad TEXT NOT NULL,
    pais TEXT NOT NULL,
    temperatura TEXT NOT NULL,
    sensacion TEXT NOT NULL,
    humedad TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    velocidad TEXT NOT NULL,
    hora TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()


def guardar_ciudad_clima(informacion):

    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor() 

    if informacion.tipo == "Consulta":
        cursor.execute("""
    INSERT INTO consultas
    (tipo, ciudad, pais, temperatura, sensacion, humedad,  descripcion, velocidad, hora_consulta, fecha_consulta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,(
        informacion.tipo,
        informacion.ciudad,
        informacion.pais,
        informacion.temperatura,
        informacion.sensacion,
        informacion.humedad,
        informacion.descripcion,
        informacion.velocidad,
        informacion.hora_consulta,
        informacion.fecha_consulta
    )) 
    
    else:
        cursor.execute("""
    INSERT INTO seguimiento
    (tipo, ciudad, pais, temperatura, sensacion, humedad,  descripcion, velocidad, hora)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,(
        informacion.tipo,
        informacion.ciudad,
        informacion.pais,
        informacion.temperatura,
        informacion.sensacion,
        informacion.humedad,
        informacion.descripcion,
        informacion.velocidad,
        informacion.hora
    )) 
        
    conexion.commit()
    conexion.close()

        
def cargar_ciudad_Clima():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, tipo, ciudad, pais, temperatura, sensacion, humedad,  descripcion, velocidad, hora_consulta, fecha_consulta
        FROM consultas
    """)

    fila_consultas = cursor.fetchall()

    consultas = []

    for fila in fila_consultas:
        tipo=fila[1]
        id=fila[0]
        datos = {"Ciudad":fila[2], 
                "Pais":fila[3],
                "Temperatura":fila[4],
                "Sensación":fila[5],
                "Humedad":fila[6],
                "Descripción":fila[7],
                "Velocidad":fila[8],
                "Hora_Consulta":fila[9],
                "Fecha_Consulta":fila[10]}
        consulta = CiudadClima(id,tipo,datos)
        consultas.append(consulta)

    cursor.execute("""
    SELECT id, tipo, ciudad, pais, temperatura, sensacion, humedad,  descripcion, velocidad, hora
        FROM seguimiento
    """)

    fila_consultas = cursor.fetchall()

    seguimiento = []

    for fila in fila_consultas:
        tipo=fila[1]
        id=fila[0]
        datos = {"Ciudad":fila[2], 
                "Pais":fila[3],
                "Temperatura":fila[4],
                "Sensación":fila[5],
                "Humedad":fila[6],
                "Descripción":fila[7],
                "Velocidad":fila[8],
                "Hora":fila[9]}
        seguir = CiudadClima(id,tipo,datos)
        seguimiento.append(seguir)

    conexion.close()

    return consultas, seguimiento

def editar_seguimiento(id,editar_nombre,nombre,hora):

    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()

    if editar_nombre is True:
        if hora != None:
            cursor.execute("""
            UPDATE seguimiento
            SET ciudad = ?,
            hora = ?
            WHERE id = ?
            """, (nombre, hora, id))
        else:
            cursor.execute("""
            UPDATE seguimiento
            SET ciudad = ?
            WHERE id = ?
            """, (nombre, id))

    else:
        cursor.execute("""
            UPDATE seguimiento
            SET hora = ?
            WHERE id = ?
            """, (hora, id))

    conexion.commit()
    conexion.close()

def eliminar_ciudad(informacion):

    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()

    tipo = informacion.tipo
    ciudad_id = informacion.id

    if tipo == "Consulta":
    
        cursor.execute(""" 
    DELETE FROM consultas
    WHERE id = ?
    """, (ciudad_id,))
        
    else:
        
        cursor.execute("""
    DELETE FROM seguimiento
    WHERE id = ?
    """, (ciudad_id,))
        
    conexion.commit()
    conexion.close()