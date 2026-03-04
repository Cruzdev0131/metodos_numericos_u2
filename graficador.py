import numpy as np
import matplotlib.pyplot as plt

def graficar(f, raiz):
    xs = np.linspace(-10, 10, 400)
    ys = f(xs)

    plt.axhline(0)
    plt.plot(xs, ys)
    
    if raiz is not None:
        plt.scatter(raiz, f(raiz))
    
    plt.title("Gráfica de la función")
    plt.show()