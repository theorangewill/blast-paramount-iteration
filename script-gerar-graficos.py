#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import pprint
import numpy as np
import scipy.stats
import os

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return h

try:
    os.mkdir("graficos")
except:
    pass
experimentos = {}
dados =  {'r5.xlarge' : {'preco':0.252/3600},
          'r5.2xlarge' : {'preco':0.504/3600},
          'r5.4xlarge' : {'preco':1.008/3600},
          'r5.12xlarge' : {'preco':3.024/3600},
          'r5.24xlarge' : {'preco':6.048/3600}}
instanciaV = ('r5.xlarge', 'r5.2xlarge', 'r5.4xlarge', 'r5.12xlarge', 'r5.24xlarge')
entradaV = ('pequeno', 'grande')
threadV = ('2', '4', '8', '16', '32', '48', '64', '96')
tamanhoV = ('pi', 'full')
colors = ('#e57914', '#18ce64', '#1ca8ef', '#ce18a9', '#d13714', '#aed114', '#f9bb7a', '#a55e13',
            '#e3c712', '#85e312', '#3a21cc', '#cc23c4', '#36d9d1', '#a437de')

if len(sys.argv) == 1:
    print "ERRO: não há arquivo para leitura"
    print("\tpython script-gerar-graficos.py <nome arquivo>")
    exit()

pp = pprint.PrettyPrinter(indent=2)
instancias = []
for arquivo in sys.argv[1:]:
    arq = open(arquivo, 'r')
    nomearquivo = arquivo[8:-4]
    numerocores = arq.readline().replace("\n","")
    experimentos[nomearquivo] = {}
    dados[nomearquivo]['numerocores'] = int(numerocores)
    linha = " "
    entradas = []
    while linha:
        linha = arq.readline().replace("\n","")
        if linha == "&":
            experimentosPI = []
            experimentosFULL = []
            nomeentrada = arq.readline().replace("\n","")[9:]
            entrada = nomeentrada[13:]
            experimentos[nomearquivo][entrada] = {'nome' : nomeentrada, 'pi' : {}, 'full' : {}}
        elif linha == "*":
            threads = arq.readline().replace("\n","")
            execucoesPI = []
            execucoesFULL = []
            for exe in range(5):
                #LEITURA DAS 5 ITERACOES
                paramountiteration = int(arq.readline().replace("\n",""))
                dadosPI = [float(0.0)]*paramountiteration
                for pi in range(paramountiteration):
                    i = arq.readline().split(";")
                    dadosPI[pi] += float(i[1])
                execucoesPI.append(dadosPI)
                linha = arq.readline().replace("\n","")
                #LEITIRA DAS 50 ITERACOES
                total = int(arq.readline().replace("\n",""))
                dadosFULL = [float(0.0)]*total
                for t in range(total):
                    i = arq.readline().split(";")
                    dadosFULL[t] += float(i[1])
                execucoesFULL.append(dadosFULL)
            execucoesPI = ([(a+b+c+d+e)/5 for a, b, c, d, e in zip(execucoesPI[0], execucoesPI[1], execucoesPI[2], execucoesPI[3], execucoesPI[4])])
            experimentosPI.append([threads,sum(execucoesPI),execucoesPI])
            experimentos[nomearquivo][entrada]['pi'][threads] = {'n':threads, 'tempo':float(sum(execucoesPI)), 'erro': mean_confidence_interval(execucoesPI),'iteracoes':execucoesPI}
            execucoesFULL = ([(a+b+c+d+e)/5 for a, b, c, d, e in zip(execucoesFULL[0], execucoesFULL[1], execucoesFULL[2], execucoesFULL[3], execucoesFULL[4])])
            experimentosFULL.append([threads,sum(execucoesFULL),execucoesFULL])
            experimentos[nomearquivo][entrada]['full'][threads] = {'n':threads, 'tempo':float(sum(execucoesFULL)), 'erro': mean_confidence_interval(execucoesPI),'iteracoes':execucoesFULL}
    arq.close()

pp.pprint(experimentos)


#GRAFICO DE VALIDACAO DO PARAMOUNT ITERATION EM UMA INSTANCIA E ENTRADA PARA DIFERENTES THREADS
for instancia in experimentos:
    for entrada in experimentos[instancia]:
        for thread,color in zip(experimentos[instancia][entrada]['full'],colors):
            plt.plot(experimentos[instancia][entrada]['full'][thread]['iteracoes'], '-', label=str(thread)+" threads" , color=color)
        plt.xlabel('iteracoes')
        plt.ylabel('tempo(s)')
        #plt.title("Tempo de execucao de 50 iteracoes para " + experimentos[instancia][entrada]['nome'] + "\n na instancia " + instancia + " com diferentes numero de threads")
        plt.legend(loc='upper left')
        plt.savefig('graficos/'+entrada+'-'+instancia.replace(".","")+'-validinstance.svg', format="svg")
        #plt.show()
        plt.clf()

        tempo = np.inf
        melhor = []
        for thread in experimentos[instancia][entrada]['full']:
            if tempo >= experimentos[instancia][entrada]['full'][thread]['tempo']:
                tempo = experimentos[instancia][entrada]['full'][thread]['tempo']
                melhor = [thread,tempo]

        print "Instancia " + instancia + " Entrada " + entrada
        for thread in experimentos[instancia][entrada]['full']:
            print "\tSpeedup de " + melhor[0] + " threads(" + str(melhor[1]) + ") em relação a " + thread + " threads(" + str(experimentos[instancia][entrada]['full'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['full'][thread]['tempo']/melhor[1])


print "--------------------------------------------------------------"
#GRAFICO DE VALIDACAO DO PARAMOUNT ITERATION EM UMA INSTANCIA E NUMERO DE THREADS PARA DIFERENTES INSTANCIAS
for entrada in entradaV:
    for thread in threadV:
        for instancia,color in zip(experimentos,colors):
            if int(thread) <= dados[instancia]['numerocores']:
                if int(thread) == 48 and dados[instancia]['numerocores'] == 96:
                    continue
                plt.plot(experimentos[instancia][entrada]['full'][thread]['iteracoes'], '-', label=instancia, color=color)
        plt.xlabel('iteracoes')
        plt.ylabel('tempo(s)')
        #plt.title("Tempo de execucao de 50 iteracoes para " + experimentos['r5.xlarge'][entrada]['nome'] + "\n com " + thread + " threads para diferentes instancias")
        plt.legend(loc='upper left')
        plt.savefig('graficos/'+entrada+'-'+thread+'-validthread.svg', format="svg")
        #plt.show()
        plt.clf()

        tempo = np.inf
        melhor = []
        for instancia in experimentos:
            if int(thread) <= dados[instancia]['numerocores']:
                if int(thread) == 48 and dados[instancia]['numerocores'] == 96:
                    continue
                if tempo >= experimentos[instancia][entrada]['full'][thread]['tempo']:
                    tempo = experimentos[instancia][entrada]['full'][thread]['tempo']
                    melhor = [instancia,tempo]

        print "Entrada " + entrada + " Threads " + thread
        for instancia in experimentos:
            if int(thread) <= dados[instancia]['numerocores']:
                if int(thread) == 48 and dados[instancia]['numerocores'] == 96:
                    continue
                print "\tSpeedup de " + melhor[0] + "(" + str(melhor[1]) + ") em relação a " + instancia + "(" + str(experimentos[instancia][entrada]['full'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['full'][thread]['tempo']/melhor[1])


print "--------------------------------------------------------------"


for entrada in entradaV:
    for thread in threadV:
        tempo = np.inf
        melhorpi = ['0',1]
        for instancia in experimentos:
            if int(thread) <= dados[instancia]['numerocores']:
                if int(thread) == 48 and dados[instancia]['numerocores'] == 96:
                    continue
                if tempo >= experimentos[instancia][entrada]['pi'][thread]['tempo']:
                    tempo = experimentos[instancia][entrada]['pi'][thread]['tempo']
                    melhorpi = [instancia,tempo]
        tempo = np.inf
        melhorfull = ['0',1]
        for instancia in experimentos:
            if int(thread) <= dados[instancia]['numerocores']:
                if int(thread) == 48 and dados[instancia]['numerocores'] == 96:
                    continue
                if tempo >= experimentos[instancia][entrada]['full'][thread]['tempo']:
                    tempo = experimentos[instancia][entrada]['full'][thread]['tempo']
                    melhorfull = [instancia,tempo]


        print "Entrada " + entrada + " Thread " + thread
        if melhorfull[0] != melhorpi[0]:
            print "O MELHOR DO FULL NÃO É O MELHOR DO PARAMOUNT ITERATION"
            for instancia in experimentos:
                if int(thread) <= dados[instancia]['numerocores']:
                    if int(thread) == 48 and dados[instancia]['numerocores'] == 96:
                        continue
                    print "\tSpeedup de " + melhorfull[0] + " (" + str(melhorfull[1]) + ") em relação a " + instancia + " (" + str(experimentos[instancia][entrada]['full'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['full'][thread]['tempo']/melhorfull[1])
                    print "\t\t\tO mesmo não é visto no Paramount Iteration com o " + melhorpi[0] + " (" + str(melhorpi[1]) + ") em relação a " + instancia + " (" + str(experimentos[instancia][entrada]['pi'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['pi'][thread]['tempo']/melhorpi[1])
        else:
            for instancia in experimentos:
                if int(thread) <= dados[instancia]['numerocores']:
                    if int(thread) == 48 and dados[instancia]['numerocores'] == 96:
                        continue
                    print "\tSpeedup de " + melhorfull[0] + " (" + str(melhorfull[1]) + ") em relação a " + instancia + " (" + str(experimentos[instancia][entrada]['full'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['full'][thread]['tempo']/melhorfull[1])
                    print "\t\t\tO mesmo é visto no Paramount Iteration com o melhor " + melhorpi[0] + " (" + str(melhorpi[1]) + ") em relação a " + instancia + " (" + str(experimentos[instancia][entrada]['pi'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['pi'][thread]['tempo']/melhorpi[1])

print "--------------------------------------------------------------"


#GRAFICO DO TEMPO EM UMA INSTANCIA PARA DIFERENTES NUMEROS DE THREADS
for instancia in experimentos:
    for entrada in experimentos[instancia]:
        tempos = []
        for thread in experimentos[instancia][entrada]['pi']:
            tempos.append([thread,experimentos[instancia][entrada]['pi'][thread]['tempo']])
        tempos.sort(key = lambda x: int(x[0]))
        plt.plot([item[0] for item in tempos], [item[1] for item in tempos], 'o-', color=colors[0])
        plt.xlabel('numero de threads')
        plt.ylabel('tempo(s)')
        #plt.title("Tempo de execucao de 5 iteracoes para " + experimentos[instancia][entrada]['nome'] + "\n na instancia " + instancia + " com diferentes numero de threads")
        #plt.legend(loc='upper left')
        plt.savefig('graficos/'+entrada+'-'+instancia.replace(".","")+'-timing.svg', format="svg")
        #plt.show()
        plt.clf()

        tempo = np.inf
        melhorpi = ['0',1]
        for thread in experimentos[instancia][entrada]['pi']:
            if tempo >= experimentos[instancia][entrada]['pi'][thread]['tempo']:
                tempo = experimentos[instancia][entrada]['pi'][thread]['tempo']
                melhorpi = [thread,tempo]
        tempo = np.inf
        melhorfull = ['0',1]
        for thread in experimentos[instancia][entrada]['full']:
            if tempo >= experimentos[instancia][entrada]['full'][thread]['tempo']:
                tempo = experimentos[instancia][entrada]['full'][thread]['tempo']
                melhorfull = [thread,tempo]


        print "Instancia " + instancia + " Entrada " + entrada
        if melhorfull[0] != melhorpi[0]:
            print "O MELHOR DO FULL NÃO É O MELHOR DO PARAMOUNT ITERATION"
            for thread in experimentos[instancia][entrada]['pi']:
                print "\tSpeedup de " + melhorfull[0] + " threads(" + str(melhorfull[1]) + ") em relação a " + thread + " threads (" + str(experimentos[instancia][entrada]['full'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['full'][thread]['tempo']/melhorfull[1])
                print "\t\t\tO mesmo não é visto no Paramount Iteration com o " + melhorpi[0] + " threads (" + str(melhorpi[1]) + ") em relação a " + thread + " threads (" + str(experimentos[instancia][entrada]['pi'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['pi'][thread]['tempo']/melhorpi[1])


        else:
            for thread in experimentos[instancia][entrada]['pi']:
                print "\tSpeedup de " + melhorfull[0] + " threads(" + str(melhorfull[1]) + ") em relação a " + thread + " threads (" + str(experimentos[instancia][entrada]['full'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['full'][thread]['tempo']/melhorfull[1])
                print "\t\t\tO mesmo é visto no Paramount Iteration com o melhor " + melhorpi[0] + " threads (" + str(melhorpi[1]) + ") em relação a " + thread + " threads (" + str(experimentos[instancia][entrada]['pi'][thread]['tempo']) + "): " + str(experimentos[instancia][entrada]['pi'][thread]['tempo']/melhorpi[1])

print "--------------------------------------------------------------"

#CALCULO DO OVERHEAD DE CADA UM
for entrada in entradaV:
    print "ENTRADA: " + entrada

    print "OVEHEAD DE TEMPO"
    tempo = np.inf
    for instancia in experimentos:
        for thread in experimentos[instancia][entrada]['pi']:
            if tempo >= experimentos[instancia][entrada]['pi'][thread]['tempo']:
                tempo = experimentos[instancia][entrada]['pi'][thread]['tempo']
                melhorpi = [instancia,thread,tempo]
    tempo = np.inf
    for instancia in experimentos:
        for thread in experimentos[instancia][entrada]['full']:
            if tempo >= experimentos[instancia][entrada]['full'][thread]['tempo']:
                tempo = experimentos[instancia][entrada]['full'][thread]['tempo']
                melhorfull = [instancia,thread,tempo]
    if melhorfull[0] != melhorpi[0]:
        print "\tA MELHOR INSTANCIA FOI DIFERENTE"
    if melhorfull[1] != melhorpi[1]:
        print "\tA MELHOR THREAD FOI DIFERENTE"
    print "\tA MELHOR CONFIGURACAO FULL " + melhorfull[0] + "-" + melhorfull[1] + " = " + str(melhorfull[2]) + " a um custo de " + str(melhorfull[2]*dados[melhorfull[0]]['preco'])
    print "\tA MELHOR CONFIGURACAO PI " + melhorpi[0] + "-" + melhorpi[1] + " = " + str(melhorpi[2]) + " a um custo de " + str(melhorpi[2]*dados[melhorpi[0]]['preco'])

    for instancia in experimentos:
        for thread in experimentos[instancia][entrada]['pi']:
            print "\t\t" + instancia + " com " + thread + " threads (" + str(experimentos[instancia][entrada]['pi'][thread]['tempo']) + ") = " +  str(experimentos[instancia][entrada]['pi'][thread]['tempo']/melhorpi[2])

    print "\nOVEHEAD DE PRECO"
    custo = np.inf
    for instancia in experimentos:
        for thread in experimentos[instancia][entrada]['pi']:
            if custo >= experimentos[instancia][entrada]['pi'][thread]['tempo']*dados[instancia]['preco']:
                custo = experimentos[instancia][entrada]['pi'][thread]['tempo']*dados[instancia]['preco']
                melhorpi = [instancia,thread,custo,experimentos[instancia][entrada]['pi'][thread]['tempo']]
    custo = np.inf
    for instancia in experimentos:
        for thread in experimentos[instancia][entrada]['full']:
            if custo >= experimentos[instancia][entrada]['full'][thread]['tempo']*dados[instancia]['preco']:
                custo = experimentos[instancia][entrada]['full'][thread]['tempo']*dados[instancia]['preco']
                melhorfull = [instancia,thread,custo,experimentos[instancia][entrada]['full'][thread]['tempo']]
    if melhorfull[0] != melhorpi[0]:
        print "\tA MELHOR INSTANCIA FOI DIFERENTE"
    if melhorfull[1] != melhorpi[1]:
        print "\tA MELHOR THREAD FOI DIFERENTE"
    print "\tA MELHOR CONFIGURACAO FULL " + melhorfull[0] + "-" + melhorfull[1] + " = " + str(melhorfull[2]) + " a um tempo de " + str(melhorfull[3])
    print "\tA MELHOR CONFIGURACAO PI " + melhorpi[0] + "-" + melhorpi[1] + " = " + str(melhorpi[2]) + " a um tempo de " + str(melhorpi[3])

    print "\tOVERHEAD COM PI"
    for instancia in experimentos:
        for thread in experimentos[instancia][entrada]['pi']:
            print "\t\t" + instancia + " com " + thread + " threads (" + str(experimentos[instancia][entrada]['pi'][thread]['tempo']) + ") = " +  str(experimentos[instancia][entrada]['pi'][thread]['tempo']*dados[instancia]['preco']/(melhorpi[2]))

    print "\tOVERHEAD COM FULL"
    for instancia in experimentos:
        for thread in experimentos[instancia][entrada]['full']:
            print "\t\t" + instancia + " com " + thread + " threads (" + str(experimentos[instancia][entrada]['full'][thread]['tempo']) + ") = " +  str(experimentos[instancia][entrada]['full'][thread]['tempo']*dados[instancia]['preco']/(melhorfull[2]))




print "--------------------------------------------------------------"
#GRAFICO DO TEMPO PARA TODAS INSTANCIAS PARA DIFERENTES NUMEROS DE THREADS
for entrada in entradaV:
    for instancia,color in zip(experimentos,colors):
        tempos = []
        for thread in experimentos[instancia][entrada]['pi']:
            tempos.append([thread,experimentos[instancia][entrada]['pi'][thread]['tempo']])
        tempos.sort(key = lambda x: int(x[0]))
        plt.plot([item[0] for item in tempos], [item[1] for item in tempos], 'o-', label=instancia, color=color)
    plt.xlabel('numero de threads')
    plt.ylabel('tempo(s)')
    #plt.title("Tempo de execucao de 5 iteracoes para " + experimentos[instancia][entrada]['nome'] + "\n em todas as instancias com diferentes numero de threads")
    plt.legend(loc='upper right')
    plt.savefig('graficos/'+entrada+'-timing.svg', format="svg")
    #plt.show()
    plt.clf()


#GRAFICO DO CUSTO BENEFGIFICIO
for entrada in entradaV:
    tempos = []
    i = 0
    for instancia,color in zip(experimentos,colors):
        tempo = np.inf
        for thread in experimentos[instancia][entrada]['pi']:
            if tempo >= experimentos[instancia][entrada]['pi'][thread]['tempo']:
                tempo = experimentos[instancia][entrada]['pi'][thread]['tempo']
                melhortempo = [thread,tempo, experimentos[instancia][entrada]['pi'][thread]['erro']]
        tempos.append(melhortempo)
        #plt.scatter( melhortempo[1]*dados[instancia]['preco'], melhortempo[1], color=color )
        #    plt.errorbar( experimentos[instancia][entrada]['pi'][thread]['tempo']*dados[instancia]['preco'], experimentos[instancia][entrada]['pi'][thread]['tempo'], experimentos[instancia][entrada]['pi'][thread]['erro'], experimentos[instancia][entrada]['pi'][thread]['erro']*dados[instancia]['preco'], label=instancia+'-'+thread+'-threads', color=colors[i], capsize=3, marker='.')
        plt.errorbar( melhortempo[1]*dados[instancia]['preco'], melhortempo[1], melhortempo[2], melhortempo[2]*dados[instancia]['preco'], label=instancia+'-'+melhortempo[0]+'-threads', color=color, capsize=3, marker='.')

        #plt.annotate( instancia+'-'+melhortempo[0]+'-threads', (melhortempo[1]*dados[instancia]['preco'], melhortempo[1]) )
    plt.xlabel('Custo (USD)')
    plt.ylabel('tempo(s)')
    #plt.title("Custo beneficio para " + experimentos[instancia][entrada]['nome'] + "\n para os melhores desempenhos de todas as instancias")
    plt.legend(loc='upper right')
    plt.savefig('graficos/'+entrada+'-custobeneficio.svg', format="svg")
    #plt.show()
    plt.clf()
    for instancia,color in zip(experimentos,colors):
        tempo = np.inf
        for thread in experimentos[instancia][entrada]['full']:
            if tempo >= experimentos[instancia][entrada]['full'][thread]['tempo']:
                tempo = experimentos[instancia][entrada]['full'][thread]['tempo']
                melhortempo = [thread,tempo, experimentos[instancia][entrada]['full'][thread]['erro']]
        tempos.append(melhortempo)
        #plt.scatter( melhortempo[1]*dados[instancia]['preco'], melhortempo[1], color=color )
        plt.errorbar( melhortempo[1]*dados[instancia]['preco'], melhortempo[1], melhortempo[2], melhortempo[2]*dados[instancia]['preco'], label=instancia+'-'+melhortempo[0]+'-threads', color=color, capsize=3, marker='.')
        #plt.annotate( instancia+'-'+melhortempo[0]+'-threads', (melhortempo[1]*dados[instancia]['preco'], melhortempo[1]) )
    plt.xlabel('Custo (USD)')
    plt.ylabel('tempo(s)')
    #plt.title("Custo beneficio para " + experimentos[instancia][entrada]['nome'] + "\n para os melhores desempenhos de todas as instancias")
    plt.legend(loc='upper right')
    plt.savefig('graficos/'+entrada+'-custobeneficio-full.svg', format="svg")
    #plt.show()
    plt.clf()
