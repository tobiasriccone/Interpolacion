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

cota_inferior = float(input("Ingrese la cota inferior: "))
cota_superior = float(input("Ingrese la cota superior: "))
pares = []
for _ in range(3):
    x = random.uniform(cota_inferior, cota_superior)
    y = random.uniform(cota_inferior, cota_superior)
    pares.append((x, y))
pares = sorted(pares, key=lambda pair: pair[0])
diferencias_divididas = calcular_diferencias_divididas(pares)
polinomio_interpolador = calcular_polinomio_interpolador(pares, diferencias_divididas)
grado_polinomio = len(polinomio_interpolador) - 1
x_vals = np.linspace(cota_inferior, cota_superior, 100)
y_vals = []
for x in x_vals:
    y = 0
    for termino in polinomio_interpolador:
        producto = 1
        for factor in termino[:-1]:
            producto *= eval(factor.replace("x", str(x)))
        y += termino[-1] * producto
    y_vals.append(y)
plt.plot(x_vals, y_vals, label="Polinomio Interpolador")
plt.scatter(*zip(*pares), color="red", label="Pares de Datos")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Polinomio Interpolador - Datos Ordenados")
plt.show()
pares_reverso = sorted(pares, key=lambda pair: pair[0], reverse=True)
diferencias_divididas_reverso = calcular_diferencias_divididas(pares_reverso)
polinomio_interpolador_reverso = calcular_polinomio_interpolador(pares_reverso, diferencias_divididas_reverso)
grado_polinomio_reverso = len(polinomio_interpolador_reverso) - 1
es_mismo_polinomio = polinomio_interpolador == polinomio_interpolador_reverso
y_vals_reverso = []
for x in x_vals:
    y = 0
    for termino in polinomio_interpolador_reverso:
        producto = 1
        for factor in termino[:-1]:
            producto *= eval(factor.replace("x", str(x)))
        y += termino[-1] * producto
    y_vals_reverso.append(y)
plt.plot(x_vals, y_vals_reverso, label="Polinomio Interpolador Reverso")
plt.scatter(*zip(*pares), color="red", label="Pares de Datos")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Polinomio Interpolador Reverso - Datos Ordenados")
plt.show()
random.shuffle(pares)
diferencias_divididas_desordenado = calcular_diferencias_divididas(pares)
polinomio_interpolador_desordenado = calcular_polinomio_interpolador(pares, diferencias_divididas_desordenado)
grado_polinomio_desordenado = len(polinomio_interpolador_desordenado) - 1
y_vals_desordenado = []
for x in x_vals:
    y = 0
    for termino in polinomio_interpolador_desordenado:
        producto = 1
        for factor in termino[:-1]:
            producto *= eval(factor.replace("x", str(x)))
        y += termino[-1] * producto
    y_vals_desordenado.append(y)
plt.plot(x_vals, y_vals_desordenado, label="Polinomio Interpolador Desordenado")
plt.scatter(*zip(*pares), color="red", label="Pares de Datos")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Polinomio Interpolador - Datos Desordenados")
plt.show()
print("Grado del Polinomio Interpolador (Datos Ordenados):", grado_polinomio)
print("Grado del Polinomio Interpolador Reverso:", grado_polinomio_reverso)
print("¿Es el mismo polinomio?:", es_mismo_polinomio)
print("Grado del Polinomio Interpolador (Datos Desordenados):", grado_polinomio_desordenado)
polinomio_str = "P(x) = "
for termino in polinomio_interpolador:
    coeficiente = termino[-1]
    grado = len(termino) - 2
    if grado == 0:
        polinomio_str += f"{coeficiente:.2f} "
    elif grado == 1:
        polinomio_str += f"{coeficiente:.2f}x + "
    else:
        polinomio_str += f"{coeficiente:.2f}x^{grado} + "
polinomio_str = polinomio_str[:-3]
print(polinomio_str)