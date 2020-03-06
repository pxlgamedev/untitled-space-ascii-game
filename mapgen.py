from bearlibterminal import terminal
from tilecreator import NewTile
import random
import math

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
		self.root = [0,0,0]
		self.multitile = False
		# store the current animation frame
		self.anim = ''

class MapGen:
	def make_sector(main, depth, height, width):
		terminal.printf(main.center_text('Scanning sector...'), 12, 'Scanning sector...')
		loading = int(main.window_center - depth / 2)
		center = [int(depth /2), int(height /2), int(width /2)]
		map_layer = []
		for z in range(depth):
			map_height = []
			for y in range(height):
				map_width = []
				for x in range(width):
					tile = Object()
					chance = random.randrange(0, 10000)
					if chance < 9800:
						NewTile.empty_space(tile)
					elif chance < 9995:
						NewTile.add_dust(tile)
					else:
						NewTile.add_sun(tile)
					map_width.append(tile)
				map_height.append(map_width)
			terminal.printf(loading + z, 14, '✦')
			terminal.refresh()
			map_layer.append(map_height)
		# test of generating a central sun for the solar_system generator
		MapGen.add_sun(map_layer, center[0],center[1],center[2], 16, MapGen.rand_color(), MapGen.rand_color())
		MapGen.add_planet(map_layer, center[0] + 24,center[1] + 24,center[2], 5, MapGen.rand_color(), MapGen.rand_color())
		print('map generated')
		terminal.printf(main.center_text('Map Generated'), 3, 'Map Generated!')
		terminal.refresh()
		return(map_layer)

	def rand_color():
		color = random.choice(['magenta','pink','red','blue','green','yellow','orange','brown','grey','indigo','purple', 'lavender'])
		shade = random.choice(['darkest ', 'darker ', 'dark ', '', 'light ', 'lighter ', 'lightest '])
		#print(shade + color)
		return shade + color

	def add_planet(map, z, y, x, rad, color, color2):
		center = map[z][y][x]
		for iz in range(rad):
			for iy in range(rad):
				for ix in range(rad):
					dist = math.sqrt(iz * iz + iy * iy + ix * ix)
					if dist < rad and dist > rad -1.5:
						NewTile.add_planet_atmo(map[z+iz][y+iy][x+ix], [z,y,x], color2)
						NewTile.add_planet_atmo(map[z+iz][y+iy][x-ix], [z,y,x], color2)
						NewTile.add_planet_atmo(map[z+iz][y-iy][x+ix], [z,y,x], color2)
						NewTile.add_planet_atmo(map[z+iz][y-iy][x-ix], [z,y,x], color2)
						NewTile.add_planet_atmo(map[z-iz][y+iy][x+ix], [z,y,x], color2)
						NewTile.add_planet_atmo(map[z-iz][y+iy][x-ix], [z,y,x], color2)
						NewTile.add_planet_atmo(map[z-iz][y-iy][x+ix], [z,y,x], color2)
						NewTile.add_planet_atmo(map[z-iz][y-iy][x-ix], [z,y,x], color2)
		rad = rad - 1
		for iz in range(rad):
			for iy in range(rad):
				for ix in range(rad):
					dist = math.sqrt(iz * iz + iy * iy + ix * ix)
					if dist < rad and dist > rad -1.5:
						NewTile.add_planet_surface(map[z+iz][y+iy][x+ix], [z,y,x], color)
						NewTile.add_planet_surface(map[z+iz][y+iy][x-ix], [z,y,x], color)
						NewTile.add_planet_surface(map[z+iz][y-iy][x+ix], [z,y,x], color)
						NewTile.add_planet_surface(map[z+iz][y-iy][x-ix], [z,y,x], color)
						NewTile.add_planet_surface(map[z-iz][y+iy][x+ix], [z,y,x], color)
						NewTile.add_planet_surface(map[z-iz][y+iy][x-ix], [z,y,x], color)
						NewTile.add_planet_surface(map[z-iz][y-iy][x+ix], [z,y,x], color)
						NewTile.add_planet_surface(map[z-iz][y-iy][x-ix], [z,y,x], color)
					if  dist < rad -1.5:
						NewTile.empty_space(map[z+iz][y+iy][x+ix])
						NewTile.empty_space(map[z+iz][y+iy][x-ix])
						NewTile.empty_space(map[z+iz][y-iy][x+ix])
						NewTile.empty_space(map[z+iz][y-iy][x-ix])
						NewTile.empty_space(map[z-iz][y+iy][x+ix])
						NewTile.empty_space(map[z-iz][y+iy][x-ix])
						NewTile.empty_space(map[z-iz][y-iy][x+ix])
						NewTile.empty_space(map[z-iz][y-iy][x-ix])

	def add_sun(map, z, y, x, rad, color, color2):
		center = map[z][y][x]
		for iz in range(rad):
			for iy in range(rad):
				for ix in range(rad):
					dist = math.sqrt(iz * iz + iy * iy + ix * ix)
					if dist < rad and dist > rad -1.5:
						NewTile.add_stellar_corona(map[z+iz][y+iy][x+ix], [z,y,x], color2)
						NewTile.add_stellar_corona(map[z+iz][y+iy][x-ix], [z,y,x], color2)
						NewTile.add_stellar_corona(map[z+iz][y-iy][x+ix], [z,y,x], color2)
						NewTile.add_stellar_corona(map[z+iz][y-iy][x-ix], [z,y,x], color2)
						NewTile.add_stellar_corona(map[z-iz][y+iy][x+ix], [z,y,x], color2)
						NewTile.add_stellar_corona(map[z-iz][y+iy][x-ix], [z,y,x], color2)
						NewTile.add_stellar_corona(map[z-iz][y-iy][x+ix], [z,y,x], color2)
						NewTile.add_stellar_corona(map[z-iz][y-iy][x-ix], [z,y,x], color2)
		rad = rad - 1
		for iz in range(rad):
			for iy in range(rad):
				for ix in range(rad):
					dist = math.sqrt(iz * iz + iy * iy + ix * ix)
					if dist < rad and dist > rad -1.5:
						NewTile.add_stellar_surface(map[z+iz][y+iy][x+ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z+iz][y+iy][x-ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z+iz][y-iy][x+ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z+iz][y-iy][x-ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z-iz][y+iy][x+ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z-iz][y+iy][x-ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z-iz][y-iy][x+ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z-iz][y-iy][x-ix], [z,y,x], color)
					if  dist < rad -1.5:
						NewTile.empty_space(map[z+iz][y+iy][x+ix])
						NewTile.empty_space(map[z+iz][y+iy][x-ix])
						NewTile.empty_space(map[z+iz][y-iy][x+ix])
						NewTile.empty_space(map[z+iz][y-iy][x-ix])
						NewTile.empty_space(map[z-iz][y+iy][x+ix])
						NewTile.empty_space(map[z-iz][y+iy][x-ix])
						NewTile.empty_space(map[z-iz][y-iy][x+ix])
						NewTile.empty_space(map[z-iz][y-iy][x-ix])

	def add_sphere_hollow(map, z, y, x, rad, color):
		center = map[z][y][x]
		for iz in range(rad):
			for iy in range(rad):
				for ix in range(rad):
					dist = math.sqrt(iz * iz + iy * iy + ix * ix)
					if dist < rad and dist > rad -1.5:
						NewTile.add_stellar_surface(map[z+iz][y+iy][x+ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z+iz][y+iy][x-ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z+iz][y-iy][x+ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z+iz][y-iy][x-ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z-iz][y+iy][x+ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z-iz][y+iy][x-ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z-iz][y-iy][x+ix], [z,y,x], color)
						NewTile.add_stellar_surface(map[z-iz][y-iy][x-ix], [z,y,x], color)
					if  dist < rad -1.5:
						NewTile.empty_space(map[z+iz][y+iy][x+ix])
						NewTile.empty_space(map[z+iz][y+iy][x-ix])
						NewTile.empty_space(map[z+iz][y-iy][x+ix])
						NewTile.empty_space(map[z+iz][y-iy][x-ix])
						NewTile.empty_space(map[z-iz][y+iy][x+ix])
						NewTile.empty_space(map[z-iz][y+iy][x-ix])
						NewTile.empty_space(map[z-iz][y-iy][x+ix])
						NewTile.empty_space(map[z-iz][y-iy][x-ix])
'''
	def add_sphere_solid(self, z, y, x, rad):
		center = self.coords[z][y][x]
		for iz in range(rad):
			for iy in range(rad):
				for ix in range(rad):
					dist = math.sqrt(iz * iz + iy * iy + ix * ix)
					if dist < rad:
						self.add_sun(coords[z+iz][y+iy][x+ix])
						self.add_sun(coords[z+iz][y+iy][x-ix])
						self.add_sun(coords[z+iz][y-iy][x+ix])
						self.add_sun(coords[z+iz][y-iy][x-ix])
						self.add_sun(coords[z-iz][y+iy][x+ix])
						self.add_sun(coords[z-iz][y+iy][x-ix])
						self.add_sun(coords[z-iz][y-iy][x+ix])
						self.add_sun(coords[z-iz][y-iy][x-ix])

	def add_cube(self, z, y, x, rad):
		center = self.coords[z][y][x]
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
		center = self.coords[z][y][x]
		self.add_sun(coords[z+rad][y+rad][x+rad])
		self.add_sun(coords[z+rad][y+rad][x-rad])
		self.add_sun(coords[z+rad][y-rad][x+rad])
		self.add_sun(coords[z+rad][y-rad][x-rad])
		self.add_sun(coords[z-rad][y+rad][x+rad])
		self.add_sun(coords[z-rad][y+rad][x-rad])
		self.add_sun(coords[z-rad][y-rad][x+rad])
		self.add_sun(coords[z-rad][y-rad][x-rad])

	def add_center(self, z, y, x):
		center = self.coords[z][y][x]
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
'''
