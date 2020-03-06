from bearlibterminal import terminal
from configparser import ConfigParser
from inputlistener import input_listener
from intro import Intro

from mapgen import MapGen
import random
import time
import math

config = ConfigParser()
config.read('main.ini')
class ASCII_WORLD:
	game_title = 'This is Space'
	window_width = config.getint('innit', 'window_width')
	window_height = config.getint('innit', 'window_height')
	window_center = int(window_width / 2)
	tile_size = config.getint('innit', 'tile_size')

	# map size and depth increases world gen time, limited impact on performance
	# planet gen assumes even numbered
	map_depth = 64
	map_size = 128

	# render range adjusts around player position
	render_range = [10,50,25]
	coords = []

	# color_range is used to change tile color depending on current z level
	# color range list is build for a max z depth of ten
	# it must be modified if you want to increase or decrease z render depth
	color_range = ['lightest ','lighter ','light ','','','','','dark ','darker ','darkest ']

	# character starting position on the map
	chr_pos = [map_depth -1, int(map_size / 2), int(map_size /2)]

	# Starting line for the message console [bottom]
	console_pos = window_height - 3
	# Satring line for the ship console [right side]
	ship_console_pos = int(window_center + (render_range[2] / 2))

	input_state = 'intro'
	mouse_pos_y = 0
	mouse_pos_x = 0
	menu_num = 0
	dev_mode = config.getboolean('innit', 'dev_mode')

	pause = False

	def __init__(self):
		terminal.open()
		terminal.set(f"window: title={self.game_title}, size={self.window_width}x{self.window_height}; font: MegaFont.ttf, size={self.tile_size}")
		intro_text = '                '
		#terminal.printf(self.center_text(intro_text), 1, intro_text)
		terminal.printf(self.center_text(intro_text), 12, intro_text)
		terminal.refresh()
		input_listener(self)

	def main_menu(self, num, x, y, click, enter):
		self.input_state = 'main'
		dict = [
				['[color=grey] New Game', 'New Game'],
				['[color=grey]   Continue', '  Continue'],
				['[color=grey]     Quit Game', '    Quit Game'],
				]
		terminal.clear()
		terminal.layer(0)
		button0_rect = [self.center_text(dict[0][1]), 16, 8, 1]
		button1_rect = [self.center_text(dict[1][1]), 18, 10, 1]
		button2_rect = [self.center_text(dict[2][1]), 20, 13, 1]
		self.menu_num += num
		if self.menu_num > 2:
			self.menu_num = 0
		if self.menu_num < 0:
			self.menu_num = 2
		if x != 0 or y != 0:
			clickable = False
			if y >= button0_rect[1] and y <= button0_rect[1] + button0_rect[3]:
				if x >= button0_rect[0] and x <= button0_rect[0] + button0_rect[2]:
					clickable = True
					self.menu_num = 0
			if y >= button1_rect[1] and y <= button1_rect[1] + button1_rect[3]:
				if x >= button1_rect[0] and x <= button1_rect[0] + button1_rect[2]:
					clickable = True
					self.menu_num = 1
			if y >= button2_rect[1] and y <= button2_rect[1] + button2_rect[3]:
				if x >= button2_rect[0] and x <= button2_rect[0] + button2_rect[2]:
					clickable = True
					self.menu_num = 2
		if self.menu_num == 0:
			terminal.printf(button0_rect[0], button0_rect[1], dict[0][1])
		else:
			terminal.printf(button0_rect[0], button0_rect[1], dict[0][0])
		if self.menu_num == 1 and num != 0:
			terminal.printf(button1_rect[0], button1_rect[1], dict[1][1])
			if self.coords == []:
				self.main_menu(num, 0, 0, False, False)
				return
		else:
			terminal.printf(button1_rect[0], button1_rect[1], dict[1][0])
		if self.menu_num == 2:
			terminal.printf(button2_rect[0], button2_rect[1], dict[2][1])
		else:
			terminal.printf(button2_rect[0], button2_rect[1], dict[2][0])
		terminal.printf(self.center_text('This is [color=red]Space  '), 11, 'This is [color=red]Space  ')
		#terminal.printf(self.center_text('press Enter'), 12, 'press Enter')
		terminal.refresh()
		if (click == True and clickable == True) or enter == True:
			if self.menu_num == 0:
				self.load_sector()
			if self.menu_num == 1:
				self.input_state = 'sector'
			if self.menu_num == 2:
				terminal.close()

	def load_sector(self):
		terminal.layer(0)
		self.chr_pos = [self.map_depth -1, int(self.map_size / 2), int(self.map_size /2)]
		terminal.clear()
		terminal.printf(self.center_text('Preparing emergency display console'), 6, 'Preparing emergency display console')
		self.input_state = 'loading'
		self.coords = MapGen.make_sector(self, self.map_depth, self.map_size, self.map_size)
		self.input_state = 'sector'
		terminal.clear()
		key = terminal.read()


	def move_character(self, z, y, x):
		new_coords = [self.chr_pos[0] + z,self.chr_pos[1] + y,self.chr_pos[2] + x]
		if new_coords[0] >= self.map_depth:
			new_coords[0] = self.map_depth - 1
		if new_coords[1] >= self.map_size:
			new_coords[1] = self.map_size - 1
		if new_coords[2] >= self.map_size:
			new_coords[2] = self.map_size - 1
		tile = self.coords[new_coords[0]][new_coords[1]][new_coords[2]]
		#print(tile.char)
		if tile.solid == False:
			self.chr_pos[0] += z
			self.chr_pos[1] += y
			self.chr_pos[2] += x
		message = ''
		if tile.solid == True:
			message = '[color=green]cannot enter body'
		if self.chr_pos[0] < 0:
			self.chr_pos[0] = 0
			message = '[color=green]edge of stellar region reached'
		if self.chr_pos[1] < 0:
			self.chr_pos[1] = 0
			message = '[color=green]edge of stellar region reached'
		if self.chr_pos[2] < 0:
			self.chr_pos[2] = 0
			message = '[color=green]edge of stellar region reached'
		if self.chr_pos[0] >= len(self.coords):
			message = '[color=green]edge of stellar region reached'
			self.chr_pos[0] = len(self.coords) - 1
		if self.chr_pos[1] >= len(self.coords[0]):
			message = '[color=green]edge of stellar region reached'
			self.chr_pos[1] = len(self.coords[0]) - 1
		if self.chr_pos[2] >= len(self.coords[0][0]):
			message = '[color=green]edge of stellar region reached'
			self.chr_pos[2] = len(self.coords[0][0]) - 1
		self.message_console(message, 1)

	def message_console(self, text, priority):
		terminal.layer(self.map_depth + 3)
		terminal.clear_area(0, self.console_pos + priority, self.window_width, 1)
		terminal.printf(self.center_text(text), self.console_pos + priority, text)

	def dev_console(self, text, priority):
		terminal.layer(self.map_depth + 3)
		terminal.clear_area(0, priority, self.window_width, 1)
		terminal.printf(0, priority, text)

	def ship_console(self, text, priority):
		terminal.layer(self.map_depth + 3)
		terminal.clear_area(self.ship_console_pos, priority, self.window_width, 1)
		terminal.printf(self.ship_console_pos, priority, text)

	def center_text(self, string):
		offset = int(terminal.measure(string)[0] /2)
		return (self.window_center - offset)

if __name__ == '__main__':
	ascii_world = ASCII_WORLD()
print('Thank you for Playing!')
terminal.close()
