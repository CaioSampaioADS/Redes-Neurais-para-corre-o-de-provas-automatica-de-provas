import numpy as np
from random import *

'''def TratarTexto():
    resposta = input("Digite sua resposta")
    resposta = resposta.lower()
    respostaCripto = []
    respostasCorretas = ["linguagem de programacao", "forma de programar computador", "linguagem de programar computadores", "programação interpretada", "linguagem programacao orienteda"]
    respostasErradas = ["maneiras de cozinhar", "tipos de corrida rua", "jogo de computador"]

    for i in range(0, len(resposta)):
        respostaCripto.append(ord(resposta[i]))

    if len(respostaCripto) < 50:
        for i in range(0, 50-len(respostaCripto)):
            respostaCripto.append(1)

    return respostaCripto, respostasCorretas, respostasErradas, resposta'''

def DefiniResultadoEsperado(respostaUsuario, respostaCorreta, respostaErrada):
    resultadoEsperado = 0
    if respostaUsuario in respostaCorreta:
        resultadoEsperado = 1
    elif respostaUsuario in respostaErrada:
        resultadoEsperado = 0

    return resultadoEsperado

def TreinamentoRedeNeural():

    respostasCorretasCripto = []
    respostasCorretas = ["linguagem de programacao", "forma de programar computador",
                         "linguagem de programar computadores", "programação interpretada",
                         "linguagem programacao orienteda"]

    respostasErradas = ["maneiras de cozinhar", "tipos de corrida rua", "jogo de computador"]

    respostaCriptografada = []

    sigmoid = []
    pesosCamadaEntrada = []
    pesos = np.zeros((50))

    passada = 0
    pesosv = []
    pesosvCamadaOculta = []

    for resposta in range(0, 9):
        respostaCriptografada.clear()
        resposta = input("digite uma resposta")

        resultadoEsperada = 0
        if resposta in respostasCorretas:
            resultadoEsperada = 1
        elif resposta in respostasErradas:
            resultadoEsperada = 0


        for i in range(0, len(resposta)):
            respostaCriptografada.append(ord(resposta[i]))

        if len(respostaCriptografada) < 50:
            for i in range(0, 50 - len(respostaCriptografada)):
                respostaCriptografada.append(1)

        respostaCriptoNP = np.array(respostaCriptografada)
        respostaCriptoNP = respostaCriptoNP / 100

        while True:

            sigmoid.clear()
            pesosvCamadaOculta.clear()

            for j in range(0, 4):
                pesosv.clear()

                if passada == 0:
                    for i in range(0, 50):
                        pesosv.append(uniform(-1, 1))

                    pesos = np.array(pesosv)
                print(f"pesos = {pesos}")
                multiplicacaoEntradaPelosPesos = respostaCriptoNP * pesos
                somatoria = np.sum(multiplicacaoEntradaPelosPesos)
                sigmoid.append(1 / (1 + np.exp(-somatoria)))

            if passada ==0:
                for i in range(0, 4):
                    pesosvCamadaOculta.append(uniform(-1,1))

                pesosCamadaOculta = np.array(pesosvCamadaOculta)


            multiplicacaoOcultaPelosPesos = sigmoid * pesosCamadaOculta
            somatoriaCamadaOculta = np.sum(multiplicacaoOcultaPelosPesos)
            sigmoidFinal = 1 / (1 + np.exp(-somatoriaCamadaOculta))
            passada += 1

            print(sigmoidFinal)
            if sigmoidFinal > 0.5:
                print("resposta correta")
                if resultadoEsperada == 1:
                    break
            else:
                print("resposta incorreta")
                if resultadoEsperada == 0:
                    break

            erro = resultadoEsperada - sigmoidFinal

            pesoAntigo = np.array(pesos)


            for i in range(0, 50):
                pesos[i] = pesos[i] + (0.2 * respostaCriptoNP[i] * erro)

            for i in range(0, 4):
                pesosCamadaOculta[i] = pesosCamadaOculta[i] + (0.2 * sigmoid[i] * erro)

            diferenca = pesoAntigo - pesos
            diferenca = np.sum(diferenca)
            print(f'diferenca = {diferenca}')




    arquivo = open('pesosCamadaEntrada.txt', 'w')
    for i in range(0, 50):
        arquivo.write(str(pesos[i]) + " ")

    arquivoOculta = open('pesosCamadaOculta.txt', 'w')
    for i in range(0, 4):
        arquivoOculta.write(str(pesosCamadaOculta[i]) + " ")

def RedeNeural():
    resposta = input('digite uma resposta para verificar se está correta')
    respostaCriptografada = []
    for i in range(0, len(resposta)):
        respostaCriptografada.append(ord(resposta[i]))

    if len(respostaCriptografada) < 50:
        for i in range(0, 50 - len(respostaCriptografada)):
            respostaCriptografada.append(1)

    respostaCriptoNP = np.array(respostaCriptografada)
    respostaCriptoNP = respostaCriptoNP / 100

    arquivo = open("pesosCamadaEntrada.txt", 'r')
    pesos = arquivo.read()
    pesos = pesos.split()

    for i in range(0, len(pesos)):
        pesos[i] = float(pesos[i])

    sigmoid = []
    for i in range(0, 4):
        pesos = np.array(pesos)

        multiplicacaoEntradaPelosPesos = respostaCriptoNP * pesos
        somatoria = np.sum(multiplicacaoEntradaPelosPesos)

        sigmoid.append(1/(1+np.exp(-somatoria)))



    arquivoCamadaOculta = open("pesosCamadaOculta.txt", 'r')
    pesosCamadaOculta = arquivoCamadaOculta.read()
    pesosCamadaOculta = pesosCamadaOculta.split()

    for i in range(0, len(pesosCamadaOculta)):
        pesosCamadaOculta[i] = float(pesosCamadaOculta[i])

    pesosCamadaOculta = np.array(pesosCamadaOculta)

    multiplicacaoSigmoidPelosPesos = sigmoid * pesosCamadaOculta

    somatoriaOculta = np.sum(multiplicacaoSigmoidPelosPesos)

    sigmoidFinal = 1/(1 + np.exp(-somatoriaOculta))

    if sigmoidFinal > 0.5:
        print("resposta correta")
    elif sigmoidFinal < 0.5:
        print('resposta errada')












'''respostaCripto, respostasCorretas, repostaErradas, resposta = TratarTexto()'''

'''re = DefiniResultadoEsperado(resposta, respostasCorretas, repostaErradas)'''

decisao = int(input('digite 1 para treinar e 2 para testar'))
if decisao == 1:
    TreinamentoRedeNeural()
elif decisao == 2:
    RedeNeural()