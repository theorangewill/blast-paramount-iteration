#!/bin/bash

# GERANDO DBS A PARTIR DE DUAS SEQUENCIAS
DBPEQUENO=entradas/human_genoma_pequeno
DBGRANDE=entradas/human_genoma_grande
makeblastdb -in $DBPEQUENO.fa -parse_seqids -dbtype nucl -out human_genoma_pequeno
makeblastdb -in $DBGRANDE.fa -parse_seqids -dbtype nucl -out human_genoma_grande
ENTRADA=Homo_sapiens.GRCh38.cds.all.fa.gz

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
		blastnpi -query $ENTRADA -db $j -out ${j:0:9}-saida_$THREADS_$i.out -max_target_seqs 5 -task blastn -num_threads $THREADS
	done
done

if [ $NUMEROCORES -ge 48 ]; then
	echo "*"
	echo $NUMEROCORES
	for i in {1..5}
	do
		blastnpi -query $ENTRADA -db $j -out ${j:0:9}-saida_$THREADS_$i.out -max_target_seqs 5 -task blastn -num_threads $THREADS
	done
fi
	echo "!"
	for i in {1..5}
	do
		blastn -query $ENTRADA -db $j -out ${j:0:9}-saida_final_$i.out -max_target_seqs 5 -task blastn -num_threads $NUMEROCORES
	done
done
