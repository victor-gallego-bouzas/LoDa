import customtkinter as ctk
import subprocess
import threading
import os
import sys
from tkinter import messagebox

class AppPrincipal(ctk.CTk):

#Aquí vamos a deficir la aparencia de nuestra pantalla de control principal donde iniciaremos el
#observador que controlará los albarenes que entren, boton para abrir la carpeta de los albaranes
#para registrar la salida y el boton de salida
    def __init__(self):       
        super().__init__()
        self.title("LoDa Logistics v1.0")
        self.geometry("450x550") 
        ctk.set_appearance_mode("dark")
        self.label = ctk.CTkLabel(self, text="Control de Albaranes LoDa", font=("Arial", 22, "bold"))
        self.label.pack(pady=30)
        self.btn_monitor = ctk.CTkButton(self, text="MONITOR DE ENTRADA", 
                                          fg_color="#2ecc71", hover_color="#27ae60",
                                          height=45, font=("Arial", 13, "bold"),
                                          command=self.lanzar_monitor)
        self.btn_monitor.pack(pady=10)
        self.btn_carpeta = ctk.CTkButton(self, text="CARPETA DE ENTRADA", 
                                          command=self.abrir_carpeta)
        self.btn_carpeta.pack(pady=10)
        self.label_sep = ctk.CTkLabel(self, text="──────────────────────────", text_color="gray")
        self.label_sep.pack(pady=10)
        self.btn_salida = ctk.CTkButton(self, text="REGISTRAR SALIDA", 
                                         fg_color="#D35400", hover_color="#A04000",
                                         height=45, font=("Arial", 13, "bold"),
                                         command=self.abrir_ventana_salida)
        self.btn_salida.pack(pady=10)
        self.btn_salir = ctk.CTkButton(self, text="APAGAR", 
                                       fg_color="#E74C3C", hover_color="#C0392B",
                                       height=40,
                                       command=self.salir_total)
        self.btn_salir.pack(pady=30)
        self.status_label = ctk.CTkLabel(self, text="Estado: SISTEMA APAGADO ⚪", text_color="gray")
        self.status_label.pack(pady=10)

#Creamos un hilo para que ell archivo observador funcione por separado y este observando la carpeta de 
#entrada a la espera de ver un archivo nuevo   
    def lanzar_monitor(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_monitor = os.path.join(directorio_actual, "observador.py")
        def ejecutar():
            subprocess.run([sys.executable, ruta_monitor])
        threading.Thread(target=ejecutar, daemon=True).start()        
        self.status_label.configure(text="Estado: MONITOR ACTIVO 👀", text_color="#2ecc71")
        self.btn_monitor.configure(state="disabled", text="MONITOR EN EJECUCIÓN...")

#Para ejecutar el monitor donde ingresamos la salida del camión
    def abrir_ventana_salida(self):
        try:
            from pantalla_salida import PantallaSalida
            ventana = PantallaSalida()
            ventana.focus()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de salida: {e}")

#Función para abrir la carpeta donde se introducen los albaranes
    def abrir_carpeta(self):
        ruta = os.path.abspath("database/entrada/")
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        os.startfile(ruta)

#Función para salis del programa
    def salir_total(self):
        print("🛑 Apagando sistema...")
        self.destroy() 
        os._exit(0)

#Bloque de arranque
if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()