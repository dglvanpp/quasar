import sympy as sp
from sympy import latex, sympify, diff, limit, integrate, solve, oo
import json

def _error_json(mensaje):
    return json.dumps({
        "exito": False,
        "pasos": [],
        "resultado_final": f"\\text{{Error de cálculo: }} {mensaje}"
    }, ensure_ascii=False)

# ==========================================
# CÁLCULO DIFERENCIAL
# ==========================================

def derivar_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)

        pasos = [
            {
                "titulo": "1. Función Original",
                "contenido": f"f(x) = {latex(expr)}"
            },
            {
                "titulo": "2. Aplicando regla de linealidad",
                "contenido": f"\\text{{Regla de la suma/resta: se deriva cada término de }} \\left[{latex(expr)}\\right] \\text{{ por separado.}}"
            }
        ]

        terminos = sp.Add.make_args(expr)
        contador = 3

        for t in terminos:
            dt = diff(t, x)
            if t.is_constant():
                pasos.append({
                    "titulo": f"{contador}. Derivada de constante",
                    "contenido": f"\\frac{{d}}{{dx}}\\left[{latex(t)}\\right] = 0 \\quad \\text{{(La derivada de un número es cero)}}"
                })
            else:
                pasos.append({
                    "titulo": f"{contador}. Derivando término",
                    "contenido": f"\\frac{{d}}{{dx}}\\left[{latex(t)}\\right] = {latex(dt)}"
                })
            contador += 1

        derivada_final = diff(expr, x)

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"f'(x) = {latex(derivada_final)}"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))

def limite_con_pasos(funcion_str, limite_val):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)

        if limite_val.lower() in ['inf', 'infinito', 'oo']:
            val = oo
        elif limite_val.lower() in ['-inf', '-infinito', '-oo']:
            val = -oo
        else:
            val = sympify(limite_val)

        resultado = limit(expr, x, val)

        pasos = [
            {
                "titulo": "1. Límite a evaluar",
                "contenido": f"\\lim_{{x \\to {latex(val)}}} \\left({latex(expr)}\\right)"
            },
            {
                "titulo": "2. Sustitución directa",
                "contenido": f"\\text{{Evaluando la expresión en }} x = {latex(val)}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"\\lim_{{x \\to {latex(val)}}} f(x) = {latex(resultado)}"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))

def max_min_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        primera_derivada = diff(expr, x)
        puntos_criticos = solve(primera_derivada, x)
        segunda_derivada = diff(primera_derivada, x)

        pasos = [
            {
                "titulo": "1. Función Original",
                "contenido": f"f(x) = {latex(expr)}"
            },
            {
                "titulo": "2. Primera derivada f'(x)",
                "contenido": f"f'(x) = {latex(primera_derivada)}"
            }
        ]

        puntos_reales = [p for p in puntos_criticos if p.is_real]
        if puntos_reales:
            str_puntos = ", ".join([latex(p) for p in puntos_reales])
            pasos.append({
                "titulo": "3. Puntos críticos (Igualar f'(x) a 0)",
                "contenido": f"x = {str_puntos}"
            })
            pasos.append({
                "titulo": "4. Segunda derivada (Criterio)",
                "contenido": f"f''(x) = {latex(segunda_derivada)}"
            })
        else:
            pasos.append({
                "titulo": "3. Puntos críticos",
                "contenido": "\\text{No existen puntos críticos en los números reales.}"
            })

        resultados_evaluacion = []
        for p in puntos_reales:
            evaluacion = segunda_derivada.subs(x, p)
            if evaluacion > 0:
                tipo = "\\text{Mínimo}"
            elif evaluacion < 0:
                tipo = "\\text{Máximo}"
            else:
                tipo = "\\text{Punto de Inflexión}"

            val_y = expr.subs(x, p)
            resultados_evaluacion.append(f"\\text{{En }} x={latex(p)} \\rightarrow {tipo} \\text{{ en }} ({latex(p)}, {latex(val_y)})")

        res_final = "\\\\".join(resultados_evaluacion) if resultados_evaluacion else "\\text{No se encontraron máximos ni mínimos.}"

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": res_final
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))

# ==========================================
# CÁLCULO INTEGRAL (22 TEMAS)
# ==========================================

def diferenciales_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        derivada = diff(expr, x)

        pasos = [
            {
                "titulo": "1. Fórmula de Diferencial",
                "contenido": "\\text{Se utiliza la relación: } dy = f'(x) dx"
            },
            {
                "titulo": "2. Derivación de la función",
                "contenido": f"f'(x) = \\frac{{d}}{{dx}}\\left[{latex(expr)}\\right] = {latex(derivada)}"
            },
            {
                "titulo": "3. Multiplicación por el diferencial",
                "contenido": "\\text{Se multiplica la derivada obtenida por el incremento } dx."
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"dy = \\left({latex(derivada)}\\right) dx"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def esquema_general_integracion_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        
        # PASO 1: Forzamos la expansión algebraica
        expr_expandida = sp.expand(expr)
        
        pasos = [
            {
                "titulo": "1. Integral Original",
                "contenido": f"\\int \\left({latex(expr)}\\right) dx"
            }
        ]

        if expr != expr_expandida:
            pasos.append({
                "titulo": "2. Expansión Algebraica",
                "contenido": f"\\int \\left({latex(expr_expandida)}\\right) dx"
            })

        # PASO 2: Separar en múltiples integrales (Linealidad)
        terminos = sp.Add.make_args(expr_expandida)
        texto_separado = ""
        for i, t in enumerate(terminos):
            signo = "+" if i > 0 and not str(t).startswith("-") else ""
            texto_separado += f"{signo} \\int \\left({latex(t)}\\right) dx "

        pasos.append({
            "titulo": "3. Propiedad de Linealidad",
            "contenido": texto_separado
        })

        # PASO 3: Extracción de constantes (Nuevo)
        texto_constantes = ""
        terminos_sin_constante = []
        
        for i, t in enumerate(terminos):
            signo = "+" if i > 0 and not str(t).startswith("-") else ""
            # Separa el número de la variable (ej. 4x^3 -> constante=4, funcion=x^3)
            constante, funcion = t.as_coeff_Mul()
            terminos_sin_constante.append(funcion)
            
            if constante == 1:
                texto_constantes += f"{signo} \\int \\left({latex(funcion)}\\right) dx "
            elif constante == -1:
                texto_constantes += f"{signo} - \\int \\left({latex(funcion)}\\right) dx "
            else:
                texto_constantes += f"{signo} {latex(constante)} \\int \\left({latex(funcion)}\\right) dx "

        pasos.append({
            "titulo": "4. Extracción de constantes",
            "contenido": texto_constantes
        })

        # PASO 4: Detección heurística de Sustitución u = ax (Nuevo)
        texto_sustituciones = []
        for funcion in terminos_sin_constante:
            # Inspeccionamos si la función tiene un argumento interno (ej. 4x dentro de exp)
            if funcion.args and len(funcion.args) == 1:
                arg = funcion.args[0]
                # Verificamos si el argumento es lineal (su segunda derivada es 0) y no es solo 'x'
                if arg.has(x) and sp.diff(arg, x, 2) == 0 and sp.diff(arg, x) != 1:
                    derivada_u = sp.diff(arg, x)
                    texto_sustituciones.append(
                        f"\\text{{Para }} \\int {latex(funcion)} dx : \\quad u = {latex(arg)} \\implies du = {latex(derivada_u)} dx \\implies dx = \\frac{{du}}{{{latex(derivada_u)}}}"
                    )
        
        if texto_sustituciones:
            pasos.append({
                "titulo": "5. Cambio de variable (Sustitución)",
                "contenido": " \\\\ ".join(texto_sustituciones)
            })

        # PASO 5: Integrar término a término
        resultados_parciales = []
        for t in terminos:
            resultados_parciales.append(integrate(t, x))
        
        texto_integrado = ""
        for i, res in enumerate(resultados_parciales):
            signo = "+" if i > 0 and not str(res).startswith("-") else ""
            texto_integrado += f"{signo} \\left({latex(res)}\\right) "

        pasos.append({
            "titulo": "6. Integración individual",
            "contenido": texto_integrado
        })

        # PASO 6: Factorización final
        integral_res = sum(resultados_parciales)
        resultado_factorizado = sp.together(integral_res)

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(resultado_factorizado)} + C"
        }, ensure_ascii=False)

    except Exception as e:
        return _error_json(str(e))


def integrales_indefinidas_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        integral_res = integrate(expr, x)

        pasos = [
            {
                "titulo": "1. Planteamiento",
                "contenido": f"\\text{{Dada la integral indefinida: }} \\int \\left({latex(expr)}\\right) dx"
            },
            {
                "titulo": "2. Antiderivada",
                "contenido": f"F(x) = {latex(integral_res)}"
            },
            {
                "titulo": "3. Constante de integración",
                "contenido": "\\text{Se suma C para representar la familia de funciones primitivas.}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def sustitucion_simple_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        
        pasos = [
            {
                "titulo": "1. Análisis de la Integral",
                "contenido": f"\\text{{Dada la integral: }} \\int \\left({latex(expr)}\\right) dx. \\text{{ Buscamos una función }} u(x) \\text{{ cuya derivada }} u'(x) \\text{{ sea un factor del integrando.}}"
            }
        ]
        
        # Intentar detectar u
        u_candidata = x
        for sub in expr.atoms(sp.Pow, sp.exp, sp.sin, sp.cos, sp.tan, sp.log, sp.sqrt):
            if sub.is_Pow:
                base = sub.args[0]
                if base != x:
                    u_candidata = base
                    break
            elif len(sub.args) > 0:
                arg = sub.args[0]
                if arg != x:
                    u_candidata = arg
                    break
        
        du_val = diff(u_candidata, x)
        
        pasos.append({
            "titulo": "2. Elección de la variable u",
            "contenido": f"\\text{{Elegimos }} u = {latex(u_candidata)} \\text{{ porque su derivada simplificará la expresión.}}"
        })
        
        pasos.append({
            "titulo": "3. Cálculo del diferencial du",
            "contenido": f"\\text{{Derivamos }} u \\text{{ respecto a }} x: \\\\ \\frac{{du}}{{dx}} = {latex(du_val)} \\implies du = \\left({latex(du_val)}\\right) dx"
        })
        
        pasos.append({
            "titulo": "4. Despeje de dx",
            "contenido": f"\\text{{Despejamos }} dx \\text{{ para realizar la sustitución: }} dx = \\frac{{du}}{{{latex(du_val)}}}"
        })
        
        # Intentar mostrar la integral en términos de u (sustitución simbólica)
        u_sym = sp.Symbol('u')
        expr_u = expr.subs(u_candidata, u_sym)
        # Simplificación manual para mostrar du
        integrando_u = sp.simplify(expr_u / du_val)
        
        pasos.append({
            "titulo": "5. Cambio de variable",
            "contenido": f"\\text{{Sustituimos }} u \\text{{ y }} dx \\text{{ en la integral original: }} \\\\ \\int {latex(integrando_u)} du"
        })
        
        integral_u = integrate(integrando_u, u_sym)
        pasos.append({
            "titulo": "6. Integración respecto a u",
            "contenido": f"\\text{{Resolvemos la integral en términos de }} u: \\\\ {latex(integral_u)} + C"
        })
        
        integral_final = integral_u.subs(u_sym, u_candidata)
        pasos.append({
            "titulo": "7. Retorno a la variable original x",
            "contenido": f"\\text{{Sustituimos }} u = {latex(u_candidata)} \\text{{ de vuelta: }} \\\\ {latex(integral_final)} + C"
        })

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_final)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def sustitucion_tcp_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        
        pasos = [
            {
                "titulo": "1. Identificación del Trinomio",
                "contenido": f"\\text{{Analizamos el denominador de la expresión: }} {latex(expr)}. \\text{{ Buscamos completar el Trinomio Cuadrado Perfecto (TCP).}}"
            }
        ]
        
        numerador, denominador = sp.fraction(expr)
        if denominador != 1:
            poly = sp.Poly(denominador, x)
            if poly.degree() == 2:
                coeffs = poly.all_coeffs()
                if len(coeffs) == 3:
                    a, b, c = coeffs
                    
                    pasos.append({
                        "titulo": "2. Proceso de completar el cuadrado",
                        "contenido": f"\\text{{Dada la forma }} {latex(a)}x^2 + {latex(b)}x + {latex(c)}, \\text{{ sumamos y restamos }} \\left(\\frac{{b}}{{2a}}\\right)^2 = \\left(\\frac{{{latex(b)}}}{{2({latex(a)})}}\\right)^2"
                    })
                    
                    h = -b / (2*a)
                    k = c - a*h**2
                    tcp_forma = a * (x - h)**2 + k
                    
                    pasos.append({
                        "titulo": "3. Reescritura del denominador",
                        "contenido": f"\\text{{El denominador se transforma en: }} {latex(a)}(x - ({latex(h)}))^2 + {latex(k)}"
                    })
                    
                    pasos.append({
                        "titulo": "4. Sustitución de variable",
                        "contenido": f"\\text{{Definimos }} u = x - ({latex(h)}) \\implies du = dx. \\text{{ La integral toma una forma estándar.}}"
                    })
                    
                    pasos.append({
                        "titulo": "5. Identificación de la forma integrable",
                        "contenido": "\\text{La expresión resultante suele ser del tipo } \\int \\frac{du}{u^2 + a^2} \\text{ (Arctan) o } \\int \\frac{du}{u^2 - a^2} \\text{ (Logaritmo).}"
                    })
        
        integral_res = integrate(expr, x)
        
        pasos.append({
            "titulo": "6. Integración y Simplificación",
            "contenido": f"\\text{{Aplicamos la fórmula correspondiente y simplificamos: }} \\\\ {latex(integral_res)} + C"
        })

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def sustitucion_u2_a2_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        
        pasos = [
            {
                "titulo": "1. Análisis de la estructura",
                "contenido": f"\\text{{Se analiza la integral: }} \\int {latex(expr)} dx. \\text{{ Buscamos patrones de suma o diferencia de cuadrados.}}"
            }
        ]
        
        _, denom = sp.fraction(expr)
        if denom != 1:
            terminos = sp.Add.make_args(denom)
            u2_term = None
            a2_term = None
            for t in terminos:
                if t.has(x): u2_term = t
                else: a2_term = t
            
            if u2_term is not None and a2_term is not None:
                u_val = sp.sqrt(u2_term)
                a_val = sp.sqrt(sp.Abs(a2_term))
                
                pasos.append({
                    "titulo": "2. Identificación de u^2 y a^2",
                    "contenido": f"\\text{{Identificamos }} u^2 = {latex(u2_term)} \\text{{ y }} a^2 = {latex(sp.Abs(a2_term))}."
                })
                
                pasos.append({
                    "titulo": "3. Obtención de u y a",
                    "contenido": f"\\text{{Calculamos las raíces: }} u = {latex(u_val)} \\implies a = {latex(a_val)}."
                })
                
                du_dx = diff(u_val, x)
                pasos.append({
                    "titulo": "4. Diferencial de u",
                    "contenido": f"\\text{{Calculamos }} du = u'(x)dx = {latex(du_dx)} dx."
                })

        pasos.append({
            "titulo": "5. Selección de la fórmula",
            "contenido": "\\text{Dependiendo del signo entre } u^2 \\text{ y } a^2 \\text{, elegimos entre: } \\\\ \\int \\frac{du}{u^2+a^2}, \\int \\frac{du}{u^2-a^2} \\text{ o } \\int \\frac{du}{a^2-u^2}."
        })

        integral_res = integrate(expr, x)
        pasos.append({
            "titulo": "6. Aplicación y Resultado",
            "contenido": f"\\text{{Aplicamos la fórmula y simplificamos: }} \\\\ {latex(integral_res)} + C"
        })

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def potencias_trig_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        
        pasos = [
            {
                "titulo": "1. Análisis de Funciones Trigonométricas",
                "contenido": f"\\text{{Evaluamos las potencias presentes en: }} \\int {latex(expr)} dx"
            }
        ]
        
        pasos.append({
            "titulo": "2. Identificación de exponentes",
            "contenido": "\\text{Observamos si los exponentes son pares o impares para determinar la estrategia.}"
        })
        
        pasos.append({
            "titulo": "3. Selección de Estrategia",
            "contenido": "\\text{Si hay un exponente impar, reservamos un factor para } du. \\text{ Si son pares, usamos identidades de ángulo medio.}"
        })
        
        pasos.append({
            "titulo": "4. Aplicación de Identidades Pitagóricas",
            "contenido": "\\text{Usamos } \\sin^2 x + \\cos^2 x = 1 \\text{ o } 1 + \\tan^2 x = \\sec^2 x \\text{ para transformar el integrando.}"
        })
        
        pasos.append({
            "titulo": "5. Cambio de variable",
            "contenido": "\\text{Realizamos una sustitución } u = \\sin x, u = \\cos x, \\text{ etc., según sea el caso.}"
        })
        
        integral_res = integrate(expr, x)
        pasos.append({
            "titulo": "6. Integración y Simplificación",
            "contenido": f"\\text{{Resolvemos la integral resultante y regresamos a la variable original: }} \\\\ {latex(integral_res)} + C"
        })

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def integrales_trigonometricas_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        integral_res = integrate(expr, x)

        pasos = [
            {
                "titulo": "1. Integral Trigonométrica",
                "contenido": f"\\int \\left({latex(expr)}\\right) dx"
            },
            {
                "titulo": "2. Aplicación de fórmula directa",
                "contenido": "\\text{Se identifica la función trigonométrica y se aplica su fórmula de integración estándar.}"
            },
            {
                "titulo": "3. Resultado",
                "contenido": f"\\text{{La antiderivada es: }} {latex(integral_res)}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def sustitucion_trig_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        
        pasos = [
            {
                "titulo": "1. Identificación del Caso",
                "contenido": f"\\text{{Analizamos la expresión radical en: }} \\int {latex(expr)} dx. \\text{{ Buscamos formas }} \\sqrt{{a^2-u^2}}, \\sqrt{{a^2+u^2}} \\text{{ o }} \\sqrt{{u^2-a^2}}."
            }
        ]
        
        pasos.append({
            "titulo": "2. Selección de la Sustitución",
            "contenido": "\\text{Dependiendo del radical, elegimos: } \\\\ "
                       "\\bullet \\sqrt{a^2-x^2} \\implies x = a \\sin \\theta \\\\ "
                       "\\bullet \\sqrt{a^2+x^2} \\implies x = a \\tan \\theta \\\\ "
                       "\\bullet \\sqrt{x^2-a^2} \\implies x = a \\sec \\theta"
        })
        
        pasos.append({
            "titulo": "3. Cálculo del diferencial dx",
            "contenido": "\\text{Derivamos } x \\text{ respecto a } \\theta \\text{ para obtener } dx. \\text{ Por ejemplo, si } x = a\\sin\\theta \\implies dx = a\\cos\\theta d\\theta."
        })
        
        pasos.append({
            "titulo": "4. Sustitución y Simplificación",
            "contenido": "\\text{Sustituimos } x \\text{ y } dx \\text{ en la integral. El radical se simplifica usando identidades pitagóricas.}"
        })
        
        pasos.append({
            "titulo": "5. Integración en términos de theta",
            "contenido": "\\text{Resolvemos la integral trigonométrica resultante.}"
        })
        
        pasos.append({
            "titulo": "6. Uso del Triángulo de Referencia",
            "contenido": "\\text{Dibujamos un triángulo rectángulo basado en la sustitución original para relacionar } \\theta \\text{ con } x."
        })
        
        integral_res = integrate(expr, x)
        pasos.append({
            "titulo": "7. Resultado Final",
            "contenido": f"\\text{{Expresamos el resultado en términos de x: }} \\\\ {latex(integral_res)} + C"
        })

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def integracion_por_partes_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        
        pasos = [
            {
                "titulo": "1. Análisis del integrando",
                "contenido": f"\\text{{Dada la integral: }} \\int {latex(expr)} dx. \\text{{ Identificamos un producto de dos funciones distintas.}}"
            }
        ]
        
        pasos.append({
            "titulo": "2. Selección de u y dv (LIATE)",
            "contenido": "\\text{Usamos la prioridad LIATE (Logarítmicas, Inversas, Algebráicas, Trigonométricas, Exponenciales) para elegir } u."
        })
        
        # Lógica para intentar identificar u y dv
        if expr.is_Mul:
            args = expr.args
            u_val = args[0]
            dv_val = sp.Mul(*args[1:])
            du_val = diff(u_val, x)
            v_val = integrate(dv_val, x)
            
            pasos.append({
                "titulo": "3. Determinación de componentes",
                "contenido": f"\\text{{Elegimos: }} \\\\ u = {latex(u_val)} \\implies du = {latex(du_val)} dx \\\\ dv = {latex(dv_val)} dx \\implies v = {latex(v_val)}"
            })
            
            pasos.append({
                "titulo": "4. Planteamiento de la fórmula",
                "contenido": f"\\text{{Aplicamos }} \\int u dv = uv - \\int v du: \\\\ ({latex(u_val)})({latex(v_val)}) - \\int ({latex(v_val)})({latex(du_val)}) dx"
            })
            
            v_du = sp.simplify(v_val * du_val)
            pasos.append({
                "titulo": "5. Simplificación de la nueva integral",
                "contenido": f"\\text{{La integral resultante a resolver es: }} \\int {latex(v_du)} dx"
            })
        else:
            pasos.append({
                "titulo": "3. Identificación de componentes",
                "contenido": "\\text{Definimos } u \\text{ y } dv \\text{ tales que } v = \\int dv \\text{ sea calculable.}"
            })
            pasos.append({
                "titulo": "4. Aplicación de la fórmula",
                "contenido": "\\text{Sustituimos en } uv - \\int v du."
            })
            pasos.append({
                "titulo": "5. Evaluación",
                "contenido": "\\text{Resolvemos la integral restante.}"
            })
        
        integral_res = integrate(expr, x)
        pasos.append({
            "titulo": "6. Resultado Final",
            "contenido": f"\\text{{Combinamos los términos y agregamos la constante de integración: }} \\\\ {latex(integral_res)} + C"
        })

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def fracciones_parciales_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        
        # Descomposición real en fracciones parciales
        descompuesta = sp.apart(expr)
        
        pasos = [
            {
                "titulo": "1. Integral Racional Original",
                "contenido": f"\\int \\left({latex(expr)}\\right) dx"
            }
        ]

        if expr == descompuesta:
             pasos.append({
                "titulo": "Nota",
                "contenido": "\\text{La expresión no se puede descomponer más en fracciones parciales simples.}"
            })
        else:
            pasos.append({
                "titulo": "2. Descomposición en Fracciones Parciales",
                "contenido": f"\\int \\left({latex(descompuesta)}\\right) dx"
            })
            
            # Separamos los términos de las fracciones parciales
            terminos = sp.Add.make_args(descompuesta)
            texto_separado = " + ".join([f"\\int \\left({latex(t)}\\right) dx" for t in terminos]).replace("+ -", "- ")
            
            pasos.append({
                "titulo": "3. Separación por linealidad",
                "contenido": texto_separado
            })

        # Resultado final
        integral_res = integrate(expr, x)
        
        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def integral_definida_con_pasos(funcion_str, limite_inf, limite_sup):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        a_val = sympify(limite_inf)
        b_val = sympify(limite_sup)

        antiderivada = integrate(expr, x)
        
        # Evaluaciones
        val_b = antiderivada.subs(x, b_val)
        val_a = antiderivada.subs(x, a_val)
        integral_res = val_b - val_a

        pasos = [
            {
                "titulo": "1. Antiderivada General",
                "contenido": f"\\text{{Primero calculamos la integral indefinida: }} \\int {latex(expr)} dx = {latex(antiderivada)}"
            },
            {
                "titulo": "2. Teorema Fundamental del Cálculo",
                "contenido": f"\\text{{Evaluamos en el intervalo [}}{latex(a_val)}, {latex(b_val)}\\text{{]: }} F({latex(b_val)}) - F({latex(a_val)})"
            },
            {
                "titulo": "3. Sustitución y Resta",
                "contenido": f"F({latex(b_val)}) = {latex(val_b)} \\\\ F({latex(a_val)}) = {latex(val_a)} \\\\ \\text{{Resultado: }} {latex(val_b)} - ({latex(val_a)})"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)}"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def area_entre_curvas_con_pasos(funcion_str, limite_inf, limite_sup):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        a_val = sympify(limite_inf)
        b_val = sympify(limite_sup)

        area_res = integrate(expr, (x, a_val, b_val))
        antiderivada = integrate(expr, x)

        pasos = [
            {
                "titulo": "1. Planteamiento del Área",
                "contenido": f"\\text{{Se define el área neta como: }} A = \\int_{{{latex(a_val)}}}^{{{latex(b_val)}}} \\left({latex(expr)}\\right) dx"
            },
            {
                "titulo": "2. Cálculo de la Primitiva",
                "contenido": f"\\text{{Obtenemos la integral indefinida de la diferencia: }} F(x) = {latex(antiderivada)}"
            },
            {
                "titulo": "3. Evaluación y Solución",
                "contenido": f"\\text{{Evaluamos en los límites }} {latex(b_val)} \\text{{ y }} {latex(a_val)} \\text{{ para encontrar la superficie.}}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"A = {latex(area_res)} \\text{{ u}}^2"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def volumen_solidos_revolucion_con_pasos(funcion_str, limite_inf, limite_sup):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        a_val = sympify(limite_inf)
        b_val = sympify(limite_sup)

        expr_cuadrado = sp.expand(expr**2)
        volumen_res = sp.pi * integrate(expr_cuadrado, (x, a_val, b_val))

        pasos = [
            {
                "titulo": "1. Método de Discos",
                "contenido": f"\\text{{El volumen de revolución alrededor del eje X es: }} V = \\pi \\int_{{{latex(a_val)}}}^{{{latex(b_val)}}} [f(x)]^2 dx"
            },
            {
                "titulo": "2. Función al Cuadrado",
                "contenido": f"\\text{{Elevamos el radio al cuadrado: }} [f(x)]^2 = {latex(expr_cuadrado)}"
            },
            {
                "titulo": "3. Integración Final",
                "contenido": f"\\text{{Se integra }} {latex(expr_cuadrado)} \\text{{ y se multiplica por }} \\pi \\text{{ en el intervalo dado.}}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"V = {latex(volumen_res)} \\text{{ u}}^3"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def volumen_seccion_transversal_con_pasos(funcion_str, limite_inf, limite_sup):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        a = sympify(limite_inf)
        b = sympify(limite_sup)

        volumen_res = integrate(expr, (x, a, b))

        pasos = [
            {
                "titulo": "1. Ecuación de Sección Transversal",
                "contenido": "\\text{Se define el volumen integrando el área conocida de la sección transversal } A(x) \\text{ a lo largo de un eje.}"
            },
            {
                "titulo": "2. Planteamiento de la integral",
                "contenido": f"V = \\int_{{{latex(a)}}}^{{{latex(b)}}} \\left({latex(expr)}\\right) dx"
            },
            {
                "titulo": "3. Cálculo total",
                "contenido": "\\text{Se efectúa la suma acumulada (integral) de las infinitas rebanadas bidimensionales.}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"V = {latex(volumen_res)} \\text{{ u}}^3"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def integrales_avanzadas_2_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        integral_res = integrate(expr, x)

        pasos = [
            {
                "titulo": "1. Identificación del caso avanzado",
                "contenido": f"\\text{{Integral de alta complejidad: }} \\int \\left({latex(expr)}\\right) dx"
            },
            {
                "titulo": "2. Análisis heurístico",
                "contenido": "\\text{El motor simbólico combina sustituciones sucesivas, métodos por partes y descomposición algebraica de manera simultánea.}"
            },
            {
                "titulo": "3. Primitiva final",
                "contenido": "\\text{Se extrae el resultado simplificado tras aplicar las múltiples transformaciones requeridas.}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def constante_integracion_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        integral_res = integrate(expr, x)

        pasos = [
            {
                "titulo": "1. Definición formal",
                "contenido": "\\text{Dada la integral indefinida } \\int f'(x)dx = F(x) + C \\text{, donde C recibe el nombre de constante de integración.}"
            },
            {
                "titulo": "2. Integración de la función",
                "contenido": f"\\text{{Se calcula la antiderivada principal: }} F(x) = {latex(integral_res)}"
            },
            {
                "titulo": "3. Adición de la constante",
                "contenido": "\\text{Se añade + C para indicar que existe una familia infinita de funciones que comparten la misma derivada.}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def areas_con_pasos(funcion_str, limite_inf, limite_sup):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        a = sympify(limite_inf)
        b = sympify(limite_sup)

        area_res = integrate(expr, (x, a, b))

        pasos = [
            {
                "titulo": "1. Fórmula de Área",
                "contenido": "\\text{El área limitada por la curva, el eje X y las rectas verticales es: } \\text{Área} = \\int_{a}^{b}f(x)dx"
            },
            {
                "titulo": "2. Sustitución de límites",
                "contenido": f"\\text{{Se evalúa la función continua en el intervalo dado: }} \\int_{{{latex(a)}}}^{{{latex(b)}}} \\left({latex(expr)}\\right) dx"
            },
            {
                "titulo": "3. Resolución",
                "contenido": "\\text{Aplicando el Teorema Fundamental del Cálculo, obtenemos la superficie neta expresada en unidades cuadradas.}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"A = {latex(area_res)} \\text{{ u}}^2"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def volumen_capas_con_pasos(funcion_str, limite_inf, limite_sup):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        a_val = sympify(limite_inf)
        b_val = sympify(limite_sup)

        integrando = sp.expand(x * expr)
        volumen_res = 2 * sp.pi * integrate(integrando, (x, a_val, b_val))

        pasos = [
            {
                "titulo": "1. Método de Capas Cilíndricas",
                "contenido": f"\\text{{El volumen rotando en el eje Y es: }} V = 2\\pi \\int_{{{latex(a_val)}}}^{{{latex(b_val)}}} x \\cdot f(x) dx"
            },
            {
                "titulo": "2. Armado del Integrando",
                "contenido": f"\\text{{Multiplicamos radio por altura: }} x \\cdot f(x) = {latex(integrando)}"
            },
            {
                "titulo": "3. Evaluación Definida",
                "contenido": f"\\text{{Se integra en el intervalo dado y se multiplica por el factor }} 2\\pi."
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"V = {latex(volumen_res)} \\text{{ u}}^3"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def longitud_arco_con_pasos(funcion_str, limite_inf, limite_sup):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        a_val = sympify(limite_inf)
        b_val = sympify(limite_sup)

        derivada = diff(expr, x)
        derivada_cuad = sp.simplify(derivada**2)
        integrando = sp.simplify(sp.sqrt(1 + derivada_cuad))
        longitud = integrate(integrando, (x, a_val, b_val))

        pasos = [
            {
                "titulo": "1. Estructura de Longitud de Arco",
                "contenido": f"L = \\int_{{{latex(a_val)}}}^{{{latex(b_val)}}} \\sqrt{{1 + [f'(x)]^2}} dx"
            },
            {
                "titulo": "2. Derivada y su Cuadrado",
                "contenido": f"f'(x) = {latex(derivada)} \\implies [f'(x)]^2 = {latex(derivada_cuad)}"
            },
            {
                "titulo": "3. Integrando Simplificado",
                "contenido": f"\\text{{La expresión a integrar es: }} \\sqrt{{1 + {latex(derivada_cuad)}}} = {latex(integrando)}"
            }
        ]

        if isinstance(longitud, sp.Integral):
            resultado = f"L \\approx {latex(longitud.evalf(5))} \\text{{ u}}"
            pasos.append({
                "titulo": "4. Nota sobre la Integración",
                "contenido": "\\text{La integral resultante es compleja y se resuelve mediante aproximación numérica.}"
            })
        else:
            resultado = f"L = {latex(longitud)} \\text{{ u}}"

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": resultado
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def diferenciales_aplicadas_con_pasos(funcion_str, valor_x, delta_x):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        val_x = sympify(valor_x)
        d_x = sympify(delta_x)

        derivada = diff(expr, x)
        dy_eval = derivada.subs(x, val_x) * d_x

        pasos = [
            {
                "titulo": "1. Aproximación por diferenciales",
                "contenido": "\\text{Se utiliza el diferencial lineal para estimar el cambio: } dy = f'(x) dx"
            },
            {
                "titulo": "2. Cálculo de la derivada",
                "contenido": f"f'(x) = {latex(derivada)}"
            },
            {
                "titulo": "3. Evaluación numérica",
                "contenido": f"\\text{{Sustituyendo }} x={latex(val_x)} \\text{{ y }} dx={latex(d_x)} \\text{{ en la derivada para obtener el incremento aproximado.}}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"dy \\approx {latex(dy_eval)}"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def metodos_combinados_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        integral_res = integrate(expr, x)

        pasos = [
            {
                "titulo": "1. Análisis de métodos múltiples",
                "contenido": "\\text{Se detecta una estructura que requiere estrategias híbridas (ej. sustitución seguida por integración por partes).}"
            },
            {
                "titulo": "2. Ejecución secuencial",
                "contenido": "\\text{Se aplican las reglas del álgebra y transformaciones trigonométricas de manera encadenada.}"
            },
            {
                "titulo": "3. Simplificación de la Primitiva",
                "contenido": "\\text{Se agrupan términos semejantes para presentar el resultado final compacto.}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))


def repaso_general_con_pasos(funcion_str):
    try:
        x = sp.Symbol('x')
        expr = sympify(funcion_str)
        integral_res = integrate(expr, x)

        pasos = [
            {
                "titulo": "1. Selector Dinámico de Integración",
                "contenido": "\\text{Evaluación global del comportamiento de la función para seleccionar la ruta analítica idónea.}"
            },
            {
                "titulo": "2. Procesamiento Simbólico",
                "contenido": f"\\text{{Procesando la integral general: }} \\int \\left({latex(expr)}\\right) dx"
            },
            {
                "titulo": "3. Solución Universal",
                "contenido": "\\text{Resultado obtenido tras la aplicación del método óptimo determinado por el motor matemático.}"
            }
        ]

        return json.dumps({
            "exito": True,
            "pasos": pasos,
            "resultado_final": f"{latex(integral_res)} + C"
        }, ensure_ascii=False)
    except Exception as e:
        return _error_json(str(e))