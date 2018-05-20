import pygame
import sys
from pygame.locals import *
from random import *

class Ball(pygame.sprite.Sprite):#ball继承pygame的中精灵基类
	def __init__(self,image,grayball_image,position,speed,bg_size,target):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.left,self.rect.top = position
		self.grayball_image = pygame.image.load(grayball_image).convert_alpha()
		self.speed = speed
		self.side = [choice([-1,1]),choice([-1,1])]#choice从一个列表里面选一个【】
		self.width,self.height = bg_size[0],bg_size[1]
		self.radius = self.rect.width/2
		self.target = target
		self.control = False
		self.collide = False
		
	#运动	
	def move(self):
		#区分随机方向和空盒子方向
		if self.control:
			self.rect = self.rect.move(self.speed)
		else:
			self.rect = self.rect.move(self.side[0] * self.speed[0] , \
												self.side[1] * self.speed[1])
		if  self.rect.right < 0:
			self.rect.left = self.width
		if self.rect.left > self.width:
			self.rect.right = 0
		if self.rect.bottom < 0:
			self.rect.top = self.height
		if self.rect.top > self.height:
			self.rect.bottom = 0
	#check检测鼠标1秒产生的事件是否匹配ball的target
	def check(self,motion):
		if self.target < motion < self.target+5:#范围
			return True
		else:
			return False
			
			
			
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
	grayball_image ="100像素精灵球灰色.png"
	victory_image = "victory.png"
	
	running = True
	#添加背景音乐
	pygame.mixer.music.load("bg_music2.mp3")
	pygame.mixer.music.set_volume(0.8)
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
	
	hole=[(93,103,91,101),(388,398,191,201),(623,633,42,52),(608,618,321,331),(93,103,341,351)]
	victorys=[]
	
	balls =[]
	ball_num=5
	#创建一个组，用于碰撞函数
	group = pygame.sprite.Group()
	#生成5个ball
	for i in range(ball_num):
		position = randint(0,width-100),randint(0,height-100)
		print(position)
		speed = [randint(1,3),randint(1,3)]
		#5*(i+1)表示target,target表示每个球的目标，即鼠标每一秒产生的事件需匹配这个target，然后可控
		ball = Ball(ball_image,grayball_image,position,speed,bg_size,6*(i+1))
		while pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
			ball.rect.left,ball.rect.top = randint(0,width-100),randint(0,height-100) 
		balls.append(ball)
		group.add(ball)
	
	#生成motion参数，即鼠标的事件数
	motion =  0 
	#自定义事件,记录鼠标
	MYITEM = USEREVENT+1
	pygame.time.set_timer(MYITEM,1000)
	#生成一个摩擦版带鼠标
	glassboard = Glassboard(glassboard_image,mouse_image,bg_size)

	#加载图片
	gameover_image = pygame.image.load(go_image).convert_alpha() 
	
	#获取gameover的图片rect
	go_rect = gameover_image.get_rect()
	#获取界面中间的位置，填gameover图片
	go_rect.left , go_rect.top = (width-go_rect.width)//2 , (height-go_rect.height)//2
	#gameover_display设置为False,不显示gameover_image
	gameover_display = False
	#设置键盘按住之后的重复事件，即按住上下左右可以，有不同的加速度
	pygame.key.set_repeat(100,100)#参数1的100是100毫秒后开始，参数2的100是每100毫秒的响应一次
	#时间对象
	clock = pygame.time.Clock()
	
	
	while running:
		for event in  pygame.event.get():
			if event.type == QUIT:
				sys.exit
			#识别游戏结束
			if event.type == GAMEOVER:
				lose_sound.play()
				pygame.time.delay(2000)
				gameover_display = True
				running = False
			#识别鼠标事件是否匹配球的目标
			if event.type == MYITEM:
				if motion :
					for each in group :
						if each.check(motion):
							each.speed = [0,0]
							each.control = True
					motion = 0
			#记录鼠标事件
			if event.type == MOUSEMOTION:
				motion += 1
			#键盘事件
			if event.type == KEYDOWN:
				
				if event.key == K_w:
					for ball in group:
						if ball.control:
							#因为w是向上的意思，且坐标轴向上为递减
							ball.speed[1] -= 1
				if event.key == K_s:
					for ball in group:
						if ball.control:
							ball.speed[1] += 1
				if event.key == K_a:
					for ball in group:
						if ball.control:
							ball.speed[0] -= 1
				if event.key == K_d:
					for ball in group:
						if ball.control:
							ball.speed[0] +=1
				#路过坑里就按空格键，锁定球
				if  event.key == K_SPACE:
					
					for ball in group:
						if ball.control:
							for i in hole:
								print("进入for循环")
								if i[0] <= ball.rect.left <= i[1] and \
									i[2] <= ball.rect.top <=i[3]:
									win_sound.play()
									ball.speed = [0,0]
									group.remove(ball)
									#锁定球之后，其他球就会从上面飞过，无碰撞
									temp = balls.pop(balls.index(ball))#把球从原来的balls pop出来
									balls.insert(0,temp)#再把球插到balls的第一个位置
									#删除坑
									hole.remove(i)
							#如果没有坑了，就游戏胜利
							if not hole:
								print("胜利")
								pygame.mixer.music.stop()#停止音乐
								win_sound.play()#再播放胜利的音乐
								pygame.time.delay(3000)#延迟3秒
								victory = pygame.image.load(victory_image).convert_alpha()
								
								victory_position = (width - victory_image.get_width())//2,\
															(height - victory_image.get_height())//2
								victorys.append((victory,victory_position))
								
				
		#显示背景
		screen.blit(background,(0,0))
		#显示摩擦版
		screen.blit(glassboard.glassboard_image,glassboard.glassboard_rect)
		#获取真正鼠标的位置
		glassboard.mouse_rect.left , glassboard.mouse_rect.top = pygame.mouse.get_pos()
		
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
			#检测是否碰撞，反向
			if ball.collide:
				ball.speed = [randint(1,3),randint(1,3)]
				ball.collide=False
			#检测是否可控，变色
			if ball.control:
				#可控球，灰色
				screen.blit(ball.grayball_image,ball.rect)
			else:
				#不可控，正常颜色
				screen.blit(ball.image,ball.rect)
		for ball in group:
			group.remove(ball)
			#检测碰撞函数
			if pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
				ball.side[0] = -ball.side[0]
				ball.side[1] = -ball.side[1]
				#碰撞后颜色改变之前，设置side=-1
				if ball.control:	
					ball.side[0] = -1
					ball.side[1] = -1
					ball.control = False
				#碰撞记录
				ball.collide  = True
			group.add(ball)
		
		for each in victorys:
			screen.blit(each[0],each[1])
		#如果结束，则显示gameover_image
		if gameover_display:
			screen.blit(gameover_image,go_rect)
			
		pygame.display.flip()
		
		clock.tick(30)
		
if __name__ == '__main__':
	main()
