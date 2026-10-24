import sympy as sp
import json
import motor_pasos
import pasos_calculo

def experto_matematicas(datos_entrada, rama):
    """
    Motor experto definitivo para Matemáticas (Geometría Analítica y Cálculo).
    Resuelve ecuaciones de cónicas, deriva, integra y calcula volúmenes/áreas.
    """
    try:
        # ==========================================
        # 1. DECLARACIÓN UNIVERSAL DE SÍMBOLOS
        # ==========================================
        x, y, x1, y1, x2, y2, x3, y3 = sp.symbols('x y x1 y1 x2 y2 x3 y3')
        A, B, C_cte, D, E, F = sp.symbols('A B C_cte D E F')
        m, b, a, c, p, r, h, k, theta = sp.symbols('m b a c p r h k theta')

        # Variables para Cálculo
        limite_val = sp.symbols('limite_val')
        limite_inf, limite_sup = sp.symbols('limite_inf limite_sup')

        # ==========================================
        # 2. MOTOR DE GEOMETRÍA ANALÍTICA
        # ==========================================
        if rama == "geometria_analitica":
            banco_ecuaciones = [
                # Distancia y Punto Medio
                sp.Eq(D, sp.sqrt((x2 - x1)**2 + (y2 - y1)**2)),

                # Línea Recta
                sp.Eq(m, (y2 - y1) / (x2 - x1)),                # Pendiente
                sp.Eq(A*x + B*y + C_cte, 0),                    # General
                sp.Eq(y - y1, m*(x - x1)),                      # Punto-pendiente
                sp.Eq(y, m*x + b),                              # Ordinaria
                sp.Eq(x/a + y/b, 1),                            # Simétrica

                # Circunferencia
                sp.Eq((x - h)**2 + (y - k)**2, r**2),           # Ordinaria
                sp.Eq(x**2 + y**2, r**2),                       # Canónica

                # Parábola (Vértice en h,k)
                sp.Eq((y - k)**2, 4*p*(x - h)),                 # Horizontal
                sp.Eq((x - h)**2, 4*p*(y - k)),                 # Vertical

                # Elipse (Vértice en h,k)
                sp.Eq((x - h)**2 / a**2 + (y - k)**2 / b**2, 1),# Horizontal
                sp.Eq((x - h)**2 / b**2 + (y - k)**2 / a**2, 1),# Vertical
                sp.Eq(c**2, a**2 - b**2),                       # Relación pitagórica elipse

                # Hipérbola (Vértice en h,k)
                sp.Eq((x - h)**2 / a**2 - (y - k)**2 / b**2, 1),# Horizontal
                sp.Eq((y - k)**2 / a**2 - (x - h)**2 / b**2, 1),# Vertical
                sp.Eq(c**2, a**2 + b**2)                        # Relación pitagórica hipérbola
            ]

            return motor_pasos.resolver_con_pasos(banco_ecuaciones, datos_entrada, nombre_motor="Geometría Analítica")

        # ==========================================
        # 3. MOTOR DE CÁLCULO DIFERENCIAL
        # ==========================================
        elif rama == "calculo_diferencial":
            operacion = datos_entrada.get('operacion')
            funcion_str = datos_entrada.get('funcion')

            if operacion == 'derivar':
                return pasos_calculo.derivar_con_pasos(funcion_str)
            elif operacion == 'limite':
                return pasos_calculo.limite_con_pasos(funcion_str, datos_entrada.get('limite_val'))
            elif operacion == 'max_min':
                return pasos_calculo.max_min_con_pasos(funcion_str)
            else:
                return json.dumps({"exito": False, "pasos": [], "resultado_final": "Operación no reconocida. Usa: derivar, limite o max_min."}, ensure_ascii=False)

        # ==========================================
        # 4. MOTOR DE CÁLCULO INTEGRAL
        # ==========================================
        elif rama == "calculo_integral":
            operacion = datos_entrada.get('operacion')
            funcion_str = datos_entrada.get('funcion')

            # Variables extraíbles si el usuario llena más campos (para áreas, volúmenes, diferenciales)
            lim_inf = datos_entrada.get('limite_inf')
            lim_sup = datos_entrada.get('limite_sup')
            valor_x = datos_entrada.get('valor_x', '1') # Para el tema de diferenciales aplicadas
            delta_x = datos_entrada.get('delta_x', '0.1')

            # --- ENRUTADOR DE LOS 22 TEMAS ---
            if operacion == 'diferenciales': return pasos_calculo.diferenciales_con_pasos(funcion_str)
            elif operacion == 'esquema_general': return pasos_calculo.esquema_general_integracion_con_pasos(funcion_str)
            elif operacion == 'integrales_indefinidas': return pasos_calculo.integrales_indefinidas_con_pasos(funcion_str)
            elif operacion == 'integrales_trigonometricas': return pasos_calculo.integrales_trigonometricas_con_pasos(funcion_str)
            elif operacion == 'sustitucion_simple': return pasos_calculo.sustitucion_simple_con_pasos(funcion_str)
            elif operacion == 'sustitucion_tcp': return pasos_calculo.sustitucion_tcp_con_pasos(funcion_str)
            elif operacion == 'sustitucion_u2_a2': return pasos_calculo.sustitucion_u2_a2_con_pasos(funcion_str)
            elif operacion == 'potencias_trig': return pasos_calculo.potencias_trig_con_pasos(funcion_str)
            elif operacion == 'sustitucion_trig': return pasos_calculo.sustitucion_trig_con_pasos(funcion_str)
            elif operacion == 'integracion_por_partes': return pasos_calculo.integracion_por_partes_con_pasos(funcion_str)
            elif operacion == 'fracciones_parciales': return pasos_calculo.fracciones_parciales_con_pasos(funcion_str)
            elif operacion == 'integral_definida': return pasos_calculo.integral_definida_con_pasos(funcion_str, lim_inf, lim_sup)
            elif operacion == 'area_entre_curvas': return pasos_calculo.area_entre_curvas_con_pasos(funcion_str, lim_inf, lim_sup)
            elif operacion == 'volumen_solidos_revolucion': return pasos_calculo.volumen_solidos_revolucion_con_pasos(funcion_str, lim_inf, lim_sup)
            elif operacion == 'volumen_seccion_transversal': return pasos_calculo.volumen_seccion_transversal_con_pasos(funcion_str, lim_inf, lim_sup)
            elif operacion == 'integrales_avanzadas_2': return pasos_calculo.integrales_avanzadas_2_con_pasos(funcion_str)
            elif operacion == 'constante_integracion': return pasos_calculo.constante_integracion_con_pasos(funcion_str)
            elif operacion == 'areas': return pasos_calculo.areas_con_pasos(funcion_str, lim_inf, lim_sup)
            elif operacion == 'volumen_capas': return pasos_calculo.volumen_capas_con_pasos(funcion_str, lim_inf, lim_sup)
            elif operacion == 'longitud_arco': return pasos_calculo.longitud_arco_con_pasos(funcion_str, lim_inf, lim_sup)
            elif operacion == 'diferenciales_aplicadas': return pasos_calculo.diferenciales_aplicadas_con_pasos(funcion_str, valor_x, delta_x)
            elif operacion == 'metodos_combinados': return pasos_calculo.metodos_combinados_con_pasos(funcion_str)
            elif operacion == 'repaso_general': return pasos_calculo.repaso_general_con_pasos(funcion_str)
            else:
                return json.dumps({"exito": False, "pasos": [], "resultado_final": "Operación no reconocida en Integral."}, ensure_ascii=False)

        elif rama == "integrales_trigonometricas":
            return pasos_calculo.integrales_trigonometricas_con_pasos(datos_entrada.get('funcion'))

    # ==========================================
    # CIERRE DE SEGURIDAD (EL 'EXCEPT' FALTANTE)
    # ==========================================
    except Exception as e:
        return json.dumps({
            "exito": False,
            "pasos": [],
            "resultado_final": f"\\text{{Error del motor Python: }} {str(e)}"
        }, ensure_ascii=False)


# ==========================================
# ÁREA DE PRUEBAS LOCALES (LABORATORIO)
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print(" 📐 MOTOR EXPERTO EN MATEMÁTICAS INICIADO")
    print("="*50)

    # PRUEBA 1: GEOMETRÍA ANALÍTICA (Encontrar el radio de una circunferencia desde su ecuación ordinaria)
    datos_geo = {'h': 0, 'k': 0, 'r': 5}
    print("\n--- PRUEBA 1: CIRCUNFERENCIA ---")
    print(experto_matematicas(datos_geo, "geometria_analitica"))

    # PRUEBA 2: CÁLCULO DIFERENCIAL (Límites Indeterminados)
    datos_limite = {'funcion': '(x**2 - 4)/(x - 2)', 'operacion': 'limite', 'limite_val': '2'}
    print("\n--- PRUEBA 2: LÍMITE INDETERMINADO (Factorización interna) ---")
    print(experto_matematicas(datos_limite, "calculo_diferencial"))

    # PRUEBA 3: CÁLCULO DIFERENCIAL (Máximos y Mínimos)
    datos_maxmin = {'funcion': 'x**3 - 3*x**2 + 2', 'operacion': 'max_min'}
    print("\n--- PRUEBA 3: MÁXIMOS Y MÍNIMOS ---")
    print(experto_matematicas(datos_maxmin, "calculo_diferencial"))

    # PRUEBA 4: CÁLCULO INTEGRAL (Volumen de Sólidos de Revolución - Discos)
    datos_vol = {'funcion': 'sqrt(x)', 'operacion': 'volumen_discos', 'limite_inf': '0', 'limite_sup': '4'}
    print("\n--- PRUEBA 4: VOLUMEN DE SÓLIDO (Discos) ---")
    print(experto_matematicas(datos_vol, "calculo_integral"))