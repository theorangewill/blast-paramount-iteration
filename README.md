# BLAST 
BLAST (Basic Local Alignment Search Tool) é um algoritmo capaz de encontrar regiões com similaridade local para sequências biológicas. Para isso, ele compara sequências nucleotídicas ou proteicas para identificar semelhanças em diferentes databases e calcular a significância estatística dos matches encontrados. Pode ser usado para encontrar relações evolutivas entre sequências, assim como ajudar a identificar membros de famílias genéticas. A NCBI fornece acesso a um conjunto de programas BLAST, por exemplo blastn, que trabalha com sequências de DNA. A aplicação pode ser encontrada nos arquivos da NCBI e é paralelizada usando multithreading.
## Trabalho
Neste respositório há o código da aplicação blastn modificado para realizar o paramount iteration.
Na compilação é possível indicar o número de iterações a serem realizadas pela técnica com a definição da variável global PARAMOUNTITERATION (se 0, então irá executar até o fim).
    
    make -j PARAMOUNTITERATION=5

Aqui há quatro scripts e uma receita para o Singularity criar uma imagem de container.

    - singularity-install.sh é responsável por instalar o Singularity e seus pré-requisitos, criar a imagem e baixar as bases de dados refseq\_rna.00 e refseq\_rna.01.
    
    - blast-recipe é a receita da imagem, onde é instalada as requisições para o BLAST e a também a própria ferramenta com PARAMOUNTITERATION=5 e PARAMOUNTITERATION=50
    
    - run-blast.sh executa os experimentos, variando o número de threads. Cada execução é realizada 5 vezes.
    
    - script-gerar-graficos.py gera gráficos e outros dados a fim de analisar resultados.
    
    - auto script.sh foi utilizado para realizar os experimentos de forma automatizada, desligando a instância ao fim do experimento.
    
## Receita
A receita desenvolvida compila duas versões do blastn. Uma com PARAMOUNTITERATION=5 (blastnpi) e outra com PARAMOUNTITERATION=50 (blastn)

## Script de Execução
O script varia o número de threads em potência de dois até o limite de núcleos presentes na máquina. Para as máquinas que possuem número de núcleos superior a 48, é executado também para o número de threads igual ao de núcleos. Cada execução é realizada cinco vezes. 

## Script de Geração de Gráficos
O script recebe todos os arquivos de saída do script de execução e constrói diversos gráficos. Um comparando a execução de 100 iterações com 5 iterações, outro comparando a execução de 5 iteraçes com diferentes números de threads e outro comparando o custo benefício entre as máquinas.

# Rodando os experimentos
É recomendado executar os experimentos em um ambiente com armazenamento mínimo de 30GB. Deve-se realizar os experimentos no sistema operacional Ubuntu 18.04.

Para cada ambiente computacional deve-se clonar este repositório e executar:

    ./singularity-install.sh
    sudo singularity exec blast-imagem.img ./run-blast.sh > saida.out
    python script-gerar-graficos.py saida.out saida2.out saida3.out
