import os
from dotenv import load_dotenv
import google.generativeai as genai
import fitz  # PyMuPDF
import PIL.Image
import io
import json


load_dotenv()
# --- 1. CONFIGURACIÓN ---
# He puesto la clave que venía en tu curl, asegúrate de que es la tuya
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

if not API_KEY:
    print("❌ ERROR: No se encontró la API_KEY en el archivo .env")
else:
    genai.configure(api_key=API_KEY)

def procesar_albaran_con_ia(ruta_pdf):
    # Abrimos el PDF y lo pasamos a imagen
    doc = fitz.open(ruta_pdf)
    pagina = doc.load_page(0)
    pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_data = pix.tobytes("png")
    imagen_pil = PIL.Image.open(io.BytesIO(img_data))

    # --- CAMBIO CLAVE AQUÍ ---
    # Usamos el nombre exacto del inicio rápido que pasaste
    model = genai.GenerativeModel('gemini-flash-latest')

    prompt = """
    Analiza este albarán y extrae estos datos en JSON puro:
    - n_albaran (8 dígitos)
    - bultos (número)
    - matriculas (lista de matrículas)
    - referencias (lista con 'ref' y 'cant')
    - soria (true/false si aparece la palabra)
    """

    # Llamada a la IA
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
        resultado = procesar_albaran_con_ia(archivo)
        print("\n✅ ¡POR FIN! RESULTADOS:")
        print(json.dumps(resultado, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"\n❌ Error: {e}")