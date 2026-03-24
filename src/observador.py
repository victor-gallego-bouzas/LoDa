import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ocr import extraer_datos
from pantalla_verificado import PanelVerificacion

# Configuración de rutas
CARPETA_ENTRADA = "database/entrada/"
CARPETA_PROCESADOS = "database/procesados/"

class ManejadorPDF(FileSystemEventHandler):
    def on_created(self, event):
        # Solo actuamos si es un archivo PDF
        if not event.is_directory and event.src_path.lower().endswith(".pdf"):
            print(f"\n✨ Nuevo PDF detectado: {os.path.basename(event.src_path)}")
            
            # Pausa de seguridad para que el sistema suelte el archivo tras crearlo
            time.sleep(2)
            
            # 1. Llamar a la IA
            print("🤖 Procesando con IA...")
            datos = extraer_datos(event.src_path)
            
            if "error" not in datos:
                print("🖥️ Abriendo panel de verificación...")
                # IMPORTANTE: Pasamos 'datos' Y 'event.src_path' (la ruta del archivo)
                app = PanelVerificacion(datos, event.src_path)
                app.mainloop()
            else:
                print(f"❌ Error al leer el PDF: {datos['error']}")

if __name__ == "__main__":
    # Creamos las carpetas si no existen
    for carpeta in [CARPETA_ENTRADA, CARPETA_PROCESADOS]:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"📁 Carpeta creada: {carpeta}")

    event_handler = ManejadorPDF()
    observer = Observer()
    observer.schedule(event_handler, CARPETA_ENTRADA, recursive=False)
    
    print(f"🚀 Monitor activo en: {CARPETA_ENTRADA}")
    print("Mueve un PDF a la carpeta 'entrada' para probar.")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()