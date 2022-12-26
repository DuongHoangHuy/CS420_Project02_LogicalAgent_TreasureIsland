import pygame
pygame.init()

AGENT = (198, 81, 97) #AGENT
PIRATE = (214, 16, 16) #PIRATE
GOLD = (250, 211, 82) #GOLD

MOUNTAIN = (0, 0, 0) # MOUNTAIN
PRISON = (0, 0, 128) # PRISON

MASKED = (128, 128, 128) # MASKED
SEA = (61, 146, 194) # SEA
C1 = (183, 169, 204)
C2 = (140, 101, 134)
C3 = (214, 172, 139)
C4 = (98, 138, 113)
C5 = (184, 155, 150)
C6 = (160, 154, 86)
C7 = (161, 128, 96)
C8 = (189, 123, 55)
C9 = (93, 115, 78)
C10 = (168, 188, 172)

REGIONS = [SEA, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10]


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

	def is_mountain(self):
		if self.entity == 'M':
			return True
		return False
	
	def is_sea(self):
		if self.region == SEA:
			return True
		return False 
		
	def make_masked(self):
		self.is_masked = True

	def draw(self, win, FONT):
		region_color = self.region
		if self.is_masked:
			region_color = MASKED
		pygame.draw.rect(win, region_color, (self.x, self.y, self.width, self.height))

		entity_color = (0,0,0)
		if self.entity == 'T':
			entity_color = GOLD
		elif self.entity == 'A':
			entity_color = AGENT
		elif self.entity == 'Pi':
			entity_color = PIRATE
		elif self.entity == 'P':
			entity_color = PRISON
		elif self.entity == 'M':
			entity_color = MOUNTAIN

		text = FONT.render(self.entity, True, entity_color)
		center_rect = (self.x + self.width/2 - text.get_rect().width/2, 
					   self.y + self.height/2 - text.get_rect().height/2)
		win.blit(text, center_rect)

	def __lt__(self, other):
		return False


# if __name__ = "__main__":
    