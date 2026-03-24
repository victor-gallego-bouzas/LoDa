import os
from dotenv import load_dotenv
import google.generativeai as genai
import fitz  # PyMuPDF
import PIL.Image
import io
import json


load_dotenv()
#Aquí conectamos con la API de gemini para extraer datos del albaran 
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

#Creamos función para la extracción de datos
def extraer_datos(ruta_pdf):
#En esta parte creamos una imagen del PDF
    doc = fitz.open(ruta_pdf)
    pagina = doc.load_page(0)
    pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_data = pix.tobytes("png")
    imagen_pil = PIL.Image.open(io.BytesIO(img_data))
    model = genai.GenerativeModel('gemini-flash-latest')
#Creamos el prompt para la extraccion correcta de datos
    prompt = """
    Analiza este albarán y extrae estos datos en JSON puro:
    {
      "n_albaran": "8 dígitos",
      "bultos": "número",
      "transportista": "SORIA o SESE o TR-PROPIO",
      "matricula": "texto",
      "remolque": "texto",
      "referencias": [ {"ref": "codigo", "cant": numero} ]
    }
    IMPORTANTE: Responde solo el JSON.
    """
#Llamamos a Gemini
    response = model.generate_content([prompt, imagen_pil])
    
    try:
        # Limpiamos la respuesta
        texto = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(texto)
    except Exception as e:
        return {"error": "Error al procesar", "detalle": str(e), "raw": response.text}

if __name__ == "__main__":
    archivo = "database/albaran_prueba.pdf"
    print("🚀 Probando con 'gemini-flash-latest'...")
    try:
        resultado = extraer_datos(archivo)
        print("\nRESULTADOS:")
        print(json.dumps(resultado, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"\nError: {e}")