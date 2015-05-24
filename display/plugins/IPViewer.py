
  (C) 2015, rGunti
"""
import os, math, psutil, subprocess, time
import socket, fcntl, struct
from dot3k.menu import MenuOption
import dot3k.backlight

class IPViewer(MenuOption):

    def get_addr(self, ifname):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 35093, struct.pack('256s', ifname[:15].encode('utf-8')))[20:24])
        except IOError:
            return 'Offline'

    def refresh_ips(self):
        self.eth0 = self.get_addr('eth0')
        self.wlan0 = self.get_addr('wlan0')
        self.wlan1 = self.get_addr('wlan1')
        self.br0 = self.get_addr('br0')

    def __init__(self):
        self.icon_eth = [0,0,4,4,21,21,17,31]
        self.icon_wifi = [0,0,14,17,4,10,0,4,0,0]
        self.icon_br = [0,4,12,31,0,31,6,4,0]
        self.refresh_ips()
        self.is_setup = False
        MenuOption.__init__(self)

    def cleanup(self):
        self.is_setup = False

    def redraw(self, menu):
        if not self.is_setup:
            self.refresh_ips()
            menu.lcd.create_char(0, self.icon_eth)
            menu.lcd.create_char(1, self.icon_wifi)
            menu.lcd.create_char(2, self.icon_br)
            self.is_setup = True
        menu.write_row(0, chr(0) + self.eth0)
        menu.write_row(1, chr(1) + self.wlan0)
        menu.write_row(2, chr(1) + self.wlan1)
