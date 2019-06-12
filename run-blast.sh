#!/bin/bash

# GERANDO ENTRADAS A PARTIR DE DUAS BASES DE DADO
echo "GERANDO ENTRADAS"
cd blast-paramount-iteration/refseq
ENTRADA0=entrada00.fa
ENTRADA1=entrada01.fa
blastdbcmd -db refseq_rna.00 -entry all -out entrada00.fa
echo "		" $ENTRADA0 " CRIADA"
blastdbcmd -db refseq_rna.01 -entry all -out entrada01.fa
echo "		" $ENTRADA1 " CRIADA"

# RODAR OS EXPERIMENTOS

cd ..

NUMEROCORES=2
NUMEROCORES=$(nproc)

echo "NUMERO DE CORES: " $NUMEROCORES

echo "RODAR ALGORITMO"

for j in {$ENTRADA0,$ENTRADA1}
do
echo "	EXPERIMENTO COM " $j

for ((THREADS=2; THREADS <= $NUMEROCORES ; THREADS*=2))
do
	echo "		EXPERIMENTO COM " $THREADS " THREADS"
	echo "*"
	for i in {1..5}
	do
		blastn -query ref_seq/entrada00.fa -db ref_seq/refseq_rna.00 -out ${j:0:9}-saida_$THREADS_$i.out -max_target_seqs 2 -task blastn -num_threads $threads
	done
	echo "*"
done

if [ $NUMEROCORES -ge 48 ]; then
	echo "		EXPERIMENTO COM " $NUMEROCORES " THREADS"
	echo "*"
	for i in {1..5}
	do	
		blastn -query ref_seq/entrada00.fa -db ref_seq/refseq_rna.00 -out ${j:0:9}-saida_$THREADS_$i.out -max_target_seqs 2 -task blastn -num_threads $threads
	done
	echo "*"
fi

	cd c++
	make -j PARAMOUNTITERATION=0
	make install
	cd ..
	/usr/bin/time -p blastn -query ref_seq/entrada00.fa -db ref_seq/refseq_rna.00 -out ${j:0:9}-saida_final.out -max_target_seqs 2 -task blastn -num_threads $NUMEROCORES
done




