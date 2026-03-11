import tkinter as tk
from tkinter import ttk


def mostrar_tabla(titulo, columnas, filas):
    ventana = tk.Toplevel()
    ventana.title(titulo)
    ventana.geometry("800x300")

    frame = tk.Frame(ventana)
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(frame, columns=columnas, show="headings", yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor=tk.CENTER)

    for fila in filas:
        fila_formateada = [fila[0]] + [f"{x:.6f}" if isinstance(x, float) else x for x in fila[1:]]
        tree.insert("", tk.END, values=fila_formateada)

    tree.pack(expand=True, fill="both")


def _resultado(raiz, filas, return_historial):
    if return_historial:
        return raiz, filas
    return raiz


def biseccion(f, a, b, tol=1e-6, max_iter=100, return_historial=False, mostrar=True):
    if f(a) * f(b) > 0:
        return _resultado(None, [], return_historial)

    columnas = ("Iteracion", "xi", "xs", "xr", "f(xr)", "Error")
    filas = []

    for i in range(max_iter):
        c = (a + b) / 2
        error = abs(f(c))
        filas.append((i + 1, a, b, c, f(c), error))

        if error < tol:
            if mostrar:
                mostrar_tabla("Metodo de Biseccion", columnas, filas)
            return _resultado(c, filas, return_historial)

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    if mostrar:
        mostrar_tabla("Metodo de Biseccion", columnas, filas)
    return _resultado((a + b) / 2, filas, return_historial)


def falsa_posicion(f, a, b, tol=1e-6, max_iter=100, return_historial=False, mostrar=True):
    if f(a) * f(b) > 0:
        return _resultado(None, [], return_historial)

    columnas = ("Iteracion", "xi", "xs", "xr", "f(xr)", "Error")
    filas = []

    for i in range(max_iter):
        c = b - (f(b) * (b - a)) / (f(b) - f(a))
        error = abs(f(c))
        filas.append((i + 1, a, b, c, f(c), error))

        if error < tol:
            if mostrar:
                mostrar_tabla("Metodo de Falsa Posicion", columnas, filas)
            return _resultado(c, filas, return_historial)

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    if mostrar:
        mostrar_tabla("Metodo de Falsa Posicion", columnas, filas)
    return _resultado(c, filas, return_historial)


def secante(f, x0, x1, tol=1e-6, max_iter=100, return_historial=False, mostrar=True):
    columnas = ("Iteracion", "xi-1", "xi", "xi+1", "f(xi+1)", "Error")
    filas = []

    for i in range(max_iter):
        if f(x1) - f(x0) == 0:
            return _resultado(None, filas, return_historial)

        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        error = abs(x2 - x1)
        filas.append((i + 1, x0, x1, x2, f(x2), error))

        if error < tol:
            if mostrar:
                mostrar_tabla("Metodo de la Secante", columnas, filas)
            return _resultado(x2, filas, return_historial)

        x0, x1 = x1, x2

    if mostrar:
        mostrar_tabla("Metodo de la Secante", columnas, filas)
    return _resultado(x2, filas, return_historial)


def newton(f, df, x0, tol=1e-6, max_iter=100, return_historial=False, mostrar=True):
    columnas = ("Iteracion", "xi", "f(xi)", "f'(xi)", "xi+1", "Error")
    filas = []

    for i in range(max_iter):
        if df(x0) == 0:
            return _resultado(None, filas, return_historial)

        x1 = x0 - f(x0) / df(x0)
        error = abs(x1 - x0)
        filas.append((i + 1, x0, f(x0), df(x0), x1, error))

        if error < tol:
            if mostrar:
                mostrar_tabla("Metodo de Newton-Raphson", columnas, filas)
            return _resultado(x1, filas, return_historial)

        x0 = x1

    if mostrar:
        mostrar_tabla("Metodo de Newton-Raphson", columnas, filas)
    return _resultado(x1, filas, return_historial)
