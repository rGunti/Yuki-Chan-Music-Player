#!/bin/bash

echo "Script is starting up..."
echo "Creating PID..."
echo $$ > /tmp/player.sh.pid

#echo "Starting up Hotspot..."
#service hostapd restart

#echo "Starting up DHCP Server..."
#udhcpd -f >> /var/log/udhcpd.player.log &

echo "Starting MPD..."
service mpd restart

echo "Initializing MPD..."
mpc update > /dev/null
mpc clear > /dev/null
mpc listall | mpc add
mpc shuffle > /dev/null
mpc repeat on > /dev/null
mpc play > /dev/null

echo "Starting Firmware..."
while true; do
	sudo python /script/py/player/main.py #>> /script/py/player/player.log
	if [ $? -eq 0 ]; then
		echo "Firmware has been quit by User"
		break
	else
		echo "Firmware crashed, restarting..."
	fi
done

echo "Script is quitting, deleting PID file..."
rm /tmp/player.sh.pid

echo "Script has ended!"
