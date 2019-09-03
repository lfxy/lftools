#!/bin/bash

auto_ssh_copy_id () {
    expect -c "set timeout -1;
        spawn ssh-copy-id -i $HOME/.ssh/id_rsa.pub -p $4 $1@$2;
            expect {
                {Are you sure you want to continue connecting *} {send -- yes\r;exp_continue;}
                {*password:} {send -- $3\r;exp_continue;}
                eof {exit 0;}
            };"
}

#yum -y install expect

#[ ! -f /root/.ssh/id_rsa.pub ] && key_generate

USER=root
PWD=kuorong2019
PORT=22
IPLIST=$(cat ./hosts | grep -v "::" | grep -v "127.0.0.1" | grep -v "localhost" | awk '{print $1}')

for IP in $IPLIST
do
    auto_ssh_copy_id $USER $IP $PWD $PORT
done
