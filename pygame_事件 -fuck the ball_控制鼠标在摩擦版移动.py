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
		self.radius = self.rect.width/2
		
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
#生成摩擦版
class Glassboard(pygame.sprite.Sprite):
		def __init__(self,glassboard_image,mouse_image,bg_size):
			#初始化动画精灵
			pygame.sprite.Sprite.__init__(self)
			#摩擦版
			self.glassboard_image = pygame.image.load(glassboard_image).convert_alpha()
			self.glassboard_rect = self.glassboard_image.get_rect()
			self.glassboard_rect.left , self.glassboard_rect.top = (bg_size[0] - self.glassboard_rect.width)//2,\
																							  (bg_size[1] - self.glassboard_rect.height)
			#鼠标
			self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
			self.mouse_rect = self.mouse_image.get_rect()
			self.mouse_rect.left , self.mouse_rect.top = self.glassboard_rect.left , self.glassboard_rect.top
			
			#设置原来在摩擦版的鼠标不可见
			pygame.mouse.set_visible(False)
			
def main():
	pygame.init()
	mouse_image = "鼠标.png"
	glassboard_image = "摩擦版.png"
	ball_image = "100像素精灵球.png"
	bg_image = "草原5个点.png"
	go_image = "游戏结束.png"
	
	running = True
	#添加背景音乐
	pygame.mixer.music.load("bg_music2.mp3")
	pygame.mixer.music.set_volume(0.2)
	pygame.mixer.music.play()
	
	#添加特效
	win_sound = pygame.mixer.Sound("成功.wav")
	lose_sound = pygame.mixer.Sound("失败.wav")
	hole_sound = pygame.mixer.Sound("球进洞.wav")
	
	#音乐播完之后，发送一个游戏结束的事件过去
	GAMEOVER = USEREVENT
	pygame.mixer.music.set_endevent(GAMEOVER)
	
	bg_size = width , height = 801,502 
	screen = pygame.display.set_mode(bg_size)
	pygame.display.set_caption("python_fuck the ball_初步结构")
	
	background = pygame.image.load(bg_image).convert_alpha()
	
	balls =[]
	ball_num=5
	#创建一个组，用于碰撞函数
	group = pygame.sprite.Group()
	#生成5个ball
	for i in range(ball_num):
		position = randint(0,width-100),randint(0,height-100)
		print(position)
		speed = [randint(-10,10),randint(-10,10)]
		ball = Ball(ball_image,position,speed,bg_size)
		while pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
			ball.rect.left,ball.rect.top = randint(0,width-100),randint(0,height-100) 
		balls.append(ball)
		group.add(ball)
		
	#生成一个摩擦版带鼠标
	glassboard = Glassboard(glassboard_image,mouse_image,bg_size)
	#时间对象
	clock = pygame.time.Clock()
	#加载图片
	gameover_image = pygame.image.load(go_image).convert_alpha() 
	
	#获取gameover的图片rect
	go_rect = gameover_image.get_rect()
	#获取界面中间的位置，填gameover图片
	go_rect.left , go_rect.top = (width-go_rect.width)//2 , (height-go_rect.height)//2
	#gameover_display设置为False,不显示gameover_image
	gameover_display = False
	
	
	while running:
		for event in  pygame.event.get():
			if event.type == QUIT:
				sys.exit
			if event.type == GAMEOVER:
				lose_sound.play()
				pygame.time.delay(2000)
				gameover_display = True
				running = False
				
		#显示背景
		screen.blit(background,(0,0))
		#显示摩擦版
		screen.blit(glassboard.glassboard_image,glassboard.glassboard_rect)
		#获取真正鼠标的位置
		glassboard.mouse_rect.left , glassboard.mouse_rect.top = pygame.mouse.get_pos()
		print(glassboard.mouse_rect.right)
		#如果鼠标位置越过摩擦版的左边界，则纠正
		if glassboard.mouse_rect.left < glassboard.glassboard_rect.left:
			glassboard.mouse_rect.left = glassboard.glassboard_rect.left
		#右边界
		if glassboard.mouse_rect.left >glassboard.glassboard_rect.right - glassboard.mouse_rect.width:
			glassboard.mouse_rect.left = glassboard.glassboard_rect.right- glassboard.mouse_rect.width
		#buttom
		#不能是lassboard.glassboard_rect.height- glassboard.mouse_rect.height，因为height是摩擦版的高度
		#要求是整个界面的高度，所以为bottom
		if glassboard.mouse_rect.top > glassboard.glassboard_rect.bottom - glassboard.mouse_rect.height:
			glassboard.mouse_rect.top = glassboard.glassboard_rect.bottom - glassboard.mouse_rect.height
		#top
		#什么时候用top，什么时候用height？
		#top表示对象的高坐标，height表示对象的高
		if glassboard.mouse_rect.top < glassboard.glassboard_rect.top:
			glassboard.mouse_rect.top = glassboard.glassboard_rect.top
		
		#显示鼠标
		screen.blit(glassboard.mouse_image,glassboard.mouse_rect)
		#显示ball
		for ball in balls:
			ball.move()
			screen.blit(ball.image,ball.rect)
		for ball in group:
			group.remove(ball)
			#检测碰撞函数
			if pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
				ball.speed[0] = -ball.speed[0]
				ball.speed[1] = -ball.speed[1]
			group.add(ball)
		#如果结束，则显示gameover_image
		if gameover_display:
			screen.blit(gameover_image,go_rect)
		pygame.display.flip()
		
		clock.tick(30)
		
if __name__ == '__main__':
	main()
