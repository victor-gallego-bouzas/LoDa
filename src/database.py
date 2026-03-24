import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
#Conexión con base de datos
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
        # Extraemos valores (usando varios nombres por si la IA varía)
        val_matricula = datos_gui.get("matricula") or datos_gui.get("Matricula", "S/M")
        val_remolque = datos_gui.get("remolque") or datos_gui.get("Remolque", "S/R")
        val_transp = datos_gui.get("transportista") or datos_gui.get("Datos de transportista", "DESCONOCIDO")
        val_albaran = datos_gui.get("n_albaran") or datos_gui.get("ALbarán Nº", "000000")
        val_bultos = datos_gui.get("bultos") or datos_gui.get("N . Bultos", "0")
        
        # 1. Tabla CAMION
        sql_camion = "INSERT INTO camion (matricula_camion, matricula_remolque, transportista, fecha, hora) VALUES (%s, %s, %s, CURDATE(), CURTIME())"
        cursor.execute(sql_camion, (val_matricula, val_remolque, val_transp))
        id_camion_db = cursor.lastrowid # Guardamos el ID del camión
        
        # 2. Tabla ALBARAN
        sql_albaran = "INSERT INTO albaran (num_albaran, num_bultos, id_camion) VALUES (%s, %s, %s)"
        cursor.execute(sql_albaran, (val_albaran, val_bultos, id_camion_db))
        id_albaran_db = cursor.lastrowid # <--- ESTA ES LA VARIABLE QUE FALLABA
        
        # 3. Tabla MATERIAL
        referencias = datos_gui.get("referencias", [])
        
        if referencias:
            sql_material = "INSERT INTO material (ref_material, cantidad, id_albaran) VALUES (%s, %s, %s)"
            for item in referencias:
                # Usamos los nombres que definimos en el prompt de la IA
                ref = item.get("ref") or item.get("referencia", "N/A")
                cant = item.get("cant") or item.get("cantidad", 0)
                
                # Insertamos usando id_albaran_db (la variable que definimos arriba)
                cursor.execute(sql_material, (ref, cant, id_albaran_db))
        
        db.commit()
        print(f"✅ Éxito total: Albarán {val_albaran} guardado con sus materiales.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error real en la inserción: {e}")
        # Lanzamos el error para que la GUI no diga "Guardado correctamente" si ha fallado
        raise e 
    finally:
        cursor.close()
        db.close()