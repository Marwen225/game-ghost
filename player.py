import pygame

WIDTH, HEIGHT = 640, 384

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Player, self).__init__()
		self.x = x
		self.y = y

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []

		self.size = 24

		for i in range(1,3):
			image = pygame.image.load(f'Assets/Player/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.idle_list.append(image)
		for i in range(1,6):
			image = pygame.image.load(f'Assets/Player/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (24, 24))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 5):
			image = pygame.image.load(f'Assets/Player/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.attack_list.append(image)
		for i in range(1,11):
			image = pygame.image.load(f'Assets/Player/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'Assets/Player/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.fall_index = 0

		self.jump_height = 15
		self.speed = 3
		self.sprint_speed = 6  # Vitesse de sprint (2x plus rapide)
		self.is_sprinting = False
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False
		self.double_jump_available = True  # Permet un double saut
		self.has_double_jumped = False     # Vérifie si déjà utilisé
		
		# Variables pour l'accrochage au mur (wall-grab)
		self.wall_grab_available = False
		self.is_wall_grabbing = False
		self.touching_wall = False
		self.wall_side = 0  # -1 = mur à gauche, 1 = mur à droite
		self.wall_slide_speed = 1  # Vitesse de glissement lent sur le mur
		self.wall_climb_speed = 2  # Vitesse de montée sur le mur
		self.wall_grab_stamina = 120  # Stamina pour s'accrocher (2 secondes)
		self.wall_grab_timer = 0   # Timer actuel
		self.max_wall_grab_timer = self.wall_grab_stamina  # Timer maximum pour l'affichage

		# Effets de dégâts
		self.damage_flash_timer = 0  # Timer pour le clignotement rouge
		self.damage_flash_duration = 30  # Durée du clignotement (frames)
		self.invulnerable_timer = 0  # Timer d'invulnérabilité
		self.invulnerable_duration = 60  # Durée d'invulnérabilité après dégâts

		self.grenades = 5
		self.health = 100
		
		# Système d'armes
		self.current_weapon = 0  # 0 = Pistolet, 1 = Shotgun
		self.weapon_names = ["Pistolet", "Shotgun"]
		self.ammo_shotgun = 20  # Munitions pour le shotgun
		
		# === SYSTÈME DE COMPÉTENCES ===
		self.unlocked_skills = []  # Liste des compétences débloquées
		
		# Compétence 1: Charge Shot (débloquée niveau 2)
		self.charge_shot_available = False
		self.charge_timer = 0
		self.max_charge_time = 60  # 1 seconde de charge
		self.is_charging = False
		self.charge_particles = []
		
		# Compétence 2: Bouclier + Mode Rafale (débloquée niveau 3)
		self.shield_available = False
		self.shield_active = False
		self.shield_hits = 0  # Compteur d'attaques absorbées
		self.shield_max_hits = 2
		self.shield_duration = 600  # 10 secondes
		self.shield_timer = 0
		self.shield_cooldown = 1200  # 20 secondes
		self.shield_cooldown_timer = 0
		
		# Mode rafale
		self.rapid_fire_available = False
		self.rapid_fire_active = False
		self.rapid_fire_duration = 300  # 5 secondes
		self.rapid_fire_timer = 0
		self.rapid_fire_charge = 0  # Charge obtenue en tuant des ennemis
		self.rapid_fire_max_charge = 5  # 5 kills pour activer

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		# Reset wall detection
		self.touching_wall = False
		self.wall_side = 0
		
		# Checking collision with ground
		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# above ground
				if self.rect.y + dy <= tile[1].y:
					dy = tile[1].top - self.rect.bottom
					# Réinitialiser le double saut et l'accrochage quand on touche le sol
					self.double_jump_available = True
					self.has_double_jumped = False
					self.wall_grab_available = False
					self.is_wall_grabbing = False
					self.wall_grab_timer = self.wall_grab_stamina  # Recharger stamina

		# Checking collision with rocks & stones
		for tile in world.rock_list:
			# Collision horizontale (murs)
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# Détecter quel côté du mur on touche
				if dx > 0:  # Se déplace vers la droite, mur à droite
					self.wall_side = 1
					self.touching_wall = True
				elif dx < 0:  # Se déplace vers la gauche, mur à gauche
					self.wall_side = -1
					self.touching_wall = True
				dx = 0
				
				# Activer l'accrochage si on est en l'air et qu'on a de la stamina
				if self.wall_grab_timer > 0:
					self.wall_grab_available = True
					
			# Collision verticale
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					self.jump = False
					self.vel = self.jump_height
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					# Réinitialiser le double saut et l'accrochage quand on touche le sol
					self.double_jump_available = True
					self.has_double_jumped = False
					self.wall_grab_available = False
					self.is_wall_grabbing = False
					self.wall_grab_timer = self.wall_grab_stamina  # Recharger stamina

		return dx, dy

	def perform_double_jump(self):
		"""Permet d'effectuer un double saut si disponible"""
		if self.double_jump_available and not self.has_double_jumped:
			self.vel = self.jump_height * 0.8  # Double saut un peu moins haut
			self.has_double_jumped = True
			return True
		return False

	def start_wall_grab(self):
		"""Commence à s'accrocher au mur"""
		if self.wall_grab_available and self.touching_wall and self.wall_grab_timer > 0:
			self.is_wall_grabbing = True
			return True
		return False

	def can_wall_grab(self):
		"""Vérifie si on peut s'accrocher au mur"""
		return self.wall_grab_available and self.touching_wall and self.wall_grab_timer > 0

	def stop_wall_grab(self):
		"""Arrête de s'accrocher au mur"""
		self.is_wall_grabbing = False

	def wall_jump_from_grab(self):
		"""Effectue un saut depuis l'accrochage au mur"""
		if self.is_wall_grabbing:
			# Saut plus puissant depuis l'accrochage
			self.vel = self.jump_height * 1.2
			self.jump = True
			self.is_wall_grabbing = False
			return True
		return False

	def wall_climb(self, direction):
		"""Grimpe sur le mur (up=1, down=-1)"""
		if self.is_wall_grabbing and self.wall_grab_timer > 0:
			self.dy = -direction * self.wall_climb_speed
			# Consommer plus de stamina en grimpant
			self.wall_grab_timer -= 2
			return True
		return False

	def change_weapon(self):
		"""Change d'arme (pistolet <-> shotgun)"""
		self.current_weapon = (self.current_weapon + 1) % len(self.weapon_names)
		return self.weapon_names[self.current_weapon]

	def can_shoot(self):
		"""Vérifie si le joueur peut tirer avec l'arme actuelle"""
		if self.current_weapon == 0:  # Pistolet
			return True
		elif self.current_weapon == 1:  # Shotgun
			return self.ammo_shotgun > 0
		return False

	def shoot(self):
		"""Consomme les munitions selon l'arme"""
		if self.current_weapon == 1:  # Shotgun
			self.ammo_shotgun -= 1

	def take_damage(self, damage_amount):
		"""Applique des dégâts au joueur avec effets visuels"""
		if self.invulnerable_timer <= 0:  # Seulement si pas invulnérable
			# Vérifier si le bouclier est actif
			if self.shield_active and self.shield_hits < self.shield_max_hits:
				self.shield_hits += 1
				print(f"Bouclier activé ! Attaques restantes: {self.shield_max_hits - self.shield_hits}")
				if self.shield_hits >= self.shield_max_hits:
					self.deactivate_shield()
				return False  # Pas de dégâts grâce au bouclier
			
			self.health -= damage_amount
			self.hit = True
			
			# Activer les effets de dégâts
			self.damage_flash_timer = self.damage_flash_duration
			self.invulnerable_timer = self.invulnerable_duration
			
			return True  # Dégâts appliqués
		return False  # Pas de dégâts (invulnérable)

	# === MÉTHODES DE COMPÉTENCES ===
	def unlock_skill(self, skill_name):
		"""Débloquer une nouvelle compétence"""
		if skill_name == "charge_shot":
			self.charge_shot_available = True
			self.unlocked_skills.append("charge_shot")
			return "Charge Shot débloqué ! Maintenez Espace pour charger."
		elif skill_name == "shield_rapid":
			self.shield_available = True
			self.rapid_fire_available = True
			self.unlocked_skills.append("shield_rapid")
			return "Bouclier et Mode Rafale débloqués !"
		return "Compétence inconnue"

	def start_charge_shot(self):
		"""Commencer à charger le tir"""
		if self.charge_shot_available and not self.is_charging:
			self.is_charging = True
			self.charge_timer = 0
			return True
		return False

	def update_charge_shot(self):
		"""Mettre à jour la charge du tir"""
		if self.is_charging:
			self.charge_timer += 1
			# Ajouter des particules de charge
			if self.charge_timer % 5 == 0:  # Particules toutes les 5 frames
				self.create_charge_particle()

	def stop_charge_shot(self):
		"""Arrêter la charge et retourner le niveau de charge"""
		if self.is_charging:
			charge_level = min(self.charge_timer / self.max_charge_time, 1.0)
			self.is_charging = False
			self.charge_timer = 0
			self.charge_particles.clear()
			return charge_level
		return 0

	def create_charge_particle(self):
		"""Créer des particules de charge autour du joueur"""
		import random
		import math
		
		# Créer des particules en cercle autour du joueur
		angle = random.uniform(0, 2 * math.pi)
		distance = random.uniform(15, 25)
		x = self.rect.centerx + math.cos(angle) * distance
		y = self.rect.centery + math.sin(angle) * distance
		
		particle = {
			'x': x, 'y': y,
			'life': 30,
			'color': (100 + random.randint(0, 155), 100, 255)
		}
		self.charge_particles.append(particle)

	def activate_shield(self):
		"""Activer le bouclier"""
		if self.shield_available and not self.shield_active and self.shield_cooldown_timer <= 0:
			self.shield_active = True
			self.shield_hits = 0
			self.shield_timer = self.shield_duration
			print("Bouclier activé !")
			return True
		return False

	def deactivate_shield(self):
		"""Désactiver le bouclier"""
		if self.shield_active:
			self.shield_active = False
			self.shield_cooldown_timer = self.shield_cooldown
			print("Bouclier désactivé")

	def activate_rapid_fire(self):
		"""Activer le mode rafale"""
		if self.rapid_fire_available and not self.rapid_fire_active and self.rapid_fire_charge >= self.rapid_fire_max_charge:
			self.rapid_fire_active = True
			self.rapid_fire_timer = self.rapid_fire_duration
			self.rapid_fire_charge = 0
			print("Mode Rafale activé !")
			return True
		return False

	def add_rapid_fire_charge(self):
		"""Ajouter de la charge au mode rafale (en tuant un ennemi)"""
		if self.rapid_fire_available and self.rapid_fire_charge < self.rapid_fire_max_charge:
			self.rapid_fire_charge += 1
			print(f"Charge rafale: {self.rapid_fire_charge}/{self.rapid_fire_max_charge}")

	def can_rapid_fire(self):
		"""Vérifier si le tir rapide est disponible"""
		return self.rapid_fire_active

	def update_animation(self, is_moving=False):
		self.counter += 1
		
		# Mise à jour des timers d'effets
		if self.damage_flash_timer > 0:
			self.damage_flash_timer -= 1
		if self.invulnerable_timer > 0:
			self.invulnerable_timer -= 1
		
		# === MISE À JOUR DES COMPÉTENCES ===
		# Charge shot
		self.update_charge_shot()
		
		# Bouclier
		if self.shield_active:
			self.shield_timer -= 1
			if self.shield_timer <= 0:
				self.deactivate_shield()
		
		if self.shield_cooldown_timer > 0:
			self.shield_cooldown_timer -= 1
		
		# Mode rafale
		if self.rapid_fire_active:
			self.rapid_fire_timer -= 1
			if self.rapid_fire_timer <= 0:
				self.rapid_fire_active = False
				print("Mode Rafale terminé")
		
		# Mise à jour des particules de charge
		for particle in self.charge_particles[:]:
			particle['life'] -= 1
			if particle['life'] <= 0:
				self.charge_particles.remove(particle)
		
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.attack_list):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if not is_moving and not self.attack and not self.hit:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
				elif is_moving and not self.attack and not self.hit:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.direction == -1:
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
			elif not is_moving:
				# Utiliser l'animation idle, mais garder l'orientation du joueur
				self.image = self.idle_list[self.idle_index]
				if self.direction == -1:
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]


	def update(self, moving_left, moving_right, world, is_sprinting=False):
		self.dx = 0
		self.dy = 0
		self.is_sprinting = is_sprinting
		
		# Variable pour savoir si le joueur bouge actuellement
		is_moving = moving_left or moving_right

		# Choix de la vitesse selon le sprint
		current_speed = self.sprint_speed if self.is_sprinting else self.speed

		# Gestion de l'accrochage au mur
		if self.is_wall_grabbing:
			# Quand on s'accroche, on peut monter/descendre
			if moving_left and self.wall_side == -1:
				# Maintenir l'accrochage au mur gauche
				self.dx = 0
			elif moving_right and self.wall_side == 1:
				# Maintenir l'accrochage au mur droit
				self.dx = 0
			else:
				# Lâcher le mur si on bouge dans l'autre direction
				self.stop_wall_grab()
		else:
			# Mouvement normal
			if moving_left:
				self.dx = -current_speed
				self.direction = -1
			elif moving_right:
				self.dx = current_speed
				self.direction = 1
			else:
				# Quand on arrête de bouger, on garde la dernière direction
				if not self.jump:
					self.walk_index = 0

		if self.jump:
			F = (1/2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity

			if self.vel < -15:
				self.vel = self.jump_height
				self.jump = False
		elif self.is_wall_grabbing:
			# Accrochage au mur - pas de gravité, contrôle vertical
			self.dy = 0
			# Consommer la stamina
			self.wall_grab_timer -= 1
			if self.wall_grab_timer <= 0:
				self.stop_wall_grab()  # Plus de stamina, lâcher le mur
		else:
			# Gravité normale ou glissement sur mur
			if self.touching_wall and not self.is_wall_grabbing and self.vel > self.wall_slide_speed:
				self.dy = self.wall_slide_speed  # Glissement lent
			else:
				self.dy += self.vel

		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		# Passer l'état de mouvement à l'animation
		self.update_animation(is_moving)

		
	def draw(self, win):
		# Effet de clignotement lors des dégâts
		if self.damage_flash_timer > 0:
			if self.damage_flash_timer % 6 < 3:  # Clignotement rapide
				return  # Ne pas dessiner (effet de clignotement)
		
		# Effet de couleur rouge lors des dégâts
		if self.damage_flash_timer > 0:
			# Créer une surface rouge semi-transparente
			red_surface = self.image.copy()
			red_surface.fill((255, 50, 50), special_flags=pygame.BLEND_ADD)
			win.blit(red_surface, self.rect)
		else:
			# Affichage normal
			win.blit(self.image, self.rect)
		
		# === EFFETS VISUELS DES COMPÉTENCES ===
		# Dessiner les particules de charge
		for particle in self.charge_particles:
			pygame.draw.circle(win, particle['color'], 
							 (int(particle['x']), int(particle['y'])), 2)
		
		# Effet visuel du bouclier
		if self.shield_active:
			# Dessiner un cercle bleu autour du joueur
			shield_alpha = int(100 + 50 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
			shield_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
			pygame.draw.circle(shield_surface, (0, 150, 255, shield_alpha), (30, 30), 28, 3)
			win.blit(shield_surface, (self.rect.centerx - 30, self.rect.centery - 30))
		
		# Effet visuel du mode rafale
		if self.rapid_fire_active:
			# Aura rouge autour du joueur
			rapid_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
			glow_alpha = int(80 + 40 * abs(pygame.time.get_ticks() % 500 - 250) / 250)
			pygame.draw.circle(rapid_surface, (255, 100, 100, glow_alpha), (20, 20), 18)
			win.blit(rapid_surface, (self.rect.centerx - 20, self.rect.centery - 20))
