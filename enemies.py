import random
import math
import pygame
from projectiles import Bullet

TILE_SIZE = 16

pygame.mixer.init()
bullet_fx = pygame.mixer.Sound('Sounds/ghost_shot.mp3')

class Ghost(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Ghost, self).__init__()

		self.x = x
		self.y = y
		self.win = win
		self.initial_pos_x = x

		self.size = 32

		self.walk_left = []
		self.walk_right = []
		self.hit_list = []
		self.death_list = []

		for i in range(1,6):
			image = pygame.image.load(f'Assets/Ghost/Enemywalk{i}.png')
			right = right = pygame.transform.scale(image, (self.size, self.size))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 3):
			image = pygame.image.load(f'Assets/Ghost/Enemyhit{i}.png')
			image = pygame.transform.scale(image, (self.size, self.size))
			self.hit_list.append(image)
		for i in range(1,9):
			image = pygame.image.load(f'Assets/Ghost/Enemydead{i}.png')
			image = pygame.transform.scale(image, (self.size, self.size))
			self.death_list.append(image)

		self.walk_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.counter = 0

		self.dx = random.choice([-1, 1])
		self.alive = True
		self.health = 100
		self.hit = False
		self.on_death_bed = False

		self.image = self.walk_right[self.walk_index]
		self.rect = self.image.get_rect(center=(self.x, self.y))

	def update(self, screen_scroll, bullet_group, p):
		if self.health:
			self.rect.x += (self.dx + screen_scroll)
			self.x += screen_scroll
			if abs(self.rect.x - self.x) >= 2 * TILE_SIZE:
				self.dx *= -1

		if self.health <= 0:
			self.on_death_bed = True

		self.counter += 1
		if self.counter % 5 == 0:
			if self.on_death_bed:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.kill()
					self.alive = False
			if self.hit:
				self.hit_index += 1
				if self.hit_index >= len(self.hit_list):
					self.hit_index = 0
					self.hit = False
			else:
				self.walk_index  = (self.walk_index + 1) % len(self.walk_left)
				
		if self.counter % 50 == 0:
			if self.health > 0 and (abs(p.rect.x - self.rect.x) <= 200):
				x, y = self.rect.center
				direction = self.dx
				bullet = Bullet(x, y, direction, (160, 160, 160), 2, self.win)
				bullet_group.add(bullet)
				bullet_fx.play()

		if self.alive:
			if self.on_death_bed:
				self.image = self.death_list[self.death_index]
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
			else:
				if self.dx == -1:
					self.image = self.walk_left[self.walk_index]
				elif self.dx == 1:
					self.image = self.walk_right[self.walk_index]

	def draw(self, win):
		win.blit(self.image, self.rect)

class FlyingGhost(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(FlyingGhost, self).__init__()

		self.x = x
		self.y = y
		self.initial_x = x
		self.initial_y = y
		self.win = win

		self.size = 28

		self.walk_left = []
		self.walk_right = []
		self.hit_list = []
		self.death_list = []

		# Utiliser les mêmes sprites mais avec une couleur différente
		for i in range(1,6):
			image = pygame.image.load(f'Assets/Ghost/Enemywalk{i}.png')
			right = pygame.transform.scale(image, (self.size, self.size))
			# Teinter en bleu pour différencier
			right.fill((100, 100, 255), special_flags=pygame.BLEND_ADD)
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 3):
			image = pygame.image.load(f'Assets/Ghost/Enemyhit{i}.png')
			image = pygame.transform.scale(image, (self.size, self.size))
			image.fill((100, 100, 255), special_flags=pygame.BLEND_ADD)
			self.hit_list.append(image)
		for i in range(1,9):
			image = pygame.image.load(f'Assets/Ghost/Enemydead{i}.png')
			image = pygame.transform.scale(image, (self.size, self.size))
			image.fill((100, 100, 255), special_flags=pygame.BLEND_ADD)
			self.death_list.append(image)

		self.walk_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.counter = 0

		# Comportement de vol
		self.dx = 1
		self.dy = 0
		self.flight_radius = 80  # Rayon de vol autour du point initial
		self.speed = 1.5
		self.chase_range = 150  # Distance à laquelle il commence à poursuivre
		
		self.alive = True
		self.health = 75  # Moins de vie que le fantôme normal
		self.hit = False
		self.on_death_bed = False

		self.image = self.walk_right[self.walk_index]
		self.rect = self.image.get_rect(center=(self.x, self.y))

	def update(self, screen_scroll, bullet_group, p):
		if self.health > 0:
			# Calcul de la distance au joueur
			player_distance = ((p.rect.centerx - self.rect.centerx) ** 2 + (p.rect.centery - self.rect.centery) ** 2) ** 0.5
			
			if player_distance <= self.chase_range:
				# Mode poursuite : voler vers le joueur
				if p.rect.centerx > self.rect.centerx:
					self.dx = self.speed
				else:
					self.dx = -self.speed
				
				if p.rect.centery > self.rect.centery:
					self.dy = self.speed * 0.7
				else:
					self.dy = -self.speed * 0.7
			else:
				# Mode patrol : vol en cercle autour du point initial
				self.counter += 1
				angle = self.counter * 0.02  # Plus lent
				target_x = self.initial_x + math.cos(angle) * 40  # Rayon réduit
				target_y = self.initial_y + math.sin(angle) * 30  # Rayon vertical réduit
				
				if target_x > self.rect.centerx:
					self.dx = self.speed * 0.5
				else:
					self.dx = -self.speed * 0.5
				
				if target_y > self.rect.centery:
					self.dy = self.speed * 0.3
				else:
					self.dy = -self.speed * 0.3

			# Mise à jour de la position avec limites
			new_x = self.rect.x + self.dx + screen_scroll
			new_y = self.rect.y + self.dy
			
			# Limiter aux bords de l'écran (avec une marge)
			if new_x > -50 and new_x < 640 + 50:
				self.rect.x = new_x
				self.x += screen_scroll
			if new_y > -50 and new_y < 384 + 50:
				self.rect.y = new_y

		if self.health <= 0:
			self.on_death_bed = True

		self.counter += 1
		# Animation
		if self.counter % 7 == 0:
			if self.on_death_bed:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.kill()
					self.alive = False
			if self.hit:
				self.hit_index += 1
				if self.hit_index >= len(self.hit_list):
					self.hit_index = 0
					self.hit = False
			else:
				self.walk_index  = (self.walk_index + 1) % len(self.walk_left)
				
		# Tir moins fréquent que le fantôme normal
		if self.counter % 80 == 0:
			if self.health > 0 and player_distance <= 180:
				x, y = self.rect.center
				direction = 1 if self.dx > 0 else -1
				bullet = Bullet(x, y, direction, (100, 100, 255), 2, self.win)
				bullet_group.add(bullet)
				bullet_fx.play()

		# Sélection de l'image
		if self.alive:
			if self.on_death_bed:
				self.image = self.death_list[self.death_index]
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
			else:
				if self.dx < 0:
					self.image = self.walk_left[self.walk_index]
				else:
					self.image = self.walk_right[self.walk_index]

	def draw(self, win):
		win.blit(self.image, self.rect)