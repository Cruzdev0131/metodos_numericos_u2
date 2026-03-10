import tkinter as tk
from tkinter import ttk

def mostrar_tabla(titulo, columnas, filas):
    ventana = tk.Toplevel()
    ventana.title(titulo)
    ventana.geometry("800x300")
    
    # Crear un marco para la tabla y la barra de desplazamiento
    frame = tk.Frame(ventana)
    frame.pack(expand=True, fill='both', padx=10, pady=10)
    
    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(frame, columns=columnas, show='headings', yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)
    
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor=tk.CENTER)
        
    for fila in filas:
        # Formateamos a 6 decimales para los números y evitar desbordes
        fila_formateada = [fila[0]] + [f"{x:.6f}" if isinstance(x, float) else x for x in fila[1:]]
        tree.insert('', tk.END, values=fila_formateada)
        
    tree.pack(expand=True, fill='both')

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    if f(a)*f(b) > 0:
        return None
        
    columnas = ("Iteración", "xi", "xs", "xr", "f(xr)", "Error")
    filas = []
    
    for i in range(max_iter):
        c = (a+b)/2
        error = abs(f(c))
        
        filas.append((i+1, a, b, c, f(c), error))
        
        if error < tol:
            mostrar_tabla("Método de Bisección", columnas, filas)
            return c
            
        if f(a)*f(c) < 0:
            b = c
        else:
            a = c
            
    mostrar_tabla("Método de Bisección", columnas, filas)
    return (a+b)/2


def falsa_posicion(f, a, b, tol=1e-6, max_iter=100):
    if f(a)*f(b) > 0:
        return None
        
    columnas = ("Iteración", "xi", "xs", "xr", "f(xr)", "Error")
    filas = []
    
    for i in range(max_iter):
        c = b - (f(b)*(b-a))/(f(b)-f(a))
        error = abs(f(c))
        
        filas.append((i+1, a, b, c, f(c), error))
        
        if error < tol:
            mostrar_tabla("Método de Falsa Posición", columnas, filas)
            return c
            
        if f(a)*f(c) < 0:
            b = c
        else:
            a = c
            
    mostrar_tabla("Método de Falsa Posición", columnas, filas)
    return c


def secante(f, x0, x1, tol=1e-6, max_iter=100):
    columnas = ("Iteración", "xi-1", "xi", "xi+1", "f(xi+1)", "Error")
    filas = []
    
    for i in range(max_iter):
        if f(x1) - f(x0) == 0:
            return None
            
        x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))
        error = abs(x2-x1)
        
        filas.append((i+1, x0, x1, x2, f(x2), error))
        
        if error < tol:
            mostrar_tabla("Método de la Secante", columnas, filas)
            return x2
            
        x0, x1 = x1, x2
        
    mostrar_tabla("Método de la Secante", columnas, filas)
    return x2


def newton(f, df, x0, tol=1e-6, max_iter=100):
    columnas = ("Iteración", "xi", "f(xi)", "f'(xi)", "xi+1", "Error")
    filas = []
    
    for i in range(max_iter):
        if df(x0) == 0:
            return None
            
        x1 = x0 - f(x0)/df(x0)
        error = abs(x1-x0)
        
        filas.append((i+1, x0, f(x0), df(x0), x1, error))
        
        if error < tol:
            mostrar_tabla("Método de Newton-Raphson", columnas, filas)
            return x1
            
        x0 = x1
        
    mostrar_tabla("Método de Newton-Raphson", columnas, filas)
    return x1