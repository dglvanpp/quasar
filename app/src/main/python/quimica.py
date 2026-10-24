import sympy as sp
import re
import json
import motor_pasos

def experto_quimica(datos_entrada, rama):
    """
    Motor experto definitivo en Química III y IV.
    Maneja Gases, Soluciones, Termoquímica, Ácido-Base, Electroquímica y Teoría Orgánica/Industrial.
    """
    try:
        # ==========================================
        # 1. DECLARACIÓN UNIVERSAL DE VARIABLES
        # ==========================================
        # Gases y Soluciones
        P1, V1, T1, P2, V2, T2, P, V, n, R, T = sp.symbols('P1 V1 T1 P2 V2 T2 P V n R T')
        M, m_soluto, PM, V_solucion, N1, N2 = sp.symbols('M m_soluto PM V_solucion N1 N2') 
        
        # Termoquímica (Calor y Entalpía)
        Q, m, Ce, delta_T, delta_H, H_prod, H_react = sp.symbols('Q m Ce delta_T delta_H H_prod H_react')
        
        # Electroquímica (Leyes de Faraday)
        masa_dep, I, t, PE_eq = sp.symbols('masa_dep I t PE_eq')
        
        # Ácido-Base (pH y pOH)
        pH, pOH, H_ion, OH_ion = sp.symbols('pH pOH H_ion OH_ion')

        banco_ecuaciones = []

        # ==========================================
        # 2. EL BANCO DE ECUACIONES MATEMÁTICAS
        # ==========================================
        if rama == "leyes_gases":
            banco_ecuaciones = [
                sp.Eq(P1 * V1, P2 * V2),                             # Boyle
                sp.Eq(V1 / T1, V2 / T2),                             # Charles
                sp.Eq(P1 / T1, P2 / T2),                             # Gay-Lussac
                sp.Eq((P1 * V1) / T1, (P2 * V2) / T2),               # General
                sp.Eq(P * V, n * R * T)                              # Gas Ideal
            ]

        elif rama == "soluciones":
            banco_ecuaciones = [
                sp.Eq(M, (m_soluto / PM) / V_solucion),              # Molaridad
                sp.Eq(n, m_soluto / PM),                             # Moles
                sp.Eq(V1 * N1, V2 * N2)                              # Principio de Equivalencia (Titulación/Dilución)
            ]
            
        elif rama == "termoquimica":
            banco_ecuaciones = [
                sp.Eq(Q, m * Ce * delta_T),                          # Calor específico
                sp.Eq(delta_H, H_prod - H_react)                     # Ley de Hess (Entalpía)
            ]
            
        elif rama == "acido_base":
            banco_ecuaciones = [
                sp.Eq(pH + pOH, 14),                                 # Constante de ionización del agua (Kw)
                sp.Eq(pH, -sp.log(H_ion, 10)),                       # Potencial de Hidrógeno
                sp.Eq(pOH, -sp.log(OH_ion, 10))                      # Potencial de Hidroxilo
            ]
            
        elif rama == "electroquimica":
            banco_ecuaciones = [
                sp.Eq(masa_dep, (I * t * PE_eq) / 96500)             # 1ra Ley de Faraday (96500 Coulombs)
            ]

        # ==========================================
        # 3. EL CEREBRO LÓGICO (TEORÍA Y REGLAS)
        # ==========================================
        elif rama == "teoria_conceptos":
            busqueda = str(datos_entrada.get('concepto', '')).lower()
            base_conocimiento = {
                "markovnikov": "Regla de Markovnikov: En la adición a alquenos/alquinos asimétricos, la parte negativa se adiciona al átomo de carbono con menor número de hidrógenos, y el hidrógeno al carbono con más hidrógenos.",
                "le chatelier": "Principio de Le Chatelier: Si un sistema en equilibrio químico es perturbado (por presión, temperatura o concentración), el sistema se desplazará para contrarrestar dicha perturbación. Los catalizadores NO alteran el equilibrio, solo la velocidad para alcanzarlo.",
                "reacciones organicas": "- Alcanos: Combustión y Sustitución (Halogenación en 3 etapas: iniciación, propagación, terminación).\n- Alquenos/Alquinos: Adición al doble/triple enlace.\n- Benceno: Sustitución electrofílica (Nitración, Sulfonación, Halogenación). Resonancia le da gran estabilidad.",
                "operaciones unitarias": "Operaciones Unitarias: Transformaciones FÍSICAS (Destilación, filtración, cristalización, molienda, centrifugación).\nProcesos Unitarios: Cambios QUÍMICOS irreversibles (Alquilación, esterificación, saponificación).",
                "celdas": "Celdas Electrolíticas: Usan energía eléctrica para forzar una reacción no espontánea (ej. electrodeposición).\nCeldas Galvánicas: Generan corriente eléctrica a partir de una reacción química espontánea.",
                "acidos y bases": "- Arrhenius: Ácidos liberan H+, bases liberan OH- en agua.\n- Brönsted-Lowry: Ácidos donan protones, bases aceptan protones (pares conjugados).\n- Lewis: Ácidos aceptan par de electrones, bases donan par de electrones."
            }
            
            for clave, definicion in base_conocimiento.items():
                if clave in busqueda:
                    return json.dumps({
                        "exito": True,
                        "pasos": [{"titulo": f"Concepto: {clave.title()}", "contenido": definicion}],
                        "resultado_final": definicion
                    }, ensure_ascii=False)
            return json.dumps({
                "exito": False, "pasos": [],
                "resultado_final": "Concepto no encontrado en la base de datos de Química Orgánica/Industrial."
            }, ensure_ascii=False)

        # ==========================================
        # 4. CÁLCULO DE PESO MOLECULAR (Offline)
        # ==========================================
        elif rama == "peso_molecular":
            formula = str(datos_entrada.get('formula', '')).upper()
            pesos = {'H': 1, 'C': 12, 'N': 14, 'O': 16, 'NA': 23, 'MG': 24, 'AL': 27, 'S': 32, 'CL': 35.5, 'K': 39, 'CA': 40, 'FE': 56, 'CU': 63.5, 'ZN': 65, 'AG': 108, 'PB': 207}
            elementos = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
            peso_total = 0
            desglose = []

            for elemento, cantidad in elementos:
                elem_upper = elemento.upper()
                if elem_upper in pesos:
                    cant = int(cantidad) if cantidad else 1
                    subtotal = pesos[elem_upper] * cant
                    peso_total += subtotal
                    desglose.append(f"{elemento}: {pesos[elem_upper]} x {cant} = {subtotal} g/mol")
                else:
                    return json.dumps({
                        "exito": False, "pasos": [],
                        "resultado_final": f"Elemento '{elemento}' no encontrado en la base de datos offline."
                    }, ensure_ascii=False)

            resultado_texto = f"Peso Molecular de {formula} = {peso_total} g/mol"
            return json.dumps({
                "exito": True,
                "pasos": [
                    {"titulo": "1. Identificamos los elementos de la fórmula", "contenido": ", ".join(f"{e}{c if c else ''}" for e, c in elementos)},
                    {"titulo": "2. Calculamos el peso de cada elemento", "contenido": "\n".join(desglose)},
                    {"titulo": "3. Sumamos todos los subtotales", "contenido": resultado_texto}
                ],
                "resultado_final": resultado_texto
            }, ensure_ascii=False)

        else:
            return json.dumps({"exito": False, "pasos": [], "resultado_final": "Rama no reconocida."}, ensure_ascii=False)

        # ==========================================
        # 5. EL MOTOR DE PASOS (procedimiento detallado)
        # ==========================================
        return motor_pasos.resolver_con_pasos(banco_ecuaciones, datos_entrada, nombre_motor="Química")

    except Exception as e:
        return json.dumps({"exito": False, "pasos": [], "resultado_final": f"Error crítico en el motor químico: {e}"}, ensure_ascii=False)

# ==========================================
# ÁREA DE PRUEBAS LOCALES (LABORATORIO)
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print(" ⚗️ MOTOR EXPERTO EN QUÍMICA (III y IV) INICIADO")
    print("="*50)
    
    # PRUEBA 1: ELECTROQUÍMICA (Leyes de Faraday)
    # Depositar un metal con una corriente de 5 Amperes (I) durante 3600 segundos (t), Peso Equivalente (PE_eq) = 108
    datos_faraday = {'I': 5, 't': 3600, 'PE_eq': 108}
    print("\n--- PRUEBA 1: ELECTRÓLISIS (Ley de Faraday) ---")
    print(experto_quimica(datos_faraday, "electroquimica"))
    
    # PRUEBA 2: ÁCIDO-BASE (Cálculo cruzado de pH)
    # Si tenemos un pOH de 2.5, el motor deducirá el pH automáticamente
    datos_ph = {'pOH': 2.5}
    print("\n--- PRUEBA 2: POTENCIAL DE HIDRÓGENO (pH / pOH) ---")
    print(experto_quimica(datos_ph, "acido_base"))

    # PRUEBA 3: SOLUCIONES (Principio de Equivalencia V1*N1 = V2*N2)
    # Si tenemos 500ml de solución 2N y la rebajamos a 1N, ¿cuál será el volumen final?
    datos_titulacion = {'V1': 500, 'N1': 2, 'N2': 1}
    print("\n--- PRUEBA 3: TITULACIÓN / DILUCIÓN ---")
    print(experto_quimica(datos_titulacion, "soluciones"))

    # PRUEBA 4: CONSULTA TEÓRICA INDUSTRIAL Y ORGÁNICA
    # Preguntar por las reglas de las operaciones industriales y Markovnikov
    datos_teoria = {'concepto': 'operaciones unitarias'}
    print("\n--- PRUEBA 4: CONSULTA TEÓRICA CONCEPTUAL ---")
    print(experto_quimica(datos_teoria, "teoria_conceptos"))