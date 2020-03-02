from bearlibterminal import terminal
import random
import math

window_width = 80
window_center = int(window_width / 2)

tile_size = 12

# map size and depth increases world gen time, limited impact on performance
# must be even numbers for planet gen to work
map_depth = 64
map_size = 64

# render range adjusts around player position
render_range = [10,50,25]

# color range is build for a max z depth of ten
# it must be modified if you want to increase or decrease z render depth
color_range = ['lightest ','lighter ','light ','','','','','dark ','darker ','darkest ']

# character starting position on the map
chr_pos = [map_depth, int(map_size / 2), int(map_size /2)]

# Starting line for the message console
console_pos = 33

class Object:
	def __init__(self):
		self.z = 0
		self.y = 0
		self.x = 0
		self.char = ' '
		self.name = ''
		self.type = ''
		self.scan = ''
		self.color = ''
		self.solid = False

class ASCII_WORLD:
	def __init__(self):
		terminal.open()
		terminal.set(f"window: title='Untitled Space ascii Game', size={window_width}x35, resizeable=true; font: MegaFont.ttf, size={tile_size}")
		terminal.set("input.filter={keyboard, mouse+}")
		intro_text = 'Preparing to Enter Stellar Region!'
		terminal.printf(self.center_text(intro_text), 1, intro_text)
		terminal.refresh()
		self.make_map(map_depth, map_size, map_size)
		self.render_starchart()
		self.input_listener()

	def move_character(self, z, y, x):
		new_coords = [chr_pos[0] + z,chr_pos[1] + y,chr_pos[2] + x]
		if new_coords[0] >= map_depth:
			new_coords[0] = map_depth - 1
		if new_coords[1] >= map_size:
			new_coords[1] = map_size - 1
		if new_coords[2] >= map_size:
			new_coords[2] = map_size - 1
		tile = coords[new_coords[0]][new_coords[1]][new_coords[2]]
		print(tile.char)
		if tile.solid == False:
			chr_pos[0] += z
			chr_pos[1] += y
			chr_pos[2] += x
			self.render_starchart()
		if tile.solid == True:
			self.message_console('cannot enter body', 1)

	def input_listener(self):
		global chr_pos
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
		terminal.layer(map_depth + 3)
		terminal.clear_area(0, console_pos + priority, window_width, 1)
		terminal.printf(self.center_text(text), console_pos + priority, text)
		terminal.refresh()

	def center_text(self, string):
		offset = int(terminal.measure(string)[0] /2)
		return (window_center - offset)

	def render_starchart(self):
		terminal.clear()
		global chr_pos
		scanner = True
		message = '[color=red]edge of stellar region reached'
		if chr_pos[0] < 0:
			chr_pos[0] = 0
			self.message_console(message, 1)
		if chr_pos[1] < 0:
			chr_pos[1] = 0
			self.message_console(message, 1)
		if chr_pos[2] < 0:
			chr_pos[2] = 0
			self.message_console(message, 1)
		if chr_pos[0] >= len(coords):
			self.message_console(message, 1)
			chr_pos[0] = len(coords) - 1
		if chr_pos[1] >= len(coords[0]):
			self.message_console(message, 1)
			chr_pos[1] = len(coords[0]) - 1
		if chr_pos[2] >= len(coords[0][0]):
			self.message_console(message, 1)
			chr_pos[2] = len(coords[0][0]) - 1
		center_screen = window_center - int(render_range[1] / 2)
		z_start = max(0, int(chr_pos[0] - render_range[0]/ 2))
		y_start = max(0, int(chr_pos[1] - render_range[1]/ 2))
		x_start = max(0, int(chr_pos[2] - render_range[2]/ 2))
		z_range = (z_start + render_range[0])
		y_range = (y_start + render_range[1])
		x_range = (x_start + render_range[2])
		if z_range >= map_depth:
			z_range = map_depth
			z_start = map_depth - render_range[0]
		if y_range > map_size:
			y_range = map_size
			y_start = map_size - render_range[1]
		if x_range > map_size:
			x_range = map_size
			x_start = map_size - render_range[2]
		for z in range(z_start, z_range):
			terminal.layer(z - z_start)
			#print( z - z_start, z - (chr_pos[0] - render_range[0]))
			for y in range(y_start, y_range):
				for x in range(x_start, x_range):
					tile = coords[z][y][x]
					if tile.char != ' ':
						offset_z = z - (chr_pos[0] - render_range[0])
						dist = z - chr_pos[0]
						z_color = '[color='+ color_range[max(0, min(z - z_start, len(color_range) -1))] + 'white]'
						offset = '[offset=' + str((y - chr_pos[1]) * offset_z) + ',' + str((x - chr_pos[2]) * offset_z) + ']' + z_color +tile.char
						if tile.solid == True:
							#TODO add scanner range to ship stats
							s_range = 2
							if scanner == True and z - chr_pos[0] > -s_range and z - chr_pos[0] < s_range and y - chr_pos[1] > -s_range and y - chr_pos[1] < s_range and x - chr_pos[2] > -s_range and x - chr_pos[2] < s_range:
								# only scan the nearest body, will be
								scanner = False
								offset = '[color='+tile.color +']'+ tile.char
								r = ' '
								if dist < 0:
									r = '-'
								if dist > 0:
									r = '+'
								terminal.layer(map_depth + 1)
								terminal.printf((y -y_start - 2) + center_screen, (x - x_start + -1), r + '   ' + tile.name)
								self.message_console('Approaching Stellar Mass', 0)
								if tile.scan != '' and dist == 0:
									terminal.printf((y -y_start - 6) + center_screen, (x - x_start + 1), 'scan:   ' + tile.type)
									terminal.printf((y -y_start + 2) + center_screen, (x - x_start + 2), tile.scan)
								terminal.layer(0)
								terminal.printf((y -y_start) + center_screen, x - x_start, '[bkcolor=darkest grey] ')
								terminal.layer(z)
						terminal.printf((y -y_start) + center_screen, x - x_start, offset)
		terminal.layer(chr_pos[0])
		terminal.printf((chr_pos[1] - y_start) + center_screen, chr_pos[2] - x_start, '@')
		terminal.refresh()
		print('render done')

	def make_map(self, depth, height, width):
		global coords
		terminal.printf(self.center_text('Scanning sector...'), 5, 'Scanning sector...')
		map_layer = []
		loading = int(window_center - depth / 2)
		center = [int(depth /2), int(height /2), int(width /2)]
		for z in range(depth):
			map_height = []
			for y in range(height):
				map_width = []
				for x in range(width):
					tile = Object()
					chance = random.randrange(0, 10000)
					if chance < 9800:
						tile.char = ' '
						tile.solid = False
					elif chance < 9995:
						tile.char = random.choice(".,'") # '♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼')
						tile.solid = False
						tile.type = 'Dust'
					else:
						self.add_sun(tile)
					map_width.append(tile)
				map_height.append(map_width)
			terminal.printf(loading + z, 6, '☼')
			terminal.refresh()
			map_layer.append(map_height)
		coords = map_layer
		# test of generating a central sun for the solar_system generator
		#self.add_sphere(center[0],center[1],center[2], 4)
		print('map generated')
		terminal.printf(self.center_text('Map Generated'), 3, 'Map Generated!')
		terminal.refresh()

	def add_sphere(self, z, y, x, rad):
		center = coords[z][y][x]
		for iz in range(rad):
			for iy in range(rad):
				for ix in range(rad):
					print(math.sqrt(iz * iz + iy * iy + ix * ix))
					if math.sqrt(iz * iz + iy * iy + ix * ix) <= rad:
						self.add_sun(coords[z+iz][y+iy][x+ix])
						self.add_sun(coords[z+iz][y+iy][x-ix])
						self.add_sun(coords[z+iz][y-iy][x+ix])
						self.add_sun(coords[z+iz][y-iy][x-ix])
						self.add_sun(coords[z-iz][y+iy][x+ix])
						self.add_sun(coords[z-iz][y+iy][x-ix])
						self.add_sun(coords[z-iz][y-iy][x+ix])
						#if math.sqrt(iz * iz + iy * iy + ix * ix) <= -rad:
						self.add_sun(coords[z-iz][y-iy][x-ix])

	def add_cube(self, z, y, x, rad):
		center = coords[z][y][x]
		for iz in range(rad):
			for iy in range(rad):
				for ix in range(rad):
					self.add_sun(coords[z+iz][y+iy][x+ix])
					self.add_sun(coords[z+iz][y+iy][x-ix])
					self.add_sun(coords[z+iz][y-iy][x+ix])
					self.add_sun(coords[z+iz][y-iy][x-ix])
					self.add_sun(coords[z-iz][y+iy][x+ix])
					self.add_sun(coords[z-iz][y+iy][x-ix])
					self.add_sun(coords[z-iz][y-iy][x+ix])
					#if math.sqrt(iz * iz + iy * iy + ix * ix) <= -rad:
					self.add_sun(coords[z-iz][y-iy][x-ix])

	def add_corners(self, z, y, x, rad):
		center = coords[z][y][x]
		self.add_sun(coords[z+rad][y+rad][x+rad])
		self.add_sun(coords[z+rad][y+rad][x-rad])
		self.add_sun(coords[z+rad][y-rad][x+rad])
		self.add_sun(coords[z+rad][y-rad][x-rad])
		self.add_sun(coords[z-rad][y+rad][x+rad])
		self.add_sun(coords[z-rad][y+rad][x-rad])
		self.add_sun(coords[z-rad][y-rad][x+rad])
		self.add_sun(coords[z-rad][y-rad][x-rad])

	def add_center(self, z, y, x):
		center = coords[z][y][x]
		rad = 4
		for iz in range(rad):
			izr = int(iz * math.pi)
			for iy in range(rad):
				iyr = int(iy * math.pi)
				for ix in range(rad):
					ixr = int(ix * math.pi)
					self.add_sun(coords[z+izr][y+iyr][x+ixr])
					self.add_sun(coords[z+izr][y+iyr][x-ixr])
					self.add_sun(coords[z+izr][y-iyr][x+ixr])
					self.add_sun(coords[z+izr][y-iyr][x-ixr])
					self.add_sun(coords[z-izr][y+iyr][x+ixr])
					self.add_sun(coords[z-izr][y+iyr][x-ixr])
					self.add_sun(coords[z-izr][y-iyr][x+ixr])
					self.add_sun(coords[z-izr][y-iyr][x-ixr])


	def add_sun(self, tile):
		tile.char = random.choice("☼")# ☺☻')
		tile.solid = True
		tile.type = 'G type star'
		tile.name = 'unknown'
		tile.scan = 'Scan shows water'
		tile.color = random.choice(['yellow', 'blue', 'red'])

if __name__ == '__main__':
	ascii_world = ASCII_WORLD()
print('Thank you for Playing!')
terminal.close()
