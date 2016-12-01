#!/bin/bash

if [ $# == 0 ]; then
    echo caozhiqiang1@10.209.11.11
    ssh caozhiqiang1@10.209.11.11
    exit 0
fi


ip_tail=""
while getopts ":c:h:" opt
do
    case $opt in
        c)
            ip_tail=$OPTARG
            echo "root@10.15.137."$ip_tail
            ssh root@10.15.137.$ip_tail
            ;;
        h)
            ip_tail=$OPTARG
            echo root@192.168.1.$ip_tail
            ssh root@192.168.1.$ip_tail
            ;;
        ?)
            echo "error" && exit 1
            ;;
    esac
done

