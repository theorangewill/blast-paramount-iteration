#!/bin/bash

# GERANDO DBS A PARTIR DE DUAS SEQUENCIAS
DBMINI=entradas/human_genoma_mini
makeblastdb -in $DBMINI.fa -parse_seqids -dbtype nucl -out entradas/human_genoma_mini > saida.out
ENTRADA=entradas/Homo_sapiens.GRCh38.cds.all.fa

# RODAR OS EXPERIMENTOS
NUMEROCORES=$(nproc)
blastn -query $ENTRADA -db $DBMINI -out saida.out -max_target_seqs 5 -task blastn -num_threads $NUMEROCORES

