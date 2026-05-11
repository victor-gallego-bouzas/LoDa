import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from monitor_carpeta import extraer_datos
from pantalla_verificado import PanelVerificacion

#Configuración de rutas donde entraran los archivos y donde irán una vez procesados
CARPETA_ENTRADA = "database/entrada/"
CARPETA_PROCESADOS = "database/procesados/"

class ManejadorPDF(FileSystemEventHandler):
    def __init__(self):
        self.procesando = False
        
    def on_created(self, event):

#Solo actuamos si es un archivo PDF
        if not event.is_directory and event.src_path.lower().endswith(".pdf"):
            
#Si ya estamos procesando un PDF, ignoramos cualquier otro evento para evitar duplicados
            if self.procesando:
                return

            self.procesando = True
            
            try:
                print(f"\n✨ Nuevo PDF detectado: {os.path.basename(event.src_path)}")
                time.sleep(2)
                
                print("🤖 Procesando con IA...")
                datos = extraer_datos(event.src_path)

                if "error" not in datos:
                    print("🖥️ Abriendo panel de verificación...")
                    app = PanelVerificacion(datos, event.src_path)
                    app.mainloop()
                else:
                    print(f"❌ Error al leer el PDF: {datos['error']}")
            
            finally:
                self.procesando = False

#Iniciamos la observación de la carpeta a la espera del ingreso de albaranes
if __name__ == "__main__":
    event_handler = ManejadorPDF()
    observer = Observer()
    observer.schedule(event_handler, CARPETA_ENTRADA, recursive=False)
    
    print(f"🚀 Monitor activo en: {CARPETA_ENTRADA}")
    print("A la espera de un ingreso")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()