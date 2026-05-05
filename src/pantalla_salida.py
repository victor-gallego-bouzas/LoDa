import customtkinter as ctk
from tkinter import messagebox
from rellenado_excel import registrar_salida_semanal, registrar_salida_diaria

#Creamos una vantalla hija donde registraremos la salida de los camiones 
class PantallaSalida(ctk.CTkToplevel):
#Creamos la estética de la pantalla y la funcionalidad del botón    
    def __init__(self):
        super().__init__()
        self.title("LoDa - Registro de Salida (Excel)")
        self.geometry("400x300")
        self.grab_set()
        ctk.CTkLabel(self, text="SALIDA", font=("Arial", 18, "bold")).pack(pady=20)      
        ctk.CTkLabel(self, text="Introduce Matrícula o Remolque:").pack(pady=5)
        self.entry_id = ctk.CTkEntry(self, width=250, placeholder_text="Ej: 1234ABC")
        self.entry_id.pack(pady=10)
        self.btn_confirmar = ctk.CTkButton(self, text="REGISTRAR SALIDA", 
                                          fg_color="#E67E22", 
                                          command=self.ejecutar_registro_excel)
        self.btn_confirmar.pack(pady=20)

#Creamos lla función que nos pide la entrada de matrículaa y ingresa en los excel correspondietes la hora de salida con el
#debido control de errores en caso de que falle o no encuentre matrícula
    def ejecutar_registro_excel(self):
        identificador = self.entry_id.get().strip().upper()       
        if not identificador:
            messagebox.showwarning("Atención", "Por favor, introduce una matrícula.")
            return
        try:
            res_semanal = registrar_salida_semanal(identificador)
            res_diario = registrar_salida_diaria(identificador)
            if res_semanal or res_diario:
                messagebox.showinfo("Éxito", f"Hora de salida registrada para: {identificador}")
                self.destroy()
            else:
                messagebox.showwarning("No encontrado", 
                    "No se encontró el vehículo")                
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al acceder a los Excel: {e}")