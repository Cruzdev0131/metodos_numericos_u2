import sympy as sp
import numpy as np
from tkinter import simpledialog, messagebox
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

x = sp.symbols('x')

def obtener_funcion():
    # Ventana para ingresar la función
    funcion_input = simpledialog.askstring("Entrada", "Ingresa la función en términos de x (ej: 2x-1 o x**2):")
    
    if not funcion_input:
        return None, None, None

    try:
        # Permite que SymPy entienda "2x" como "2*x"
        transformaciones = (standard_transformations + (implicit_multiplication_application,))
        expr = parse_expr(funcion_input, transformations=transformaciones)
        
        # Convertir a funciones numéricas
        f = sp.lambdify(x, expr, "numpy")
        df_expr = sp.diff(expr, x)
        df = sp.lambdify(x, df_expr, "numpy")
        
        return f, df, expr
    except Exception as e:
        messagebox.showerror("Error", f"Sintaxis inválida: {e}")
        return None, None, None