# main.py
from fastapi import FastAPI, HTTPException, Body
from dotenv import load_dotenv
import os
import webbrowser
import threading
import logging
from openai import OpenAI
from comparador import Factura, comparar_facturas_con_ia

# 🔧 Logging
logging.basicConfig(level=logging.INFO)

# 🔐 Cargar claves desde .env
load_dotenv()
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

# 🧠 Inicializar clientes
deepseek_client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com/v1")
openai_client = OpenAI(api_key=openai_key)

# 🚀 FastAPI
app = FastAPI(title="Comparador Inteligente de Facturas con Fallback")

@app.post("/comparar")
def comparar_endpoint(
    factura_actual: Factura = Body(...),
    factura_anterior: Factura = Body(...)
):
    try:
        resultado = comparar_facturas_con_ia(factura_actual, factura_anterior, deepseek_client, openai_client)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🌐 Abrir Swagger UI automáticamente
if __name__ == "__main__":
    def abrir_docs():
        webbrowser.open_new("http://127.0.0.1:8000/docs")
    threading.Timer(1.5, abrir_docs).start()

    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)