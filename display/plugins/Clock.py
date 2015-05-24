#!/usr/bin/env python
"""
	CLOCK.PY
	
	Clock Plugin
	
	(C) 2015, rGunti
"""
import time, datetime, copy, math, psutil
from dot3k.menu import Menu, MenuOption

class Clock(MenuOption):
	def __init__(self):
		self.last = self.millis()
		MenuOption.__init__(self)
	
	def redraw(self, menu):
		menu.write_row(0, datetime.datetime.now().strftime("   %d.%m.%Y"))
		menu.write_row(1, "")
		menu.write_row(2, datetime.datetime.now().strftime("    %H:%M:%S"))