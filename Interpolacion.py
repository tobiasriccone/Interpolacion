import random
import matplotlib.pyplot as plt
import numpy as np

def calcular_diferencias_divididas(pares):
    n = len(pares)
    diferencias = [[0] * n for _ in range(n)]
    for i in range(n):
        diferencias[i][0] = pares[i][1]
    for j in range(1, n):
        for i in range(n - j):
            diferencias[i][j] = (diferencias[i + 1][j - 1] - diferencias[i][j - 1]) / (pares[i + j][0] - pares[i][0])
    return diferencias[0]

def calcular_polinomio_interpolador(pares, diferencias):
    n = len(pares)
    polinomio = []
    for i in range(n):
        termino = [diferencias[i]]
        for j in range(i):
            termino.insert(0, f"(x - {pares[j][0]})")
        polinomio.append(termino)
    return polinomio

def grafPol(pol, puntos, titulo):
    x_vals = np.linspace(cota_inferior, cota_superior, 200)
    y_vals = []
    for x in x_vals:
        y = 0
        for termino in pol:
            producto = 1
            for factor in termino[:-1]:
                producto *= eval(factor.replace("x", str(x)))
            y += termino[-1] * producto
        y_vals.append(y)
    plt.plot(x_vals, y_vals)
    plt.scatter(*zip(*puntos), color="red")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.title(f"Polinomio Interpolador - {titulo}")
    plt.show()

def crearPol(puntos):
    coef = calcular_diferencias_divididas(puntos)
    return calcular_polinomio_interpolador(puntos, coef)

def generarPuntos():
    puntos = []
    for _ in range(20):
        x = random.uniform(cota_inferior, cota_superior)
        y = random.uniform(cota_inferior, cota_superior)
        puntos.append((x, y))
    return puntos

cota_inferior = -10 # float(input("Ingrese la cota inferior: "))
cota_superior = 10 # float(input("Ingrese la cota superior: "))
puntos = generarPuntos()

puntosOrd = sorted(puntos, key=lambda pair: pair[0])
polOrd = crearPol(puntosOrd)
grafPol(polOrd, puntosOrd, "Ordenado")
gradoPolOrd = len(polOrd) - 1

puntosRev = sorted(puntos, key=lambda pair: pair[0], reverse=True)
polRev = crearPol(puntosRev)
grafPol(polRev, puntosRev, "Reverso")
gradoPolRev = len(polRev) - 1

mismoPol = polOrd == polRev

random.shuffle(puntos)
polDes = crearPol(puntos)
grafPol(polDes, puntos, "Desordenado")
gradoPolDes = len(polDes) - 1

print("Grado del Polinomio Interpolador (Datos Ordenados):", gradoPolOrd)
print("Grado del Polinomio Interpolador (Datos Desordenados):", gradoPolDes)
print("¿Es el mismo polinomio?:", mismoPol)
print("Grado del Polinomio Interpolador Reverso:", gradoPolRev)
polinomio_str = "P(x) = "
for termino in polOrd:
    coeficiente = termino[-1]
    grado = len(termino) - 2
    if grado == 0:
        polinomio_str += f"{coeficiente:.2f} "
    elif grado == 1:
        polinomio_str += f"{coeficiente:.2f}x + "
    else:
        polinomio_str += f"{coeficiente:.2f}x^{grado} + "
polinomio_str = polinomio_str[:-3]