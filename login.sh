#!/bin/bash

if [ $# == 0 ]; then
    echo "need param!"
    exit 1
elif [[ "$1" == "63" || "$1" == "trogdor" ]]; then
    echo root@172.16.31.63
    ssh root@172.16.31.63
elif [[ "$1" == "60" || "$1" == "tdn" ]]; then
    echo root@172.16.31.60
    ssh root@172.16.31.60
elif [[ $1 == "61" || "$1" == "tms" ]]; then
    echo root@172.16.31.61
    ssh root@172.16.31.61
elif [[ $1 == "demeter" || $1 == "62" ]]; then
    echo root@172.16.31.62
    ssh root@172.16.31.62
elif [[ $1 == "59" || $1 == "monitor" ]]; then
    echo caoz1@172.16.31.59
    ssh caoz1@172.16.31.59
elif [ $1 == "242" ]; then
    echo root@172.16.31.242
    ssh root@172.16.31.242
else
    echo wrong parameter
    exit -1
fi
