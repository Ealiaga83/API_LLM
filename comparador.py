# comparador.py
from openai import OpenAI
from pydantic import BaseModel
import logging

# 🔧 Logging
logging.basicConfig(level=logging.INFO)

class Servicio(BaseModel):
    nombre: str
    precio: float

class Factura(BaseModel):
    id: int
    cliente: str
    fecha: str
    servicios: list[Servicio]

def construir_prompt(f1: Factura, f2: Factura) -> str:
    def servicios_a_texto(servicios):
        return "\n".join([f"- {s.nombre}: ${s.precio}" for s in servicios])
    return f"""
Cliente: {f1.cliente}

Factura actual:
Fecha: {f1.fecha}
Servicios:
{servicios_a_texto(f1.servicios)}

Factura anterior:
Fecha: {f2.fecha}
Servicios:
{servicios_a_texto(f2.servicios)}

Compara ambas facturas y genera una descripción en lenguaje natural.
"""

def comparar_facturas_con_ia(f1: Factura, f2: Factura, deepseek_client: OpenAI, openai_client: OpenAI):
    prompt = construir_prompt(f1, f2)
    logging.info(f"Prompt enviado:\n{prompt}")

    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        resultado = response.choices[0].message.content
        logging.info("Respuesta generada con DeepSeek ✅")
        return {"modelo": "deepseek-chat", "resultado": resultado}

    except Exception as e:
        logging.warning(f"DeepSeek falló: {str(e)}. Usando OpenAI como respaldo...")

        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            resultado = response.choices[0].message.content
            logging.info("Respuesta generada con OpenAI ✅")
            return {"modelo": "gpt-3.5-turbo", "resultado": resultado}

        except Exception as e2:
            logging.error(f"OpenAI también falló: {str(e2)}")
            raise RuntimeError(f"Error al generar respuesta: {str(e2)}")