import customtkinter as ctk
import os
import shutil
from database import insertar_todo_el_albaran
from tkinter import messagebox
from impresion import generar_documentos_especificos

#Definimos como se nos va a ver la pantalla principal donde nos saldran los daos a verificar
class PanelVerificacion(ctk.CTk):
    def __init__(self, datos_ia, ruta_pdf):
        super().__init__()
        self.ruta_pdf = ruta_pdf
        self.title("LoDa - Verificación de Datos")
        self.geometry("600x750")
        ctk.set_appearance_mode("dark")
        self.label_titulo = ctk.CTkLabel(self, text="Verificación de Albarán", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)
        self.campos_cabecera = {}
        claves_cabecera = ["n_albaran", "matricula", "remolque", "transportista", "bultos"]

#la parte de los datos (matricula, albaran, remolque, transportista)
        for clave in claves_cabecera:
            if clave in datos_ia:
                frame = ctk.CTkFrame(self)
                frame.pack(fill="x", padx=20, pady=5) 
                lbl = ctk.CTkLabel(frame, text=f"{clave.upper()}:", width=120, anchor="w")
                lbl.pack(side="left", padx=10)
                entry = ctk.CTkEntry(frame, width=300)
                entry.insert(0, str(datos_ia[clave]))
                entry.pack(side="right", padx=10, pady=5)
                self.campos_cabecera[clave] = entry

#La parte como se mostrará el listado de materiales y sus cantidades 
        ctk.CTkLabel(self, text="MATERIALES DETECTADOS", font=("Arial", 14, "bold")).pack(pady=(20, 10))
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=250)
        self.scroll_frame.pack(padx=20, pady=5)
        self.filas_materiales = []
        referencias = datos_ia.get("referencias", [])
        
        for item in referencias:
            fila_frame = ctk.CTkFrame(self.scroll_frame)
            fila_frame.pack(fill="x", pady=2)

            e_ref = ctk.CTkEntry(fila_frame, width=350)
            e_ref.insert(0, str(item.get("ref", "")))
            e_ref.pack(side="left", padx=5)

            e_cant = ctk.CTkEntry(fila_frame, width=80)
            e_cant.insert(0, str(item.get("cant", "")))
            e_cant.pack(side="left", padx=5)

            self.filas_materiales.append({"ref": e_ref, "cant": e_cant})

#Definimos el formaato de los diferentes botones  
        self.btn_guardar = ctk.CTkButton(self, text="CONFIRMAR Y GUARDAR EN BD", 
                                         fg_color="green", hover_color="darkgreen",
                                         command=self.guardar_datos)
        self.btn_guardar.pack(pady=(30, 10))

        self.btn_salir = ctk.CTkButton(self, text="SALIR Y CERRAR", 
                                       fg_color="#E74C3C", hover_color="#C0392B",
                                       command=self.terminar_programa)
        self.btn_salir.pack(pady=10)

#Con esta función 
    def guardar_datos(self):
#Aqui congemos los datos ya correguidos que tenemos en la pantalla de verificacion
        datos_finales = {clave: entry.get() for clave, entry in self.campos_cabecera.items()}
        
#Recoger materiales y sus cantidades
        lista_materiales = []
        for fila in self.filas_materiales:
            lista_materiales.append({
                "ref": fila["ref"].get(),
                "cant": fila["cant"].get()
            })
        datos_finales["referencias"] = lista_materiales
        
#Guardamos en la Base de datos y lo metemos en una try para que si salta un error en el guardado no se cierre el programa
        try:
            print("🗄️ Guardando en Base de Datos...")
            insertar_todo_el_albaran(datos_finales)
            
#Registrar en Excels de Semanal y Diario
            matricula_val = datos_finales.get("matricula", "")
            remolque_val = datos_finales.get("remolque", "")
            
            if matricula_val:
                from rellenado_excel import registrar_entrada_excel, registrar_horario_diario
                registrar_entrada_excel(matricula_val, remolque_val)
                registrar_horario_diario(datos_finales)
            
#Generar y imprimimos (creamos un print d emomento)de 
            print("🖨️ Generando documentos de salida y comprobación...")
            generar_documentos_especificos(datos_finales)

#Mover PDF a procesados
            dest = "database/procesados/"
            if not os.path.exists(dest): 
                os.makedirs(dest)
            shutil.move(self.ruta_pdf, os.path.join(dest, os.path.basename(self.ruta_pdf)))
            print("✅ Proceso completado: BD + Excels + Impresión + Archivo movido.")
            messagebox.showinfo("Éxito", "Albarán procesado correctamente.\nDocumentos de salida listos.")
            self.destroy()
            
        except Exception as e:
            print(f"❌ Error al procesar: {e}")
            messagebox.showerror("Error de Guardado", f"No se pudo completar el proceso: {e}\n\nVerifica que los Excels estén cerrados.")

#La funciñon del botón "Salir y Cerrar"
    def terminar_programa(self):
        print("🛑 Sistema apagado por el usuario.")
        self.quit()
        os._exit(0)