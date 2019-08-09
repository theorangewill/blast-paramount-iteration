#!/bin/bash

#INSTALAR SINGULARITY
echo "INSTALANDO DEPENDENCIAS"
DIRETORIO=$(pwd)
sudo DEBIAN_FRONTEND=noninteractive apt-get update -qy && \
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -qy build-essential \
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
cd ${DIRETORIO}

#CRIAR IMAGEM A PARTIR DA RECIPE
echo "CRIANDO IMAGEM"
tar xf ncbi-blast-2.9.0+-src.tar.xz
sudo singularity build blast-imagem.img blast-recipe2.def

#BAIXANDO BASES DE DADOS
echo "BAIXANDO BASES DE DADOS"
mkdir entradas
cd entradas
wget ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.1.fa.gz
wget ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.2.fa.gz
wget ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.3.fa.gz
wget ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.4.fa.gz
wget ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.5.fa.gz
wget ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.6.fa.gz
wget ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.7.fa.gz
gunzip *.gz
cat Homo_sapiens.GRCh38.dna.chromosome.1.fa >> human_genoma_pequeno.fa
cat Homo_sapiens.GRCh38.dna.chromosome.2.fa >> human_genoma_pequeno.fa
cat Homo_sapiens.GRCh38.dna.chromosome.3.fa >> human_genoma_pequeno.fa
cat Homo_sapiens.GRCh38.dna.chromosome.4.fa >> human_genoma_pequeno.fa
cat Homo_sapiens.GRCh38.dna.chromosome.5.fa >> human_genoma_pequeno.fa
cat Homo_sapiens.GRCh38.dna.chromosome.6.fa >> human_genoma_pequeno.fa
cat Homo_sapiens.GRCh38.dna.chromosome.7.fa >> human_genoma_pequeno.fa
wget ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/cds/Homo_sapiens.GRCh38.cds.all.fa.gz
gunzip Homo_sapiens.GRCh38.cds.all.fa.gz
rm *chromosome*
cd ..
