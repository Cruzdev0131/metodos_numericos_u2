from parser import obtener_funcion
from metodos import biseccion, falsa_posicion, secante, newton
from graficador import graficar
import numpy as np

def buscar_intervalos(f, inicio=-50, fin=50, pasos=1000):
    xs = np.linspace(inicio, fin, pasos)
    intervalos = []
    
    for i in range(len(xs)-1):
        if f(xs[i])*f(xs[i+1]) < 0:
            intervalos.append((xs[i], xs[i+1]))
    
    return intervalos


def main():
    f, df, expr = obtener_funcion()
    
    print("\nMétodos disponibles:")
    print("1. Bisección")
    print("2. Falsa Posición")
    print("3. Secante")
    print("4. Newton-Raphson")
    
    opcion = int(input("Elige método: "))
    
    intervalos = buscar_intervalos(f)
    raices = []

    for a, b in intervalos:
        if opcion == 1:
            raiz = biseccion(f, a, b)
        elif opcion == 2:
            raiz = falsa_posicion(f, a, b)
        elif opcion == 3:
            raiz = secante(f, a, b)
        elif opcion == 4:
            raiz = newton(f, df, (a+b)/2)
        else:
            print("Opción inválida")
            return
        
        if raiz is not None:
            raices.append(raiz)

    if not raices:
        print("No se encontraron raíces.")
        return

    raices = sorted(raices)
    
    print("\nRaíces encontradas:")
    for r in raices:
        print(r)

    print("\n1. Raíz menor")
    print("2. Raíz mayor")
    eleccion = int(input("¿Cuál quieres?: "))
    
    if eleccion == 1:
        raiz_final = raices[0]
    else:
        raiz_final = raices[-1]
    
    print("Raíz seleccionada:", raiz_final)
    graficar(f, raiz_final)


if __name__ == "__main__":
    main()