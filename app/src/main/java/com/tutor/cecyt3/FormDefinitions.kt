package com.tutor.cecyt3

enum class TipoCampo { NUMERO, TEXTO, LISTA_NUMEROS, SELECTOR }

data class CampoFormulario(
    val clave: String,
    val etiqueta: String,
    val tipo: TipoCampo = TipoCampo.NUMERO,
    val opciones: List<String>? = null,           // solo para SELECTOR
    val mostrarSoloSi: Pair<String, List<String>>? = null // (clave del selector, valores que lo activan)
)

object Materias {

    val nombresBonitos = mapOf(
        "matematicas" to "📐 Matemáticas",
        "fisica" to "⚛️ Física III y IV",
        "quimica" to "⚗️ Química III y IV",
        "probabilidad" to "📊 Probabilidad y Estadística"
    )

    val ramasPorMateria = mapOf(
        "matematicas" to listOf("geometria_analitica", "calculo_diferencial", "calculo_integral", "integrales_trigonometricas"),
        "fisica" to listOf("electrostatica", "electrodinamica", "electromagnetismo", "induccion_ondas"),
        "quimica" to listOf("leyes_gases", "soluciones", "termoquimica", "acido_base", "electroquimica", "teoria_conceptos", "peso_molecular"),
        "probabilidad" to listOf("estadistica_descriptiva", "combinatoria", "probabilidad_binomial", "teorema_bayes")
    )

    val nombresRamas = mapOf(
        "geometria_analitica" to "Geometría Analítica",
        "calculo_diferencial" to "Cálculo Diferencial",
        "calculo_integral" to "Cálculo Integral",
        "integrales_trigonometricas" to "Integrales Trigonométricas",
        "electrostatica" to "Electrostática",
        "electrodinamica" to "Electrodinámica (Circuitos)",
        "electromagnetismo" to "Electromagnetismo",
        "induccion_ondas" to "Inducción y Ondas",
        "leyes_gases" to "Leyes de los Gases",
        "soluciones" to "Soluciones",
        "termoquimica" to "Termoquímica",
        "acido_base" to "Ácido-Base",
        "electroquimica" to "Electroquímica",
        "teoria_conceptos" to "Teoría / Conceptos",
        "peso_molecular" to "Peso Molecular",
        "estadistica_descriptiva" to "Estadística Descriptiva",
        "combinatoria" to "Combinatoria",
        "probabilidad_binomial" to "Distribución Binomial",
        "teorema_bayes" to "Teorema de Bayes"
    )
}

object FormDefinitions {

    // Para las ramas "algebraicas" el usuario solo llena lo que SABE;
    // los campos vacíos se ignoran y el motor de SymPy deduce el resto.
    private fun camposNumericos(vararg claves: String): List<CampoFormulario> =
        claves.map { CampoFormulario(it, it.replace("_", " ")) }

    val definiciones: Map<String, List<CampoFormulario>> = mapOf(

        "geometria_analitica" to camposNumericos(
            "x1", "y1", "x2", "y2", "m", "b", "a", "c", "p", "r", "h", "k"
        ),

        "calculo_diferencial" to listOf(
            CampoFormulario("funcion", "f(x) =", TipoCampo.TEXTO),
            CampoFormulario(
                "operacion", "¿Qué quieres hacer?", TipoCampo.SELECTOR,
                opciones = listOf("derivar", "limite", "max_min")
            ),
            CampoFormulario(
                "limite_val", "x tiende a...", TipoCampo.NUMERO,
                mostrarSoloSi = "operacion" to listOf("limite")
            )
        ),

        // === AQUI EMPIEZA LA MAGIA DE LOS 22 TEMAS ===
        "calculo_integral" to listOf(
            CampoFormulario("funcion", "f(x) =", TipoCampo.TEXTO),
            CampoFormulario(
                "operacion", "¿Qué quieres hacer?", TipoCampo.SELECTOR,
                opciones = listOf(
                    "diferenciales", "esquema_general", "integrales_indefinidas",
                    "integrales_trigonometricas", "sustitucion_simple", "sustitucion_tcp", 
                    "sustitucion_u2_a2", "potencias_trig", "sustitucion_trig", 
                    "integracion_por_partes", "fracciones_parciales", "integral_definida", 
                    "area_entre_curvas", "volumen_solidos_revolucion", "volumen_seccion_transversal",
                    "integrales_avanzadas_2", "constante_integracion", "areas",
                    "volumen_capas", "longitud_arco", "diferenciales_aplicadas",
                    "metodos_combinados", "repaso_general"
                )
            ),
            CampoFormulario(
                "limite_inf", "límite inferior (a)", TipoCampo.NUMERO,
                mostrarSoloSi = "operacion" to listOf(
                    "integral_definida", "area_entre_curvas", "volumen_solidos_revolucion",
                    "volumen_seccion_transversal", "areas", "volumen_capas", "longitud_arco"
                )
            ),
            CampoFormulario(
                "limite_sup", "límite superior (b)", TipoCampo.NUMERO,
                mostrarSoloSi = "operacion" to listOf(
                    "integral_definida", "area_entre_curvas", "volumen_solidos_revolucion",
                    "volumen_seccion_transversal", "areas", "volumen_capas", "longitud_arco"
                )
            ),
            CampoFormulario(
                "valor_x", "Valor inicial (x)", TipoCampo.NUMERO,
                mostrarSoloSi = "operacion" to listOf("diferenciales_aplicadas")
            ),
            CampoFormulario(
                "delta_x", "Incremento (dx)", TipoCampo.NUMERO,
                mostrarSoloSi = "operacion" to listOf("diferenciales_aplicadas")
            )
        ),
        // === FIN DE LOS 22 TEMAS ===

        "integrales_trigonometricas" to listOf(
            CampoFormulario("funcion", "f(x) =", TipoCampo.TEXTO)
        ),

        "electrostatica" to camposNumericos(
            "F", "K", "q1", "q2", "r", "E", "A", "Q_carga", "V", "d", "W", "Ep", "C", "K_diel"
        ),

        "electrodinamica" to camposNumericos(
            "V", "I", "R", "P", "Q_cal", "t", "rho", "L", "A", "R_0", "alpha", "delta_T"
        ),

        "electromagnetismo" to camposNumericos(
            "B", "phi", "theta", "I", "r", "N", "F", "q", "v", "m", "L", "I_g", "R_g", "R_s", "R_m", "V_g"
        ),

        "induccion_ondas" to camposNumericos(
            "E_fem", "N", "delta_phi", "delta_t", "B", "L", "v", "E_max", "A", "omega",
            "V_max", "N_p", "N_s", "V_p", "V_s", "I_p", "I_s", "v_onda", "lamda_onda", "T_periodo", "f"
        ),

        "leyes_gases" to camposNumericos("P1", "V1", "T1", "P2", "V2", "T2", "P", "V", "n", "R", "T"),

        "soluciones" to camposNumericos("M", "m_soluto", "PM", "V_solucion", "V1", "N1", "V2", "N2", "n"),

        "termoquimica" to camposNumericos("Q", "m", "Ce", "delta_T", "delta_H", "H_prod", "H_react"),

        "acido_base" to camposNumericos("pH", "pOH", "H_ion", "OH_ion"),

        "electroquimica" to camposNumericos("masa_dep", "I", "t", "PE_eq"),

        "teoria_conceptos" to listOf(
            CampoFormulario("concepto", "Concepto a buscar (ej. Markovnikov, Le Chatelier...)", TipoCampo.TEXTO)
        ),

        "peso_molecular" to listOf(
            CampoFormulario("formula", "Fórmula química (ej. H2O, C6H12O6)", TipoCampo.TEXTO)
        ),

        "estadistica_descriptiva" to listOf(
            CampoFormulario("datos", "Lista de datos, separados por coma", TipoCampo.LISTA_NUMEROS)
        ),

        "combinatoria" to camposNumericos("n", "r"),

        "probabilidad_binomial" to camposNumericos("n", "x", "p"),

        "teorema_bayes" to camposNumericos("p_A", "p_B_dado_A", "p_B_dado_no_A")
    )
}