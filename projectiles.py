import math
import pygame
from particles import Explosion

WIDTH, HEIGHT = 640, 384

pygame.mixer.init()
grenade_blast_fx = pygame.mixer.Sound('Sounds/grenade blast.wav')
grenade_blast_fx.set_volume(0.6)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, color, type_, win, angle=0, speed=10):
		super(Bullet, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.color = color
		self.type = type_
		self.win = win
		self.angle = angle  # Pour les tirs en éventail

		self.speed = speed
		self.radius = 4
		
		# Calcul des vitesses selon l'angle
		if angle != 0:
			self.speed_x = self.speed * math.cos(math.radians(angle))
			self.speed_y = self.speed * math.sin(math.radians(angle))
		else:
			self.speed_x = self.speed * direction if direction != 0 else self.speed
			self.speed_y = 0
		
		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

	def update(self, screen_scroll, world):
		# Mouvement selon l'angle pour le shotgun
		if self.angle != 0:
			self.x += self.speed_x + screen_scroll
			self.y += self.speed_y
		else:
			# Mouvement normal pour les balles classiques
			if self.direction == -1:
				self.x -= self.speed + screen_scroll
			if self.direction == 0 or self.direction == 1:
				self.x += self.speed + screen_scroll

		# Supprimer si sort de l'écran
		if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
			self.kill()

		for tile in world.ground_list:
			if tile[1].collidepoint(self.x, self.y):
				self.kill()
		for tile in world.rock_list:
			if tile[1].collidepoint(self.x, self.y):
				self.kill()

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

class Grenade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, win):
		super(Grenade, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.win = win

		self.speed = 10
		self.vel_y = -11
		self.timer = 15
		self.radius = 4

		if self.direction == 0:
			self.direction = 1

		pygame.draw.circle(self.win, (200, 200, 200), (self.x, self.y), self.radius+1)
		self.rect = pygame.draw.circle(self.win, (255, 50, 50), (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 1)

	def update(self, screen_scroll, p, enemy_group, explosion_group, world):
		self.vel_y += 1
		dx = self.direction * self.speed
		dy = self.vel_y

		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
				if self.rect.y <= tile[1].y:
					dy = 0
					self.speed -= 1
					if self.speed <= 0:
						self.speed = 0

		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
				self.direction *= -1
				dx = self.direction * self.speed
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
				if self.rect.y <= tile[1].y:
					dy = 0
					self.speed -= 1
					if self.speed <= 0:
						self.speed = 0

		if self.rect.y > WIDTH:
			self.kill()

		if self.speed == 0:
			self.timer -= 1
			if self.timer <= 0:
				grenade_blast_fx.play()
				for _ in range(30):
					explosion = Explosion(self.x, self.y, self.win)
					explosion_group.add(explosion)

				p_distance = math.sqrt((p.rect.centerx - self.x) ** 2 + (p.rect.centery - self.y) ** 2 )
				if p_distance <= 100:
					if p_distance > 80:
						p.health -= 20
					elif p_distance > 40:
						p.health -= 50
					elif p_distance >= 0:
						p.health -= 80
					p.hit = True

				for e in enemy_group:
					e_distance = math.sqrt((e.rect.centerx - self.x) ** 2 + (e.rect.centery - self.y) ** 2)
					if e_distance < 80:
						e.health -= 100

				self.kill()
 
		self.x += dx + screen_scroll
		self.y += dy

		pygame.draw.circle(self.win, (200, 200, 200), (self.x, self.y), self.radius+1)
		self.rect = pygame.draw.circle(self.win, (255, 50, 50), (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 1)