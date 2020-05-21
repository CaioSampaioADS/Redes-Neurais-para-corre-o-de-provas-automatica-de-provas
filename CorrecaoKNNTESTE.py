# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

from KNN import KNN

import pandas as pd

respostas = pd.read_csv("respostas.csv")


def TransformaMinusculo(x):
    y = []
    for i in range(0, len(x)):
        y.append(x[i].lower())
    return y


respostasSplit = []
respostasTotais = []
respostasCorretas = []
respostasErradas = []
X = []

for i in range(0, len(respostas['RESPOSTAS CORRETAS'])):
    respostasSplit.append(respostas['RESPOSTAS CORRETAS'][i].split())
    respostasSplit.append(respostas['RESPOSTAS ERRADAS'][i].split())
        
for i in range(0, len(respostas['RESPOSTAS CORRETAS'])):
    respostasCorretas.append(respostas['RESPOSTAS CORRETAS'][i].split())
    
for i in range(0, len(respostas['RESPOSTAS ERRADAS'][0])):
    respostasErradas.append(respostas['RESPOSTAS ERRADAS'][i].split())



for i in range(0, len(respostasSplit)):
    for j in range(0, len(respostasSplit[i])):
        respostasTotais.append(respostasSplit[i][j])
        
respostasTotais = sorted(set(respostasTotais))

respostasTotais = TransformaMinusculo(respostasTotais)

for i in range(0, len(respostasCorretas)):
    for j in range(0, len(respostasCorretas[i])):
        respostasCorretas[i][j] = respostasCorretas[i][j].lower()
        
for i in range(0, len(respostasErradas)):
    for j in range(0, len(respostasErradas[i])):
        respostasErradas[i][j] = respostasErradas[i][j].lower()


x = []

for i in range(0, len(respostasCorretas)):
    x.append([])
    for j in range(0, len(respostasTotais)):
        somatoria = 0
        for h in range(0, len(respostasCorretas[i])):
            if respostasTotais[j] == respostasCorretas[i][h]:
                somatoria += 1
        x[i].append(somatoria)
        
        
        
for i in range(len(respostasCorretas), len(respostasErradas) + len(respostasCorretas)):
    x.append([])
    for j in range(0, len(respostasTotais)):
        somatoria = 0
        for h in range(0, len(respostasErradas[i - len(respostasCorretas)])):
            if respostasTotais[j] == respostasErradas[i - len(respostasCorretas)][h]:
                somatoria += 1
        x[i].append(somatoria)

y = [1,1,1,1,1,1,1,0,0,0,0,0,0,0]
knn = KNN(x,y)

respostaClassificar = input("O que é estatistica").lower().split()

respostaClassificarNumerico = []
for i in range(0, len(respostasTotais)):
    somatoria = 0
    for j in range(0, len(respostaClassificar)):
        if respostasTotais[i] == respostaClassificar[j]:
            somatoria += 1
    respostaClassificarNumerico.append(somatoria)
        
        
rr = knn.Classificar(respostaClassificarNumerico)


if rr == 1:
    print("resposta correta")
else:
    print("resposta incorreta")

        

    
