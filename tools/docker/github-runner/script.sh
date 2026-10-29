#!/bin/bash

token=$1
name_prefix=$2
url=$3
tags=$4
name="${name_prefix}-$(printf '%05x' $((RANDOM % 0x100000)))"

echo "Token: ${token}"
echo "Name: ${name}"
echo "Tags: ${tags}"
echo "Url: ${url}"

./config.sh \
    --url "${url}" \
    --work _work --replace \
    --runnergroup Default \
    --labels "${tags}" \
    --name "${name}" --token "${token}"

./run.sh
