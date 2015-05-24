#!/usr/bin/env python
"""
  WIFISCAN.PY
  
  WiFi Hotspot Plugin
  Original Source: https://github.com/pimoroni/dot3k/blob/master/python/examples/advanced/plugins/wlan.py

  Changes:
  - Removed Bar
  - Improved Display Style of WiFi Networks

  (C) 2015, rGunti
"""
from dot3k.menu import MenuOption
import dot3k.backlight
import wifi, threading


class WiFiScan(MenuOption):
  def __init__(self):
    self.items = []

    self.selected_item = 0

    self.scanning = False

    MenuOption.__init__(self)
    
    self.is_setup = False

  def begin(self):
    pass

  def setup(self, config):
    MenuOption.setup(self, config)

  def update_options(self):
    pass

  def cleanup(self):
    self.is_setup = False
  
  def select(self):
   return False

  def left(self):
    return False

  def right(self):
    return True

  def up(self):
    self.selected_item = (self.selected_item - 1) % len(self.items)
    return True
  
  def down(self):
    self.selected_item = (self.selected_item + 1) % len(self.items)
    return True
  
  def scan(self):
    update = threading.Thread(None, self.do_scan)
    update.daemon = True
    update.start()

  def do_scan(self):
    if self.scanning:
      return False

    self.scanning = True

    result = wifi.scan.Cell.all('wlan0')
    self.items = result

    print(result)

    self.scanning = False

  def redraw(self, menu):
    if self.scanning:
      menu.clear_row(0)
      menu.write_option(row=1,text='Scanning...')
      menu.clear_row(2)
      return True

    if not self.is_setup:
        menu.lcd.create_char(0,[0,24,30,31,30,24,0,0]) # Play
        menu.lcd.create_char(1,[0,27,27,27,27,27,0,0]) # Pause

        menu.lcd.create_char(4,[0,4,14,0,0,14,4,0]) # Up down arrow
        menu.lcd.create_char(5,[0,0,10,27,10,0,0,0]) # Left right arrow

        self.scan()

        self.is_setup = True
   
    if len(self.items):
      item = self.items[self.selected_item]

      status = 'Open'
      if item.encrypted:
        status = 'Secured: ' + str(item.encryption_type)

      menu.write_option(row=0,text=str(item.ssid),scroll=len(str(item.ssid))>16)
      menu.write_option(row=1,icon='',text=status,scroll=len(status)>16)
      menu.write_option(row=2,text='CH' + str(item.channel) + ' ' + item.frequency)

    else:
      menu.clear_row(0)
      menu.write_row(1,"No networks found!")
      menu.clear_row(2)