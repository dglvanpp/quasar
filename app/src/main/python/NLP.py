import re
import json


def analizar_texto_universal(texto_usuario):
    """
    Recibe una oración en lenguaje natural y devuelve un JSON con:
    - materia / rama detectadas (o null si no se reconoce nada)
    - datos: diccionario de variables numéricas encontradas explícitas (ej. "V=12")
    - reconocido: True/False
    - mensaje: texto amigable para mostrar si algo falla

    Se devuelve como JSON (string) para que sea trivial de leer desde Kotlin
    con org.json, sin pelearse con la conversión de dict de Python a Java.
    """
    texto = texto_usuario.lower()

    # 1. Extraer pares "clave=valor" explícitos, ej: "V=12, R=4"
    datos = {}
    for m in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(-?\d+\.?\d*)', texto_usuario):
        datos[m.group(1)] = m.group(2)

    # 2. Reglas materia/rama por palabras clave (se revisan en orden,
    #    la primera coincidencia gana)
    reglas = [
        ("matematicas", "calculo_diferencial", ["derivada", "derivar", "límite", "limite", "máximo y mínimo", "maximo y minimo", "punto critico", "punto crítico"]),
        ("matematicas", "calculo_integral", ["integral", "integrar", "área bajo la curva", "area bajo la curva", "volumen de revolución", "volumen de revolucion", "longitud de arco"]),
        ("matematicas", "geometria_analitica", ["distancia entre puntos", "pendiente", "circunferencia", "parábola", "parabola", "elipse", "hipérbola", "hiperbola"]),
        ("fisica", "electrostatica", ["ley de coulomb", "coulomb", "campo eléctrico", "campo electrico", "capacitor", "carga eléctrica", "carga electrica"]),
        ("fisica", "electrodinamica", ["ley de ohm", "resistencia", "corriente eléctrica", "corriente electrica", "potencia eléctrica", "potencia electrica", "circuito"]),
        ("fisica", "electromagnetismo", ["campo magnético", "campo magnetico", "fuerza magnética", "fuerza magnetica", "solenoide", "amperímetro", "amperimetro", "voltímetro", "voltimetro"]),
        ("fisica", "induccion_ondas", ["ley de faraday", "transformador", "fem inducida", "onda", "frecuencia"]),
        ("quimica", "leyes_gases", ["ley de boyle", "ley de charles", "gas ideal", "presión y volumen", "presion y volumen"]),
        ("quimica", "soluciones", ["molaridad", "dilución", "dilucion", "titulación", "titulacion"]),
        ("quimica", "termoquimica", ["calor específico", "calor especifico", "entalpía", "entalpia", "ley de hess"]),
        ("quimica", "acido_base", ["ph", "poh", "ácido", "acido", "base"]),
        ("quimica", "electroquimica", ["electrólisis", "electrolisis", "electrodeposición", "electrodeposicion", "faraday"]),
        ("quimica", "peso_molecular", ["peso molecular", "masa molar"]),
        ("probabilidad", "estadistica_descriptiva", ["media", "mediana", "moda", "desviación estándar", "desviacion estandar", "varianza"]),
        ("probabilidad", "combinatoria", ["combinaciones", "permutaciones", "factorial"]),
        ("probabilidad", "probabilidad_binomial", ["distribución binomial", "distribucion binomial", "binomial"]),
        ("probabilidad", "teorema_bayes", ["teorema de bayes", "bayes"]),
    ]

    for materia, rama, palabras in reglas:
        if any(p in texto for p in palabras):
            resultado = {
                "materia": materia,
                "rama": rama,
                "datos": datos,
                "reconocido": True,
                "mensaje": f"Detecté: {materia} / {rama}"
            }
            return json.dumps(resultado, ensure_ascii=False)

    if datos:
        resultado = {
            "materia": None,
            "rama": None,
            "datos": datos,
            "reconocido": False,
            "mensaje": "Encontré datos numéricos pero no identifiqué el tema. Elige materia y rama manualmente."
        }
    else:
        resultado = {
            "materia": None,
            "rama": None,
            "datos": {},
            "reconocido": False,
            "mensaje": "No reconocí el tema. Intenta con palabras como 'ley de ohm', 'derivada', 'ph', 'combinaciones'..."
        }
    return json.dumps(resultado, ensure_ascii=False)
