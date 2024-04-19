#!/bin/bash
source /home/pi_emitter/ir_emitter.conf

echo $ROOMNAME
dirname=data_$ROOMNAME
mkdir -p /home/pi_emitter/$dirname 

hostn=$(hostname)
filename=ip_$hostn.txt


echo "$(hostname -I)" >> /home/pi_emitter/$filename
echo "$(date)" >> /home/pi_emitter/$filename


mv /home/pi_emitter/$filename /home/pi_emitter/$dirname/$filename

sshpass -p Ha1lll1oo1 rsync -aPvbc -e 'ssh -p 8080' /home/pi_emitter/$dirname/ pi_server@masterarbeit.ddns.net:$dirname 

