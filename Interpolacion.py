import random
import re
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

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
# def grafPol(pol, puntos, titulo):
#     x_vals = np.linspace(cota_inferior, cota_superior, 200)
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
# def crearPol(puntos):
#     coef = calcular_diferencias_divididas(puntos)
#     return calcular_polinomio_interpolador(puntos, coef)
#
# def generarPuntos():
#     puntos = []
#     for _ in range(20):
#         x = random.uniform(cota_inferior, cota_superior)
#         y = random.uniform(cota_inferior, cota_superior)
#         puntos.append((x, y))
#     return puntos

# cota_inferior = -10 # float(input("Ingrese la cota inferior: "))
# cota_superior = 10 # float(input("Ingrese la cota superior: "))
# puntos = generarPuntos()
#
# puntosOrd = sorted(puntos, key=lambda pair: pair[0])
# polOrd = crearPol(puntosOrd)
# grafPol(polOrd, puntosOrd, "Ordenado")
# gradoPolOrd = len(polOrd) - 1
#
# puntosRev = sorted(puntos, key=lambda pair: pair[0], reverse=True)
# polRev = crearPol(puntosRev)
# grafPol(polRev, puntosRev, "Reverso")
# gradoPolRev = len(polRev) - 1
#
# mismoPol = polOrd == polRev
#
# random.shuffle(puntos)
# polDes = crearPol(puntos)
# grafPol(polDes, puntos, "Desordenado")
# gradoPolDes = len(polDes) - 1
#
# print("Grado del Polinomio Interpolador (Datos Ordenados):", gradoPolOrd)
# print("Grado del Polinomio Interpolador (Datos Desordenados):", gradoPolDes)
# print("¿Es el mismo polinomio?:", mismoPol)
# print("Grado del Polinomio Interpolador Reverso:", gradoPolRev)
# polinomio_str = "P(x) = "
# for termino in polOrd:
#     coeficiente = termino[-1]
#     grado = len(termino) - 2
#     if grado == 0:
#         polinomio_str += f"{coeficiente:.2f} "
#     elif grado == 1:
#         polinomio_str += f"{coeficiente:.2f}x + "
#     else:
#         polinomio_str += f"{coeficiente:.2f}x^{grado} + "
# polinomio_str = polinomio_str[:-3]

def calcular():
    yCalcular = 240

def validarCotas():
    cartelErrorCotas.place_forget()
    min = inputCotaMin.get()
    max = inputCotaMax.get()
    if min == "" or min == "-" or min.startswith("-.") or min.startswith(".") or max == "" or max == "-" or max.startswith("-.") or max.startswith(".") :
        cartelErrorCotas.place(x=70, y=210)
        raise Exception("Error")
    else:
        inputCotaMin.config(state=DISABLED)
        inputCotaMax.config(state=DISABLED)
        getElementoPorTexto(Button, "Calcular").config(state=DISABLED)
        calcular()

def ingresarCotas():
    yIngresarCotas = 140
    label(posX, yIngresarCotas, "Ingrese la cota mínima:")
    inputCotaMin.place(x=170, y=yIngresarCotas, width=30, height=25)
    yIngresarCotas += 35
    label(posX, yIngresarCotas, "Ingrese la cota máxima:")
    inputCotaMax.place(x=170, y=yIngresarCotas, width=30, height=25)
    yIngresarCotas += 35
    Button(root, text="Calcular", command=validarCotas).place(x=posX, y=yIngresarCotas)

def getElementoPorTexto(tipoElemento, texto):
    for widget in root.winfo_children():
        if isinstance(widget, tipoElemento) and widget["text"] == texto:
            return widget
    raise Exception(f"No se encontro el elemento con el texto '{texto}'")

def validarCantPtosIngrsado():
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
    Button(root, text="Siguiente", command=validarCantPtosIngrsado).place(x=360, y=yInicio-2)

def titulos():
    labelBold(posX, 10, "TP Polinomio Interpolador - Métodos Numéricos", 16)
    labelBold(posX, 45, "Grupo 08 conformado por Riccone y Nicotra", 12)
    label(posX, 75, "------------------------------------")

root = Tk()
root.geometry("800x650")
root.resizable(False, False)
root.title("Polinomio Interpolador")

posX = 10
inputCantNros = Entry(root, validate="key", validatecommand=(root.register(teclaValidaCantPtos), '%P'))
inputCotaMin = Entry(root, validate="key", validatecommand=(root.register(teclaValidaCotas), '%P'))
inputCotaMax = Entry(root, validate="key", validatecommand=(root.register(teclaValidaCotas), '%P'))

cartelErrorCantPtos = Label(root, text="Vacío", font=("Arial", 11), fg="red")
cartelErrorCotas = Label(root, text="Error, reintente", font=("Arial", 11), fg="red")

titulos()
inicio()

root.mainloop()