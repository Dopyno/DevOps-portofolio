#!/bin/bash

rm -rf workspace

GREEN='\033[0;32m'
NC='\033[0m' # No Color


log(){
	printf "${GREEN}$(date) - $1${NC}\n"
}

root="workspace"
repo=https://github.com/VBota1/FastDemoRestApi.git

log "mkdir $root"
#create the directory
mkdir $root

##clone the repository
if git clone ${repo} $root
then
	log "log successfuly clone ${repo}"
else 
	log "Fail to clone"
	exit 2
fi	

log "cd $root"
#create the directory
###access the workspace
cd $root

####create the enviroment
python3 -m venv venv
source venv/bin/activate

log "pip install -r requirements.txt"
##### Install dependencies
pip install -r requirements.txt

#### Run and test
log "pytest"
pytest

log "deactivate"
deactivate

cd ..

log "rm -rf workspace"
rm -rf workspace
