# -*- coding: utf-8 -*-
"""
Created on Sat May  9 17:08:33 2020

@author: PICHAU
"""

import pandas as pd
import nltk




nltk.download('stopwords')

stopWords = nltk.corpus.stopwords.words('portuguese')
stopWords.append('a')

#preparando dados de treino


respostas = pd.read_csv("respostas.csv")


respostasSplit=[]

for i in range(0, len(respostas['RESPOSTAS CORRETAS'])): 
    respostasSplit.append(respostas['RESPOSTAS CORRETAS'][i].split())
    respostasSplit.append(respostas['RESPOSTAS ERRADAS'][i].split())
    
    
respostasCorretas = [respostas['RESPOSTAS CORRETAS'][i].split() for i in range(len(respostas['RESPOSTAS CORRETAS']))]

respostasErradas = [respostas['RESPOSTAS ERRADAS'][i].split() for i in range(len(respostas['RESPOSTAS CORRETAS']))]


respostasTotais = []


for i in range(len(respostasSplit)):
    for j in range(len(respostasSplit[i])):
        if not respostasSplit[i][j] in stopWords:
            respostasTotais.append(respostasSplit[i][j].lower())
            

respostasTotais = sorted(set(respostasTotais))

x = []
y = []



for i in range(len(respostasCorretas)):
    x.append([])
    for j in range(len(respostasTotais)):
        qnt = 0
        for h in range(len(respostasCorretas[i])):
            if respostasTotais[j] == respostasCorretas[i][h]:
                qnt += 1
        x[i].append(qnt)
    y.append(1)
    
    
for i in range(len(respostasErradas)):
    x.append([])
    for j in range(len(respostasTotais)):
        qnt = 0 
        for h in range(len(respostasErradas[i])):
            if respostasTotais[j] == respostasErradas[i][h]:
                qnt += 1
        x[i+len(respostasCorretas)].append(qnt)
    y.append(0)
    
#-----------------------------------------------------------------------------------------------------------------------------------------

#preparando respostar à corrigir
    

DataFrameTemp = pd.read_csv('paraCorrigir.csv')

paraCorrigir = []

for i in range(len(DataFrameTemp)):
    paraCorrigir.append({'resposta': DataFrameTemp['respostas'][i].lower().split(), 'respostaCorreta': DataFrameTemp['classificacao'][i]})
    



respostasParaCorrigir = []

for i in range(len(paraCorrigir)):
    respostasParaCorrigir.append([])
    for j in range(len(respostasTotais)):
        qnt = 0
        for h in range(len(paraCorrigir[i]['resposta'])):
            if respostasTotais[j] == paraCorrigir[i]['resposta'][h]:
                qnt += 1       
        respostasParaCorrigir[i].append(qnt)
    

for i in range(len(respostasParaCorrigir)):
    paraCorrigir[i]['resposta'].clear()
    paraCorrigir[i]['resposta'] = respostasParaCorrigir[i]
    
#------------------------------------------------------------------------------------------------------------------------------------------
#testes com KNN pessoal
    
from KNN import KNN

knn = KNN(x, y)

acuraciaKNNPessoal = {'acertos': 0, 'erros': 0}
    
for i in range(len(paraCorrigir)):
    rr = knn.Classificar(paraCorrigir[i]['resposta'],quantidadeKProximos = 3)
    
    if rr == paraCorrigir[i]['respostaCorreta']:
        acuraciaKNNPessoal['acertos'] += 1
    else:
        acuraciaKNNPessoal['erros'] += 1
#--------------------------------------------------------------------------------------------------------------------------------------------
#testes com KNN sklearn
        
from sklearn.neighbors import KNeighborsClassifier

neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(x, y)


acuraciaKNNSklearn = {'acertos': 0, 'erros': 0}
    
for i in range(len(paraCorrigir)):
    rr = neigh.predict([paraCorrigir[i]['resposta']])
    
    if rr == paraCorrigir[i]['respostaCorreta']:
        acuraciaKNNSklearn['acertos'] += 1
    else:
        acuraciaKNNSklearn['erros'] += 1
#--------------------------------------------------------------------------------------------------------------------------------------------
#testes REG. Logistica SKlearn
        
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(random_state=0).fit(x, y)

acuraciaRegLogisticaSklearn = {'acertos': 0, 'erros': 0}

for i in range(len(paraCorrigir)):
    rr = clf.predict([paraCorrigir[i]['resposta']])
    
    if rr == paraCorrigir[i]['respostaCorreta']:
        acuraciaRegLogisticaSklearn['acertos'] += 1
    else: 
        acuraciaRegLogisticaSklearn['erros'] += 1

#---------------------------------------------------------------------------------------------------------------------------------------------------
#testes SVM SKLEARN
        
from sklearn.svm import SVC
svm = SVC(gamma='auto')
svm.fit(x, y)

acuraciaSVMSklearn = {'acertos': 0, 'erros': 0}
    
for i in range(len(paraCorrigir)):
    rr = svm.predict([paraCorrigir[i]['resposta']])
    
    if rr == paraCorrigir[i]['respostaCorreta']:
        acuraciaSVMSklearn['acertos'] += 1
    else: 
        acuraciaSVMSklearn['erros'] += 1
#-------------------------------------------------------------------------------------------------------------------------------------------------
#testes Redes Neurais
        
import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras.utils.vis_utils import plot_model
from ann_visualizer.visualize import ann_viz;
x = np.array(x)
y = np.array(y)
Classificador = Sequential()
Classificador.add(Dense(units=109, activation = 'relu', input_dim = 109))
Classificador.add(Dense(units=200, activation = 'relu'))
Classificador.add(Dense(units=200, activation = 'relu'))
Classificador.add(Dense(units=200, activation = 'relu'))
Classificador.add(Dense(units=1, activation = 'sigmoid'))
Classificador.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])



Classificador.fit(x, y, batch_size=10, nb_epoch = 1000)

acuraciaRedesNeuraisKeras = {'acertos': 0, 'erros': 0}

for i in range(len(paraCorrigir)):
    previsao = Classificador.predict(np.array([paraCorrigir[i]['resposta']]))
    
    if previsao[0][0] > 0.5:
        previsao[0][0] = 1
    else:
        previsao[0][0] = 0 
        
    
    print(previsao[0][0])

    
        
    if previsao[0][0] == paraCorrigir[i]['respostaCorreta']:
        acuraciaRedesNeuraisKeras['acertos'] += 1
    else: 
        acuraciaRedesNeuraisKeras['erros'] += 1
        
        
ann_viz(Classificador, title="Artificial Neural network - Model Visualization")


previsao = Classificador.predict(np.array([paraCorrigir[2]['resposta']]))
            





