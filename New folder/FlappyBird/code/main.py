import pygame, sys, time
from settings import *
from button import Button
from random import choice, randint

BGspeed = 300
Gspeed = 360
PlaneUpspeed = 400
gravity = 600
obsSizeSC = 1
obsSpawnT = 1400
BirdSizeSC = 0.3
mode = 0

scale_factor = 0


class Game:
	global mode
	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Flappy Bird')
		self.clock = pygame.time.Clock()
		self.active = False
		self.status = 0
		self.var = 0
		self.selM = 0

		# sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# scale factor
		bg_height = pygame.image.load('background.png').get_height()
		self.scale_factor = WINDOW_HEIGHT / bg_height
		global scale_factor
		scale_factor = self.scale_factor

		# sprite setup 
		BG(self.all_sprites,self.scale_factor)
		Ground([self.all_sprites,self.collision_sprites],self.scale_factor)

		# timer
		self.obstacle_timer = pygame.USEREVENT + 1

		# text
		self.font = pygame.font.Font('BD_Cartoon_Shout.ttf',30)
		self.score = 0
		self.start_offset = 0

		# menu
		self.arrow_surf = pygame.image.load('arrow.png').convert_alpha()
		self.menu_surf = Game.get_font(35).render("Tap to Start", True, "#ffffff")
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,(WINDOW_HEIGHT / 2) + (WINDOW_HEIGHT * 0.33)))

		# music 
		self.music = pygame.mixer.Sound('music.wav')
		self.music.play(loops = -1)

	def collisions(self):
		if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
		or self.plane.rect.top <= 0:
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			self.plane.kill()
			global mode
			global Pstatus
			mode = 0
			self.status = 2
			self.active = False
			Pstatus = 0

	def display_score(self):

		if self.active and self.status == 1:
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
			y = WINDOW_HEIGHT / 10
			score_surf = self.font.render("score   " + str(self.score),True,"#b68f40")
			score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
			# Maxscore
			maxscore = self.score

			i = 1

			file = open('maxScore.txt', 'w+')
			
			if(self.score >= 1):
				#for i in file:
					if(maxscore > int(i)):
						file.write(str(maxscore))
					else:
						maxscore = int(i)

			file.close()
		else:
			maxscore = self.score
			y = WINDOW_HEIGHT / 10
			x = WINDOW_WIDTH / 2
			score_surf = self.font.render("Your score   " + str(self.score),True,"#b68f40")
			score_rect = score_surf.get_rect(midtop = (x,y))
			maxscore_surf = self.font.render("Max score   " + str(maxscore),True,"#008000")
			maxscore_rect = maxscore_surf.get_rect(midtop = (x,y + 50))
			self.display_surface.blit(maxscore_surf,maxscore_rect)

		self.display_surface.blit(score_surf,score_rect)


	def get_font(size): # Returns Press-Start-2P in the desired size
		return pygame.font.Font("BD_Cartoon_Shout.ttf", size)

	def run(self):
	
		last_time = time.time()
		while True:
			
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			if(self.status == 1):
				
			# event loop
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						if self.active:
							self.plane.jump()
						else:
							self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)
							self.active = True
							self.start_offset = pygame.time.get_ticks()

					if event.type == self.obstacle_timer and self.active:
						Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)
			
			# game logic
				self.display_surface.fill('black')
				self.all_sprites.update(dt)
				self.all_sprites.draw(self.display_surface)
				self.display_score()

				if self.active: 
					self.collisions()
				else:
					self.display_surface.blit(self.menu_surf,self.menu_rect)
					# select mode
					#MENU_MOUSE_POS = pygame.mouse.get_pos()

					#SEL_BUTTON = Button(image=pygame.image.load("Play Rect.png").convert(), pos=(WINDOW_WIDTH / 9.2, WINDOW_HEIGHT * (0.85)), 
                    #        text_input="SELECT MODE?", font = Game.get_font(30), base_color="#d7fcd4", hovering_color="White")
					
			elif(self.status == 2):
				self.display_surface.fill('black')
				self.all_sprites.update(dt)
				self.all_sprites.draw(self.display_surface)
				self.display_score()

				if self.active: 
					self.collisions()
				else:
					self.display_surface.blit(self.menu_surf,self.menu_rect)
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pygame.quit()
							sys.exit()
						elif(event.type == pygame.MOUSEBUTTONDOWN):
							self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)
							self.active = True
							self.start_offset = pygame.time.get_ticks()
							self.status = 1
						elif event.type == pygame.KEYDOWN:
							if event.key == pygame.K_SPACE:
								global mode
								mode = 0
								self.status = 0
		


			elif(self.status == 0 or mode == 0):
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
				self.all_sprites.draw(self.display_surface)
				MENU_TEXT = Game.get_font(100).render("MAIN MENU", True, "#b68f40")
				MENU_RECT = MENU_TEXT.get_rect(center=(WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 0.34 * WINDOW_HEIGHT))
				self.display_surface.blit(MENU_TEXT, MENU_RECT)
				MENU_MOUSE_POS = pygame.mouse.get_pos()

				EASY_BUTTON = Button(image=pygame.image.load("Play Rect.png").convert(), pos=(WINDOW_WIDTH / 2, 430), 
                            text_input="EASY", font = Game.get_font(50), base_color="#d7fcd4", hovering_color="White")
				
				NORM_BUTTON = Button(image=pygame.image.load("Play Rect.png").convert(), pos=(WINDOW_WIDTH / 2, 550), 
                            text_input="NORMAL", font = Game.get_font(50), base_color="#d7fcd4", hovering_color="White")
				
				CHAL_BUTTON = Button(image=pygame.image.load("Play Rect.png").convert(), pos=(WINDOW_WIDTH / 2, 670), 
                            text_input="CHALLENGE", font = Game.get_font(50), base_color="#d7fcd4", hovering_color="White")
				
				EASY_BUTTON.update(self.display_surface)
				NORM_BUTTON.update(self.display_surface)
				CHAL_BUTTON.update(self.display_surface)

				if(self.selM == 0):
					EASY_BUTTON.changeColor((EASY_BUTTON.x_pos, EASY_BUTTON.y_pos))
					EASY_BUTTON.update(self.display_surface)
					self.arrow_rect = self.arrow_surf.get_rect(center=(WINDOW_WIDTH / 2 - 230, 420))
				elif(self.selM == 1):
					NORM_BUTTON.changeColor((NORM_BUTTON.x_pos, NORM_BUTTON.y_pos))
					NORM_BUTTON.update(self.display_surface)
					self.arrow_rect = self.arrow_surf.get_rect(center=(WINDOW_WIDTH / 2 - 230, 540))
				else:
					CHAL_BUTTON.changeColor((CHAL_BUTTON.x_pos, CHAL_BUTTON.y_pos))
					CHAL_BUTTON.update(self.display_surface)
					self.arrow_rect = self.arrow_surf.get_rect(center=(WINDOW_WIDTH / 2 - 230, 660))

				self.display_surface.blit(self.arrow_surf,self.arrow_rect)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							if(self.selM == 0):
								self.selM = 1
							elif(self.selM == 1):
								self.selM = 2
							else:
								self.selM = 0

					
				
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if(self.selM == 0):
							mode = 1
						elif(self.selM == 1):
							mode = 2
						else:
							mode = 3
						
							

				if(mode == 1):
					global gravity
					gravity = 175
					global BGspeed
					BGspeed = 120
					global Gspeed
					Gspeed = 135
					global PlaneUpspeed
					PlaneUpspeed = 250
					global obsSizeSC
					obsSizeSC = 0.4
					global obsSpawnT
					obsSpawnT = 1200
					self.status = 2
					
				elif(mode == 2):
					
					gravity = 275
					
					BGspeed = 140
					
					Gspeed = 155
					
					PlaneUpspeed = 320
					
					obsSizeSC = 0.66
					
					obsSpawnT = 1200

					self.status = 2
					
				elif(mode == 3):
					
					gravity = 355
					
					BGspeed = 160
					
					Gspeed = 175
					
					PlaneUpspeed = 330
					
					obsSizeSC = 0.9
					
					obsSpawnT = 1200

					self.status = 2
					

				pygame.time.set_timer(self.obstacle_timer,obsSpawnT)
					

			
			print(mode)

			pygame.display.update()
			# self.clock.tick(FRAMERATE)

class BG(pygame.sprite.Sprite):

	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		bg_image = pygame.image.load('background.png').convert()

		full_height = bg_image.get_height() * scale_factor
		full_width = bg_image.get_width() * scale_factor
		full_sized_image = pygame.transform.scale(bg_image,(full_width,full_height))
		
		self.image = pygame.Surface((full_width * 2,full_height))
		self.image.blit(full_sized_image,(0,0))
		self.image.blit(full_sized_image,(full_width,0))

		self.rect = self.image.get_rect(topleft = (0,0))
		self.pos = pygame.math.Vector2(self.rect.topleft)


	def update(self,dt):
		self.pos.x -= BGspeed * dt
		if self.rect.centerx <= 0:
			self.pos.x = 0
		self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		self.sprite_type = 'ground'
		
		# image
		ground_surf = pygame.image.load('ground.png').convert()
		self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size()) * scale_factor)

		full_height = ground_surf.get_height()
		full_width = ground_surf.get_width()
		full_sized_image = pygame.transform.scale(ground_surf,(full_width,full_height))
		
		self.image = pygame.Surface((full_width * 2,full_height))
		self.image.blit(full_sized_image,(0,0))
		self.image.blit(full_sized_image,(full_width,0))
		
		# position
		self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)


	def update(self,dt):
		self.pos.x -= Gspeed * dt
		if self.rect.centerx <= 0:
			self.pos.x = 0

		self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):

		super().__init__(groups)

		# image 
		self.import_frames(scale_factor)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

		# rect
		self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20,WINDOW_HEIGHT / 2))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# movement
		self.direction = 0

		# mask
		self.mask = pygame.mask.from_surface(self.image)

		# sound
		self.jump_sound = pygame.mixer.Sound('jump.wav')
		self.jump_sound.set_volume(0.3)

	def import_frames(self,scale_factor):
		self.frames = []
		for i in range(3):
			surf = pygame.image.load(f'red{i}.png').convert_alpha()
			scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor * BirdSizeSC)
			self.frames.append(scaled_surface)

	def apply_gravity(self,dt):
		self.direction += gravity * dt
		self.pos.y += self.direction * dt
		self.rect.y = round(self.pos.y)

	def jump(self):
		self.jump_sound.play()
		self.direction = -PlaneUpspeed

	def animate(self,dt):
		self.frame_index += 10 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def rotate(self):
		rotated_plane = pygame.transform.rotozoom(self.image,-self.direction * 0.06,1)
		self.image = rotated_plane
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.apply_gravity(dt)
		self.animate(dt)
		self.rotate()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		self.sprite_type = 'obstacle'

		orientation = choice(('up','down'))
		surf = pygame.image.load(f'{choice((0,1))}.png').convert_alpha()
		self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor * obsSizeSC)
		
		x = WINDOW_WIDTH + randint(40,100)

		if orientation == 'up':
			y = WINDOW_HEIGHT + randint(10,50)
			self.rect = self.image.get_rect(midbottom = (x,y))
		else:
			y = randint(-50,-10)
			self.image = pygame.transform.flip(self.image,False,True)
			self.rect = self.image.get_rect(midtop = (x,y))

		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.pos.x -= 400 * dt
		self.rect.x = round(self.pos.x)
		if self.rect.right <= -100:
			self.kill()


if __name__ == '__main__':
	game = Game()
	game.run()