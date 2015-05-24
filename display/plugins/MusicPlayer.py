#!/usr/bin/env python
"""
	MUSICPLAYER.PY
	
	Music Player Plugin
	
	(C) 2015, rGunti
"""
import time, datetime, copy, math, psutil
import dot3k.lcd as lcd
import subprocess as sp
from dot3k.menu import Menu, MenuOption
from mpd import MPDClient

def util_execute_command(args):
	p = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE)
	out, err = p.communicate()
	return out
def util_get_safe_from_map(map,key,default=""):
	if key in map:
		return map[key]
	else:
		return default
def util_is_numeric(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
def util_get_time(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	if h >= 1:
		return "%d:%02d:%02d" % (h, m, s)
	else:
		return "%d:%02d" % (m, s)

class MusicPlayer(MenuOption):
	def do_play(self):
		self.mpd.pause()
	def do_back(self):
		self.mode = 0

	def __init__(self):
		self.mode = 0 # 0:Player View, 1:Menu
		self.selindex = 0
		self.options = [
			"Pause",
			"Back"
		]
		self.actions = [
			self.do_play,
			self.do_back
		]
		self.mpd = MPDClient()
		self.mpd.timeout = 10
		self.mpd.idletimeout = None
		self.is_setup = False

		# Icons
		self.anim_play = [[0,0,8,12,14,12,8,0],[0,0,4,6,7,6,4,0],[0,0,2,3,19,3,2,0],[0,0,1,17,25,17,1,0],[0,0,16,24,28,24,16,0]]
		self.anim_pause = [[0,0,0,0,0,0,0,0],[0,27,27,27,27,27,27,0]]
		self.icon_stop = [0,0,31,31,31,31,31,0]
		
		try:
			self.mpd.connect("localhost", 6600)
		except socket.error:
			print("Could not connect to MPD")
		
		MenuOption.__init__(self)
	
	def up(self):
		print("UP")
		if self.mode == 0:
			util_execute_command(["mpc", "volume", "+5"])
		elif self.mode == 1:	# Menu
			#print("selindex=" + str(self.selindex) + " ; len-options=" + str(len(self.options)))
			self.selindex = (self.selindex - 1) % len(self.options)
	
	def down(self):
		print("DOWN")
		if self.mode == 0:
			util_execute_command(["mpc", "volume", "-5"])
		elif self.mode == 1:	# Menu
			#print("selindex=" + str(self.selindex) + " ; len-options=" + str(len(self.options)))
			self.selindex = (self.selindex + 1) % len(self.options)
	
	def left(self):
		print("LEFT")
		if self.mode == 1:
			self.mode = 0
			return False
		else:
			if self.mode == 0:
				util_execute_command(["mpc", "prev"])
			return True
	
	def right(self):
		if self.mode == 0:
			util_execute_command(["mpc", "next"])
		print("RIGHT")
	
	def select(self):
		print("SELECT ; mode=" + str(self.mode))
		if self.mode == 0:
			self.mode = 1
		elif self.mode == 1:	# Menu
			self.actions[ self.selindex ]()
			self.mode = 0
	
	def get_current_option(self):
		return self.options[ self.selindex ]

	def get_next_option(self):
		return self.options[ (self.selindex + 1) % len(self.options) ]

	def get_prev_option(self):
		return self.options[ (self.selindex - 1) % len(self.options) ]
	
	def getAnimFrame(self,char,fps):
		return char[ int(round(time.time()*fps) % len(char)) ]

	def cleanup(self):
		self.is_setup = False

	def redraw(self, menu):
		#lcd.clear()
		#print "MusicPlayer redraw"
		if not self.is_setup:
			# This needs a modified version of st7036.py (pull request sent on GitHub 2015-05-24 18:42 CEST)
			menu.lcd.create_animation(0, self.anim_play, 4)
			menu.lcd.create_animation(1, self.anim_pause, 2)
			menu.lcd.create_char(2, self.icon_stop)
			self.is_setup = True

		if self.mode == 0:	# Player View
			status = self.mpd.status()
			song = self.mpd.currentsong()
			state = util_get_safe_from_map(status, "state", "")

			song_title = util_get_safe_from_map(song, "title")
			song_artist = util_get_safe_from_map(song, "artist")
			song_time = util_get_safe_from_map(status, "elapsed", 0)
			song_pos = util_get_safe_from_map(status, "song", 0)
			song_pllength = util_get_safe_from_map(status, "playlistlength", 0)

			if util_is_numeric(song_time):
				song_time = util_get_time(float(song_time))
			else:
				song_time = ""

			status_line = ""
			#status_line = "  "
			if state == "play":
				if util_is_numeric(song_pos):
					song_pos = str(int(song_pos) + 1)

				if util_is_numeric(song_pllength) and float(song_pllength) >= 1000:
					status_line = status_line + song_pos
				else:
					status_line = status_line + chr(0) + song_pos + "/" + song_pllength
			elif state == "pause":
				status_line = chr(1) + "PAUSE"
			else:
				status_line = chr(2) + state

			if state == "play" or state == "pause":
				spacecnt = 16-len(status_line)-len(song_time)
				for i in range(spacecnt):
					status_line = status_line + " "
				status_line = status_line + song_time
			else:
				status_line = status_line

			menu.write_option(
					row=0,
					text=song_title,
					scroll=len(song_title)>16,
					scroll_speed=200,
					scroll_delay=2000,
					scroll_repeat=5000,
					scroll_padding='   '
				)
			menu.write_option(
					row=1,
					text=song_artist,
					scroll=len(song_artist)>16,
					scroll_speed=200,
					scroll_delay=2000,
					scroll_repeat=5000,
					scroll_padding='   '
				)
			menu.write_option(2, status_line)
			menu.lcd.update_animations()
		elif self.mode == 1:	# Menu
			prev_opt = self.get_prev_option()
			curr_opt = self.get_current_option()
			next_opt = self.get_next_option()
			#print(str(self.selindex) + " " + prev_opt + " " + curr_opt + " " + next_opt)
			menu.write_option( 
				row=0,
				margin=1,
				icon='*' if self.selindex == 0 else '',
				text=self.options[0]
			)
			menu.write_option( 
				row=2,
				margin=1,
				icon='*' if self.selindex == 1 else '',
				text=self.options[1]
			)
			menu.clear_row(1)