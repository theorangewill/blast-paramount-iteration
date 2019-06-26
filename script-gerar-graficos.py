#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import pprint
from numpy import inf


experimentos = {}
dados =  {'r5.xlarge' : {'cost':0.252},
          'r5.2xlarge' : {'cost':0.504},
          'r5.4xlarge' : {'cost':1.008},
          'r5.12xlarge' : {'cost':3.024},
          'r5.24xlarge' : {'cost':6.048}}
instanciaV = ('r5.xlarge', 'r5.2xlarge', 'r5.4xlarge', 'r5.12xlarge', 'r5.24xlarge')
entradaV = ('pequeno', 'grande')
threadV = ('2', '4', '8', '16', '32', '48', '64', '96')
tamanhoV = ('pi', 'full')

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
            experimentos[nomearquivo][entrada]['pi'][threads] = {'n':threads, 'tempo':float(sum(execucoesPI)), 'iteracoes':execucoesPI}
            execucoesFULL = ([(a+b+c+d+e)/5 for a, b, c, d, e in zip(execucoesFULL[0], execucoesFULL[1], execucoesFULL[2], execucoesFULL[3], execucoesFULL[4])])
            experimentosFULL.append([threads,sum(execucoesFULL),execucoesFULL])
            experimentos[nomearquivo][entrada]['full'][threads] = {'n':threads, 'tempo':float(sum(execucoesFULL)), 'iteracoes':execucoesFULL}
    arq.close()

pp.pprint(experimentos)

colors = ('#e57914', '#18ce64', '#1ca8ef', '#ce18a9', '#d13714', '#aed114', '#f9bb7a', '#a55e13')


#GRAFICO DE VALIDACAO DO PARAMOUNT ITERATION EM UMA INSTANCIA E ENTRADA PARA DIFERENTES THREADS
#for instancia in experimentos:
#    for entrada in experimentos[instancia]:
#        for thread,color in zip(experimentos[instancia][entrada]['full'],colors):
#            plt.plot(experimentos[instancia][entrada]['full'][thread]['iteracoes'], '-', label=str(thread)+" threads" , color=color)
#        plt.xlabel('iteracoes')
#        plt.ylabel('tempo(s)')
#        plt.title("Tempo de execucao de 50 iteracoes para " + experimentos[instancia][entrada]['nome'] + "\n na instancia " + instancia + " com diferentes numero de threads")
#        plt.legend(loc='upper left')
#        plt.show()
#        plt.savefig(instancia+'-'+entrada+'-pi5.png')

for entrada in entradaV:
    for thread in threadV:
        for instancia in experimentos:
            if int(thread) <= dados[instancia]['numerocores']:
            print type(thread)

exit(1)
for instancia in instancias:
    for entrada in instancia[1]:
        for experimentoTOTAL,color in zip(entrada[2],colors):
            print ""#plt.plot(experimentoTOTAL[2], 'o-', label=str(experimentoTOTAL[0])+" threads" , color=color)
        #plt.xlabel('iteracoes')
        #plt.ylabel('tempo(s)')
        #plt.title("Tempo de execucao de 50 iteracoes para " + entrada[0] + "\n na instancia " + instancia[0] + " com diferentes numero de threads")
        #plt.legend(loc='upper left')
        #plt.show()
        #plt.savefig(maquina[0]+'-'+entrada[0]+'-pi5.png')

melhormaquina = []
threads = [2,4,8,16,32,48,64,96]
#GRAFICO DE VALIDACAO DO PARAMOUNT ITERATION EM UMA THREAD E ENTRADA PARA DIFERENTES INSTANCIAS
for thread in [2,4,8,16,32,48,64,96]:
    for i in range(len(instancias[1])):
        #print instancias[i][1][0]
        for j in range(len(instancias[i][1])):
            for k in range(len(instancias[i][1][j][1])):
                if int(instancias[i][1][j][1][k][0]) == thread:
                    print instancias[i][1][j][1][k]
            #print instancias[i][1]
            #print instancias[i][1][j]
            #print instancias[i][1][j][0]
                    entr = [entrada[2] for entrada in instancias[i][1][j][1]]

            print entr
            print "*"
    print ""
    print ""
        #print entr;

exit();


for maquina in maquinas:
    melhorentrada = []
    for entrada in maquina[1]:
        melhortempo = inf
        execucaotempo = []
        execucaothreads = []
        for experimentos, color, it in zip(entrada[1][:-1],colors, iteracoes):
            if melhortempo > experimentos[1]:
                melhortempo = experimentos[1]
            execucaotempo.append(experimentos[1])
            execucaothreads.append(experimentos[0])
        plt.plot(execucaothreads, execucaotempo, 'o-', color=colors[0])
            #plt.plot( iteracoes, experimentos[2], 'o-', color=color, label=experimentos[0] + " threads")
        for it in range(len(execucaotempo)):
            plt.annotate("{:.2f}".format(execucaotempo[it]), (execucaothreads[it], execucaotempo[it]))
        plt.xlabel('numero de threads')
        plt.ylabel('tempo(s)')
        plt.title("Tempo de execucao de 5 iteracoes para " + entrada[0] + "\n na instancia " + maquina[0] + " com diferentes numero de threads")
        plt.show()
        plt.savefig(maquina[0]+'-'+entrada[0]+'-pi5.png')
        print(maquina[0]+'-'+entrada[0]+'-pi5.png')
        precomaquina = 0.0
        for preco in precos:
            if maquina[0] == preco[0]:
                precomaquina = preco[1]
        melhorentrada.append([maquina[0], entrada[0], precomaquina*melhortempo, melhortempo])
    melhormaquina.append(melhorentrada)

for entrada in range(len(melhormaquina[0])):
    for maquina,color in zip(melhormaquina,colors):
        plt.scatter( maquina[entrada][2], maquina[entrada][3], color=color )
        plt.annotate( maquina[entrada][0], (maquina[entrada][2], maquina[entrada][3]) )
    plt.xlabel('custo(USD)')
    plt.ylabel('tempo(s)')
    plt.title("Custo-beneficio das instancias para " + maquinas[1][1][entrada][0])
    plt.show()
    plt.savefig(maquinas[1][entrada][0][0]+'-cb.png')
    print(maquinas[1][1][entrada][0]+'-cb.png')
    for maquina,color in zip(maquinas,colors):
        plt.plot( maquina[1][entrada][1][-1][2], label=maquina[0], color=color )
    plt.title("Tempo de execucao de 100 iteracoes para " + maquinas[1][1][entrada][0])
    plt.legend(loc='upper left')
    plt.xlabel('iteracoes')
    plt.ylabel('tempo(s)')
    plt.show()
    plt.savefig(maquinas[1][1][entrada][0]+'-pi100.png')
    print(maquinas[1][1][entrada][0]+'-pi100.png')
