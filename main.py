from bearlibterminal import terminal
from mapgen import MapGen
import random
import math


class ASCII_WORLD:
	window_width = 80
	window_center = int(window_width / 2)
	tile_size = 12

	# map size and depth increases world gen time, limited impact on performance
	# must be even numbers for planet gen to work
	map_depth = 256
	map_size = 256

	# render range adjusts around player position
	render_range = [10,50,25]

	# color range is build for a max z depth of ten
	# it must be modified if you want to increase or decrease z render depth
	color_range = ['lightest ','lighter ','light ','','','','','dark ','darker ','darkest ']

	# character starting position on the map
	chr_pos = [map_depth, int(map_size / 2), int(map_size /2)]

	# Starting line for the message console
	console_pos = 33
	def __init__(self):
		terminal.open()
		terminal.set(f"window: title='Untitled Space ascii Game', size={self.window_width}x35, resizeable=true; font: MegaFont.ttf, size={self.tile_size}")
		terminal.set("input.filter={keyboard, mouse+}")
		intro_text = 'Preparing to Enter Stellar Region!'
		terminal.printf(self.center_text(intro_text), 1, intro_text)
		terminal.refresh()
		self.coords = MapGen.make_sector(self, self.map_depth, self.map_size, self.map_size)
		self.render_starchart()
		self.input_listener()

	def move_character(self, z, y, x):
		new_coords = [self.chr_pos[0] + z,self.chr_pos[1] + y,self.chr_pos[2] + x]
		if new_coords[0] >= self.map_depth:
			new_coords[0] = self.map_depth - 1
		if new_coords[1] >= self.map_size:
			new_coords[1] = self.map_size - 1
		if new_coords[2] >= self.map_size:
			new_coords[2] = self.map_size - 1
		tile = self.coords[new_coords[0]][new_coords[1]][new_coords[2]]
		print(tile.char)
		if tile.solid == False:
			self.chr_pos[0] += z
			self.chr_pos[1] += y
			self.chr_pos[2] += x
			self.render_starchart()
		if tile.solid == True:
			self.message_console('[color=green]cannot enter body', 1)

	def input_listener(self):
		global tile_size
		while True:
			key = terminal.read()
			if (key == terminal.TK_LEFT or key == terminal.TK_KP_4 or key == terminal.TK_KP_7 or key == terminal.TK_KP_1):
				print('left')
				self.move_character(0,-1,0)
			if (key == terminal.TK_RIGHT or key == terminal.TK_KP_6  or key == terminal.TK_KP_3 or key == terminal.TK_KP_9):
				print('right')
				self.move_character(0,1,0)
			if (key == terminal.TK_UP or key == terminal.TK_KP_8 or key == terminal.TK_KP_9 or key == terminal.TK_KP_7):
				print('up')
				self.move_character(0,0,-1)
			if (key == terminal.TK_DOWN or key == terminal.TK_KP_2 or key == terminal.TK_KP_1 or key == terminal.TK_KP_3):
				print('down')
				self.move_character(0,0,1)
			if (key == terminal.TK_W or key == terminal.TK_KP_MINUS):
				print('forward')
				self.move_character(-1,0,0)
			if (key == terminal.TK_S or key == terminal.TK_KP_PLUS):
				print('back')
				self.move_character(1,0,0)
			if (key == terminal.TK_ENTER):
				print('enter')
			if (key == terminal.TK_MOUSE_SCROLL):
				print('mouse')
				tile_size += int(terminal.state(terminal.TK_MOUSE_WHEEL))
				terminal.set(f"font: MegaFont.ttf, size={tile_size}")
				self.render_starchart()
			if (key == terminal.TK_ESCAPE or key == terminal.TK_CLOSE):
				#terminal.close()
				break
			if (key == terminal.TK_RESIZED):
				print('hello')
				self.render_starchart()

	def message_console(self, text, priority):
		terminal.layer(self.map_depth + 3)
		terminal.clear_area(0, self.console_pos + priority, self.window_width, 1)
		terminal.printf(self.center_text(text), self.console_pos + priority, text)
		terminal.refresh()

	def center_text(self, string):
		offset = int(terminal.measure(string)[0] /2)
		return (self.window_center - offset)

	def render_starchart(self):
		terminal.clear()
		scanner = True
		message = '[color=green]edge of stellar region reached'
		if self.chr_pos[0] < 0:
			self.chr_pos[0] = 0
			self.message_console(message, 1)
		if self.chr_pos[1] < 0:
			self.chr_pos[1] = 0
			self.message_console(message, 1)
		if self.chr_pos[2] < 0:
			self.chr_pos[2] = 0
			self.message_console(message, 1)
		if self.chr_pos[0] >= len(self.coords):
			self.message_console(message, 1)
			self.chr_pos[0] = len(self.coords) - 1
		if self.chr_pos[1] >= len(self.coords[0]):
			self.message_console(message, 1)
			self.chr_pos[1] = len(self.coords[0]) - 1
		if self.chr_pos[2] >= len(self.coords[0][0]):
			self.message_console(message, 1)
			self.chr_pos[2] = len(self.coords[0][0]) - 1
		center_screen = self.window_center - int(self.render_range[1] / 2)
		z_start = max(0, int(self.chr_pos[0] - self.render_range[0]/ 2))
		y_start = max(0, int(self.chr_pos[1] - self.render_range[1]/ 2))
		x_start = max(0, int(self.chr_pos[2] - self.render_range[2]/ 2))
		z_range = (z_start + self.render_range[0])
		y_range = (y_start + self.render_range[1])
		x_range = (x_start + self.render_range[2])
		if z_range >= self.map_depth:
			z_range = self.map_depth
			z_start = self.map_depth - self.render_range[0]
		if y_range > self.map_size:
			y_range = self.map_size
			y_start = self.map_size - self.render_range[1]
		if x_range > self.map_size:
			x_range = self.map_size
			x_start = self.map_size - self.render_range[2]
		for z in range(z_start, z_range):
			terminal.layer(z - z_start)
			#print( z - z_start, z - (self.chr_pos[0] - self.render_range[0]))
			for y in range(y_start, y_range):
				for x in range(x_start, x_range):
					tile = self.coords[z][y][x]
					if tile.char != ' ':
						offset_z = z - (self.chr_pos[0] - self.render_range[0])
						dist = z - self.chr_pos[0]
						z_color = '[color='+ self.color_range[max(0, min(z - z_start, len(self.color_range) -1))] + 'white]'
						offset = '[offset=' + str((y - self.chr_pos[1]) * offset_z) + ',' + str((x - self.chr_pos[2]) * offset_z) + ']' + z_color +tile.char
						if tile.solid == True:
							#TODO add scanner range to ship stats
							s_range = 2
							if scanner == True and z - self.chr_pos[0] > -s_range and z - self.chr_pos[0] < s_range and y - self.chr_pos[1] > -s_range and y - self.chr_pos[1] < s_range and x - self.chr_pos[2] > -s_range and x - self.chr_pos[2] < s_range:
								# only scan the nearest body, will be
								scanner = False
								offset = '[color='+tile.color +']'+ tile.char
								r = ' '
								if dist < 0:
									r = 'scan:   (-)'
								if dist > 0:
									r = 'scan:   (+)'
								terminal.layer(self.map_depth + 1)
								terminal.printf((y -y_start + 2) + center_screen, (x - x_start + -1), tile.name)
								terminal.printf((y -y_start - 6) + center_screen, (x - x_start + 1), r)
								self.message_console('Approaching Stellar Mass', 0)
								if tile.scan != '' and dist == 0:
									terminal.printf((y -y_start - 6) + center_screen, (x - x_start + 1), 'scan:   ' + tile.type)
									terminal.printf((y -y_start + 2) + center_screen, (x - x_start + 2), tile.scan)
								terminal.layer(0)
								terminal.printf((y -y_start) + center_screen, x - x_start, '[bkcolor=darkest grey] ')
								terminal.layer(z)
						terminal.printf((y -y_start) + center_screen, x - x_start, offset)
		terminal.layer(self.chr_pos[0])
		terminal.printf((self.chr_pos[1] - y_start) + center_screen, self.chr_pos[2] - x_start, '@')
		terminal.refresh()
		print('render done')

if __name__ == '__main__':
	ascii_world = ASCII_WORLD()
print('Thank you for Playing!')
terminal.close()
