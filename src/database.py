import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

#Cargamos la configuracion que no compartimos con Github porque contiene las llaves de la API
load_dotenv()

#Conexión con la base de datos
def conectar():
           return mysql.connector.connect(
            host='localhost',
            user='root',
            password='loda1234',
            database='loda'
        )

def insertar_todo_el_albaran(datos_gui):
    db = conectar()
    cursor = db.cursor()
    
    try:
#Aquí extraemos los datos que buscamos dandole varias opciones por si la API de Gemini extrae los datos de otra manera
        val_matricula = datos_gui.get("matricula") or datos_gui.get("Matricula", "S/M")
        val_remolque = datos_gui.get("remolque") or datos_gui.get("Remolque", "S/R")
        val_transp = datos_gui.get("transportista") or datos_gui.get("Datos de transportista", "DESCONOCIDO")
        val_albaran = datos_gui.get("n_albaran") or datos_gui.get("ALbarán Nº", "000000")
        val_bultos = datos_gui.get("bultos") or datos_gui.get("N . Bultos", "0")
        
#Insertamos los datos en la tabla CAMION
        sql_camion = "INSERT INTO camion (matricula_camion, matricula_remolque, transportista, fecha, hora) VALUES (%s, %s, %s, CURDATE(), CURTIME())"
        cursor.execute(sql_camion, (val_matricula, val_remolque, val_transp))
        id_camion_db = cursor.lastrowid # Guardamos el ID del camión
        
#Insertamos los datos en la tabla ALBARAN
        sql_albaran = "INSERT INTO albaran (num_albaran, num_bultos, id_camion) VALUES (%s, %s, %s)"
        cursor.execute(sql_albaran, (val_albaran, val_bultos, id_camion_db))
        id_albaran_db = cursor.lastrowid
        
#Insertamos los datos en la tabla MATERIAL
        referencias = datos_gui.get("referencias", [])
        
        if referencias:
            sql_material = "INSERT INTO material (ref_material, cantidad, id_albaran) VALUES (%s, %s, %s)"
            for item in referencias:
#Usamos los nombres que definimos en el prompt para Gemini ya ue es así como viene en la hoja
                ref = item.get("ref") or item.get("referencia", "N/A")
                cant = item.get("cant") or item.get("cantidad", 0)
                
#Insertamos usando id_albaran_db (la variable que definimos arriba)
                cursor.execute(sql_material, (ref, cant, id_albaran_db))

#Guardamos los datos
        db.commit()
        print(f"✅ Albarán {val_albaran} guardado")

#Aquí borraamos los datos en caso que ocurra un error como no leer albaran o dejar espacios en blanco
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
#Lanzamos un error en un ventanaa en caso de ue algo falle
        raise e 
    finally:
#Cerramos base de datos
        cursor.close()
        db.close()