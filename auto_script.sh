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

sudo ./singularity-install.sh
