#!/bin/bash
# Download the career matches and the player info of one player.
# Usage: bash scripts/download_data.sh SerenaWilliams

PLAYER=${1:-SerenaWilliams}

mkdir -p data
curl -s -o data/${PLAYER}Career.js https://www.tennisabstract.com/jsmatches/${PLAYER}Career.js
curl -s -o data/${PLAYER}.js https://www.tennisabstract.com/jsmatches/${PLAYER}.js
