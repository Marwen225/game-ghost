import pygame

from world import World, load_level
from player import Player
from enemies import Ghost
from particles import Trail, DamageParticle
from projectiles import Bullet, Grenade
from button import Button
from texts import Text, Message, BlinkingText, MessageBox

pygame.init()

WIDTH, HEIGHT = 640, 384
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
TILE_SIZE = 16

clock = pygame.time.Clock()
FPS = 45

# IMAGES **********************************************************************

BG1 = pygame.transform.scale(pygame.image.load('assets/BG1.png'), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load('assets/BG2.png'), (WIDTH, HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load('assets/BG3.png'), (WIDTH, HEIGHT))
MOON = pygame.transform.scale(pygame.image.load('assets/moon.png'), (300, 220))

# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
instructions_font = 'Fonts/BubblegumSans-Regular.ttf'
# about_font = 'Fonts/DalelandsUncialBold-82zA.ttf'

ghostbusters = Message(WIDTH//2 + 50, HEIGHT//2 - 90, 90, "GhostBusters", title_font, (255, 255, 255), win)
left_key = Message(WIDTH//2 + 10, HEIGHT//2 - 90, 20, "Press left arrow key to go left", instructions_font, (255, 255, 255), win)
right_key = Message(WIDTH//2 + 10, HEIGHT//2 - 65, 20, "Press right arrow key to go right", instructions_font, (255, 255, 255), win)
up_key = Message(WIDTH//2 + 10, HEIGHT//2 - 45, 20, "Press up arrow key to jump (double jump + wall-grab!)", instructions_font, (255, 255, 255), win)
space_key = Message(WIDTH//2 + 10, HEIGHT//2 - 25, 20, "Press space key to shoot", instructions_font, (255, 255, 255), win)
g_key = Message(WIDTH//2 + 10, HEIGHT//2 - 5, 20, "Press g key to throw grenade", instructions_font, (255, 255, 255), win)
shift_key = Message(WIDTH//2 + 10, HEIGHT//2 + 15, 20, "Press shift to sprint", instructions_font, (255, 255, 255), win)
tab_key = Message(WIDTH//2 + 10, HEIGHT//2 + 35, 20, "Press tab to change weapon", instructions_font, (255, 255, 255), win)
wall_grab_key = Message(WIDTH//2 + 10, HEIGHT//2 + 55, 20, "Press C to grab wall, W/S to climb", instructions_font, (255, 255, 255), win)
game_won_msg = Message(WIDTH//2 + 10, HEIGHT//2 - 5, 20, "You have won the game", instructions_font, (255, 255, 255), win)


t = Text(instructions_font, 18)
font_color = (12, 12, 12)
play = t.render('Play', font_color)
about = t.render('About', font_color)
controls = t.render('Controls', font_color)
exit = t.render('Exit', font_color)
main_menu = t.render('Main Menu', font_color)

about_font = pygame.font.SysFont('Times New Roman', 20)
with open('Data/about.txt') as f:
	info = f.read().replace('\n', ' ')

# BUTTONS *********************************************************************

ButtonBG = pygame.image.load('Assets/ButtonBG.png')
bwidth = ButtonBG.get_width()

play_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2, ButtonBG, 0.5, play, 10)
about_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 35, ButtonBG, 0.5, about, 10)
controls_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 70, ButtonBG, 0.5, controls, 10)
exit_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 105, ButtonBG, 0.5, exit, 10)
main_menu_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 130, ButtonBG, 0.5, main_menu, 20)

# MUSIC ***********************************************************************

pygame.mixer.music.load('Sounds/mixkit-complex-desire-1093.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

diamond_fx = pygame.mixer.Sound('Sounds/point.mp3')
diamond_fx.set_volume(0.6)
bullet_fx = pygame.mixer.Sound('Sounds/bullet.wav')
jump_fx = pygame.mixer.Sound('Sounds/jump.mp3')
health_fx = pygame.mixer.Sound('Sounds/health.wav')
menu_click_fx = pygame.mixer.Sound('Sounds/menu.mp3')
next_level_fx = pygame.mixer.Sound('Sounds/level.mp3')
grenade_throw_fx = pygame.mixer.Sound('Sounds/grenade throw.wav')
grenade_throw_fx.set_volume(0.6)

# GROUPS **********************************************************************

trail_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
damage_particle_group = pygame.sprite.Group()  # Particules de dégâts

objects_group = [water_group, diamond_group, potion_group, enemy_group, exit_group]

p_image = pygame.transform.scale(pygame.image.load('Assets/Player/PlayerIdle1.png'), (32,32))
p_rect = p_image.get_rect(center=(470, 200))
p_dy = 1
p_ctr = 1

# LEVEL VARIABLES **************************************************************

ROWS = 24
COLS = 40
SCROLL_THRES = 200
MAX_LEVEL = 3

level = 1
level_length = 0
screen_scroll = 0
bg_scroll = 0
dx = 0

# SCREEN SHAKE VARIABLES *******************************************************
screen_shake = 0
screen_shake_intensity = 5

# RESET ***********************************************************************

def reset_level(level):
	trail_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	enemy_group.empty()
	water_group.empty()
	diamond_group.empty()
	potion_group.empty()
	exit_group.empty()
	damage_particle_group.empty()  # Vider les particules de dégâts

	# LOAD LEVEL WORLD

	world_data, level_length = load_level(level)
	w = World(objects_group)
	w.generate_world(world_data, win)

	return world_data, level_length, w

def reset_player():
	p = Player(250, 50)
	moving_left = False
	moving_right = False
	is_sprinting = False

	return p, moving_left, moving_right, is_sprinting

# MAIN GAME *******************************************************************

main_menu = True
about_page = False
controls_page = False
exit_page = False
game_start = False
game_won = True
running = True
while running:
	win.fill((0,0,0))
	
	# Calcul de la secousse d'écran
	shake_x = 0
	shake_y = 0
	if screen_shake > 0:
		import random
		shake_x = random.randint(-screen_shake_intensity, screen_shake_intensity)
		shake_y = random.randint(-screen_shake_intensity, screen_shake_intensity)
		screen_shake -= 1
	
	for x in range(5):
		win.blit(BG1, ((x*WIDTH) - bg_scroll * 0.6 + shake_x, 0 + shake_y))
		win.blit(BG2, ((x*WIDTH) - bg_scroll * 0.7 + shake_x, 0 + shake_y))
		win.blit(BG3, ((x*WIDTH) - bg_scroll * 0.8 + shake_x, 0 + shake_y))

	if not game_start:
		win.blit(MOON, (-40 + shake_x, 150 + shake_y))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_UP:
				if p.is_wall_grabbing:
					# Saut depuis l'accrochage au mur
					if p.wall_jump_from_grab():
						jump_fx.play()
				elif not p.jump and not p.has_double_jumped:
					# Saut normal
					p.jump = True
					jump_fx.play()
				elif p.double_jump_available and not p.has_double_jumped:
					# Double saut
					if p.perform_double_jump():
						jump_fx.play()
			
			# Contrôles pour l'accrochage au mur
			if event.key == pygame.K_c:
				if p.can_wall_grab():
					p.start_wall_grab()
			
			# Contrôles des compétences
			if event.key == pygame.K_v:
				# Activer le bouclier
				if p.activate_shield():
					print("🛡️ Bouclier activé!")
			if event.key == pygame.K_x:
				# Activer le mode rafale
				if p.activate_rapid_fire():
					print("🔥 Mode Rafale activé!")
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				is_sprinting = True
			if event.key == pygame.K_TAB:
				# Changer d'arme
				weapon_name = p.change_weapon()
				print(f"Arme: {weapon_name}")
			if event.key == pygame.K_SPACE:
				# Commencer la charge si charge shot disponible
				if p.charge_shot_available:
					p.start_charge_shot()
				elif p.can_shoot():
					# Tir normal si pas de charge shot
					x, y = p.rect.center
					direction = p.direction
					
					if p.current_weapon == 0:  # Pistolet normal
						bullet = Bullet(x, y, direction, (240, 240, 240), 1, win)
						bullet_group.add(bullet)
						bullet_fx.play()
					elif p.current_weapon == 1:  # Shotgun
						# Tir en éventail (5 balles)
						angles = [-20, -10, 0, 10, 20]
						for angle in angles:
							bullet = Bullet(x, y, direction, (255, 200, 50), 1, win, 
								           angle=angle if direction == 1 else -angle, speed=8)
							bullet_group.add(bullet)
						p.shoot()  # Consomme munition
						bullet_fx.play()

					p.attack = True
			if event.key == pygame.K_g:
				if p.grenades:
					p.grenades -= 1
					grenade = Grenade(p.rect.centerx, p.rect.centery, p.direction, win)
					grenade_group.add(grenade)
					grenade_throw_fx.play()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_SPACE:
				# Relâchement de la charge shot
				if p.charge_shot_available and p.is_charging:
					charge_level = p.stop_charge_shot()
					if charge_level > 0 and p.can_shoot():
						# Tirer selon le niveau de charge
						x, y = p.rect.center
						direction = p.direction
						
						if charge_level >= 1.0:  # Charge complète
							# Super tir qui traverse les ennemis
							bullet = Bullet(x, y, direction, (255, 255, 100), 1, win)
							bullet.damage = 150  # Triple dégâts
							bullet.piercing = True  # Traverse les ennemis
							bullet_group.add(bullet)
							print("🔥 Super Charge Shot!")
						elif charge_level >= 0.5:  # Charge moyenne
							bullet = Bullet(x, y, direction, (255, 200, 100), 1, win)
							bullet.damage = 100  # Double dégâts
							bullet_group.add(bullet)
							print("⚡ Charge Shot!")
						else:  # Charge faible
							bullet = Bullet(x, y, direction, (255, 150, 100), 1, win)
							bullet.damage = 75  # 1.5x dégâts
							bullet_group.add(bullet)
						
						bullet_fx.play()
						p.shoot()  # Consommer munitions si shotgun
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				is_sprinting = False
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				is_sprinting = False

	if main_menu:
		ghostbusters.update()
		trail_group.update()
		win.blit(p_image, p_rect)
		p_rect.y += p_dy
		p_ctr += p_dy
		if p_ctr > 15 or p_ctr < -15:
			p_dy *= -1
		t = Trail(p_rect.center, (220, 220, 220), win)
		trail_group.add(t)


		if play_btn.draw(win):
			menu_click_fx.play()
			world_data, level_length, w = reset_level(level)
			p, moving_left, moving_right, is_sprinting = reset_player()

			game_start = True
			main_menu = False
			game_won = False

		if about_btn.draw(win):
			menu_click_fx.play()
			about_page = True
			main_menu = False

		if controls_btn.draw(win):
			menu_click_fx.play()
			controls_page = True
			main_menu = False

		if exit_btn.draw(win):
			menu_click_fx.play()
			running = False

	elif about_page:
		MessageBox(win, about_font, 'GhostBusters', info)
		if main_menu_btn.draw(win):
			menu_click_fx.play()
			about_page = False
			main_menu = True

	elif controls_page:
		left_key.update()
		right_key.update()
		up_key.update()
		space_key.update()
		g_key.update()
		shift_key.update()
		tab_key.update()
		wall_grab_key.update()

		if main_menu_btn.draw(win):
			menu_click_fx.play()
			controls_page = False
			main_menu = True

	elif exit_page:
		pass

	elif game_won:
		game_won_msg.update()
		if main_menu_btn.draw(win):
			menu_click_fx.play()
			controls_page = False
			main_menu = True
			level = 1

			
	elif game_start:
		win.blit(MOON, (-40, -10))
		w.draw_world(win, screen_scroll)

		# Updating Objects ********************************************************

		bullet_group.update(screen_scroll, w)
		grenade_group.update(screen_scroll, p, enemy_group, explosion_group, w)
		explosion_group.update(screen_scroll)
		damage_particle_group.update(screen_scroll)  # Particules de dégâts
		trail_group.update()
		water_group.update(screen_scroll)
		water_group.draw(win)
		diamond_group.update(screen_scroll)
		diamond_group.draw(win)
		potion_group.update(screen_scroll)
		potion_group.draw(win)
		exit_group.update(screen_scroll)
		exit_group.draw(win)

		enemy_group.update(screen_scroll, bullet_group, p)
		enemy_group.draw(win)

		if p.jump:
			t = Trail(p.rect.center, (220, 220, 220), win)
			trail_group.add(t)

		# Contrôles de grimpe en mode continu
		key = pygame.key.get_pressed()
		if p.is_wall_grabbing:
			if key[pygame.K_w] or key[pygame.K_UP]:
				p.wall_climb(1)  # Monter
			elif key[pygame.K_s] or key[pygame.K_DOWN]:
				p.wall_climb(-1)  # Descendre
		
		# Tir automatique en mode rafale
		if p.rapid_fire_active and pygame.time.get_ticks() % 5 == 0:  # Tir toutes les 5ms
			if p.can_shoot():
				x, y = p.rect.center
				direction = p.direction
				bullet = Bullet(x, y, direction, (255, 100, 100), 1, win)
				bullet_group.add(bullet)
				# Pas de son pour éviter le spam audio
		
		screen_scroll = 0
		p.update(moving_left, moving_right, w, is_sprinting)
		p.draw(win)

		if (p.rect.right >= WIDTH - SCROLL_THRES and bg_scroll < (level_length*TILE_SIZE) - WIDTH) \
			or (p.rect.left <= SCROLL_THRES and bg_scroll > abs(dx)):
			dx = p.dx
			p.rect.x -= dx
			screen_scroll = -dx
			bg_scroll -= screen_scroll


		# Collision Detetction ****************************************************

		if p.rect.bottom > HEIGHT:
			p.health = 0

		if pygame.sprite.spritecollide(p, water_group, False):
			p.health = 0
			level = 1

		if pygame.sprite.spritecollide(p, diamond_group, True):
			diamond_fx.play()
			pass

		# Collision directe avec les ennemis
		enemy_collision = pygame.sprite.spritecollide(p, enemy_group, False)
		if enemy_collision:
			if p.take_damage(10):  # Dégâts plus faibles pour le contact direct
				print(f"Contact avec ennemi! Vie: {p.health}")
				# Activer la secousse d'écran
				screen_shake = 10
				# Créer des particules de dégâts
				for _ in range(6):
					particle = DamageParticle(p.rect.centerx, p.rect.centery, win)
					damage_particle_group.add(particle)

		if pygame.sprite.spritecollide(p, exit_group, False):
			next_level_fx.play()
			
			# Sauvegarder l'état du joueur avant de changer de niveau
			saved_health = p.health
			saved_skills = p.unlocked_skills.copy() if hasattr(p, 'unlocked_skills') else []
			saved_charge_shot = getattr(p, 'charge_shot_available', False)
			saved_shield = getattr(p, 'shield_available', False)
			saved_rapid_fire = getattr(p, 'rapid_fire_available', False)
			
			# Débloquer des compétences selon le niveau terminé
			skill_message = ""
			if level == 1:  # Fin du niveau 1 -> débloquer Charge Shot
				skill_message = p.unlock_skill("charge_shot")
				saved_charge_shot = True
				saved_skills.append("charge_shot")
			elif level == 2:  # Fin du niveau 2 -> débloquer Bouclier + Rafale
				skill_message = p.unlock_skill("shield_rapid")
				saved_shield = True
				saved_rapid_fire = True
				saved_skills.append("shield_rapid")
			
			level += 1
			if level <= MAX_LEVEL:
				world_data, level_length, w = reset_level(level)
				p, moving_left, moving_right, is_sprinting = reset_player() 
				
				# Restaurer l'état du joueur
				p.health = saved_health
				p.unlocked_skills = saved_skills
				p.charge_shot_available = saved_charge_shot
				p.shield_available = saved_shield
				p.rapid_fire_available = saved_rapid_fire

				screen_scroll = 0
				bg_scroll = 0
				
				if skill_message:
					print(f"🎉 {skill_message}")
			else:
				game_won = True


		potion = pygame.sprite.spritecollide(p, potion_group, False)
		if potion:
			if p.health < 100:
				potion[0].kill()
				p.health += 15
				health_fx.play()
				if p.health > 100:
					p.health = 100


		for bullet in bullet_group:
			enemy =  pygame.sprite.spritecollide(bullet, enemy_group, False)
			if enemy and bullet.type == 1:
				if not enemy[0].hit:
					enemy[0].hit = True
					# Appliquer les dégâts selon le type de balle
					damage = getattr(bullet, 'damage', 50)  # Dégâts par défaut ou personnalisés
					enemy[0].health -= damage
					
					# Vérifier si l'ennemi est mort pour donner des charges de rafale
					if enemy[0].health <= 0:
						p.add_rapid_fire_charge()
				
				# Si c'est un tir perçant, ne pas détruire la balle
				if not getattr(bullet, 'piercing', False):
					bullet.kill()
			if bullet.rect.colliderect(p):
				if bullet.type == 2:
					# Utiliser la nouvelle méthode de dégâts
					if p.take_damage(20):
						print(f"Joueur touché! Vie: {p.health}")
						# Activer la secousse d'écran
						screen_shake = 15
						# Créer des particules de dégâts
						for _ in range(8):
							particle = DamageParticle(p.rect.centerx, p.rect.centery, win)
							damage_particle_group.add(particle)
					bullet.kill()

		# drawing variables *******************************************************

		if p.alive:
			color = (0, 255, 0)
			if p.health <= 40:
				color = (255, 0, 0)
			pygame.draw.rect(win, color, (6, 8, p.health, 20), border_radius=10)
		pygame.draw.rect(win, (255, 255, 255), (6, 8, 100, 20), 2, border_radius=10)

		for i in range(p.grenades):
			pygame.draw.circle(win, (200, 200, 200), (20 + 15*i, 40), 5)
			pygame.draw.circle(win, (255, 50, 50), (20 + 15*i, 40), 4)
			pygame.draw.circle(win, (0, 0, 0), (20 + 15*i, 40), 1)
		
		# Affichage arme actuelle et munitions
		font = pygame.font.Font(None, 24)
		weapon_text = font.render(f"Arme: {p.weapon_names[p.current_weapon]}", True, (255, 255, 255))
		win.blit(weapon_text, (10, 55))
		
		if p.current_weapon == 1:  # Shotgun
			ammo_text = font.render(f"Munitions: {p.ammo_shotgun}", True, (255, 255, 255))
			win.blit(ammo_text, (10, 75))
		
		# Indicateur de sprint
		if is_sprinting:
			sprint_text = font.render("SPRINT!", True, (255, 255, 0))
			win.blit(sprint_text, (WIDTH - 80, 10))
		
		# Affichage arme actuelle et munitions
		font = pygame.font.Font(None, 24)
		weapon_text = font.render(f"Arme: {p.weapon_names[p.current_weapon]}", True, (255, 255, 255))
		win.blit(weapon_text, (10, 55))
		
		if p.current_weapon == 1:  # Shotgun
			ammo_text = font.render(f"Munitions: {p.ammo_shotgun}", True, (255, 255, 255))
			win.blit(ammo_text, (10, 75))
		
		# Indicateur de sprint
		if is_sprinting:
			sprint_text = font.render("SPRINT!", True, (255, 255, 0))
			win.blit(sprint_text, (WIDTH - 80, 10))
		
		if p.health <= 0:
			world_data, level_length, w = reset_level(level)
			p, moving_left, moving_right, is_sprinting = reset_player() 

			screen_scroll = 0
			bg_scroll = 0

			main_menu = True
			about_page = False
			controls_page = False
			game_start = False

		# Affichage de la stamina d'accrochage au mur
		if p.is_wall_grabbing:
			stamina_width = int(150 * (p.wall_grab_timer / p.wall_grab_stamina))
			pygame.draw.rect(win, (255, 0, 0), (WIDTH//2 - 75, 30, 150, 10))  # Fond rouge
			pygame.draw.rect(win, (0, 255, 0), (WIDTH//2 - 75, 30, stamina_width, 10))  # Barre verte
			
			# Texte "Wall Grab"
			wall_grab_font = pygame.font.SysFont("Arial", 16)
			wall_grab_text = wall_grab_font.render("Wall Grab", True, (255, 255, 255))
			win.blit(wall_grab_text, (WIDTH//2 - 35, 45))

		# === INTERFACE DES COMPÉTENCES ===
		ui_font = pygame.font.SysFont("Arial", 14)
		y_offset = 60
		
		# Barre de charge (Charge Shot)
		if p.is_charging:
			charge_progress = min(p.charge_timer / p.max_charge_time, 1.0)
			charge_width = int(200 * charge_progress)
			pygame.draw.rect(win, (100, 50, 0), (WIDTH//2 - 100, y_offset, 200, 8))  # Fond
			pygame.draw.rect(win, (255, 200, 0), (WIDTH//2 - 100, y_offset, charge_width, 8))  # Barre
			
			charge_text = ui_font.render("CHARGE SHOT", True, (255, 255, 255))
			win.blit(charge_text, (WIDTH//2 - 50, y_offset + 12))
			y_offset += 35

		# Statut du bouclier
		if p.shield_available:
			if p.shield_active:
				shield_text = ui_font.render(f"🛡️ SHIELD: {p.shield_max_hits - p.shield_hits} hits left", True, (100, 255, 255))
				win.blit(shield_text, (10, y_offset))
			elif p.shield_cooldown_timer > 0:
				cooldown_sec = int(p.shield_cooldown_timer / 60)
				shield_text = ui_font.render(f"🛡️ Shield cooldown: {cooldown_sec}s", True, (150, 150, 150))
				win.blit(shield_text, (10, y_offset))
			else:
				shield_text = ui_font.render("🛡️ Shield ready [V]", True, (255, 255, 255))
				win.blit(shield_text, (10, y_offset))
			y_offset += 20

		# Statut du mode rafale
		if p.rapid_fire_available:
			if p.rapid_fire_active:
				rapid_sec = int(p.rapid_fire_timer / 60)
				rapid_text = ui_font.render(f"🔥 RAPID FIRE: {rapid_sec}s left", True, (255, 100, 100))
				win.blit(rapid_text, (10, y_offset))
			else:
				rapid_text = ui_font.render(f"🔥 Rapid Fire: {p.rapid_fire_charge}/{p.rapid_fire_max_charge} kills [X]", True, (255, 255, 255))
				win.blit(rapid_text, (10, y_offset))
			y_offset += 20

	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 4, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()