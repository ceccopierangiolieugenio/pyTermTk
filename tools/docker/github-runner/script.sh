#!/bin/bash

echo "First input: $1"
echo "Second input: $2"

./config.sh \
    --url https://github.com/ceccopierangiolieugenio/pyTermTk \
    --work _work --replace \
    --runnergroup Default \
    --labels "self-hosted,Linux,ARM64" \
    --name $2 --token $1

./run.sh