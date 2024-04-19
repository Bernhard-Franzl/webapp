#!/bin/bash
dirname=$(basename /home/pi_receiver/data_*)
hostn=$(hostname)
filename=ip_$hostn.txt

echo "$(hostname -I)" >> /home/pi_receiver/$filename
echo "$(date)" >> /home/pi_receiver/$filename

mv /home/pi_receiver/$filename /home/pi_receiver/$dirname/$filename

#sshpass -p Ha1lll1oo1 rsync -aPvbc -e 'ssh -p 8080' /home/pi_receiver/$filename pi_server@masterarbeit.ddns.net:/home/pi_server/$filename 
#sshpass -p Ha1lll1oo1 rsync -arvRPz -e 'ssh -p 8080' ip_adress.txt pi_server@masterarbeit.ddns.net:ip_adress_1.txt
