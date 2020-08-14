# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 17:04:13 2020

@author: PICHAU
"""


def preprocessamento():
    import pandas as pd
    import nltk
    
    
    
    
    nltk.download('stopwords')
    
    stopWords = nltk.corpus.stopwords.words('portuguese')
    stopWords.append('a')
    
    #preparando dados de treino
    
    
    respostas = pd.read_csv("respostasDireitoAmbiental.csv").dropna()
    
    
    respostasSplit=[]
    
    for i in range(0, len(respostas['RESPOSTAS CORRETAS'])): 
        respostasSplit.append(respostas['RESPOSTAS CORRETAS'][i].split())
        respostasSplit.append(respostas['RESPOSTAS ERRADAS'][i].split())
        
        
        
    '''codigo especial comentar depois'''
    
    '''for i in range(len(respostasSplit)):
        if respostasSplit[i] == ['a']:
            del respostasSplit[i]'''
            
    '''fim codigo especial'''
        
        
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
        
    return x, y, respostasTotais
    
x, y, respostasTotais = preprocessamento()
    
def knn(x,y, resposta):
    import numpy as np
    from sklearn.neighbors import KNeighborsClassifier
    

    resposta = resposta.split()


    stringProcessada = []
    for h in range(len(respostasTotais)):
        qnt = 0
        for j in range(len(resposta)):
            if resposta[j] == respostasTotais[h]:
                qnt += 1
        stringProcessada.append(qnt)
        
    
    stringProcessada = np.array(stringProcessada).reshape(1,-1) 

    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(x, y)
    
    return neigh.predict(stringProcessada)

knn(x,y,"O princípio do dpoluidorfdsfddsf pagador significa que é possível a alguém pagar para poluir")


def reglog(x,y, resposta):
    import numpy as np
    
    resposta = resposta.split()


    stringProcessada = []
    for h in range(len(respostasTotais)):
        qnt = 0
        for j in range(len(resposta)):
            if resposta[j] == respostasTotais[h]:
                qnt += 1
        stringProcessada.append(qnt)
        
    
    stringProcessada = np.array(stringProcessada).reshape(1,-1)
    
    from sklearn.linear_model import LogisticRegression

    clf = LogisticRegression(random_state=0).fit(x, y)
    
    return clf.predict(stringProcessada)
    
reg = reglog(x,y,"A realização de obras de engenharia destinadas ao uso comercial deverá ser precedida de estudo prévio de impacto ambiental em razão do princípio da precauçã")

def svm(x, y, resposta):
    import numpy as np
    from sklearn.svm import SVC
    
    resposta = resposta.split()


    stringProcessada = []
    for h in range(len(respostasTotais)):
        qnt = 0
        for j in range(len(resposta)):
            if resposta[j] == respostasTotais[h]:
                qnt += 1
        stringProcessada.append(qnt)
        
    
    stringProcessada = np.array(stringProcessada).reshape(1,-1)
    
    
    svm = SVC(gamma='auto')
    svm.fit(x, y)
    
  

    return svm.predict(stringProcessada)
        
reg = svm(x, y, "De acordo com o estabelecido na Lei nº 9605 de 12 de fevereiro de 1998 (crimes contra o meio ambiente) constitui crime causar poluição de qualquer natureza em níveis tais que resultem ou possam resultar em danos à saúde humana ou que provoquem a mortandade de animais ou a destruição significativa da flora Este tipo penal admite apenas a forma dolosa")

def redesNeurais(x, y, resposta):
    import keras
    from keras.models import Sequential
    from keras.layers import Dense
    import numpy as np
    from keras.utils.vis_utils import plot_model
    
    
    import numpy as np
    
    resposta = resposta.split()


    stringProcessada = []
    for h in range(len(respostasTotais)):
        qnt = 0
        for j in range(len(resposta)):
            if resposta[j] == respostasTotais[h]:
                qnt += 1
        stringProcessada.append(qnt)
        
    
    stringProcessada = np.array(stringProcessada).reshape(1,-1)
    
    x = np.array(x)
    y = np.array(y)
    Classificador = Sequential()
    Classificador.add(Dense(units=700, activation = 'relu', input_dim = 554))
    Classificador.add(Dense(units=200, activation = 'relu'))
    Classificador.add(Dense(units=200, activation = 'relu'))
    Classificador.add(Dense(units=200, activation = 'relu'))
    Classificador.add(Dense(units=1, activation = 'sigmoid'))
    Classificador.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    
    
    Classificador.fit(x, y, batch_size=10, nb_epoch = 100)
    
    
    
    return Classificador.predict(stringProcessada)
    
