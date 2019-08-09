#!/bin/bash

# GERANDO DBS A PARTIR DE DUAS SEQUENCIAS
DBPEQUENO=entradas/human_genoma_pequeno
makeblastdb -in $DBPEQUENO.fa -parse_seqids -dbtype nucl -out entradas/human_genoma_pequeno > /dev/null
ENTRADA=entradas/Homo_sapiens.GRCh38.cds.all.fa

# RODAR OS EXPERIMENTOS
NUMEROCORES=$(nproc)
blastn -query $ENTRADA -db $DBPEQUENO -out /dev/null -max_target_seqs 5 -task blastn -num_threads $NUMEROCORES

