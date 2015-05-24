# Yuki-Chan Display
Yuki-Chan was built with a [Displayotron 3000][dot3k] (or [dot3k][dot3k] for short) to display information about its current system status and for controlling it.

## Menu Structure
 - Clock: *Displays the current system time*
 - Music Player: *Opens the Music Player application, connects to your local MPD server*
 - System
	 - Networking
		 - Show IPs: *Shows IP addresses of the following interfaces: eth0, wlan0, wlan1*
		 - Scan WiFi: *Scans for WiFi networks and displays them (using wifi0)*
		 - WiFi Hotspot: *Displays WiFi Hotspot Information of your hostapd configuration (`/etc/hostapd/hostapd.conf`)*
	 - CPU
		 - Usage: *Display the current CPU load*
		 - Temprature: *Display the current CPU/GPU load*
	 - Shutdown
		 - Quit FW: *Quits Yuki-Chan's Display Python Script*
		 - Reboot: *Reboots your Pi*
		 - Shutdown: *Shuts your Pi down*

## About `run.sh`
`run.sh` is a startup script that you can / should implement in your system by calling it on startup (e.g. by setting up a cronjob).
**Important!** This script has been implemented with a fixed path (related to the project). So if you choose an alternative directory for storing the firmware (`main.py`) you'll have to alter the python call in the script.
It currently does the following:

 1. Create a PID file (stored in `/tmp/player.sh.pid`)
 2. (Re)Start MPD
 2. Update MPD databaes
 3. Clear current MPD playlist
 4. Add all tracks to MPD playlist
 5. Shuffle MPD playlist
 6. Switch MPD Repeat Mode on
 7. Start MPD playback
 8. Start Firmware

In the event of an unexpected crash, the firmware will be restarted automatically. If you select a Command of the Menu `System/Shutdown`, this will not apply. The firmware will then be shutdown, `run.sh` recognizes that as a correct quit and removes the PID file. If you want, you can uncomment the last part of Line 26 (where the python call is located) so the output of the python application will be logged into a file.

[dot3k]: https://github.com/pimoroni/dot3k
