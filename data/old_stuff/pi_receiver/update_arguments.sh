#!/bin/bash
mkdir -p /etc/systemd/system/ir_receiver.service.d 
cp -f /home/pi_receiver/ir_receiver.conf /etc/systemd/system/ir_receiver.service.d

