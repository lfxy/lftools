#!/bin/bash

if [ $# == 0 ]; then
    echo caozhiqiang1@10.209.11.11
    ssh caozhiqiang1@10.209.11.11
elif [ "$1" == "155"  ]; then
    echo lfxy@192.168.1.155
    ssh lfxy@192.168.1.155
elif [[ "$1" == "111" || "$1" == "vm1" ]]; then
    echo caozq@10.15.218.111
    ssh caozq@10.15.218.111
elif [[ $1 == "vm2" || $1 == "100" ]]; then
    echo caozq@192.168.1.100
    ssh caozq@192.168.1.100
elif [[ $1 == "vm3" || $1 == "101" ]]; then
    echo caozq@192.168.1.101
    ssh caozq@192.168.1.101
elif [[ $1 == "vm4" || $1 == "102" ]]; then
    echo caozq@192.168.1.102
    ssh caozq@192.168.1.102
elif [[ $1 == "11" || "$1" == "t1" ]]; then
    echo caozhiqiang1@10.209.11.11
    ssh caozhiqiang1@10.209.11.11
else
    echo wrong parameter
    exit -1
fi
