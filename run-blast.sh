#!/bin/bash

# GERANDO ENTRADAS A PARTIR DE DUAS BASES DE DADO
echo "GERANDO ENTRADAS"
ENTRADA0=refseq/entrada00.fa
ENTRADA1=refseq/entrada01.fa
blastdbcmd -db refseq/refseq_rna.00 -entry all -out $ENTRADA0
echo "		" $ENTRADA0 " CRIADA"
blastdbcmd -db refseq/refseq_rna.01 -entry all -out $ENTRADA1
echo "		" $ENTRADA1 " CRIADA"

# RODAR OS EXPERIMENTOS



NUMEROCORES=2
NUMEROCORES=$(nproc)

echo "NUMERO DE CORES: " $NUMEROCORES

echo "RODAR ALGORITMO"
k=0
for j in $ENTRADA0 $ENTRADA1
do
echo "	EXPERIMENTO COM " $j

for ((THREADS=2; THREADS <= $NUMEROCORES ; THREADS*=2))
do
	echo "		EXPERIMENTO COM " $THREADS " THREADS"
	echo "*"
	for i in {1..5}
	do
		blastn -query $j -db refseq/refseq_rna.0$k -out ${j:0:9}-saida_$THREADS_$i.out -max_target_seqs 5 -task blastn -num_threads $THREADS
	done
	echo "*"
done

if [ $NUMEROCORES -ge 48 ]; then
	echo "		EXPERIMENTO COM " $NUMEROCORES " THREADS"
	echo "*"
	for i in {1..5}
	do	
		blastn -query $j -db refseq/refseq_rna.0$k -out ${j:0:9}-saida_$THREADS_$i.out -max_target_seqs 5 -task blastn -num_threads $THREADS
	done
	echo "*"
fi

	make -j PARAMOUNTITERATION=0
	make install
	cd ..
	/usr/bin/time -p blastn -query $j -db refseq/refseq_rna.0$k -out ${j:0:9}-saida_final.out -max_target_seqs 5 -task blastn -num_threads $NUMEROCORES
	k=k+1
done




