import pygame
import time
import random

pygame.font.init()

#game settings
width = 1200
height = 800
fps = 60

#colors
black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)

screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()

#images
background = pygame.transform.scale(pygame.image.load("assets/bg.png"),(width,height))
player = pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/fish.png"),(100,90)),True,False)
coralup = pygame.transform.scale(pygame.image.load("assets/coralup.png"),(120,700))
coraldown = pygame.transform.scale(pygame.image.load("assets/coraldown.png"),(120,700))

class Player():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.image = player
		self.mask = pygame.mask.from_surface(self.image)
	
	def draw(self,screen):
		screen.blit(self.image,(self.x,self.y))


class Obstacles_bottom():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.mask = pygame.mask.from_surface(coralup)
	
	def draw(self,screen):
		screen.blit(coralup,(self.x,self.y))
	
	def move(self, speed):
		self.x -= speed

class Obstacles_top():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.mask = pygame.mask.from_surface(coraldown)
	
	def draw(self,screen):
		screen.blit(coraldown,(self.x,self.y))
	
	def move(self, speed):
		self.x -= speed

def collide(object1, object2):
	gap_x = object2.x - object1.x
	gap_y = object2.y - object1.y
	return object1.mask.overlap(object2.mask, (gap_x, gap_y)) != None

def main_loop():
	running = True
	score = 0
	main_text = pygame.font.SysFont('freesansbold', 40)
	main_text2 = pygame.font.SysFont('freesansbold', 60, True, False)
	jump_height = 12
	player_y = 0
	gravity = 0.9
	player = Player(200,100)
	game_over = False
	game_over_counter = 0
	obstacles_bottoms = []
	obstacles_tops = []
	obstacle_speed = 5
	obstacle_start = True


	def update_screen():
		screen.blit(background,(0,0))
		score_text=main_text.render(f'SCORE: {score}',True,(255,255,255))
		player.draw(screen)
		for obstacle_bottom in obstacles_bottoms:
			obstacle_bottom.draw(screen)
		for obstacle_top in obstacles_tops:
			obstacle_top.draw(screen)
		screen.blit(score_text,(10,10))

		if game_over:
			game_over_text = main_text2.render(f'G A M E  O V E R', True, (255,0,0))
			screen.blit(game_over_text, ((width/2 - game_over_text.get_width()/2), (height/2)))
			score_over_text = main_text2.render(f'S C O R E: ' + str(score), True, (255,0,0))
			screen.blit(score_over_text, ((width/2 - score_over_text.get_width()/2), ((height/2)+50)))

		pygame.display.update()


	while running:
		timer.tick(fps)
		update_screen()


		if obstacle_start:
			obstacle_y = random.randrange(height - 350,height - 100)
			obstacle_bottom = Obstacles_bottom(width + 150, obstacle_y)
			obstacles_bottoms.append(obstacle_bottom)
			obstacle_top = Obstacles_top(width + 150, obstacle_y - 1000)
			obstacles_tops.append(obstacle_top)
			obstacle_start = False

		for obstacle_bottom in obstacles_bottoms:
			obstacle_bottom.move(obstacle_speed)

			if collide(obstacle_bottom, player):
				game_over = True
				game_over_counter += 1
				obstacle_speed = 0

			if obstacle_bottom.x == 1050:
				obstacle_start = True

			if obstacle_bottom.x == 195:
				score += 1
			
			if obstacle_bottom.x < 0:
				obstacles_bottoms.remove(obstacle_bottom)
		
		for obstacle_top in obstacles_tops:
			obstacle_top.move(obstacle_speed)

			if collide(obstacle_top, player):
				game_over = True
				game_over_counter += 1
				obstacle_speed = 0

			if obstacle_top.x < 0:
				obstacles_tops.remove(obstacle_top)
		

		

		#movement
		active_keys = pygame.key.get_pressed()
		if active_keys[pygame.K_w] or active_keys[pygame.K_SPACE] or active_keys[pygame.K_UP]:
			player_y = -jump_height
		
		if player.y + player_y < height - 30 and player.y + player_y > -50:
			player.y += player_y
			player_y += gravity
		else:
			game_over = True
			game_over_counter += 1
			obstacle_speed = 0

		#game over screen
		if game_over:
			if game_over_counter > fps * 2:
				running = False
			else:
				continue

		#exit game
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		

	


def start_menu():
	text = pygame.font.SysFont('freesansbold', 60, True, False)
	running = True
	while running:
		screen.blit(background, (0,0))
		start_label = text.render('C l i c k  A n y w h e r e  T o  S t a r t', True, (255,255,255))
		screen.blit(start_label, (width/2 - start_label.get_width()/2, (height/2)))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				main_loop()
	pygame.quit()

start_menu()