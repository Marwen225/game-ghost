import pygame
import random

class Trail(pygame.sprite.Sprite):
	def __init__(self, pos, color, win):
		super(Trail, self).__init__()
		self.color = color
		self.win = win

		self.x, self.y = pos
		self.y += 10
		self.dx = random.randint(0,20) / 10 - 1
		self.dy = -2
		self.size = random.randint(4,7)

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.size)

	def update(self):
		self.x -= self.dx
		self.y -= self.dy
		self.size -= 0.1

		if self.size <= 0:
			self.kill()

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.size)

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Explosion, self).__init__()
		self.x = x
		self.y = y
		self.win = win

		self.size = random.randint(4,9)
		self.life = 40
		self.lifetime = 0

		self.x_vel = random.randrange(-4, 4)
		self.y_vel = random.randrange(-4, 4)
		
		self.color = 150
			
	def update (self, screen_scroll):
		self.size -= 0.2
		self.lifetime += 1
		self.color -= 2
		if self.lifetime <= self.life:
			self.x += self.x_vel + screen_scroll
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(self.win, (self.color, self.color, self.color), (self.x, self.y,s,s))
		else:
			self.kill()

class DamageParticle(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(DamageParticle, self).__init__()
		self.x = x
		self.y = y
		self.win = win

		self.size = random.randint(3, 6)
		self.life = 30
		self.lifetime = 0

		self.x_vel = random.randrange(-6, 6)
		self.y_vel = random.randrange(-8, -2)
		
		self.color_red = 255
		self.color_green = random.randint(0, 50)
		self.color_blue = 0
			
	def update(self, screen_scroll):
		self.size -= 0.1
		self.lifetime += 1
		self.color_red -= 3
		self.color_green -= 1
		
		if self.lifetime <= self.life and self.size > 0:
			self.x += self.x_vel + screen_scroll
			self.y += self.y_vel
			self.y_vel += 0.3  # Gravité
			
			s = int(self.size)
			color = (max(0, self.color_red), max(0, self.color_green), self.color_blue)
			pygame.draw.circle(self.win, color, (int(self.x), int(self.y)), s)
		else:
			self.kill()