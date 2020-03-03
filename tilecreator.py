import random
prefix = ['So', 'Me', 'Ro', 'Bee', 'Adj', 'Mo', 'Per', 'Ira', 'Eur', 'Red', 'Raj', 'Edo']
mid = ["'", '-','ro','sie','ez','for','lo','ta',' ','for','rah','o','la','por','v']
suffix = ['l','alo','pah','ren','ex','vor','dahl','ern','ahv','ma','ex','en','ta','le']
# G F K 1.2% habitable rate
stars = [
		['blue', 'O type star', 'Scans show radiation'],
		['white', 'B type star', 'Scans show radio waves'],
		['yellow', 'G type star', 'Scans show water'],
		['orange', 'F type star', 'Scans Planet in habitable zone'],
		['red', 'K type star', 'Scans show water'],
		]

class NewTile:
	def empty_space(tile):
		tile.char = ' '
		tile.solid = False
		tile.type = ''
		tile.name = ''
		tile.scan = ''

	def add_dust(tile):
		tile.char = random.choice(".,'") # '♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼')
		tile.solid = False
		tile.type = 'Dust'

	def add_sun(tile):
		chance = random.randrange(0, 100)
		if chance < 90:
			star = random.choice(stars)
		elif chance < 95:
			star = random.choice(stars)
		else:
			star = random.choice(stars)
		if chance < 50:
			name = random.choice(prefix) + random.choice(mid) + random.choice(suffix)
		elif chance < 70:
			name = random.choice(prefix) + random.choice(mid) + random.choice(mid) + random.choice(suffix)
		elif chance < 90:
			name = random.choice(prefix) + random.choice(suffix)
		else:
			name = random.choice(prefix) + random.choice(suffix) + random.choice(mid) + random.choice(suffix)
		tile.char = "☼"
		tile.solid = True
		tile.type = star[1]
		tile.name = name
		tile.scan = star[2]
		tile.color = star[0]

	def add_stellar_surface(tile, center):
		tile.char = '◘'
		tile.name = ''
		tile.type = ''
		tile.scan = ''
		tile.color = ''
		tile.solid = True
		tile.root = center
		tile.multitile = True
