import sympy as sp
import motor_pasos

def experto_fisica(datos_entrada, rama):
    """
    Motor experto definitivo para Física 3 y 4.
    Contiene la base de datos de Electrostática, Electrodinámica, Electromagnetismo y Ondas.
    """
    try:
        # ==========================================
        # 1. DECLARACIÓN UNIVERSAL DE VARIABLES
        # ==========================================
        # Constantes y Electrostática
        F, K, q, q1, q2, r, epsilon, epsilon_0, epsilon_r = sp.symbols('F K q q1 q2 r epsilon epsilon_0 epsilon_r')
        E, A, Q_carga, sigma, lamda, L = sp.symbols('E A Q_carga sigma lamda L')
        V, V_A, V_B, d, W, Ep = sp.symbols('V V_A V_B d W Ep')
        
        # Capacitancia
        C, C1, C2, C_t, K_diel = sp.symbols('C C1 C2 C_t K_diel')
        
        # Electrodinámica y Circuitos
        I, t, rho, R, R_0, alpha, delta_T, R1, R2, R_t, P, Q_cal = sp.symbols('I t rho R R_0 alpha delta_T R1 R2 R_t P Q_cal')
        I_g, R_g, R_s, R_m, V_g = sp.symbols('I_g R_g R_s R_m V_g') # Galvanómetros
        
        # Electromagnetismo
        B, phi, theta, H, mu, mu_r, mu_0 = sp.symbols('B phi theta H mu mu_r mu_0')
        N, r_m, v, m = sp.symbols('N r_m v m') # r_m = radio medio, v = velocidad, m = masa
        
        # Inducción y Transformadores
        E_fem, delta_phi, delta_t, phi_f, phi_i, E_max, omega = sp.symbols('E_fem delta_phi delta_t phi_f phi_i E_max omega')
        f, V_ef, V_max, N_p, N_s, V_p, V_s, I_p, I_s = sp.symbols('f V_ef V_max N_p N_s V_p V_s I_p I_s')
        
        # Ondas
        v_onda, lamda_onda, T_periodo = sp.symbols('v_onda lamda_onda T_periodo')

        banco_ecuaciones = []

        # ==========================================
        # 2. EL BANCO DE ECUACIONES (LA BÓVEDA)
        # ==========================================
        
        if rama == "electrostatica":
            banco_ecuaciones = [
                # Ley de Coulomb y Campo Eléctrico
                sp.Eq(F, K * (q1 * q2) / r**2),
                sp.Eq(epsilon, epsilon_0 * epsilon_r),
                sp.Eq(K, 1 / (4 * sp.pi * epsilon_0)),
                sp.Eq(E, F / q),
                sp.Eq(E, K * q / r**2),
                sp.Eq(E, Q_carga / (epsilon_0 * A)), # Ley de Gauss
                
                # Densidad de carga
                sp.Eq(sigma, q / A),
                sp.Eq(lamda, q / L),
                
                # Potencial y Energía
                sp.Eq(V, Ep / Q_carga),
                sp.Eq(V, K * q / r),
                sp.Eq(V, E * d),
                sp.Eq(V, V_B - V_A),
                sp.Eq(W, F * d),
                sp.Eq(Ep, K * q * Q_carga / r),
                
                # Capacitancia
                sp.Eq(C, Q_carga / V),
                sp.Eq(C, epsilon_0 * A / d),          # Placas en el vacío
                sp.Eq(C, K_diel * epsilon_0 * A / d), # Placas con dieléctrico
                sp.Eq(C, epsilon * A / d),
                sp.Eq(C, r / K),                      # Capacitor esférico
                
                # Energía en capacitor
                sp.Eq(Ep, Q_carga * V / 2),
                sp.Eq(Ep, C * V**2 / 2),
                sp.Eq(Ep, Q_carga**2 / (2 * C))
            ]

        elif rama == "electrodinamica":
            banco_ecuaciones = [
                # Corriente y Ley de Ohm
                sp.Eq(I, q / t),
                sp.Eq(R, rho * L / A),
                sp.Eq(R_t, R_0 * (1 + alpha * delta_T)),
                sp.Eq(I, V / R),
                
                # Potencia y Efecto Joule
                sp.Eq(P, V * I),
                sp.Eq(P, I**2 * R),
                sp.Eq(P, V**2 / R),
                sp.Eq(Q_cal, 0.24 * I**2 * R * t),
                sp.Eq(Q_cal, 0.24 * P * t)
            ]

        elif rama == "electromagnetismo":
            banco_ecuaciones = [
                # Flujo y Campo
                sp.Eq(B, phi / A),
                sp.Eq(B, phi / (A * sp.sin(theta))),
                sp.Eq(H, B / mu),
                sp.Eq(mu, mu_r * mu_0),
                
                # Conductores, espiras y solenoides
                sp.Eq(B, mu_0 * I / (2 * sp.pi * r)),  # Conductor recto
                sp.Eq(B, mu_0 * I / (2 * r)),          # Espira
                sp.Eq(B, mu_0 * N * I / (2 * r)),      # Varias espiras
                sp.Eq(B, mu * N * I / L),              # Solenoide
                sp.Eq(B, mu * N * I / (2 * sp.pi * r_m)), # Toroide
                
                # Fuerzas Magnéticas (Lorentz y Ampere)
                sp.Eq(F, B * q * v),
                sp.Eq(F, B * q * v * sp.sin(theta)),
                sp.Eq(r, m * v / (q * B)),             # Ciclotrón
                sp.Eq(F, B * I * L * sp.sin(theta)),   # Conductor
                
                # Galvanómetros
                sp.Eq(R_s, (I_g / (I - I_g)) * R_g),   # Amperímetro (Shunt)
                sp.Eq(R_m, (V_g / I_g) - R_g)          # Voltímetro
            ]

        elif rama == "induccion_ondas":
            banco_ecuaciones = [
                # Faraday y Lenz
                sp.Eq(E_fem, -N * delta_phi / delta_t),
                sp.Eq(E_fem, -N * (phi_f - phi_i) / t),
                sp.Eq(E_fem, B * L * v * sp.sin(theta)),
                
                # Generadores
                sp.Eq(E_max, N * B * A * omega),
                sp.Eq(V_ef, 0.707 * V_max),
                
                # Transformadores
                sp.Eq(N_s / N_p, V_s / V_p),
                sp.Eq(V_s / V_p, I_p / I_s),
                
                # Ondas (Acústica y Óptica)
                sp.Eq(v_onda, lamda_onda / T_periodo),
                sp.Eq(v_onda, lamda_onda * f)
            ]
        else:
            import json
            return json.dumps({"exito": False, "pasos": [], "resultado_final": "Rama no reconocida. Usa: 'electrostatica', 'electrodinamica', 'electromagnetismo' o 'induccion_ondas'."}, ensure_ascii=False)

        # ==========================================
        # 3. EL MOTOR DE PASOS (procedimiento detallado)
        # ==========================================
        return motor_pasos.resolver_con_pasos(banco_ecuaciones, datos_entrada, nombre_motor="Física")

    except Exception as e:
        import json
        return json.dumps({"exito": False, "pasos": [], "resultado_final": f"Error crítico en el cálculo físico: {e}"}, ensure_ascii=False)

# ==========================================
# ÁREA DE PRUEBAS LOCALES (LABORATORIO)
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print(" ⚛️  MOTOR EXPERTO EN FÍSICA INICIADO")
    print("="*50)
    
    # PRUEBA 1: ELECTROSTÁTICA (Ley de Coulomb)
    # Buscamos la Fuerza (F) conociendo la Constante K, y las cargas q1, q2 separadas por un radio r
    datos_coulomb = {'K': 9e9, 'q1': 1.6e-19, 'q2': 1.6e-19, 'r': 0.05}
    print("\n--- PRUEBA 1: ELECTROSTÁTICA ---")
    print(f"Datos ingresados: {datos_coulomb}")
    print(experto_fisica(datos_coulomb, "electrostatica"))
    
    # PRUEBA 2: ELECTRODINÁMICA (Ley de Ohm y Potencia)
    # Si en un vehículo tenemos una batería de 12V y una resistencia de 4 Ohms
    # ¡El motor debería deducir tanto la Corriente (I) como la Potencia (P) al mismo tiempo!
    datos_circuito = {'V': 12, 'R': 4}
    print("\n--- PRUEBA 2: ELECTRODINÁMICA ---")
    print(f"Datos ingresados: {datos_circuito}")
    print(experto_fisica(datos_circuito, "electrodinamica"))

    # PRUEBA 3: ONDAS Y TRANSFORMADORES
    # Un transformador tiene 100 espiras en el primario, 500 en el secundario y recibe 120V
    datos_transformador = {'N_p': 100, 'N_s': 500, 'V_p': 120}
    print("\n--- PRUEBA 3: TRANSFORMADORES ---")
    print(f"Datos ingresados: {datos_transformador}")
    print(experto_fisica(datos_transformador, "induccion_ondas"))