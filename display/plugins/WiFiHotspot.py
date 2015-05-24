#!/usr/bin/env python
"""
	WIFIHOTSPOT.PY
	
	WiFi Hotspot Plugin
	
	(C) 2015, rGunti
"""
import time, datetime, copy, math, psutil
import dot3k.lcd as lcd
import subprocess as sp
import ConfigParser
from dot3k.menu import Menu, MenuOption
from mpd import MPDClient

def util_get_config_section_map(cp,section):
	dict1 = {}
	options = cp.options(section)
	for option in options:
		try:
			dict1[option] = cp.get(section, option)
			if dict1[option] == -1:
				print("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1
def util_get_safe_from_map(map,key,default="-"):
	if key in map:
		return map[key]
	else:
		return default

class FakeSectionHead(object):
	def __init__(self, fp):
		self.fp = fp
		self.sechead = "[fakesection]\n"

	def readline(self):
		if self.sechead:
			try:
				return self.sechead
			finally:
				self.sechead = None
		else:
			return self.fp.readline()

class WiFiHotspot(MenuOption):
	def read_config_file(self, filename):
		cp = ConfigParser.SafeConfigParser()
		cp.readfp(FakeSectionHead(open(filename)))
		return util_get_config_section_map(cp,'fakesection')

	def __init__(self):
		hostapd_config = self.read_config_file('/etc/hostapd/hostapd.conf')

		self.ssid = str(util_get_safe_from_map(hostapd_config,'ssid'))
		self.psk = str(util_get_safe_from_map(hostapd_config,'wpa_passphrase'))

		MenuOption.__init__(self)

	def redraw(self, menu):
		menu.write_option(0, "* WiFi HOTSPOT *")
		menu.write_option( 
			row=1,
			margin=5,
			text=self.ssid,
			icon='SSID:',
			scroll=len(self.ssid)>(16-5),
			scroll_speed=200,
			scroll_delay=2000,
			scroll_repeat=5000,
			scroll_padding='   '
		)
		menu.write_option( 
			row=2,
			margin=5,
			icon='PW: ',
			text=self.psk,
			scroll=len(self.psk)>(16-5),
			scroll_speed=200,
			scroll_delay=2000,
			scroll_repeat=5000,
			scroll_padding='   '
		)