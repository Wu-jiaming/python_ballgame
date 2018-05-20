import pygame
import sys
from pygame.locals import *
from random import *

class Ball(pygame.sprite.Sprite):#ball继承pygame的中精灵基类
	def __init__(self,image,position,speed,bg_size):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.left,self.rect.top = position
		self.speed = speed
		self.width,self.height = bg_size[0],bg_size[1]
	#运动	
	def move(self):
		self.rect = self.rect.move(self.speed)
		if  self.rect.right < 0:
			self.rect.left = self.width
		if self.rect.left > self.width:
			self.rect.right = 0
		if self.rect.bottom < 0:
			self.rect.top = self.height
		if self.rect.top > self.height:
			self.rect.bottom = 0
	
def main():
	pygame.init()
	ball_image = "100像素精灵球.png"
	bg_image = "草原5个点.png"
	
	running = True
	
	bg_size = width , height = 801,502 
	screen = pygame.display.set_mode(bg_size)
	pygame.display.set_caption("python_fuck the ball_初步结构")
	
	background = pygame.image.load(bg_image).convert_alpha()
	
	balls =[]
	
	for i in range(5):
		position = randint(0,width-100),randint(0,height-100)
		print(position)
		speed = [randint(-10,10),randint(-10,10)]
		ball = Ball(ball_image,position,speed,bg_size)
		balls.append(ball)

	clock = pygame.time.Clock()
	
	while running:
		for event in  pygame.event.get():
			if event.type == QUIT:
				sys.exit
				
		screen.blit(background,(0,0))
		
		for ball in balls:
			ball.move()
			screen.blit(ball.image,ball.rect)
		
		pygame.display.flip()
		clock.tick(30)
		
if __name__ == '__main__':
	main()
