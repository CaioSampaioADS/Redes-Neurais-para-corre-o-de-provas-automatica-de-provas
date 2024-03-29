# -*- coding: utf-8 -*-
"""
Created on Sat May  9 17:08:33 2020

@author: Caio Sampaio

1 = correto
0 = incorreto
"""

import pandas as pd
import nltk


nltk.download('stopwords')

stopWords = nltk.corpus.stopwords.words('portuguese')
stopWords.append('a')

lista = (('auditoriaexterna.csv','auditoriaexternaParaCorrigir.csv' ),
         ('custio.csv', 'custioParaCorrigir.csv'),
         ('Fotossintese.csv', 'FotossinteseParaCorrigir.csv'),
         ('ObjetivosDaContabilidade.csv', 'ObjetivosDaContabilidadeParaCorrigir.csv'),
         ('respostasDireitoAmbiental.csv', 'respostasDireitoAmbientalParaCorrigir.csv'),
         )

metricas = []

for arqs in lista:

    respostas = pd.read_csv(arqs[0]).dropna()
    
    
    respostasSplit=[]
    
    for i in range(0, len(respostas['RESPOSTAS CORRETAS'])): 
        respostasSplit.append(respostas['RESPOSTAS CORRETAS'][i].split())
        respostasSplit.append(respostas['RESPOSTAS ERRADAS'][i].split())
        
        
        
    '''codigo especial comentar depois
    
    for i in range(len(respostasSplit)):
        if respostasSplit[i] == ['a']:
            del respostasSplit[i]
            
    fim codigo especial'''
        
        
    respostasCorretas = [respostas['RESPOSTAS CORRETAS'][i].split() for i in range(len(respostas['RESPOSTAS CORRETAS']))]
    
    respostasErradas = [respostas['RESPOSTAS ERRADAS'][i].split() for i in range(len(respostas['RESPOSTAS CORRETAS']))]
    
    
    '''codigo especial comentar depois
    
    auxiliar = []
    for i in range(len(respostasErradas)):
       
        if not respostasErradas[i] == ['a']:
            auxiliar.append(respostasErradas[i])
            
    respostasErradas = auxiliar
    fim codigo especial'''
    
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
        
    
    #DataFrameTemp = pd.read_csv('paraCorrigir.csv')
    DataFrameTemp = pd.read_csv(arqs[1])
    
    
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
            
    metricas.append(acuraciaKNNPessoal)
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
            
    metricas.append(acuraciaRegLogisticaSklearn)
    
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
            
    metricas.append(acuraciaSVMSklearn)
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
    Classificador.add(Dense(units=700, activation = 'relu', input_dim = len(x[0])))
    Classificador.add(Dense(units=200, activation = 'relu'))
    Classificador.add(Dense(units=200, activation = 'relu'))
    Classificador.add(Dense(units=200, activation = 'relu'))
    Classificador.add(Dense(units=1, activation = 'sigmoid'))
    Classificador.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    
    
    Classificador.fit(x, y, batch_size=10, nb_epoch = 200)
    
    acuraciaRedesNeuraisKeras = {'acertos': 0, 'erros': 0}
    
    for i in range(len(paraCorrigir)):
        previsao = Classificador.predict(np.array([paraCorrigir[i]['resposta']]))
        
        if previsao[0][0] > 0.5:
            previsao[0][0] = 1
        else:
            previsao[0][0] = 0 
            
    
        
            
        if previsao[0][0] == paraCorrigir[i]['respostaCorreta']:
            acuraciaRedesNeuraisKeras['acertos'] += 1
        else: 
            acuraciaRedesNeuraisKeras['erros'] += 1
    metricas.append(acuraciaRedesNeuraisKeras)
            
    #naive bayes ------------------------------------------------------------------------------------
    from sklearn.naive_bayes import GaussianNB
    import numpy as np
    gnb = GaussianNB()
    gnb.fit(x, y)
    
    acuraciaNaiveBayes = {'acertos': 0, 'erros': 0}
    
    for i in range(len(paraCorrigir)):
        previsao = gnb.predict(np.array([paraCorrigir[i]['resposta']]))
    
        
        if previsao[0] == paraCorrigir[i]['respostaCorreta']:
            acuraciaNaiveBayes['acertos'] += 1
        else: 
            acuraciaNaiveBayes['erros'] += 1
            
    metricas.append(acuraciaNaiveBayes)
                
    #Random Forest -------------------------------------------------------------------------------------
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(max_depth=2, random_state=0)
    clf.fit(x, y)
    acuraciaRandomForest = {'acertos': 0, 'erros': 0}
    for i in range(len(paraCorrigir)):
        previsao = clf.predict(np.array([paraCorrigir[i]['resposta']]))
            
        if previsao[0] == paraCorrigir[i]['respostaCorreta']:
            acuraciaRandomForest['acertos'] += 1
        else: 
            acuraciaRandomForest['erros'] += 1
    metricas.append(acuraciaRandomForest)
    

