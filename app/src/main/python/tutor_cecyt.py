# ==========================================
# TUTOR VIRTUAL CECYT 3 - ENRUTADOR MAESTRO
# ==========================================
import matematicas
import fisica
import quimica
import probabilidad
import graficadora
import NLP


def procesar_consulta_android(materia, rama, datos_entrada):
    """
    Función principal que Chaquopy llama desde Kotlin/Java.
    Puente entre la interfaz (MainActivity) y los motores de Python.
    """
    try:
        if materia == "matematicas":
            respuesta = matematicas.experto_matematicas(datos_entrada, rama)
        elif materia == "fisica":
            respuesta = fisica.experto_fisica(datos_entrada, rama)
        elif materia == "quimica":
            respuesta = quimica.experto_quimica(datos_entrada, rama)
        elif materia == "probabilidad":
            respuesta = probabilidad.experto_probabilidad(datos_entrada, rama)
        else:
            respuesta = "Error 404: Materia no configurada en el servidor local."

        return respuesta

    except Exception as e:
        return f"Error crítico en el Enrutador Maestro: {e}"


def procesar_grafica(funcion_str, x_min, x_max):
    """
    Puente específico para el panel de ecuaciones/gráficas.
    Devuelve una lista de pares [x, y] (o un string de error).
    """
    return graficadora.generar_puntos(funcion_str, x_min, x_max)


def analizar_lenguaje_natural(texto):
    """
    Puente para la caja de texto libre en MainActivity.
    Devuelve un JSON (string) con materia/rama/datos detectados.
    """
    return NLP.analizar_texto_universal(texto)
