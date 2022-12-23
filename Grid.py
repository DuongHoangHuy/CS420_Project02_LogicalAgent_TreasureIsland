import pygame
pygame.init()

# AGENT = (255, 0, 0) #AGENT
# PIRATE = (0, 255, 0) #PIRATE
# GOLD = (255, 255, 0) #GOLD

MASKED = (128, 128, 128) #MASKED
SEA = (100, 149, 237) #SEA
MOUNTAIN = (0, 0, 0) # MOUNTAIN
PRISON = (0, 0, 128) #PRISON

OLIVE = (128, 128, 0)
GREEN = (0, 128, 0)
TEAL = (0, 128, 128)
BROWN = (165,42,42)
C1 = (230, 207, 212)
C2 = (199, 175, 196)
C3 = (121, 111, 140)
C4 = (193, 138, 129)
C5 = (255, 218, 176)
C6 = (243, 220, 190)
REGIONS = [SEA, OLIVE, GREEN, TEAL, C1, C2, C3, C4, C5, C6]


class Grid:
	def __init__(self, row, col, width, height, region):
		self.row = row
		self.col = col
		self.x = col * width + width
		self.y = row * height + height
		self.width = width
		self.height = height
		self.region = None
		self.entity = None
		self.is_masked = False
		self.set_region(region)
	
	def set_region(self, region): # decide what region of the grid
		entity = region[-1]
		if entity == 'M' or entity == 'P':
			self.region = REGIONS[int(region[:-1])]
			self.entity = entity
		else:
			self.region = REGIONS[int(region)]

	def get_pos(self):
		return (self.row, self.col)
	
	def is_barrier(self):
		if self.region == SEA or self.entity in ['M', 'P']:
			return True
		
		return False
	
	def make_mask(self):
		self.is_masked = True

	def draw(self, win, FONT):
		color = self.region
		if self.is_masked:
			color = MASKED
		pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))
		text = FONT.render(self.entity, True, (0,0,0))
		center_rect = (self.x + self.width/2 - text.get_rect().width/2, 
					   self.y + self.height/2 - text.get_rect().height/2)
		win.blit(text, center_rect)

	def __lt__(self, other):
		return False


# if __name__ = "__main__":
    