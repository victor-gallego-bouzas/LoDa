import shutil
import os
import customtkinter as ctk
from ocr import extraer_datos  # Importamos tu función de IA
from database import insertar_todo_el_albaran
import json

class PanelVerificacion(ctk.CTk):
    def __init__(self, datos_ia,ruta_pdf):
        super().__init__()
        self.ruta_pdf = ruta_pdf

        self.title("LoDa - Verificación de Albarán")
        self.geometry("500x600")
        ctk.set_appearance_mode("dark")
        self.referencias_raw = datos_ia.get("referencias", [])

        self.label_titulo = ctk.CTkLabel(self, text="Verifica los datos del Albarán", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        # Creamos campos de entrada para cada dato
        self.campos = {}
        for clave, valor in datos_ia.items():
            if clave == "error": continue
            
            frame = ctk.CTkFrame(self)
            frame.pack(fill="x", padx=20, pady=5)
            
            lbl = ctk.CTkLabel(frame, text=f"{clave}:", width=120, anchor="w")
            lbl.pack(side="left", padx=10)
            
            entry = ctk.CTkEntry(frame, width=250)
            entry.insert(0, str(valor))
            entry.pack(side="right", padx=10, pady=5)
            
            self.campos[clave] = entry

        # Botón para Guardar
        self.btn_guardar = ctk.CTkButton(self, text="Confirmar y Guardar en BD", 
                                         fg_color="green", hover_color="darkgreen",
                                         command=self.guardar_datos)
        self.btn_guardar.pack(pady=30)

    def guardar_datos(self):
        datos_finales = {clave: entry.get() for clave, entry in self.campos.items()}
        datos_finales["referencias"] = self.referencias_raw
        
        try:
            insertar_todo_el_albaran(datos_finales)
            print("✅ Guardado en BD.")

            # --- NUEVA LÓGICA: MOVER ARCHIVO ---
            carpeta_dest = "database/procesados/"
            if not os.path.exists(carpeta_dest):
                os.makedirs(carpeta_dest)
            
            nombre_archivo = os.path.basename(self.ruta_pdf)
            shutil.move(self.ruta_pdf, os.path.join(carpeta_dest, nombre_archivo))
            print(f"📂 Archivo movido a {carpeta_dest}")
            # ----------------------------------

            self.destroy()
        except Exception as e:
            print(f"❌ Error: {e}")
if __name__ == "__main__":
    archivo_pdf = "database/albaran_prueba.pdf"
    print("🤖 La IA está leyendo el PDF...")
    
    datos_extraidos = extraer_datos(archivo_pdf)
    
    if "error" not in datos_extraidos:
        app = PanelVerificacion(datos_extraidos)
        app.mainloop()
    else:
        print("Error de la IA:", datos_extraidos["error"])