#!/bin/bash

#INSTALAR SINGULARITY
echo "INSTALANDO DEPENDENCIAS"
sudo apt-get update && \
  sudo apt-get install -y build-essential \
  libssl-dev uuid-dev libgpgme11-dev libseccomp-dev pkg-config squashfs-tools

echo "INSTALANDO GOLANG"
VERSION=1.11.4
OS=linux
ARCH=amd64
export GOPATH=${HOME}/go >> ~/.bashrc
export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin >> ~/.bashrc
source ~/.bashrc
wget -O /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz https://dl.google.com/go/go${VERSION}.${OS}-${ARCH}.tar.gz && \
sudo tar -C /usr/local -xzf /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz
curl -sfL https://install.goreleaser.com/github.com/golangci/golangci-lint.sh |
  sh -s -- -b $(go env GOPATH)/bin v1.15.0

echo "INSTALANDO SINGULARITY"
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

#CRIAR IMAGEM A PARTIR DA RECIPE
echo "CRIANDO IMAGEM"
tar xf ncbi-blast-2.9.0+-src.tar.xz
sudo singularity build --sandbox blast-imagem.img blast-recipe.def

#BAIXANDO BASES DE DADOS
echo "BAIXANDO BASES DE DADOS"
mkdir refseq
cd refseq
wget https://ftp.ncbi.nlm.nih.gov/blast/db/refseq_rna.00.tar.gz
tar xf refseq_rna.00.tar.gz
rm refseq_rna.00.tar.gz
wget https://ftp.ncbi.nlm.nih.gov/blast/db/refseq_rna.01.tar.gz
tar xf refseq_rna.01.tar.gz
rm refseq_rna.01.tar.gz
cd ..

