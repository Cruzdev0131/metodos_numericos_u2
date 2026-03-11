import sympy as sp
import tkinter as tk
from tkinter import messagebox, ttk
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

x = sp.symbols("x")

BOTONES_CALCULADORA = [
    ("7", "7"), ("8", "8"), ("9", "9"), ("/", "/"), ("(", "("), (")", ")"), ("C", "__LIMPIAR__"), ("<-", "__BORRAR__"),
    ("4", "4"), ("5", "5"), ("6", "6"), ("*", "*"), ("pi", "pi"), ("E", "E"), ("x^y", "**"), ("x", "x"),
    ("1", "1"), ("2", "2"), ("3", "3"), ("-", "-"), ("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("sqrt", "sqrt("),
    ("0", "0"), (".", "."), (",", ","), ("+", "+"), ("asin", "asin("), ("acos", "acos("), ("atan", "atan("), ("abs", "abs("),
    ("ln", "ln("), ("log", "log("), ("exp", "exp("), ("x2", "**2"), ("x3", "**3"), ("frac", "()/()"),
]


def parsear_funcion(funcion_input):
    funcion_input = funcion_input.strip().replace("^", "**")
    transformaciones = standard_transformations + (implicit_multiplication_application,)
    entorno = {
        "x": x,
        "e": sp.E,
        "E": sp.E,
        "pi": sp.pi,
        "sen": sp.sin,
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "asin": sp.asin,
        "acos": sp.acos,
        "atan": sp.atan,
        "ln": sp.log,
        "log": sp.log,
        "exp": sp.exp,
        "sqrt": sp.sqrt,
        "abs": sp.Abs,
    }

    expr = parse_expr(funcion_input, transformations=transformaciones, local_dict=entorno)
    f = sp.lambdify(x, expr, "numpy")
    df_expr = sp.diff(expr, x)
    df = sp.lambdify(x, df_expr, "numpy")
    return f, df, expr


def crear_panel_calculadora(parent, entrada):
    frame_botones = ttk.Frame(parent)

    def insertar(texto):
        entrada.insert(tk.INSERT, texto)
        entrada.focus_set()

    def borrar_uno():
        pos = entrada.index(tk.INSERT)
        if pos > 0:
            entrada.delete(pos - 1, pos)
        entrada.focus_set()

    def limpiar():
        entrada.delete(0, tk.END)
        entrada.focus_set()

    total_cols = 8
    for idx, (etiqueta, token) in enumerate(BOTONES_CALCULADORA):
        fila = idx // total_cols
        col = idx % total_cols

        def accion(t=token):
            if t == "__LIMPIAR__":
                limpiar()
            elif t == "__BORRAR__":
                borrar_uno()
            elif t == "()/()":
                pos = entrada.index(tk.INSERT)
                insertar("()/()")
                entrada.icursor(pos + 1)
            else:
                insertar(t)

        ttk.Button(frame_botones, text=etiqueta, command=accion).grid(
            row=fila,
            column=col,
            padx=3,
            pady=3,
            sticky="nsew",
        )

    for c in range(total_cols):
        frame_botones.columnconfigure(c, weight=1)
    for r in range((len(BOTONES_CALCULADORA) + total_cols - 1) // total_cols):
        frame_botones.rowconfigure(r, weight=1)

    return frame_botones


def _pedir_funcion_calculadora(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Entrada de funcion")
    ventana.geometry("720x380")
    ventana.resizable(False, False)

    resultado = {"valor": None}

    ttk.Label(
        ventana,
        text="Escribe f(x). Puedes usar teclado o botones (sin, cos, tan, ln, log, exp, sqrt, potencias).",
    ).pack(anchor="w", padx=12, pady=(12, 4))

    entrada_var = tk.StringVar()
    entrada = ttk.Entry(ventana, textvariable=entrada_var, font=("Consolas", 14))
    entrada.pack(fill="x", padx=12, pady=(0, 10))
    entrada.focus_set()

    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def insertar(texto):
        entrada.insert(tk.INSERT, texto)
        entrada.focus_set()

    def borrar_uno():
        pos = entrada.index(tk.INSERT)
        if pos > 0:
            entrada.delete(pos - 1, pos)
        entrada.focus_set()

    def limpiar():
        entrada.delete(0, tk.END)
        entrada.focus_set()

    def aceptar(_event=None):
        texto = entrada_var.get().strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingresa una funcion.", parent=ventana)
            return
        resultado["valor"] = texto
        ventana.destroy()

    def cancelar(_event=None):
        resultado["valor"] = None
        ventana.destroy()

    botones = BOTONES_CALCULADORA + [("ENTER", "__ACEPTAR__"), ("Salir", "__CANCELAR__")]

    total_cols = 8
    for idx, (etiqueta, token) in enumerate(botones):
        fila = idx // total_cols
        col = idx % total_cols

        def accion(t=token):
            if t == "__LIMPIAR__":
                limpiar()
            elif t == "__BORRAR__":
                borrar_uno()
            elif t == "__ACEPTAR__":
                aceptar()
            elif t == "__CANCELAR__":
                cancelar()
            elif t == "()/()":
                pos = entrada.index(tk.INSERT)
                insertar("()/()")
                entrada.icursor(pos + 1)
            else:
                insertar(t)

        ttk.Button(frame_botones, text=etiqueta, command=accion).grid(
            row=fila,
            column=col,
            padx=3,
            pady=3,
            sticky="nsew",
        )

    for c in range(total_cols):
        frame_botones.columnconfigure(c, weight=1)
    for r in range((len(botones) + total_cols - 1) // total_cols):
        frame_botones.rowconfigure(r, weight=1)

    ventana.bind("<Return>", aceptar)
    ventana.bind("<Escape>", cancelar)
    ventana.protocol("WM_DELETE_WINDOW", cancelar)
    ventana.transient(parent)
    ventana.grab_set()
    ventana.focus_force()
    ventana.wait_window()

    return resultado["valor"]


def obtener_funcion(parent):
    while True:
        funcion_input = _pedir_funcion_calculadora(parent)
        if not funcion_input:
            return None, None, None

        try:
            f, df, expr = parsear_funcion(funcion_input)
            return f, df, expr
        except Exception as e:
            messagebox.showerror("Error", f"Sintaxis invalida: {e}", parent=parent)
