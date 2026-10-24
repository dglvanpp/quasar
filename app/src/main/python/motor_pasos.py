import sympy as sp
from sympy import latex
import json

def _texto_ecuacion(eq):
    """Convierte una ecuación de SymPy a formato LaTeX."""
    return f"{latex(eq.lhs)} = {latex(eq.rhs)}"

def _formatear_valor(valor):
    """Redondea resultados numéricos a 4 decimales y los pasa a LaTeX."""
    try:
        val_flotante = float(valor.evalf())
        # Evitamos decimales si es un número entero exacto
        if val_flotante.is_integer():
            return latex(int(val_flotante))
        return latex(round(val_flotante, 4))
    except Exception:
        return latex(valor)

def resolver_con_pasos(banco_ecuaciones, datos_entrada, nombre_motor="Motor"):
    """
    Toma un banco de ecuaciones y devuelve el JSON con los pasos.
    Todo el texto se formatea estrictamente para que KaTeX lo dibuje impecable.
    """
    pasos = []
    try:
        # 1. Convertimos los datos del usuario a símbolos de SymPy
        datos_conocidos = {}
        for variable_str, valor in datos_entrada.items():
            simbolo = sp.symbols(variable_str)
            datos_conocidos[simbolo] = sp.sympify(valor)

        if not datos_conocidos:
            return json.dumps({
                "exito": False,
                "pasos": [],
                "resultado_final": "\\text{No se recibió ningún dato para trabajar.}"
            }, ensure_ascii=False)

        # 2. Filtramos solo las fórmulas útiles
        ecuaciones_utiles = [
            eq for eq in banco_ecuaciones
            if any(sim in eq.free_symbols for sim in datos_conocidos.keys())
        ]

        if not ecuaciones_utiles:
            return json.dumps({
                "exito": False,
                "pasos": [],
                "resultado_final": "\\text{No encontré fórmulas para estos datos.}"
            }, ensure_ascii=False)

        # PASO 1: Fórmulas identificadas (Usamos 'aligned' para que queden una debajo de otra)
        lista_formulas = " \\\\ ".join(f"{_texto_ecuacion(eq)}" for eq in ecuaciones_utiles)
        pasos.append({
            "titulo": "1. Fórmulas identificadas",
            "contenido": f"\\begin{{aligned}} {lista_formulas} \\end{{aligned}}"
        })

        # PASO 2: Sustitución de datos
        datos_texto = ", \\; ".join(f"{latex(sp.symbols(k))} = {latex(sp.sympify(v))}" for k, v in datos_entrada.items())

        detalle_sustitucion = []
        ecuaciones_sustituidas = []
        for eq in ecuaciones_utiles:
            eq_sub = eq.subs(datos_conocidos)
            ecuaciones_sustituidas.append(eq_sub)
            # Usamos la flecha derecha (\rightarrow) para mostrar la conversión
            detalle_sustitucion.append(f"{_texto_ecuacion(eq)} \\quad \\rightarrow \\quad {_texto_ecuacion(eq_sub)}")

        texto_sustitucion = " \\\\ ".join(detalle_sustitucion)

        pasos.append({
            "titulo": "2. Sustituyendo los datos conocidos",
            "contenido": f"\\text{{Datos: }} {datos_texto} \\\\ \\vspace{{0.3cm}} \\\\ \\begin{{aligned}} {texto_sustitucion} \\end{{aligned}}"
        })

        # PASO 3: Resolver el sistema
        soluciones = sp.solve(ecuaciones_sustituidas, dict=True)

        if not soluciones:
            pasos.append({
                "titulo": "3. Resultado",
                "contenido": "\\text{Faltan datos para resolver o son incompatibles.}"
            })
            return json.dumps({"exito": False, "pasos": pasos, "resultado_final": "\\text{Sin solución}"}, ensure_ascii=False)

        # Formateamos el resultado final
        resultado_texto_partes = []
        for sol in soluciones:
            for variable, valor in sol.items():
                resultado_texto_partes.append(f"{latex(variable)} = {_formatear_valor(valor)}")

        resultado_texto = " \\\\ ".join(resultado_texto_partes)

        pasos.append({
            "titulo": "3. Resolviendo",
            "contenido": f"\\begin{{aligned}} {resultado_texto} \\end{{aligned}}"
        })

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"\\begin{{aligned}} {resultado_texto} \\end{{aligned}}"
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "exito": False,
            "pasos": pasos,
            "resultado_final": f"\\text{{Error crítico en }} {nombre_motor} \\text{{: {str(e)}}}"
        }, ensure_ascii=False)