from parser import obtener_funcion
from metodos import biseccion, falsa_posicion, secante, newton
from graficador import graficar
import numpy as np
import tkinter as tk # Importado para manejar la imagen del icono
from tkinter import Tk, simpledialog, messagebox

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

    raices = []

    # Pedir valores según el método elegido:
    if opcion == 1 or opcion == 2:
        xi = simpledialog.askfloat("Valores Iniciales", "Ingresa el valor de x inferior (xi):")
        xs = simpledialog.askfloat("Valores Iniciales", "Ingresa el valor de x superior (xs):")
        # Si el usuario cierra la ventana o da cancelar, detenemos el flujo
        if xi is None or xs is None: return
        
        if opcion == 1: 
            raiz = biseccion(f, xi, xs)
        else: 
            raiz = falsa_posicion(f, xi, xs)

    elif opcion == 3:
        x0 = simpledialog.askfloat("Valores Iniciales", "Ingresa el valor de xi-1:")
        x1 = simpledialog.askfloat("Valores Iniciales", "Ingresa el valor de xi:")
        if x0 is None or x1 is None: return
        
        raiz = secante(f, x0, x1)

    elif opcion == 4:
        x0 = simpledialog.askfloat("Valores Iniciales", "Ingresa el valor inicial xi:")
        if x0 is None: return
        
        raiz = newton(f, df, x0)

    # Si se encontró una raíz (no es None), agregarla a la lista
    if raiz is not None:
        raices.append(round(raiz, 6))

    if not raices:
        messagebox.showinfo("Resultado", "No se encontró la raíz o hubo un error en los cálculos.")
        return

    # Eliminar duplicados y ordenar
    raices = sorted(list(set(raices)))
    
    lista_texto = "\n".join([f"{i+1}: {r}" for i, r in enumerate(raices)])
    eleccion = simpledialog.askinteger("Raíces", f"Se encontraron estas raíces:\n{lista_texto}\n\nIngresa el número de la que quieres graficar:")
    
    if eleccion and 1 <= eleccion <= len(raices):
        graficar(f, raices[eleccion-1])

if __name__ == "__main__":
    main()