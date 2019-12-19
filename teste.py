'''from random import *
arquivo = open('pesosCamadaEntrada.txt', 'w')
pesosCamadaEntrada = []

for i in range(0, 50):
    pesosCamadaEntrada.append(uniform(-1, 1))
    arquivo.write(str(pesosCamadaEntrada[i]) + " ")
'''
'''
arquivo = open("pesosCamadaEntrada.txt", 'r')
pesos = arquivo.read()
pesos = pesos.split()
print(pesos)
'''
'''

arquivoOculta = open('pesosCamadaOculta.txt', 'w')
pesosCamadaOculta = []

for i in range(0, 4):
    pesosCamadaOculta.append(uniform(-1, 1))
    arquivoOculta.write(str(pesosCamadaOculta[i]) + " ")
'''
import numpy as np
x = np.array([2, 2, 2, 2])
y = [2, 2, 2, 2]

print(x*y)






