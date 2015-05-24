#!/usr/bin/env python
"""
	MAIN.PY
	
	Main Launch Script
	
	(C) 2015, rGunti
"""
import dot3k.lcd as lcd
import dot3k.backlight as backlight
import dot3k.joystick as joystick
import time, datetime, copy, math, psutil
from dot3k.menu import Menu, MenuOption
from plugins.MusicPlayer import MusicPlayer
from plugins.Clock import Clock
from plugins.Shutdown import Shutdown, Reboot, QuitScript
from plugins.WiFiHotspot import WiFiHotspot
from plugins.WiFiScan import WiFiScan
from plugins.IPViewer import IPViewer
from plugins.Temprature import GraphTemp, GraphCPU

def getAnimFrame(char,fps):
	return char[ int(round(time.time()*fps) % len(char)) ]
def init_animation():
	hourglass = [
		[0x1F,0x11,0x11,0x11,0x11,0x11,0x11,0x1F],[0x1F,0x1F,0x11,0x11,0x11,0x11,0x11,0x1F],
		[0x1F,0x1F,0x1F,0x11,0x11,0x11,0x11,0x1F],[0x1F,0x1F,0x1F,0x1F,0x11,0x11,0x11,0x1F],
		[0x1F,0x11,0x1F,0x1F,0x1F,0x11,0x11,0x1F],[0x1F,0x11,0x11,0x1F,0x1F,0x1F,0x11,0x1F],
		[0x1F,0x11,0x11,0x11,0x1F,0x1F,0x1F,0x1F],[0x1F,0x11,0x11,0x11,0x11,0x1F,0x1F,0x1F],
		[0x1F,0x11,0x11,0x11,0x11,0x11,0x1F,0x1F],[0x1F,0x11,0x11,0x11,0x11,0x11,0x11,0x1F]
	]
	greetingtext = [
	#	"- - - - - - - - ",
		"     Welcome    ",
		"       To       ",
		"    Yuki-Chan   "
	]
	
	dotc = 0
	texti = 0
	for x in range(127):
		backlight.rgb(x / 2, x * 2, x / 2)
		"""
		lcd.create_char(0, getAnimFrame(hourglass, 5))
		lcd.clear()
		lcd.set_cursor_position(15,2)
		lcd.write(chr(0))
		"""
		lcd.set_cursor_position(0,1)
		lcd.write(greetingtext[texti])
		
		if dotc > 30:
			texti = (texti + 1) % len(greetingtext)
			dotc = 0
		else:
			dotc += 1
		
		lcd.set_cursor_position(6,2)
		for i in range(dotc / 10):
			lcd.write(".")

	lcd.clear()
def shutdown_animation():
	lcd.set_cursor_position(3,1)
	lcd.write("Bye (^_^)/")
	for x in reversed(range(127)):
		backlight.rgb(x, x * 2, x)
	lcd.clear()

menu = Menu({}, lcd, 30)
Menu.add_item(menu, 'Music Player', MusicPlayer())
Menu.add_item(menu, 'Clock', Clock())

# System
# System/Networking
Menu.add_item(menu, 'Networking/System/Show IPs', IPViewer())
Menu.add_item(menu, 'Networking/System/Scan WiFi', WiFiScan())
Menu.add_item(menu, 'Networking/System/WiFi Hotspot', WiFiHotspot())

# System/CPU
Menu.add_item(menu, 'CPU/System/Usage', GraphCPU())
Menu.add_item(menu, 'CPU/System/Temprature', GraphTemp())

# System/Shutdown
Menu.add_item(menu, 'Shutdown/System/Reboot', Reboot())
Menu.add_item(menu, 'Shutdown/System/Shutdown', Shutdown())
Menu.add_item(menu, 'Shutdown/System/Quit FW', QuitScript())

"""
Logo
"""
REPEAT_DELAY = 0.5
@joystick.on(joystick.UP)
def handle_up(pin):
  menu.up()
  joystick.repeat(joystick.UP,menu.up,REPEAT_DELAY,0.9)

@joystick.on(joystick.DOWN)
def handle_down(pin):
  menu.down()
  joystick.repeat(joystick.DOWN,menu.down,REPEAT_DELAY,0.9)

@joystick.on(joystick.LEFT)
def handle_left(pin):
  menu.left()
  joystick.repeat(joystick.LEFT,menu.left,REPEAT_DELAY,0.9)

@joystick.on(joystick.RIGHT)
def handle_right(pin):
  menu.right()
  joystick.repeat(joystick.RIGHT,menu.right,REPEAT_DELAY,0.9)

@joystick.on(joystick.BUTTON)
def handle_button(pin):
  menu.select()

init_animation()
menu.right()
while 1:
  menu.redraw()
  time.sleep(0.05)

shutdown_animation()
