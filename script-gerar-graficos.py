#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
from numpy import inf

if len(sys.argv) == 1:
    print "ERRO: não há arquivo para leitura"
    print("\tpython script-gerar-graficos.py <nome arquivo>")
    exit()
maquinas = []
for maquina in sys.argv[1:]:
    arq = open(maquina, 'r')
    numerocores = arq.readline()
    linha = " "
    entradas = []
    while linha:
        linha = arq.readline().replace("\n","")
        if linha == "&":
            experimentos = []
            entrada = arq.readline().replace("\n","")[:-3]
        elif linha == "*":
            threads = arq.readline().replace("\n","")
            execucoes = []
            for exe in range(5):
                paramountiteration = int(arq.readline().replace("\n",""))
                iteracoes = [float(0.0)]*paramountiteration
                for pi in range(paramountiteration):
                    i = arq.readline().split(";")
                    iteracoes[pi] += float(i[1])
                execucoes.append(iteracoes)
            execucoes = ([(a+b+c+d+e)/5 for a, b, c, d, e in zip(execucoes[0], execucoes[1], execucoes[2], execucoes[3], execucoes[4])])
            experimentos.append([threads,sum(execucoes),execucoes])
            #iteracoes[:] = [float(i) / 5 for i in iteracoes]
        elif linha == "!":
            execucoes = []
            for exe in range(5):
                paramountiteration = int(arq.readline().replace("\n",""))
                iteracoes = [float(0.0)]*paramountiteration
                for pi in range(paramountiteration):
                    i = arq.readline().split(";")
                    iteracoes[pi] = float(i[1])
                execucoes.append(iteracoes)
            execucoes = ([(a+b+c+d+e)/5 for a, b, c, d, e in zip(execucoes[0], execucoes[1], execucoes[2], execucoes[3], execucoes[4])])
            experimentos.append(["final",sum(execucoes),execucoes])
            entradas.append([entrada[7:],experimentos])
        #a = raw_input();
    maquinas.append([maquina[:-4],entradas]);
    arq.close()

#maquinas - r5.24xlarge r5.12xlarge r5.4xlarge r5.2xlarge r5.xlarge r5.large
#         - entradas - refseq00 refseq01
#                    - experimentos - threads 2 4 8 16 32 64 48 96 (limite do numero de nucleos) final
#                                   - tempo total
#                                   - iteracoes - 1 2 3 4 5 , 1 ... 100
#maquinas [nome, [entrada, [threads [tempo total, [1, 2, 3, 4, 5, ... 100]]]]]
#maquinas[maquina][nome da maquina | entradas ][entrada][nome da entrada | experimentos][experimento][threads | tempo | iteracoes]

precos = [["r5.large", 0.126],
          ["r5.xlarge", 0.252],
          ["r5.2xlarge", 0.504],
          ["r5.4xlarge", 1.008],
          ["r5.12xlarge", 3.024],
          ["r5.24xlarge", 6.048]]
iteracoes = ['1', '2', '3', '4', '5']
colors = ['#e57914', '#1ca8ef', '#18ce64', '#ce18a9', '#d13714', '#aed114', '#f9bb7a', '#a55e13']
melhormaquina = []
for maquina in maquinas:
    melhorentrada = []
    for entrada in maquina[1]:
        plt.plot( maquina[1][0][1][-1][2], label="100 iteracoes", color=colors[0] )
        plt.plot( maquina[1][0][1][-2][2], label="5 iteracoes", color=colors[1] )
        plt.title("Execucao para " + entrada[0] + " na instancia " + maquina[0])
        plt.legend(loc='upper left')
        plt.xlabel('iteracoes')
        plt.ylabel('tempo(s)')
        plt.show()
        plt.savefig(maquina[0]+'-'+entrada[0]+'-pi100.png')


        melhortempo = inf
        for experimentos, color, it in zip(entrada[1][:-1],colors, iteracoes):
            if melhortempo > experimentos[1]:
                melhortempo = experimentos[1]
            plt.plot( iteracoes, experimentos[2], 'o-', color=color, label=experimentos[0] + " threads")
            for it in range(len(experimentos[2])):
                plt.annotate("{:.2f}".format(experimentos[2][it]), (iteracoes[it], experimentos[2][it]))
        plt.legend(loc='upper left')
        plt.xlabel('iteracoes')
        plt.ylabel('tempo(s)')
        plt.title("Execucao de 5 iteracoes para " + entrada[0] + "\n na instancia " + maquina[0] + " com diferentes numero de threads")
        plt.show()
        plt.savefig(maquina[0]+'-'+entrada[0]+'-pi5.png')
        precomaquina = 0.0
        for preco in precos:
            if maquina[0] == preco[0]:
                precomaquina = preco[1]
        melhorentrada.append([maquina[0], entrada[0], precomaquina, melhortempo])
    melhormaquina.append(melhorentrada)

for entrada in range(len(melhormaquina[0])):
    for maquina,color in zip(melhormaquina,colors):
        plt.scatter( maquina[entrada][2], maquina[entrada][3], color=color )
        plt.annotate( maquina[entrada][0], (maquina[entrada][2], maquina[entrada][3]) )
    plt.xlabel('custo(USD)')
    plt.ylabel('tempo(s)')
    plt.title("Custo-beneficio das instancias para " + melhormaquina[0][entrada][1])
    plt.show()
    plt.savefig(entrada[0]+'-cb.png')
