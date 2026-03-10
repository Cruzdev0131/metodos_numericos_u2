from parser import obtener_funcion
from metodos import biseccion, falsa_posicion, secante, newton
from graficador import graficar
import numpy as np
import tkinter as tk # Importado para manejar la imagen del icono
from tkinter import Tk, simpledialog, messagebox

def buscar_intervalos(f, inicio=-50, fin=50, pasos=1000):
    xs = np.linspace(inicio, fin, pasos)
    intervalos = []
    for i in range(len(xs)-1):
        if f(xs[i])*f(xs[i+1]) < 0:
            intervalos.append((xs[i], xs[i+1]))
    return intervalos

def main():
    root = Tk()
    root.withdraw() # Oculta la ventana principal de Tkinter

    # Configuración del icono de la aplicación
    try:
        # Se carga la imagen 'raiz.png' desde la carpeta del proyecto
        icono = tk.PhotoImage(file='raiz.png') 
        root.iconphoto(False, icono)
    except Exception as e:
        # Si el archivo no existe o el formato es incorrecto, el programa continúa sin icono
        print(f"Aviso: No se pudo cargar el icono 'raiz.png': {e}")

    f, df, expr = obtener_funcion()
    if f is None: return

    menu = "1. Bisección\n2. Falsa Posición\n3. Secante\n4. Newton-Raphson"
    opcion = simpledialog.askinteger("Método", f"Selecciona el método:\n\n{menu}")
    
    if not opcion or opcion not in [1, 2, 3, 4]:
        messagebox.showwarning("Aviso", "Opción no válida.")
        return

    intervalos = buscar_intervalos(f)
    raices = []

    for a, b in intervalos:
        if opcion == 1: raiz = biseccion(f, a, b)
        elif opcion == 2: raiz = falsa_posicion(f, a, b)
        elif opcion == 3: raiz = secante(f, a, b)
        elif opcion == 4: raiz = newton(f, df, (a+b)/2)
        
        if raiz is not None:
            raices.append(round(raiz, 6))

    if not raices:
        messagebox.showinfo("Resultado", "No se encontraron raíces en el rango [-50, 50].")
        return

    # Eliminar duplicados y ordenar
    raices = sorted(list(set(raices)))
    
    lista_texto = "\n".join([f"{i+1}: {r}" for i, r in enumerate(raices)])
    eleccion = simpledialog.askinteger("Raíces", f"Se encontraron estas raíces:\n{lista_texto}\n\nIngresa el número de la que quieres graficar:")
    
    if eleccion and 1 <= eleccion <= len(raices):
        graficar(f, raices[eleccion-1])

if __name__ == "__main__":
    main()