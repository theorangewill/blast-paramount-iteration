#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import pprint
import numpy as np
import scipy.stats
import os
import operator

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

pp = pprint.PrettyPrinter(indent=2)

instancias =  {'m5.2xlarge'  :  {'preco':0.384/3600},
          'm5a.2xlarge' :  {'preco':0.344/3600},
          'm4.2xlarge'  :  {'preco':0.400/3600},
          'c5.4xlarge'  :  {'preco':0.680/3600},
          'r5.xlarge'   :  {'preco':0.252/3600},
          'r5.2xlarge'  :  {'preco':0.504/3600},
          'r5.4xlarge'  :  {'preco':1.008/3600},
          'r5a.xlarge'  :  {'preco':0.226/3600},
          'r5a.2xlarge' :  {'preco':0.452/3600},
          'r4.xlarge'   :  {'preco':0.244/3600},
          'r4.2xlarge'  :  {'preco':0.532/3600},
          'x1e.2xlarge'  :  {'preco':1.668/3600}}

instanciaV = ('m5.2xlarge', 'm5a.2xlarge', 'm4.2xlarge', 'c5.4xlarge', 'r5.xlarge', 'r5.2xlarge', 'r5.4xlarge', 'r5a.xlarge', 'r5a.2xlarge', 'r4.xlarge', 'r4.2xlarge', 'x1e2.xlarge')
colors = ('#e57914', '#18ce64', '#1ca8ef', '#ce18a9', '#d13714', '#aed114', '#f9bb7a', '#a55e13',
            '#e3c712', '#85e312', '#3a21cc', '#cc23c4', '#36d9d1', '#a437de')

if len(sys.argv) == 1:
    print "ERRO: não há arquivo para leitura"
    print("\tpython script-gerar-graficos2.py <nome arquivo>")
    exit()
tempos1 = {}
tempos5 = {}
tempos10 = {}
temposfull = {}
custos1 = {}
custos5 = {}
custos10 = {}
custosfull = {}
for arquivo in sys.argv[1:]:
    arq = open(arquivo, 'r')
    nomearquivo = arquivo[9:-4]
    execucoesPI1 = []
    execucoesPI5 = []
    execucoesPI10 = []
    execucoesFULL = []
    while True:
        i = arq.readline().replace("\n","").split(";")
        execucoesFULL.append(float(i[1]))
        if int(i[0]) <= 1:
            execucoesPI1.append(float(i[1]))
        if int(i[0]) <= 5:
            execucoesPI5.append(float(i[1]))
        if int(i[0]) <= 10:
            execucoesPI10.append(float(i[1]))
        #print execucoesPI
        #print execucoesFULL
        if int(i[0]) == 400:
            break
    instancias[nomearquivo].update({'pi1' : execucoesPI1})
    tempos1.update({nomearquivo : float(sum(execucoesPI1))} )
    custos1.update({nomearquivo : float(sum(execucoesPI1))*instancias[nomearquivo]['preco']} )
    instancias[nomearquivo].update({'tempo1' : float(sum(execucoesPI1))})

    instancias[nomearquivo].update({'pi5' : execucoesPI5})
    tempos5.update({nomearquivo : float(sum(execucoesPI5))} )
    custos5.update({nomearquivo : float(sum(execucoesPI5))*instancias[nomearquivo]['preco']} )
    instancias[nomearquivo].update({'tempo5' : float(sum(execucoesPI5))})

    instancias[nomearquivo].update({'pi10' : execucoesPI10})
    tempos10.update({nomearquivo : float(sum(execucoesPI10))} )
    custos10.update({nomearquivo : float(sum(execucoesPI10))*instancias[nomearquivo]['preco']} )
    instancias[nomearquivo].update({'tempo10' : float(sum(execucoesPI10))})

    instancias[nomearquivo].update({'full':execucoesFULL})
    temposfull.update({nomearquivo : float(sum(execucoesFULL))} )
    custosfull.update({nomearquivo : float(sum(execucoesFULL))*instancias[nomearquivo]['preco']} )
    instancias[nomearquivo].update({'tempofull' : float(sum(execucoesFULL))})
    arq.close()


ordenado = sorted(temposfull.items(), key=operator.itemgetter(1))
for instancia,color,i in zip(ordenado,colors,range(len(instancias))):
    if i%3 != 0:
        continue
    if 'full' in instancias[instancia[0]]:
        plt.plot(instancias[instancia[0]]['full'], '-', label=str(instancia[0]))#, color=color)
plt.xlabel('iteracoes')
plt.ylabel('tempo(s)')
#plt.title("Tempo de execucao de 400 iteracoes para as diversas instancias")
plt.legend(loc='upper left')
plt.savefig('graficos/execucaototal.svg', format="svg")
plt.show()

overhead1 = []
overhead5 = []
overhead10 = []
overheadfull = []
ordenado1 = sorted(tempos1.items(), key=operator.itemgetter(1))
for tempo in ordenado1:
    overhead1.append(tempo[1] / ordenado1[0][1])
ordenado5 = sorted(tempos5.items(), key=operator.itemgetter(1))
for tempo in ordenado5:
    overhead5.append(tempo[1] / ordenado5[0][1])
ordenado10 = sorted(tempos10.items(), key=operator.itemgetter(1))
for tempo in ordenado10:
    overhead10.append(tempo[1] / ordenado10[0][1])
ordenado = sorted(temposfull.items(), key=operator.itemgetter(1))
for tempo in ordenado:
    overheadfull.append(tempo[1] / ordenado[0][1])

pp.pprint(ordenado1)
pp.pprint(overhead1)
pp.pprint(ordenado5)
pp.pprint(overhead5)
pp.pprint(ordenado10)
pp.pprint(overhead10)
pp.pprint(ordenado)
pp.pprint(overheadfull)
tabela = []
for o in range(len(ordenado)):
    linha = [ordenado[o][0]]
    for i in range(len(ordenado1)):
        if ordenado[o][0] == ordenado1[i][0]:
            linha.append(overhead1[i])
            break
    for i in range(len(ordenado5)):
        if ordenado[o][0] == ordenado5[i][0]:
            linha.append(overhead5[i])
            break
    for i in range(len(ordenado10)):
        if ordenado[o][0] == ordenado10[i][0]:
            linha.append(overhead10[i])
            break
    linha.append(overheadfull[o])
    tabela.append(linha)
#pp.pprint(tabela)

for linha in tabela:
    print("\t\t\\texttt{" + str(linha[0]) + "} & $" + str("{0:.2f}".format(round(linha[1],2))) + "$ & $" + str("{0:.2f}".format(round(linha[2],2))) + "$ & $" + str("{0:.2f}".format(round(linha[3],2))) + "$ & $" + str("{0:.2f}".format(round(linha[4],2))) + "$\\\\\\hline" )


overhead1 = []
overhead5 = []
overhead10 = []
overheadfull = []
ordenadocusto1 = sorted(custos1.items(), key=operator.itemgetter(1))
for custo in ordenadocusto1:
    overhead1.append(custo[1] / ordenadocusto1[0][1])
ordenadocusto5 = sorted(custos5.items(), key=operator.itemgetter(1))
for custo in ordenadocusto5:
    overhead5.append(custo[1] / ordenadocusto5[0][1])
ordenadocusto10 = sorted(custos10.items(), key=operator.itemgetter(1))
for custo in ordenadocusto10:
    overhead10.append(custo[1] / ordenadocusto10[0][1])
ordenadocusto = sorted(custosfull.items(), key=operator.itemgetter(1))
for custo in ordenadocusto:
    overheadfull.append(custo[1] / ordenadocusto[0][1])

pp.pprint(ordenadocusto1)
pp.pprint(overhead1)
pp.pprint(ordenadocusto5)
pp.pprint(overhead5)
pp.pprint(ordenadocusto10)
pp.pprint(overhead10)
pp.pprint(ordenadocusto)
pp.pprint(overheadfull)
tabela = []
for o in range(len(ordenadocusto)):
    linha = [ordenadocusto[o][0]]
    for i in range(len(ordenadocusto1)):
        if ordenadocusto[o][0] == ordenadocusto1[i][0]:
            linha.append(overhead1[i])
            break
    for i in range(len(ordenadocusto5)):
        if ordenadocusto[o][0] == ordenadocusto5[i][0]:
            linha.append(overhead5[i])
            break
    for i in range(len(ordenadocusto10)):
        if ordenadocusto[o][0] == ordenadocusto10[i][0]:
            linha.append(overhead10[i])
            break
    linha.append(overheadfull[o])
    tabela.append(linha)
#pp.pprint(tabela)

for linha in tabela:
    print("\t\t\\texttt{" + str(linha[0]) + "} & $" + str("{0:.2f}".format(round(linha[1],2))) + "$ & $" + str("{0:.2f}".format(round(linha[2],2))) + "$ & $" + str("{0:.2f}".format(round(linha[3],2))) + "$ & $" + str("{0:.2f}".format(round(linha[4],2))) + "$\\\\\\hline" )


for o in range(len(ordenadocusto)):
    for t in ordenado:
        if ordenadocusto[o][0] == t[0]:
            tempo = t[1]
            break
    plt.scatter(ordenadocusto[o][1], tempo, label= ordenadocusto[o][0])
    #    plt.errorbar( experimentos[instancia][entrada]['pi'][thread]['tempo']*dados[instancia]['preco'], experimentos[instancia][entrada]['pi'][thread]['tempo'], experimentos[instancia][entrada]['pi'][thread]['erro'], experimentos[instancia][entrada]['pi'][thread]['erro']*dados[instancia]['preco'], label=instancia+'-'+thread+'-threads', color=colors[i], capsize=3, marker='.')
    #plt.errorbar( melhortempo[1]*dados[instancia]['preco'], melhortempo[1], melhortempo[2], melhortempo[2]*dados[instancia]['preco'], label=instancia+'-'+melhortempo[0]+'-threads', color=color, capsize=3, marker='.')

    #plt.annotate( instancia+'-'+melhortempo[0]+'-threads', (melhortempo[1]*dados[instancia]['preco'], melhortempo[1]) )
plt.xlabel('Custo (USD)')
plt.ylabel('tempo(s)')
#plt.title("Custo beneficio")
plt.legend(loc='upper right')
plt.savefig('graficos/custobeneficio.svg', format="svg")
plt.show()
plt.clf()
