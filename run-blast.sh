#!/bin/bash

# GERANDO DBS A PARTIR DE DUAS SEQUENCIAS
DBPEQUENO=entradas/human_genoma_pequeno
DBGRANDE=entradas/human_genoma_grande
makeblastdb -in $DBPEQUENO.fa -parse_seqids -dbtype nucl -out entradas/human_genoma_pequeno > saida.out
makeblastdb -in $DBGRANDE.fa -parse_seqids -dbtype nucl -out entradas/human_genoma_grande > saida.out
ENTRADA=entradas/Homo_sapiens.GRCh38.cds.all.fa

# RODAR OS EXPERIMENTOS
NUMEROCORES=2
NUMEROCORES=$(nproc)
echo $NUMEROCORES

for j in $DBPEQUENO $DBGRANDE
do
echo "&"
echo $j

for ((THREADS=2; THREADS <= $NUMEROCORES ; THREADS*=2))
do
echo "*"
	echo $THREADS
	for i in {1..5}
	do
		blastnpi -query $ENTRADA -db $j -out saida.out -max_target_seqs 5 -task blastn -num_threads $THREADS
		echo "-"
		blastn -query $ENTRADA -db $j -out saida.out -max_target_seqs 5 -task blastn -num_threads $THREADS
	done
done

if [ $NUMEROCORES -ge 48 ]; then
	echo "*"
	echo $NUMEROCORES
	for i in {1..5}
	do
		blastnpi -query $ENTRADA -db $j -out saida.out -max_target_seqs 5 -task blastn -num_threads $THREADS
		echo "-"
		blastn -query $ENTRADA -db $j -out saida.out -max_target_seqs 5 -task blastn -num_threads $THREADS
	done
fi
done
