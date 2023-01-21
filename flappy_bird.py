import pygame 
import os 
import random
import neat 
import time

WIN_HEIGHT = 800
WIN_WIDTH = 500


WIN 	= pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")	
	
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

class Bird: 
	IMGS = bird_images
	MAX_ROTATION = 25 
	ROT_VEL = 20 
	ANIMATION_TIME = 5

	def __init__(self, x, y):
		self.x = x 
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self):
		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y

	def move(self):
		self.tick_count += 1
		d = self.vel * self.tick_count + 1.5*self.tick_count**2

		if d >= 16: d = 16
		if d < 0: d -= 2

		self.y = self.y + d 
		
		if d < 0 or self.y < self.height + 50:
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
		else: 
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL

	def draw(self, win):
		self.img_count += 1

		if self.img_count <= self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count <= self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count <= self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count <= self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0

		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2

		blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)


def draw_window(win, bird):
	win.blit(bg_img, (0,0))
	bird.draw(win)
	pygame.display.update()

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def main():
	bird = Bird(200, 200)
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()

	run = True
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		bird.move()
		draw_window(win, bird)

	pygame.quit()
	quit()

main()