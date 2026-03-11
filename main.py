from graficador import graficar
from metodos import biseccion, falsa_posicion, newton, secante
from parser import crear_panel_calculadora, parsear_funcion
import tkinter as tk
from tkinter import Tk, messagebox, ttk


METODOS = {
    "Biseccion": {
        "parametros": [("xi", "x inferior"), ("xs", "x superior")],
        "columnas": ("Iteracion", "xi", "xs", "xr", "f(xr)", "Error"),
    },
    "Falsa Posicion": {
        "parametros": [("xi", "x inferior"), ("xs", "x superior")],
        "columnas": ("Iteracion", "xi", "xs", "xr", "f(xr)", "Error"),
    },
    "Secante": {
        "parametros": [("x0", "xi-1"), ("x1", "xi"),
        ],
        "columnas": ("Iteracion", "xi-1", "xi", "xi+1", "f(xi+1)", "Error"),
    },
    "Newton-Raphson": {
        "parametros": [("x0", "xi inicial")],
        "columnas": ("Iteracion", "xi", "f(xi)", "f'(xi)", "xi+1", "Error"),
    },
}


class RaicesApp:
    def __init__(self, root):
        self.root = root
        self.f = None
        self.df = None
        self.expr = None
        self.raiz = None
        self.x_min = None
        self.x_max = None
        self.aproximaciones = []

        self.funcion_var = tk.StringVar()
        self.metodo_var = tk.StringVar(value="Biseccion")
        self.estado_var = tk.StringVar(value="Escribe una funcion y presiona Aplicar funcion.")
        self.expresion_var = tk.StringVar(value="Funcion actual: sin definir")
        self.raiz_var = tk.StringVar(value="Raiz estimada: -")
        self.param_vars = {
            "xi": tk.StringVar(),
            "xs": tk.StringVar(),
            "x0": tk.StringVar(),
            "x1": tk.StringVar(),
        }

        self._construir_ui()
        self._actualizar_parametros()

    def _construir_ui(self):
        self.root.title("Raices App")
        self.root.geometry("920x760")
        self.root.minsize(860, 700)

        try:
            icono = tk.PhotoImage(file="raiz.png")
            self.root.iconphoto(False, icono)
            self.root._icono = icono
        except Exception as e:
            print(f"Aviso: No se pudo cargar el icono 'raiz.png': {e}")

        contenedor = ttk.Frame(self.root, padding=16)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(3, weight=1)

        ttk.Label(contenedor, text="Raices App", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(
            contenedor,
            text="La captura de funcion, parametros y resultados se hace en esta sola ventana.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 12))

        panel_funcion = ttk.LabelFrame(contenedor, text="Funcion")
        panel_funcion.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        panel_funcion.columnconfigure(0, weight=1)

        entrada = ttk.Entry(panel_funcion, textvariable=self.funcion_var, font=("Consolas", 14))
        entrada.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        entrada.bind("<Return>", self._aplicar_funcion)

        ttk.Button(panel_funcion, text="Aplicar funcion", command=self._aplicar_funcion).grid(
            row=0, column=1, padx=(0, 12), pady=(12, 8)
        )
        ttk.Label(panel_funcion, textvariable=self.expresion_var, wraplength=860).grid(
            row=1, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 8)
        )

        calculadora = crear_panel_calculadora(panel_funcion, entrada)
        calculadora.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))

        panel_metodo = ttk.LabelFrame(contenedor, text="Metodo y parametros")
        panel_metodo.grid(row=3, column=0, sticky="nsew")
        panel_metodo.columnconfigure(0, weight=1)
        panel_metodo.rowconfigure(3, weight=1)

        fila_superior = ttk.Frame(panel_metodo)
        fila_superior.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        fila_superior.columnconfigure(4, weight=1)

        ttk.Label(fila_superior, text="Metodo:").grid(row=0, column=0, sticky="w")
        combo = ttk.Combobox(
            fila_superior,
            textvariable=self.metodo_var,
            values=list(METODOS.keys()),
            state="readonly",
            width=18,
        )
        combo.grid(row=0, column=1, sticky="w", padx=(6, 14))
        combo.bind("<<ComboboxSelected>>", self._actualizar_parametros)

        self.param_frame = ttk.Frame(fila_superior)
        self.param_frame.grid(row=0, column=2, sticky="w")

        ttk.Button(fila_superior, text="Resolver", command=self._resolver).grid(row=0, column=3, padx=(14, 8))
        ttk.Button(fila_superior, text="Graficar", command=self._graficar).grid(row=0, column=4, sticky="w")

        ttk.Label(panel_metodo, textvariable=self.estado_var, wraplength=860).grid(
            row=1, column=0, sticky="w", padx=12, pady=(0, 4)
        )
        ttk.Label(panel_metodo, textvariable=self.raiz_var, font=("Segoe UI", 11, "bold")).grid(
            row=2, column=0, sticky="w", padx=12, pady=(0, 8)
        )

        tabla_frame = ttk.Frame(panel_metodo)
        tabla_frame.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tabla_frame, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll_y.set)

    def _actualizar_parametros(self, _event=None):
        for child in self.param_frame.winfo_children():
            child.destroy()

        for idx, (clave, etiqueta) in enumerate(METODOS[self.metodo_var.get()]["parametros"]):
            ttk.Label(self.param_frame, text=f"{etiqueta}:").grid(row=0, column=idx * 2, sticky="w")
            ttk.Entry(self.param_frame, textvariable=self.param_vars[clave], width=10).grid(
                row=0, column=idx * 2 + 1, padx=(6, 12), sticky="w"
            )

        self._configurar_tabla(METODOS[self.metodo_var.get()]["columnas"])

    def _configurar_tabla(self, columnas):
        self.tree["columns"] = columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        for item in self.tree.get_children():
            self.tree.delete(item)

    def _aplicar_funcion(self, _event=None):
        texto = self.funcion_var.get().strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingresa una funcion.", parent=self.root)
            return

        try:
            self.f, self.df, self.expr = parsear_funcion(texto)
        except Exception as e:
            self.f = None
            self.df = None
            self.expr = None
            self.expresion_var.set("Funcion actual: sin definir")
            messagebox.showerror("Error", f"Sintaxis invalida: {e}", parent=self.root)
            return

        self.expresion_var.set(f"Funcion actual: {self.expr}")
        self.estado_var.set("Funcion cargada. Elige el metodo y captura los parametros.")

    def _leer_float(self, clave, etiqueta):
        texto = self.param_vars[clave].get().strip()
        if not texto:
            raise ValueError(f"Falta el valor de {etiqueta}.")
        return float(texto)

    def _resolver(self):
        if self.f is None:
            messagebox.showwarning("Aviso", "Primero aplica una funcion valida.", parent=self.root)
            return

        metodo = self.metodo_var.get()
        historial = []
        self.raiz = None
        self.x_min = None
        self.x_max = None
        self.aproximaciones = []

        try:
            if metodo == "Biseccion":
                xi = self._leer_float("xi", "x inferior")
                xs = self._leer_float("xs", "x superior")
                self.x_min, self.x_max = sorted([xi, xs])
                self.raiz, historial = biseccion(self.f, xi, xs, return_historial=True, mostrar=False)
                self.aproximaciones = [fila[3] for fila in historial]
            elif metodo == "Falsa Posicion":
                xi = self._leer_float("xi", "x inferior")
                xs = self._leer_float("xs", "x superior")
                self.x_min, self.x_max = sorted([xi, xs])
                self.raiz, historial = falsa_posicion(self.f, xi, xs, return_historial=True, mostrar=False)
                self.aproximaciones = [fila[3] for fila in historial]
            elif metodo == "Secante":
                x0 = self._leer_float("x0", "xi-1")
                x1 = self._leer_float("x1", "xi")
                self.x_min, self.x_max = sorted([x0, x1])
                self.raiz, historial = secante(self.f, x0, x1, return_historial=True, mostrar=False)
                self.aproximaciones = [fila[3] for fila in historial]
            else:
                x0 = self._leer_float("x0", "xi inicial")
                self.raiz, historial = newton(self.f, self.df, x0, return_historial=True, mostrar=False)
                self.aproximaciones = [fila[1] for fila in historial]
                if historial:
                    self.aproximaciones.append(historial[-1][4])
                if self.raiz is not None:
                    self.x_min = min(x0, self.raiz)
                    self.x_max = max(x0, self.raiz)
                    if self.x_min == self.x_max:
                        self.x_min -= 1
                        self.x_max += 1
                    margen = 0.25 * (self.x_max - self.x_min)
                    self.x_min -= margen
                    self.x_max += margen
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e), parent=self.root)
            return
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo resolver: {e}", parent=self.root)
            return

        self._configurar_tabla(METODOS[metodo]["columnas"])
        for fila in historial:
            fila_formateada = [
                f"{valor:.6f}" if isinstance(valor, float) else valor
                for valor in fila
            ]
            self.tree.insert("", "end", values=fila_formateada)

        if self.raiz is None:
            self.raiz_var.set("Raiz estimada: no encontrada")
            self.estado_var.set("El metodo no encontro una raiz valida con esos parametros.")
            return

        self.raiz_var.set(f"Raiz estimada: {self.raiz:.6f}")
        self.estado_var.set(f"{metodo} completado con {len(historial)} iteraciones.")

    def _graficar(self):
        if self.f is None or self.raiz is None:
            messagebox.showwarning("Aviso", "Primero resuelve un metodo para poder graficar.", parent=self.root)
            return

        graficar(
            self.f,
            self.raiz,
            x_min=self.x_min,
            x_max=self.x_max,
            aproximaciones=self.aproximaciones,
        )


def main():
    root = Tk()
    RaicesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
