import random
import re
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

def obtenerRaices(listaCoeficientes):
    return np.roots(listaCoeficientes)

def obtenerPolNewton(puntos):
    n = len(puntos)
    x = np.zeros(n)
    y = np.zeros(n)
    for i in range(n):
        x[i] = puntos[i][0]
        y[i] = puntos[i][1]
    a = np.zeros(n)
    for i in range(n):
        a[i] = y[i]
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            a[i] = (a[i] - a[i-1]) / (x[i] - x[i-j])
    polinomio = np.poly1d(a[n-1])
    for i in range(n-2, -1, -1):
        polinomio = np.poly1d([1, -x[i]]) * polinomio + a[i]
    return polinomio

def newton(puntos):
    deshabilitarBotones()
    polSinExp = obtenerPolNewton(puntos)
    mostrarPol(polSinExp, puntos, "Newton")

def validarDenominador(denominador):
    if denominador == 0:
        cartelErrorDivPor0.place(x=posX, y=415)
        raise Exception("División por 0")

def obtenerPolLagrange(pares):
    n = len(pares)
    polinomio = np.poly1d(0)
    for i in range(n):
        termino = np.poly1d(pares[i][1])
        for j in range(n):
            if j != i:
                denominador = pares[i][0] - pares[j][0]
                validarDenominador(denominador)
                termino *= np.poly1d([1, -pares[j][0]]) / denominador
        polinomio += termino
    return polinomio

def deshabilitarBotones():
    getElementoPorTexto(Button, "Newton").config(state=DISABLED)
    getElementoPorTexto(Button, "Lagrange").config(state=DISABLED)

def agregarExponentes(polinomio):
    exponente = int(inputCantNros.get()) - 1
    polinomioConExponentes = ''
    for coef in polinomio.coeffs:
        coef = float(coef)
        coef = "{:.1e}".format(coef).replace("e-0", "e-").replace("e+0", "e+").replace("e0", "e") if round(coef, 2) == -0.0 or round(coef, 2) == 0.0 else round(coef, 2)
        polinomioConExponentes += f'{coef} x^{exponente} + '
        exponente -= 1
    return polinomioConExponentes.replace("x^0 + ", "").replace("x^1 ", "x ")

def graficarPol(pol, puntos, raices, metodo):
    min = float(inputCotaMin.get()) - 1
    max = float(inputCotaMax.get()) + 1
    puntosX = [punto[0] for punto in puntos]
    puntosY = [punto[1] for punto in puntos]

    x = np.linspace(min, max, 100)
    y = pol(x)
    fig, ax = plt.subplots()
    listaCeros = [ 0 for _ in range(len(raices))]

    plt.plot(x, y, color='blue')
    ax.set_xlim(min, max)
    ax.set_ylim(min, max)
    plt.scatter(puntosX, puntosY, color='red', label="Puntos")
    plt.scatter(raices, listaCeros, color='green', label="Raices")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Polinomio Interpolador {metodo}')
    plt.grid(True)
    plt.legend()
    plt.show()

def mostrarPol(polSinExp, puntos, metodo):
    polConExp = agregarExponentes(polSinExp)
    raices = obtenerRaices([coef for coef in polSinExp])
    print(f"Raices: {raices}")
    print(f"Polinomio Interpolador: {polConExp}")
    seccion2.grid(row=1, column=0, padx=35, pady=415, sticky="w")
    Label(content_frame2, text=polConExp, font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10)
    label(posX, 515, f"Grado del Polinomio Interpolador: {int(inputCantNros.get())-1}")
    Button(root, text="Ver Gráfico", command=lambda: graficarPol(polSinExp, puntos, raices, metodo)).place(x=posX, y=545)

def lagrange(puntos):
    deshabilitarBotones()
    polSinExp = obtenerPolLagrange(puntos)
    mostrarPol(polSinExp, puntos, "Lagrange")

def mostrarBotonesDeCalculo(puntos):
    y = 350
    label(posX, y, "Elija el método con el cual obtener un Polinomio Interpolador:")
    y += 30
    Button(root, text="Lagrange", command=lambda: lagrange(puntos)).place(x=posX, y=y)
    Button(root, text="Newton", command=lambda: newton(puntos)).place(x=80, y=y)

def generarXY(min, max):
    return round(random.uniform(min, max), 1), round(random.uniform(min, max), 1)

def generarPuntos(cantPtos, min, max):
    puntos = []
    for i in range(cantPtos):
        x, y = generarXY(min, max)
        while x in [punto[0] for punto in puntos]:
            x, y = generarXY(min, max)
        puntos.append((x, y))
    return sorted(puntos, key=lambda pair: pair[0])

def mostrarPuntos(puntos):
    print(f"Puntos autogenerados: {puntos}")
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
    mostrarBotonesDeCalculo(puntos)

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
    if inputCantNros.get() != "" and inputCantNros.get() != "0":
        inputCantNros.config(state=DISABLED)
        getElementoPorTexto(Button, "Siguiente").config(state=DISABLED)
        ingresarCotas()
    else:
        cartelErrorCantPtos.place(x=posX, y=135)
        raise Exception("Vacío")

def teclaValidaCotas(input):
    return re.match(r"^(?:-)?\d*(?:\.\d*)?$", input) is not None

def teclaValidaCantPtos(input):
    return re.match(r"^(1?[0-9]|20)?$", input) is not None

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
root.geometry("800x600")
root.resizable(False, False)
root.title("Polinomio Interpolador")

seccion1 = LabelFrame(root, text="Puntos Ordenados")
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
cartelErrorDivPor0 = Label(root, text="Error, se produjo una división por 0. Reinicie la app y reintente", font=("Arial", 11), fg="red")

titulos()
inicio()

root.mainloop()