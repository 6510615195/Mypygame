import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from button import Button


class Game:

	def get_font(size): # Returns Press-Start-2P in the desired size
		return pygame.font.Font("BD_Cartoon_Shout.ttf", size)

	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Flappy Bird')
		self.clock = pygame.time.Clock()
		self.active = False
		self.status = 0
	

		# sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# scale factor
		bg_height = pygame.image.load('background.png').get_height()
		self.scale_factor = WINDOW_HEIGHT / bg_height

		# sprite setup 
		BG(self.all_sprites,self.scale_factor)
		Ground([self.all_sprites,self.collision_sprites],self.scale_factor)

		# timer
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer,1400)

		# text
		self.font = pygame.font.Font('BD_Cartoon_Shout.ttf',30)
		self.score = 0
		self.start_offset = 0

		# menu
		self.menu_surf = pygame.image.load('menu.png').convert_alpha()
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))

		# music 
		self.music = pygame.mixer.Sound('music.wav')
		self.music.play(loops = -1)

	def collisions(self):
		if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
		or self.plane.rect.top <= 0:
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			self.active = False
			self.plane.kill()
			status = 0


	def display_score(self):

		if self.active:
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
			y = WINDOW_HEIGHT / 10

			maxscore = self.score

			file = open('maxScore.txt', 'w+')
			
			if(self.score >= 1):
				for i in file:
					if(maxscore > int(i)):
						file.write(str(maxscore))
				
			file.close()

		else:
			y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

		score_surf = self.font.render(str(self.score),True,'black')
		score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
		self.display_surface.blit(score_surf,score_rect)

	def play(self):
		self.status = 1

		self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)

		# delta time
		dt = time.time() - last_time
		last_time = time.time()
		# game logic
		self.display_surface.fill('black')
		self.all_sprites.update(dt)
		self.all_sprites.draw(self.display_surface)
		self.display_score()

	def run(self):
		
		last_time = time.time()

		
		while True:

			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.active:
					self.plane.jump()
				else:
					self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)
					self.active = True
					self.start_offset = pygame.time.get_ticks()
						

				if self.active: 
					self.collisions()
				else:
					self.display_surface.blit(self.menu_surf,self.menu_rect)

			if self.active and self.status == 1: 
				self.collisions()
			else:
				MENU_TEXT = Game.get_font(100).render("MAIN MENU", True, "#b68f40")
				MENU_RECT = MENU_TEXT.get_rect(center=(WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 0.34 * WINDOW_HEIGHT))
				self.display_surface.blit(MENU_TEXT, MENU_RECT)
				MENU_MOUSE_POS = pygame.mouse.get_pos()

				PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png").convert(), pos=(WINDOW_WIDTH / 2, 350), 
                            text_input="PLAY", font = Game.get_font(75), base_color="#d7fcd4", hovering_color="White")
			

				OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(WINDOW_WIDTH / 2, 500), 
                            text_input="OPTIONS", font = Game.get_font(75), base_color="#d7fcd4", hovering_color="White")
				QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(WINDOW_WIDTH / 2, 650), 
                            text_input="QUIT", font = Game.get_font(75), base_color="#d7fcd4", hovering_color="White")
			
		
				for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
					button.changeColor(MENU_MOUSE_POS)
					button.update(self.display_surface)


			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
						play()
						
					if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
						self.display_surface.fill("black")
					if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
						pygame.quit()
						sys.exit()

			pygame.display.update()
			# self.clock.tick(FRAMERATE)

if __name__ == '__main__':
	game = Game()
	game.run()
		