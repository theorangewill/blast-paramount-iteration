#!/bin/bash
sudo snap install aws-cli --classic
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=AKIATSRODRVJY66I4A36
if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
	echo "Insira AWS secret key"
	read akey
	export AWS_SECRET_ACCESS_KEY=$akey
fi
export IID=$(curl http://169.254.169.254/latest/meta-data/instance-id)
git config --global credential.helper 'cache --timeout=86400'
git push

mkdir results
TYPE=$(curl http://169.254.169.254/latest/meta-data/instance-type)
FILE=results/$TYPE.txt
sudo ./singularity-install.sh
sudo singularity shell blast-imagem.img
./run-blast.sh > $FILE
git pull
git add $FILE
git commit -m "$TYPE"
git push && aws ec2 terminate-instances --instance-ids $IID
