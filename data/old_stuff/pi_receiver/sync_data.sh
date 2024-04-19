#!/bin/bash
name=$(basename /home/pi_receiver/data_*)
echo "$name"
sshpass -p Ha1lll1oo1 rsync -aPvbc -e 'ssh -p 8080' /home/pi_receiver/$name/ pi_server@masterarbeit.ddns.net:$name 
#sshpass -p Ha1lll1oo1 scp -P 8080 -r -v -p data_*/ pi_server@masterarbeit.ddns.net:/home/pi_server/
