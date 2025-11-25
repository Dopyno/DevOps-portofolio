#!/bin/bash

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No color

log(){
    printf "${GREEN}$(date '+%Y-%m-%d %H:%M:%S') - $1${NC}\n"
}

error(){
    printf "${RED}ERROR: $1${NC}\n"
}

root="workspace"
repo="https://github.com/VBota1/FastDemoRestApi.git"

cleanup(){
    log "Cleaning up workspace..."
    rm -rf "$root"
}

#remove everything if in case the execution fail
trap cleanup EXIT #trap - run the function with or without error

log "Checking dependencies..."
command -v git >/dev/null 2>&1 || { error "git not installed"; exit 1; }
command -v python3 >/dev/null 2>&1 || { error "python3 not installed"; exit 1; }

log "Creating workspace: $root"
mkdir -p "$root"

log "Cloning repo: $repo"
git clone "$repo" "$root"

pushd "$root" >/dev/null

log "Creating virtual enviroment..."
python3 -m venv venv
source venv/bin/activate

log "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

log "Runnig tests..."
pytest --maxfail=1 --disable-warnings -q

log "Deactivating env..."
deactivate

popd >/dev/null

log "Pipeline finished sucessfuly"
