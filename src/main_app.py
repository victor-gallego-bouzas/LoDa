import customtkinter as ctk
import subprocess
import threading
import os
import sys
from tkinter import messagebox

class RedirigirConsola:
    def __init__(self, app_principal):
        self.app = app_principal

    def write(self, texto):
        if texto.strip():
            self.app.after(0, self.app.escribir_log, texto.strip())

    def flush(self):
        pass

class AppPrincipal(ctk.CTk):

#Aquí vamos a deficir la aparencia de nuestra pantalla de control principal donde iniciaremos el
#observador que controlará los albarenes que entren, boton para abrir la carpeta de los albaranes
#para registrar la salida y el boton de salida
    def __init__(self):       
        super().__init__()
        self.title("LoDa Logistics v1.0")
        self.geometry("500x700") # Ajustado para que quepa el cuadro de log
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

# Cuadro de texto para seguir la actividad
        self.label_log = ctk.CTkLabel(self, text="REGISTRO DE ACTIVIDAD", font=("Arial", 10, "bold"), text_color="gray")
        self.label_log.pack(pady=(15, 0))
        
        self.log_text = ctk.CTkTextbox(self, width=420, height=180, font=("Consolas", 11))
        self.log_text.pack(padx=20, pady=5)
        self.log_text.configure(state="disabled")

        sys.stdout = RedirigirConsola(self)
        self.status_label = ctk.CTkLabel(self, text="Estado: SISTEMA APAGADO ⚪", text_color="gray")
        self.status_label.pack(pady=10)

        self.btn_salir = ctk.CTkButton(self, text="APAGAR", 
                                       fg_color="#E74C3C", hover_color="#C0392B",
                                       height=40,
                                       command=self.salir_total)
        self.btn_salir.pack(pady=20)


    def escribir_log(self, mensaje):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"> {mensaje}\n")
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

#Creamos un hilo para que el archivo observador funcione por separado y este observando la carpeta de 
#entrada a la espera de ver un archivo nuevo  y como va a ser una app portable le damos una ruta relativa 
    def lanzar_monitor(self):
        
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        ruta_monitor = os.path.join(base_path, "observador.py")
        
        def ejecutar():

            proceso = subprocess.Popen(
                [sys.executable, "-u", ruta_monitor], 
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
#Leemos la salida del observador línea por línea
            for linea in iter(proceso.stdout.readline, ''):
                if linea:        
                    self.after(0, self.escribir_log, linea.strip())
            
            proceso.stdout.close()
            proceso.wait()
            
        threading.Thread(target=ejecutar, daemon=True).start()        
        self.status_label.configure(text="Estado: MONITOR ACTIVO 👀", text_color="#2ecc71")
        self.btn_monitor.configure(state="disabled", text="MONITOR EN EJECUCIÓN...")
        self.escribir_log("Monitor iniciado correctamente.")

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