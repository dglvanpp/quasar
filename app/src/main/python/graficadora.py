import sympy as sp

def generar_puntos(funcion_str, x_min, x_max, num_puntos=200):
    """
    Recibe f(x) como texto (ej. 'x**2 - 3*x + 2'), un rango [x_min, x_max]
    y devuelve una lista de pares [x, y] listos para dibujar en Kotlin.
    Los puntos donde la función no está definida (asíntotas, dominios
    restringidos) se omiten en vez de romper la gráfica.
    """
    try:
        x = sp.symbols('x')
        funcion = sp.sympify(funcion_str)
        f_num = sp.lambdify(x, funcion, modules=['math'])

        x_min = float(x_min)
        x_max = float(x_max)
        paso = (x_max - x_min) / num_puntos

        puntos = []
        for i in range(num_puntos + 1):
            xi = x_min + i * paso
            try:
                yi = f_num(xi)
                if yi is not None and not (isinstance(yi, complex)) and abs(yi) < 1e6:
                    puntos.append([round(xi, 6), round(float(yi), 6)])
            except (ZeroDivisionError, ValueError, TypeError):
                continue  # punto no definido, se salta (ej. división entre 0)

        return puntos

    except Exception as e:
        return f"Error al graficar: {e}"


if __name__ == "__main__":
    print(generar_puntos("x**2 - 3*x + 2", -5, 5, 20))
    print(generar_puntos("1/x", -5, 5, 20))
