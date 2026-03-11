import numpy as np
import matplotlib.pyplot as plt


def graficar(f, raiz, x_min=None, x_max=None, aproximaciones=None):
    if x_min is None or x_max is None:
        if raiz is not None:
            x_min = raiz - 10
            x_max = raiz + 10
        else:
            x_min, x_max = -10, 10

    if x_min == x_max:
        x_min -= 1
        x_max += 1

    if x_min > x_max:
        x_min, x_max = x_max, x_min

    xs = np.linspace(x_min, x_max, 800)
    with np.errstate(all="ignore"):
        ys = np.asarray(f(xs), dtype=float)

    mascara = np.isfinite(ys)
    if not np.any(mascara):
        return

    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="gray", linewidth=0.6)
    plt.plot(xs[mascara], ys[mascara], label="f(x)")

    if aproximaciones:
        aprox = np.asarray(aproximaciones, dtype=float)
        aprox = aprox[np.isfinite(aprox)]
        if aprox.size > 0:
            with np.errstate(all="ignore"):
                y_aprox = np.asarray(f(aprox), dtype=float)
            mascara_aprox = np.isfinite(y_aprox)
            if np.any(mascara_aprox):
                plt.scatter(
                    aprox[mascara_aprox],
                    y_aprox[mascara_aprox],
                    color="orange",
                    s=30,
                    label="Aproximaciones",
                )

    if raiz is not None:
        with np.errstate(all="ignore"):
            y_raiz = f(raiz)
        if np.isfinite(y_raiz):
            plt.scatter(raiz, y_raiz, color="red", s=50, label="Raiz estimada")

    plt.title("Grafica de la funcion")
    plt.xlim(x_min, x_max)
    plt.grid(alpha=0.2)
    plt.legend()
    plt.show()
