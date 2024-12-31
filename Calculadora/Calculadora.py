import tkinter as tk
from tkinter import ttk
from math import sin, cos, tan, log, log1p, sqrt, pi, radians

# Crear la ventana principal
root = tk.Tk()
root.title("CALCULADORA")
root.geometry("400x600")
root.resizable(False, False)  # Tamaño fijo
root.configure(bg="#9A275A")  # Color inicial

# Establecer el ícono de la ventana
root.iconbitmap("calculadora_icon.ico")  # Cambia la ruta al archivo .ico de tu ícono

# Crear un estilo para los botones
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 16, "bold"))

# Variable para almacenar la expresión matemática
expression = ""

# Variable para el modo radianes/grados
mode = "Radianes"  # Opción por defecto

# Función para actualizar la entrada
def update_expression(value):
    global expression
    expression += str(value)
    entry_var.set(expression)

# Función para evaluar la expresión
def evaluate_expression():
    global expression
    try:
        # Realizar la evaluación de la expresión
        result = eval(expression)
        entry_var.set(result)
        expression = str(result)  # Para continuar calculando
    except Exception:
        entry_var.set("Error")
        expression = ""

# Función para borrar la entrada
def clear_expression():
    global expression
    expression = ""
    entry_var.set(expression)

# Función para borrar el último carácter
def backspace():
    global expression
    expression = expression[:-1]
    entry_var.set(expression)

# Función para cambiar el color de la calculadora
color_index = 0
colors = ["#9A275A", "#1C0D02"]  # Opciones de colores a ser cambiados

def change_color():
    global color_index
    color_index = (color_index + 1) % len(colors)
    root.configure(bg=colors[color_index])
    entry_frame.configure(bg=colors[color_index])
    buttons_frame.configure(bg=colors[color_index])
    mode_label.configure(bg=colors[color_index])  # Actualizar el fondo de la etiqueta del modo

# Función para cambiar entre modo Radianes y Grados
def toggle_mode():
    global mode
    if mode == "Radianes":
        mode = "Grados"
    else:
        mode = "Radianes"
    mode_label.config(text=mode)

# Función para realizar cálculos trigonométricos considerando radianes o grados
def calculate_trig(value, op):
    # Convertir entre radianes y grados según el modo
    if mode == "Grados":
        value = radians(value)  # Convertir a radianes si estamos en modo grados
    # Realizar el cálculo trigonométrico según la operación
    if op == "sin":
        return sin(value)
    elif op == "cos":
        return cos(value)
    elif op == "tan":
        return tan(value)

# Crear un marco para la entrada
entry_frame = tk.Frame(root, bg="#9A275A")
entry_frame.pack(pady=20)

# Variable para mostrar la entrada
entry_var = tk.StringVar()

# Crear la caja de entrada
entry = ttk.Entry(entry_frame, textvariable=entry_var, font=("Helvetica", 24), justify="right")
entry.pack(ipadx=10, ipady=10, fill="both")

# Etiqueta para mostrar el modo
mode_label = tk.Label(root, text=mode, font=("Helvetica", 16, "bold"), bg="#9A275A", fg="white")
mode_label.pack(pady=5)

# Crear un marco para los botones
buttons_frame = tk.Frame(root, bg="#9A275A")
buttons_frame.pack(expand=True, fill="both")

# Crear botones de la calculadora
def create_calculator_buttons():
    buttons = [
        ("7", "8", "9", "/", "⌫"),
        ("4", "5", "6", "*", "C"),
        ("1", "2", "3", "-", "("),
        ("0", ".", "=", "+", ")"),
        ("sin", "cos", "tan", "log", "ln"),
        ("sqrt", "pi", "^", "🌞/🌜", "Rad/Grd")
    ]

    for r, row in enumerate(buttons):
        for c, btn_text in enumerate(row):
            if btn_text == "C":
                btn = ttk.Button(buttons_frame, text=btn_text, command=clear_expression)
            elif btn_text == "⌫":
                btn = ttk.Button(buttons_frame, text=btn_text, command=backspace)
            elif btn_text == "=":
                btn = ttk.Button(buttons_frame, text=btn_text, command=evaluate_expression)
            elif btn_text == "🌞/🌜":
                btn = ttk.Button(buttons_frame, text=btn_text, command=change_color)
            elif btn_text == "Rad/Grd":
                btn = ttk.Button(buttons_frame, text=btn_text, command=toggle_mode)
            elif btn_text in ["sin", "cos", "tan", "log", "ln", "sqrt", "pi", "^"]:
                def advanced_function(op=btn_text):
                    global expression
                    try:
                        value = eval(expression)
                        if op in ["sin", "cos", "tan"]:
                            result = calculate_trig(value, op)
                        elif op == "log":
                            result = log(value)
                        elif op == "ln":
                            result = log1p(value - 1)
                        elif op == "sqrt":
                            result = sqrt(value)
                        elif op == "pi":
                            result = pi
                        elif op == "^":
                            result = eval(expression) ** 2  # Simplificación para "exp"
                        expression = str(result)
                        entry_var.set(expression)
                    except Exception:
                        entry_var.set("Error")
                        expression = ""
                btn = ttk.Button(buttons_frame, text=btn_text, command=advanced_function)
            else:
                btn = ttk.Button(buttons_frame, text=btn_text, command=lambda x=btn_text: update_expression(x))
            btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)

    # Ajustar las proporciones de las filas y columnas
    for i in range(len(buttons)):
        buttons_frame.rowconfigure(i, weight=1)
    for j in range(len(buttons[0])):
        buttons_frame.columnconfigure(j, weight=1)

# Inicializar los botones de la calculadora
create_calculator_buttons()

# Iniciar la aplicación
root.mainloop()
