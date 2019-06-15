#!/bin/bash

# GERANDO ENTRADAS A PARTIR DE DUAS BASES DE DADO
ENTRADA0=refseq/entrada00.fa
ENTRADA1=refseq/entrada01.fa
blastdbcmd -db refseq/refseq_rna.00 -entry all -out $ENTRADA0
blastdbcmd -db refseq/refseq_rna.01 -entry all -out $ENTRADA1

# RODAR OS EXPERIMENTOS
NUMEROCORES=2
NUMEROCORES=$(nproc)
echo $NUMEROCORES

k=0
for j in $ENTRADA0 $ENTRADA1
do
echo "&"
echo $ENTRADA0

for ((THREADS=2; THREADS <= $NUMEROCORES ; THREADS*=2))
do
echo "*"
	echo $THREADS
	for i in {1..5}
	do
		blastnpi -query $j -db refseq/refseq_rna.0$k -out ${j:0:9}-saida_$THREADS_$i.out -max_target_seqs 5 -task blastn -num_threads $THREADS
	done
done

if [ $NUMEROCORES -ge 48 ]; then
	echo "*"
	echo $NUMEROCORES
	for i in {1..5}
	do
		blastnpi -query $j -db refseq/refseq_rna.0$k -out ${j:0:9}-saida_$THREADS_$i.out -max_target_seqs 5 -task blastn -num_threads $THREADS
	done
fi
	echo "!"
	for i in {1..5}
	do
		blastn -query $j -db refseq/refseq_rna.0$k -out ${j:0:9}-saida_final_$i.out -max_target_seqs 5 -task blastn -num_threads $NUMEROCORES
	done
	k=$(($k+1))
done
