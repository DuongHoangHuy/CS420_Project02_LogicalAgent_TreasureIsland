import pygame
from helpers.constant import REGIONS, SEA
pygame.init()

AGENT = (198, 50, 135)#AGENT
GOLD = (250, 211, 82) #GOLD

MOUNTAIN = (0, 0, 0) # MOUNTAIN
PRISON = (0, 0, 128) # PRISON

MASKED = (128, 128, 128) # MASKED


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
			self.region = int(region[:-1])
			self.entity = entity
		else:
			self.region = int(region)

	def get_pos(self):
		return (self.row, self.col)
	
	def is_barrier(self):
		if self.is_sea() or self.entity in ['M']:
			return True
		return False

	def is_mountain(self):
		if self.entity == 'M':
			return True
		return False
	
	def is_sea(self):
		if self.region == 0:
			return True
		return False 
		
	def make_masked(self):
		self.is_masked = True
	

	def draw(self, win, FONT):
		region_color = REGIONS[self.region]
		if self.is_masked:
			region_color = MASKED
		pygame.draw.rect(win, region_color, (self.x, self.y, self.width, self.height))

		entity_color = (0,0,0)
		if self.entity == 'T':
			entity_color = region_color #GOLD
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


# if __name__ == "__main__":
# 	grid = Grid(1,1,1,1, '0')
# 	print(grid.is_sea())