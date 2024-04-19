How to setup IR-Emitter RaspberryPi with Ubuntu Server OS 22.04.:

if he doesnt find the network with nmcli
sudo systemctl restart wpa_supplicant.service

1.) sudo apt update

2.) sudo apt install unzip make gcc python-setuptools python3-setuptools network-manager net-tools raspi-config wireless-tools openssh-server sshpass

3.) install "pigpio":

wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install

sudo nano /etc/systemd/system/pigpiod.service
[Unit]
Description=Daemon required to control GPIO pins via pigpio
[Service]
ExecStart=/usr/local/bin/pigpiod
ExecStop=/bin/systemctl kill -s SIGKILL pigpiod
Type=forking
[Install]
WantedBy=multi-user.target


4.) scp pi_emitter directory from pi_server//

ping masterarbeit.ddns.net
scp -r -P 8080 pi_server@masterarbeit.ddns.net:~/pi_emitter/* ~
#scp -r berni@192.168.0.14:~/Dropbox/masterarbeit/pi_emitter_copy_27_02/* ~/


5.) move system files into /etc/systemd/system
sudo mv system/* /etc/systemd/system
rm -r system

6.) Set correct hostname
sudo nano /etc/cloud/cloud.cfg
sudo hostname raspberryemitter<Doornumber>
sudo nano /etc/hostname
sudo nano /etc/hosts

7.) ssh once to pi_server, to add to known hosts
ssh pi_server@masterarbeit.ddns.net -p 8080

8.) Enable autostart of python script, i.e.: add pigpio and python script to services:

-> change conf file correct roomname and door
sudo nano ir_emitter.conf

afterwards start and "enable" both services, sudo systemctl enable/start *.service

sudo systemctl enable ir_emitter.service pigpiod.service sync_ip.service sync_ip.timer
sudo systemctl daemon-reload
sudo systemctl restart ir_emitter.service pigpiod.service sync_ip.service sync_ip.timer


