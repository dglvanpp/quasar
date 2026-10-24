import math
import statistics
import json


def _resultado(exito, pasos, resultado_final):
    return json.dumps({"exito": exito, "pasos": pasos, "resultado_final": resultado_final}, ensure_ascii=False)


def _error(mensaje):
    return _resultado(False, [], mensaje)


def experto_probabilidad(datos_entrada, rama):
    """
    Motor experto para Probabilidad y Estadística.
    Cada rama regresa el procedimiento paso a paso, no solo el resultado.
    """
    try:
        # ==========================================
        # 1. ESTADÍSTICA DESCRIPTIVA
        # ==========================================
        if rama == "estadistica_descriptiva":
            datos = datos_entrada.get('datos', [])
            if not datos or len(datos) < 2:
                return _error("Se necesita una lista con al menos 2 datos numéricos para el análisis.")

            n = len(datos)
            media = statistics.mean(datos)
            mediana = statistics.median(datos)
            try:
                moda = statistics.mode(datos)
            except statistics.StatisticsError:
                moda = "No hay moda única (Amodal o Multimodal)"
            varianza = statistics.variance(datos)
            desviacion = statistics.stdev(datos)
            rango = max(datos) - min(datos)

            datos_ordenados = sorted(datos)

            pasos = [
                {"titulo": "1. Datos ordenados", "contenido": f"n = {n} datos\n{datos_ordenados}"},
                {"titulo": "2. Media (promedio)", "contenido":
                    f"Media = (suma de todos los datos) / n\nMedia = {sum(datos):.4f} / {n} = {media:.4f}"},
                {"titulo": "3. Mediana", "contenido":
                    f"Con los datos ordenados, el valor central es: {mediana}"},
                {"titulo": "4. Moda", "contenido": f"El valor que más se repite es: {moda}"},
                {"titulo": "5. Rango", "contenido":
                    f"Rango = máximo - mínimo = {max(datos)} - {min(datos)} = {rango}"},
                {"titulo": "6. Varianza muestral", "contenido":
                    f"Varianza = Σ(xi - media)² / (n - 1) = {varianza:.4f}"},
                {"titulo": "7. Desviación estándar", "contenido":
                    f"Desviación = √Varianza = √{varianza:.4f} = {desviacion:.4f}"},
            ]
            resultado_final = (f"Media={media:.4f} | Mediana={mediana} | Moda={moda} | "
                                f"Varianza={varianza:.4f} | Desv. Estándar={desviacion:.4f}")
            return _resultado(True, pasos, resultado_final)

        # ==========================================
        # 2. COMBINATORIA
        # ==========================================
        elif rama == "combinatoria":
            n = int(datos_entrada.get('n', 0))
            r = int(datos_entrada.get('r', 0))

            if n < r or n < 0 or r < 0:
                return _error("'n' (población) debe ser mayor o igual a 'r' (muestra), y ambos positivos.")

            factorial_n = math.factorial(n)
            permutaciones = math.perm(n, r)
            combinaciones = math.comb(n, r)

            pasos = [
                {"titulo": "1. Datos", "contenido": f"n = {n} (población total), r = {r} (elementos a elegir)"},
                {"titulo": "2. Factorial de n", "contenido": f"n! = {n}! = {factorial_n}"},
                {"titulo": "3. Permutaciones (el orden SÍ importa)", "contenido":
                    f"nPr = n! / (n-r)! = {n}! / {n - r}! = {permutaciones}"},
                {"titulo": "4. Combinaciones (el orden NO importa)", "contenido":
                    f"nCr = n! / (r!·(n-r)!) = {n}! / ({r}!·{n - r}!) = {combinaciones}"},
            ]
            resultado_final = f"Permutaciones (nPr) = {permutaciones} | Combinaciones (nCr) = {combinaciones}"
            return _resultado(True, pasos, resultado_final)

        # ==========================================
        # 3. DISTRIBUCIÓN BINOMIAL
        # ==========================================
        elif rama == "probabilidad_binomial":
            n = int(datos_entrada.get('n', 0))
            x = int(datos_entrada.get('x', 0))
            p = float(datos_entrada.get('p', 0.0))

            if not (0 <= p <= 1):
                return _error("La probabilidad 'p' debe estar en formato decimal entre 0 y 1 (ej. 0.35).")
            if x > n or x < 0:
                return _error("El número de éxitos 'x' no puede ser mayor a 'n' ni negativo.")

            q = 1 - p
            combinacion = math.comb(n, x)
            prob_x = combinacion * (p ** x) * (q ** (n - x))

            pasos = [
                {"titulo": "1. Datos", "contenido":
                    f"n (ensayos) = {n}, x (éxitos buscados) = {x}, p (prob. éxito) = {p}, q (prob. fracaso) = 1 - {p} = {q:.4f}"},
                {"titulo": "2. Fórmula de Bernoulli", "contenido":
                    "P(x) = nCx · p^x · q^(n-x)"},
                {"titulo": "3. Calculamos la combinación", "contenido":
                    f"nCx = {n}C{x} = {combinacion}"},
                {"titulo": "4. Sustituimos y calculamos", "contenido":
                    f"P({x}) = {combinacion} · ({p})^{x} · ({q:.4f})^{n - x} = {prob_x:.6f}"},
            ]
            resultado_final = f"P(x={x}) = {prob_x:.6f}  ({prob_x * 100:.2f}%)"
            return _resultado(True, pasos, resultado_final)

        # ==========================================
        # 4. TEOREMA DE BAYES
        # ==========================================
        elif rama == "teorema_bayes":
            p_A = float(datos_entrada.get('p_A', 0))
            p_B_dado_A = float(datos_entrada.get('p_B_dado_A', 0))
            p_no_A = 1 - p_A
            p_B_dado_no_A = float(datos_entrada.get('p_B_dado_no_A', 0))

            p_B_total = (p_A * p_B_dado_A) + (p_no_A * p_B_dado_no_A)
            if p_B_total == 0:
                return _error("La probabilidad total del evento B es 0, no se puede aplicar Bayes.")

            p_A_dado_B = (p_A * p_B_dado_A) / p_B_total

            pasos = [
                {"titulo": "1. Datos", "contenido":
                    f"P(A) = {p_A}, P(B|A) = {p_B_dado_A}, P(no A) = 1 - {p_A} = {p_no_A}, P(B|no A) = {p_B_dado_no_A}"},
                {"titulo": "2. Probabilidad total de B", "contenido":
                    f"P(B) = P(A)·P(B|A) + P(no A)·P(B|no A)\n"
                    f"P(B) = ({p_A})({p_B_dado_A}) + ({p_no_A})({p_B_dado_no_A}) = {p_B_total:.4f}"},
                {"titulo": "3. Aplicamos el Teorema de Bayes", "contenido":
                    f"P(A|B) = [P(A)·P(B|A)] / P(B)\n"
                    f"P(A|B) = ({p_A})({p_B_dado_A}) / {p_B_total:.4f} = {p_A_dado_B:.6f}"},
            ]
            resultado_final = f"P(A|B) = {p_A_dado_B:.6f}  ({p_A_dado_B * 100:.2f}%)"
            return _resultado(True, pasos, resultado_final)

        else:
            return _error("Rama no reconocida. Usa: 'estadistica_descriptiva', 'combinatoria', 'probabilidad_binomial' o 'teorema_bayes'.")

    except Exception as e:
        return _error(f"Error crítico en el cálculo de probabilidad: {e}")
