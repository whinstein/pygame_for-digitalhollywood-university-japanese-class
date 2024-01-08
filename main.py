import sys
print(sys.path)

import pygame
import random
import os

FPS = 40
WIDTH = 960
HEIGHT = 540
jump_high = 55
run_speed = -15
ground_high = 30
floor_high = 30
gravity_parameter = 5
one_floor_y = HEIGHT - ground_high
two_floor_y = HEIGHT / 2 - floor_high
ground_gap = 20
font_size = 40
life_bar_size = 200

student_cycle_time = 1200
energydrink_cycle_time = 5500
coin_cycle_time = 6000

student_damage = 30
player_life = 100
drink_heal = 40
#screen_stop = 0  #0:not stop 1:stop

#color map
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
PURPLE = (128,0,128)
BLUE = (0,255,255)

#初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("カミッチの日常")
clock = pygame.time.Clock()
highest_score = 0

#background draw
background_image_0 = pygame.image.load(os.path.join("img","background.jpeg")).convert()
background_image_1 = pygame.image.load(os.path.join("img","background.jpeg")).convert()
background_image_0 = pygame.transform.scale(background_image_0,(WIDTH,HEIGHT)).convert()
background_image_1 = pygame.transform.scale(background_image_1,(WIDTH,HEIGHT)).convert()

floor_image = pygame.image.load(os.path.join("img","wood.png")).convert()
floor_image.set_colorkey(WHITE)

ground_image = pygame.image.load(os.path.join("img","road.png")).convert()
ground_image_1 = pygame.image.load(os.path.join("img","road.png")).convert()
ground_image = pygame.transform.scale(ground_image,(WIDTH + 10,ground_high)).convert()
ground_image_1 = pygame.transform.scale(ground_image_1,(WIDTH + 10,ground_high)).convert()

#pic loading
player_images = []
for i in range(8):
	player_anim = pygame.image.load(os.path.join("Players",f"run_{i}.png")).convert()
	player_anim.set_colorkey(WHITE)
	player_images.append(pygame.transform.scale(player_anim,(126,72)))

player_hurt_images = []
for i in range(8):
	player_hurt_image = pygame.image.load(os.path.join("Players",f"hurt_{i%2}.png")).convert()
	player_hurt_image.set_colorkey(WHITE)
	player_hurt_images.append(pygame.transform.scale(player_hurt_image,(72,126)))

player_jump_images = []
for i in range(3):
	player_jump_image = pygame.image.load(os.path.join("Players",f"jump_{i}.png")).convert()
	player_jump_image.set_colorkey(WHITE)
	player_jump_images.append(pygame.transform.scale(player_jump_image,(114,114)))# (*0.9)

pygame.display.set_icon(player_jump_images[0])

pic_small_rate = 0.4
student_size_map = {"student0.png":(288*pic_small_rate,450*pic_small_rate),
					"student1.png":(311*pic_small_rate,400*pic_small_rate),
					"student2.png":(400*pic_small_rate,363*pic_small_rate)}
student_images = []
for i in range(3):
	stu = pygame.image.load(os.path.join("img",f"student{i}.png")).convert()
	stu.set_colorkey(BLACK)
	student_images.append(pygame.transform.scale(stu,student_size_map[f"student{i}.png"]))

coin_image = pygame.image.load(os.path.join("img","coin.png")).convert()
coin_image.set_colorkey(BLACK)

drink_image = pygame.image.load(os.path.join("img","energy_drink.png")).convert()
drink_image.set_colorkey(BLACK)

#loading music
#jump_sound = pygame.mixer.Sound(os.path.join("sound", ""))

#loading font
font_name = os.path.join("JP_font.ttf")

def gameover_screen():
	text_high = 70
	draw_text(screen, "ゲームオーバー",100, WIDTH/2, HEIGHT/5 - text_high / 2)
	draw_text(screen, "君の得点は %d "%score ,50 , WIDTH/2, HEIGHT/3)
	draw_text(screen, "今までの最高得点は %d "%highest_score ,50 , WIDTH/2, HEIGHT/3 + text_high)
	draw_text(screen, "スペースボタンを押すとゲームをリトライできます",30, WIDTH/2, HEIGHT*4/5)
	draw_text(screen, "Qボタンを押すとゲームを閉じます",30, WIDTH/2, HEIGHT*4/5 + text_high)

	pygame.display.update()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_q:
					pygame.quit()
					return True
				if event.key == pygame.K_SPACE:
					waiting = False
					return False

def draw_init():
	text_high = 50
	screen.blit(background_image_0, (0,0))
	draw_text(screen, "カミッチの日常", 100, WIDTH/2, HEIGHT/5)
	draw_text(screen, "上矢印キーを押すとジャンプできます",22, WIDTH/2, HEIGHT/4+text_high)
	draw_text(screen, "下矢印キーを押すとフロントから降りられます",22, WIDTH/2, HEIGHT/4+text_high*2)
	draw_text(screen, "コインを食べると点数が増えます、エネルギードリンクを飲むと命を回復できます",22, WIDTH/2, HEIGHT/4+text_high*3)
	draw_text(screen, "人間達を避けて学校に進みましょう！",22, WIDTH/2, HEIGHT/4+text_high*4)
	draw_text(screen, "任意ボタンを押すとゲームを始めます",40, WIDTH/2, HEIGHT*4/5+text_high)
	pygame.display.update()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return True
			elif event.type == pygame.KEYUP:
				waiting = False
				return False

def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.center = (x,y)
	#text_rect.bottom = y
	surf.blit(text_surface, text_rect)

def draw_health(surf):
	life_bar_frame = pygame.Surface((life_bar_size,life_bar_size / 5))
	life_bar_frame.fill(BLACK)
	F_rect = life_bar_frame.get_rect()
	life_num = pygame.Surface(((player.health / 100 * life_bar_size) * 0.9 ,(life_bar_size / 5) * 0.9 ))
	life_num.fill(RED)
	N_rect = life_num.get_rect()
	F_rect.right = WIDTH - life_bar_size * 0.05
	F_rect.top = (life_bar_size / 5) * 0.05
	N_rect.right = WIDTH - life_bar_size * 0.1
	N_rect.top = (life_bar_size / 5) * 0.1
	surf.blit(life_bar_frame,F_rect)
	surf.blit(life_num,N_rect)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_num = 0
		#self.image = player_hurt_image
		self.image = player_images[self.image_num]
		self.rect = self.image.get_rect()
		self.rect.x = 120
		self.rect.bottom = 450
		self.radius = self.rect.width / 2
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		self.movex = 0
		self.movey = 0
		self.jump_delta = 1     # 0 : can jump   1 : can not jump
		self.floor_hit = 0 		# 0 : no hit   	 1 : hitting
		self.ground_hit = 1 	# 0 : no hit   	 1 : hitting
		self.godown = 0 		# 0 : no go down 1 : go down
		self.health = player_life
		self.recent_y = 0

		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50
		self.hurt_or_not = 0
		self.hurt_time = 0
		self.jump_ani = 0
		self.high_infor = 0 # To know that char is jump up or jump down


	def gravity(self):
		self.movey += gravity_parameter #player fall down speed
		if self.ground_hit == 1 and self.movey >= 0: #on the ground
			self.movey = 0
			self.rect.bottom = ground.rect.top + 1
			self.jump_delta = 0
			self.godown = 0

		elif self.floor_hit == 1 and self.movey >= 0: #on the floor
			self.movey = 0
			self.rect.bottom = floor.rect.top + 1
			self.jump_delta = 0
		if self.hurt_or_not != 0:
			self.movey = 0

	def update(self):
		#print(self.rect.bottom)
		self.high_infor = self.rect.bottom
		self.rect.bottom = self.rect.bottom + self.movey

		#print(self.jump_delta)
		###ground hit test
		if self.godown == 0:
			self.floor_hit = pygame.sprite.collide_rect(self,floor)
			self.ground_hit = pygame.sprite.collide_rect(self,ground)
		elif self.godown == 1:
			self.ground_hit = pygame.sprite.collide_rect(self,ground)

		now = pygame.time.get_ticks()
		if self.jump_ani != 0 and self.hurt_or_not == 0 and now - self.last_update > self.frame_rate: #jump_animation
			self.last_update = now

			if self.high_infor - self.rect.bottom >= gravity_parameter: #jump up
				self.image = player_jump_images[0]
			elif self.high_infor - self.rect.bottom <= gravity_parameter: #jump down
				self.image = player_jump_images[2]
			else:
				self.image = player_jump_images[1]

			self.jump_ani += 1
			if self.ground_hit == 1 and self.movey >= 0:
				self.jump_ani = 0
				self.image = player_images[self.image_num]

			elif self.floor_hit == 1 and self.movey >= 0:
				self.jump_ani = 0
				self.image = player_images[self.image_num]

		if self.hurt_or_not != 0 and now - self.last_update > self.frame_rate: #hurt_animation
			self.last_update = now
			self.recent_y = self.rect.bottom
			self.image_num += 1
			self.hurt_time += 1
			if self.image_num == len(player_hurt_images):
				self.image_num = 0
			else:
				self.image = player_hurt_images[self.image_num]
				self.rect = self.image.get_rect()
				self.rect.x = 120
				self.rect.bottom = self.recent_y

			if self.hurt_time >= len(player_hurt_images):
				self.hurt_or_not = 0
				self.image = player_images[self.image_num]
				self.rect = self.image.get_rect()
				self.rect.x = 120
				self.rect.bottom = self.recent_y

		elif self.hurt_or_not == 0 and now - self.last_update > self.frame_rate: #running_animation
			#print(self.rect.bottom)
			self.hurt_time = 0
			self.last_update = now
			self.image_num += 1
			if self.image_num >= len(player_images):
				self.image_num = 0
			else:
				self.image = player_images[self.image_num]
		#print("ground %d  floor %d "%(self.ground_hit,self.floor_hit))

	def get_hurt(self):
		self.hurt_or_not = 1

	def control_jump(self,y):
		if self.jump_delta == 0 and self.hurt_or_not == 0:
			self.jump_delta = 1
			self.movey = - y
			self.jump_ani = 1
			#jump_sound.play()

	def control_down(self):
		if self.floor_hit == 1 and self.hurt_or_not == 0:
			self.godown = 1
			self.floor_hit = 0
			self.jump_delta = 1

	def energydrink_create(self):
		energydrink = Energydrink()
		all_sprites.add(energydrink)
		drinks.add(energydrink)

	def student_create(self):
		student = Student()
		all_sprites.add(student)
		students.add(student)

	def coin_create(self,level):
		coin = Coin(level)
		all_sprites.add(coin)
		coins.add(coin)

	def kill_itself(self):
		self.kill()

class Ground(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((WIDTH,floor_high))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.x = -10
		self.rect.bottom = HEIGHT
	def kill_itself(self):
		self.kill()

class Floor(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(floor_image,(random.randrange(WIDTH/2,WIDTH),floor_high)).convert()
		self.rect = self.image.get_rect()
		self.rect.left = WIDTH
		self.rect.bottom = HEIGHT / 2
		self.speedx = run_speed

	def update(self):
		self.rect.x += self.speedx
		if self.rect.right < 0:
			self.image = pygame.transform.scale(floor_image,(random.randrange(WIDTH/2,WIDTH),floor_high)).convert()
			#self.image = pygame.Surface((random.randrange(WIDTH/2,WIDTH),floor_high))
			#self.image.fill(RED)
			self.rect = self.image.get_rect()
			self.rect.left = WIDTH
			self.rect.bottom = HEIGHT / 2
	def kill_itself(self):
		self.kill()

class Energydrink(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(drink_image,(81,90))
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH
		self.speedx = run_speed
		self.level = random.randrange(2)       # 0: on the ground, 1: on the floor, 10: object no problem
		self.rect.bottom = one_floor_y - ground_gap if self.level == 0 else two_floor_y + 1

	def update(self):
		self.rect.x += self.speedx
		if self.rect.right < 0:
			self.kill()
		elif self.level == 1 and pygame.sprite.collide_rect(self,floor) == 0:
			self.kill()
		elif self.level == 1 and pygame.sprite.collide_rect(self,floor) == 1:
			self.level = 10
			self.rect.bottom = two_floor_y - ground_gap
	def kill_itself(self):
		self.kill()

class Student(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.student_random = random.randrange(3)
		self.image = pygame.transform.scale(student_images[self.student_random],student_size_map[f"student{self.student_random}.png"])
		self.rect = self.image.get_rect()
		self.radius = self.rect.width * 2 / 5
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		self.rect.left = WIDTH
		self.speedx = run_speed
		self.level = random.randrange(2)		# 0: on the ground, 1: on the floor
		self.rect.bottom = one_floor_y + 1 if self.level == 0 else two_floor_y + 1

	def update(self):
		self.rect.x += self.speedx
		if self.rect.right < 0:
			self.kill()
		elif self.level == 1 and pygame.sprite.collide_rect(self,floor) == 0:
			self.kill()

	def kill_itself(self):
		self.kill()

class Coin(pygame.sprite.Sprite):
	def __init__(self,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(coin_image,(40,40)) #square
		self.rect = self.image.get_rect()
		self.rect.left = WIDTH
		self.speedx = run_speed
		self.level = y
		self.rect.bottom = y + 1

	def update(self):
		self.rect.x += self.speedx
		if self.rect.right < 0:
			self.kill()
		elif self.level == two_floor_y and pygame.sprite.collide_rect(self,floor) == 0:
			self.kill()
		elif self.level == two_floor_y and pygame.sprite.collide_rect(self,floor) == 1:
			self.level = 10
			self.rect.bottom = two_floor_y - ground_gap
		elif self.level == one_floor_y:
			self.rect.bottom = one_floor_y - ground_gap

	def kill_itself(self):
		self.kill()


all_sprites = pygame.sprite.Group()
students = pygame.sprite.Group()
drinks = pygame.sprite.Group()
coins = pygame.sprite.Group()
player = Player()
ground = Ground()
floor = Floor()
all_sprites.add(player)
all_sprites.add(ground)
all_sprites.add(floor)
score = 0

create_drink = pygame.USEREVENT
create_student = pygame.USEREVENT + 1
create_coin = pygame.USEREVENT + 2
deside_coin_num = pygame.USEREVENT + 3
pygame.time.set_timer(create_drink,energydrink_cycle_time)
pygame.time.set_timer(create_student,student_cycle_time)
pygame.time.set_timer(create_coin,coin_cycle_time)

#game loop
show_init = True
running = True
gameover = False
background_move = 0
while running:
	if gameover == True:
		close = gameover_screen()
		if close == True:
			break
		gameover = False
		#初期化
		player.kill_itself()
		ground.kill_itself()
		floor.kill_itself()

		player = Player()
		ground = Ground()
		floor = Floor()
		all_sprites.add(player)
		all_sprites.add(ground)
		all_sprites.add(floor)
		score = 0

	if show_init == True:
		close = draw_init()
		if close == True:
			break
		show_init = False

	clock.tick(FPS)
	#get input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player.control_jump(jump_high)
			if event.key == pygame.K_DOWN:
				player.control_down()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player.control_jump(jump_high)
			if event.key == pygame.K_DOWN:
				player.control_down()

		if event.type == create_drink:
			player.energydrink_create()
		elif event.type == create_student:
			player.student_create()
		elif event.type == create_coin:
			coin_make_num = random.randrange(2,10)
			coin_loc = one_floor_y if random.randrange(2) == 0 else two_floor_y
			pygame.time.set_timer(deside_coin_num,150)                #coin gap
		elif event.type == deside_coin_num and coin_make_num > 0:
			player.coin_create(coin_loc)
			coin_make_num -= 1

	#update game
	all_sprites.update()
	player.gravity() #檢查引力
	pygame.sprite.groupcollide(students,drinks,True,False) #drink and student not collide
	pygame.sprite.groupcollide(students,coins,True,False)
	pygame.sprite.groupcollide(drinks,coins,True,False)

	hits_student = pygame.sprite.spritecollide(player, students, True, pygame.sprite.collide_circle)
	hits_drink = pygame.sprite.spritecollide(player, drinks, True)
	hits_coin = pygame.sprite.spritecollide(player,coins, True)

	if hits_drink:
		if player.health + drink_heal < player_life:
			player.health += drink_heal
		else:
			player.health = player_life
	if hits_student:
		if player.health - student_damage > 0:
			player.health -= student_damage
			player.get_hurt()
		else:
			player.health = 0
			if score > highest_score :
				highest_score = score
			gameover = True

	if hits_coin:
		score = score + 1

	#display
	#show screen
	if background_move > WIDTH:
		background_move = 0
	background_move += 3
	screen.blit(background_image_0, (0 - background_move,0))
	screen.blit(background_image_1, (WIDTH - background_move,0))
	screen.blit(ground_image,(0 - background_move,HEIGHT - ground_high))
	screen.blit(ground_image_1,(WIDTH - background_move,HEIGHT - ground_high))

	all_sprites.draw(screen)
	draw_text(screen, str(score),font_size, 30,30)
	draw_health(screen)
	pygame.display.update()
pygame.quit()