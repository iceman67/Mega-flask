sudo apt-get update
sudo apt-get -y install python3-rpi.gpio
sudo apt-get install python3-w1thermsensor
pip3 install telepot
# telepot should install for running a script in the file /etc/rc.local 
sudo pip3 install telepot
pip3 install flask

* telepot command 
/hello
/temp
/on
/off


*install and configure  ntp

sudo apt-get install ntp

$ cat /etc/rc.local
logger "Beginning force syncing NTP..."
service ntp stop
ntpd -gq
service ntp start
logger "Finished force syncing NTP..."
