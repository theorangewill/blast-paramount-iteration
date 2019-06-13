# BLAST 
BLAST (Basic Local Alignment Search Tool) é um algoritmo capaz de encontrar regiões com similaridade local para sequências biológicas. Para isso, ele compara sequências nucleotídicas ou proteicas para identificar semelhanças em diferentes databases e calcular a significância estatística dos matches encontrados. Pode ser usado para encontrar relações evolutivas entre sequências, assim como ajudar a identificar membros de famílias genéticas. A NCBI fornece acesso a um conjunto de programas BLAST, por exemplo blastn, que trabalha com sequências de DNA. A aplicação pode ser encontrada nos arquivos da NCBI e é paralelizada usando multithreading.
## Trabalho
Neste respositório há o código da aplicação blastn modificado para realizar o paramount iteration.
Na compilação é possível indicar o número de iterações a serem realizadas pela técnica com a definição da variável global PARAMOUNTITERATION.
    
    make -j PARAMOUNTITERATION=5

Aqui há dois scripts e uma receita para o Singularity criar uma imagem de container.
    - singularity-install.sh é responsável por instalar o Singularity e seus pré-requisitos, criar a imagem e baixar as bases de dados refseq\_rna.00 e refseq\_rna.01.
    - blast-recipe é a receita da imagem, onde é instalada as requisições para o BLAST e a também a própria ferramenta com PARAMOUNTITERATION=5
    - run-blast.sh executa os experimentos, variando o número de threads. Cada execução é realizada 5 vezes.
    
# Rodando os experimentos
É recomendado executar os experimentos em um ambiente com armazenamento mínimo de 16GB. Deve-se realizar os experimentos no sistema operacional Ubuntu 18.04.

Para cada ambiente computacional XX, deve-se clonar este repositório e executar os comandos seguintes.

##Instalando Singularity

    sudo apt-get update && \
      sudo apt-get install -y build-essential \
      libssl-dev uuid-dev libgpgme11-dev libseccomp-dev pkg-config squashfs-tools

    export VERSION=1.11.4 OS=linux ARCH=amd64
      wget -O /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz https://dl.google.com/go/go${VERSION}.${OS}-${ARCH}.tar.gz && \
      sudo tar -C /usr/local -xzf /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz
    echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
      echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
      source ~/.bashrc
    curl -sfL https://install.goreleaser.com/github.com/golangci/golangci-lint.sh |
      sh -s -- -b $(go env GOPATH)/bin v1.15.0
    
    mkdir -p ${GOPATH}/src/github.com/sylabs && \
       cd ${GOPATH}/src/github.com/sylabs && \
       git clone https://github.com/sylabs/singularity.git && \
       cd singularity
    git checkout v3.2.1
    cd ${GOPATH}/src/github.com/sylabs/singularity && \
       ./mconfig && \
       cd ./builddir && \
       make && \
       sudo make install
    singularity version
    cd ~/blast-paramount-iteration


##Criando a Imagem 
    tar xf ncbi-blast-2.9.0+-src.tar.xz
    sudo singularity build --sandbox blast-imagem.img blast-recipe.def

##Baixando arquivos de entrada
    mkdir refseq
    cd refseq
    wget https://ftp.ncbi.nlm.nih.gov/blast/db/refseq_rna.00.tar.gz
    tar xf refseq_rna.00.tar.gz
    rm refseq_rna.00.tar.gz
    wget https://ftp.ncbi.nlm.nih.gov/blast/db/refseq_rna.01.tar.gz
    tar xf refseq_rna.01.tar.gz
    rm refseq_rna.01.tar.gz
    cd ..

##Executando o script
    sudo singularity shell blast-imagem.img 
    ./run-blast.sh > run-blast.XX.out
    
    
    
    
    
    
