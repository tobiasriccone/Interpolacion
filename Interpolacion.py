import random
import re
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

def deshabilitarBotones():
    getElementoPorTexto(Button, "Diferencias Divididas").config(state=DISABLED)
    getElementoPorTexto(Button, "Coeficientes Incrementales").config(state=DISABLED)
    getElementoPorTexto(Button, "Lagrange").config(state=DISABLED)

def difDiv():
    deshabilitarBotones()
    seccion2.grid(row=1, column=0, padx=35, pady=415, sticky="w")
    Label(content_frame2, text="x^3 + 2x^2 - 1", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10)
    label(posX, 515, "Grado del Polinomio Interpolador: ")
    Button(root, text="Ver Gráfico").place(x=posX, y=545)

def mostrarBotonesDeCalculo():
    y = 350
    label(posX, y, "Elija el método con el cual obtener un Polinomio Interpolador:")
    y += 30
    Button(root, text="Diferencias Divididas", command=difDiv).place(x=posX, y=y)
    Button(root, text="Coeficientes Incrementales").place(x=150, y=y)
    Button(root, text="Lagrange").place(x=330, y=y)

def generarPuntos(cantPtos, min, max):
    puntos = []
    for _ in range(cantPtos):
        x = round(random.uniform(min, max), 1)
        y = round(random.uniform(min, max), 1)
        puntos.append((x, y))
    return puntos

def mostrarPuntos(puntos):
    seccion1.grid(row=1, column=0, padx=35, pady=250, sticky="w")
    Label(content_frame1, text=puntos, font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10)

def validarCotas():
    cartelErrorCotas.place_forget()
    min = inputCotaMin.get()
    max = inputCotaMax.get()
    if min == "" or min == "-" or min.startswith("-.") or min.startswith(".") or max == "" or max == "-" or max.startswith("-.") or max.startswith(".") or float(min) >= float(max):
        cartelErrorCotas.place(x=110, y=210)
        raise Exception("Error")
    else:
        inputCotaMin.config(state=DISABLED)
        inputCotaMax.config(state=DISABLED)
        getElementoPorTexto(Button, "Generar Puntos").config(state=DISABLED)

def armarYMostrarPuntos():
    validarCotas()
    puntos = generarPuntos(int(inputCantNros.get()), float(inputCotaMin.get()), float(inputCotaMax.get()))
    mostrarPuntos(puntos)
    mostrarBotonesDeCalculo()

def ingresarCotas():
    yIngresarCotas = 140
    label(posX, yIngresarCotas, "Ingrese la cota mínima:")
    inputCotaMin.place(x=170, y=yIngresarCotas, width=30, height=25)
    yIngresarCotas += 35
    label(posX, yIngresarCotas, "Ingrese la cota máxima:")
    inputCotaMax.place(x=170, y=yIngresarCotas, width=30, height=25)
    yIngresarCotas += 35
    Button(root, text="Generar Puntos", command=armarYMostrarPuntos).place(x=posX, y=yIngresarCotas)

def getElementoPorTexto(tipoElemento, texto):
    for widget in root.winfo_children():
        if isinstance(widget, tipoElemento) and widget["text"] == texto:
            return widget
    raise Exception(f"No se encontro el elemento con el texto '{texto}'")

def validarCantPtosIngresado():
    cartelErrorCantPtos.place_forget()
    if inputCantNros.get() != "":
        inputCantNros.config(state=DISABLED)
        getElementoPorTexto(Button, "Siguiente").config(state=DISABLED)
        ingresarCotas()
    else:
        cartelErrorCantPtos.place(x=posX, y=135)
        raise Exception("Vacío")

def teclaValidaCotas(input):
    return re.match(r"^(?:-)?\d*(?:\.\d*)?$", input) is not None

def teclaValidaCantPtos(input):
    return re.match(r"^(1?[1-9]|20)?$", input) is not None

def labelBold(x, y, texto, font=11):
    Label(root, text=texto, font=("Arial", font, "bold")).place(x=x, y=y)

def label(x, y, texto, font=11):
    Label(root, text=texto, font=("Arial", font)).place(x=x, y=y)

def inicio():
    yInicio = 105
    label(posX, yInicio, "Ingrese la cantidad de puntos a generar (1-20):")
    inputCantNros.place(x=320, y=yInicio, width=30, height=25)
    Button(root, text="Siguiente", command=validarCantPtosIngresado).place(x=360, y=yInicio - 2)

def titulos():
    labelBold(posX, 10, "TP Polinomio Interpolador - Métodos Numéricos", 16)
    labelBold(posX, 45, "Grupo 08 conformado por Riccone y Nicotra", 12)
    label(posX, 75, "------------------------------------")

def on_canvas_configure1(event):
    canvas1.configure(scrollregion=canvas1.bbox("all"))

def on_canvas_configure2(event):
    canvas2.configure(scrollregion=canvas2.bbox("all"))

root = Tk()
root.geometry("800x650")
root.resizable(False, False)
root.title("Polinomio Interpolador")

seccion1 = LabelFrame(root, text="Puntos")
canvas1 = Canvas(seccion1, width=700, height=50)
canvas1.grid(row=0, column=0, sticky="nsew")
content_frame1 = Frame(canvas1)
canvas1.create_window((0, 0), window=content_frame1, anchor="nw")
canvas1.configure(scrollregion=canvas1.bbox("all"))
scrollbar1 = Scrollbar(seccion1, orient="horizontal", command=canvas1.xview)
scrollbar1.grid(row=1, column=0, sticky="ew")
canvas1.configure(xscrollcommand=scrollbar1.set)
canvas1.bind("<Configure>", on_canvas_configure1)

seccion2 = LabelFrame(root, text="Polinomio Interpolador")
canvas2 = Canvas(seccion2, width=700, height=50)
canvas2.grid(row=0, column=0, sticky="nsew")
content_frame2 = Frame(canvas2)
canvas2.create_window((0, 0), window=content_frame2, anchor="nw")
canvas2.configure(scrollregion=canvas2.bbox("all"))
scrollbar2 = Scrollbar(seccion2, orient="horizontal", command=canvas2.xview)
scrollbar2.grid(row=1, column=0, sticky="ew")
canvas2.configure(xscrollcommand=scrollbar2.set)
canvas2.bind("<Configure>", on_canvas_configure2)

posX = 10
inputCantNros = Entry(root, validate="key", validatecommand=(root.register(teclaValidaCantPtos), '%P'))
inputCotaMin = Entry(root, validate="key", validatecommand=(root.register(teclaValidaCotas), '%P'))
inputCotaMax = Entry(root, validate="key", validatecommand=(root.register(teclaValidaCotas), '%P'))

cartelErrorCantPtos = Label(root, text="Vacío", font=("Arial", 11), fg="red")
cartelErrorCotas = Label(root, text="Error, reintente", font=("Arial", 11), fg="red")

titulos()
inicio()

root.mainloop()

# def grafPol(pol, puntos, min, max, titulo):
#     x_vals = np.linspace(min, max, 200)
#     y_vals = []
#     for x in x_vals:
#         y = 0
#         for termino in pol:
#             producto = 1
#             for factor in termino[:-1]:
#                 producto *= eval(factor.replace("x", str(x)))
#             y += termino[-1] * producto
#         y_vals.append(y)
#     plt.plot(x_vals, y_vals)
#     plt.scatter(*zip(*puntos), color="red")
#     plt.legend()
#     plt.xlabel("x")
#     plt.ylabel("y")
#     plt.grid()
#     plt.title(f"Polinomio Interpolador - {titulo}")
#     plt.show()
#
# def calcular_diferencias_divididas(pares):
#     n = len(pares)
#     diferencias = [[0] * n for _ in range(n)]
#     for i in range(n):
#         diferencias[i][0] = pares[i][1]
#     for j in range(1, n):
#         for i in range(n - j):
#             diferencias[i][j] = (diferencias[i + 1][j - 1] - diferencias[i][j - 1]) / (pares[i + j][0] - pares[i][0])
#     return diferencias[0]
#
# def calcular_polinomio_interpolador(pares, diferencias):
#     n = len(pares)
#     polinomio = []
#     for i in range(n):
#         termino = [diferencias[i]]
#         for j in range(i):
#             termino.insert(0, f"(x - {pares[j][0]})")
#         polinomio.append(termino)
#     return polinomio
#
# def crearPol(puntos):
#     coef = calcular_diferencias_divididas(puntos)
#     return calcular_polinomio_interpolador(puntos, coef)