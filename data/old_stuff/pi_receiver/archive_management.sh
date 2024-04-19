#!/bin/bash
working_directory=/home/pi_receiver
name=$(basename /home/pi_receiver/data_*)
if sshpass -p Ha1lll1oo1 ssh pi_server@masterarbeit.ddns.net -p 8080  true; then
    echo "webserver is alive"
    python3 $working_directory/archive_management.py
    if sshpass -p Ha1lll1oo1 rsync -aPvbc -e 'ssh -p 8080' $working_directory/archive/ pi_server@masterarbeit.ddns.net:archive/; then
        systemctl stop ir_receiver.service
        rm -r $working_directory/$name
        systemctl start ir_receiver.service
    else
        echo "sync not successful"
    fi
else
    echo "webserver is down"
fi
