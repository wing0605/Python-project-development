#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''==============================================
@Project -> File   ：Python项目开发实战入门 -> marie
@IDE    ：PyCharm
@Author ：Liu Yimin
@Date   ：2021-01-13 21:32
@Desc   ：
==============================================='''
import pygame  # 将pygame库导入到Python程序中
from pygame.locals import *  # 导入pygame中的常量
from itertools import cycle  # 导入迭代工具

import sys
import random  # 随机数

SCREENWIDTH = 822  # 窗口宽度
SCREENHEIGHT = 199  # 窗口高度
FPS = 30  # 更新画面的时间


# 定义一个移动地图
class MyMap():

	def __init__(self, x, y):
		# 加载背景图片
		self.bg = pygame.image.load("image/bg.png").convert_alpha()
		self.x = x
		self.y = y

	def map_rolling(self):
		# 根据地图背景图片的x坐标判断是否移出窗体，如果移除就给图片设置一个新的坐标点，否则按照每次5个像素向左移动
		if self.x < -790:  # 小于-790说明地图已经完全移动完毕
			self.x = 800  # 给地图一个新的坐标点
		else:
			self.x -= 5  # 向左移动5个像素

	# 更新地图
	def map_update(self):
		SCREEN.blit(self.bg, (self.x, self.y))


# 障碍类
class Obstacle():
	score = 1  # 分数
	move = 5  # 移动距离
	obstacle_y = 150  # 障碍物的y坐标

	def __init__(self):
		# 初始化障碍物矩形
		self.rect = pygame.Rect(0, 0, 0, 0)
		# 加载障碍物图片
		self.missile = pygame.image.load('image/missile.png').convert_alpha()
		self.pipe = pygame.image.load('image/pipe.png').convert_alpha()
		# 加载分数
		self.numbers = (
			pygame.image.load('image/0.png').convert_alpha(),
			pygame.image.load('image/1.png').convert_alpha(),
			pygame.image.load('image/2.png').convert_alpha(),
			pygame.image.load('image/3.png').convert_alpha(),
			pygame.image.load('image/4.png').convert_alpha(),
			pygame.image.load('image/5.png').convert_alpha(),
			pygame.image.load('image/6.png').convert_alpha(),
			pygame.image.load('image/7.png').convert_alpha(),
			pygame.image.load('image/8.png').convert_alpha(),
			pygame.image.load('image/9.png').convert_alpha(),
		)
		# 加载得分音效
		self.score_audio = pygame.mixer.Sound('audio/score.wav')
		# 0 和1 随机数
		r = random.randint(0, 1)
		if r == 0:  # 如果随机数为0显示导弹， 否则显示管道
			self.image = self.missile  # 显示导弹
			self.move = 15  # 移动速度加快
			self.obstacle_y = 100  # 导弹坐标在天上
		else:
			self.image = self.pipe  # 显示管道
		# 根据障碍物图的宽，高来设置矩形
		self.rect.size = self.image.get_size()
		# 获取位图的高宽
		self.width, self.height = self.rect.size
		# 障碍物绘制坐标
		self.x = 800
		self.y = self.obstacle_y
		self.rect.center = (self.x, self.y)

	# 障碍物移动
	def obstacle_move(self):
		self.rect.x -= self.move

	# 绘制障碍物
	def draw_obstacle(self):
		SCREEN.blit(self.image, (self.rect.x, self.rect.y))


# 玛丽类
class Marie():
	def __init__(self):
		# 初始化玛丽矩形
		self.rect = pygame.Rect(0, 0, 0, 0)
		self.jumpState = False  # 跳跃的状态
		self.jumpHeight = 130  # 跳跃的高度
		self.lowest_y = 140  # 最低坐标
		self.jumpValue = 0  # 跳跃增变量
		# 玛丽动图索引
		self.marieIndex = 0
		self.marieIndexGen = cycle([0, 1, 2])
		# 加载玛丽照片
		self.adventure_img = (
			pygame.image.load('image/adventure1.png').convert_alpha(),
			pygame.image.load('image/adventure2.png').convert_alpha(),
			pygame.image.load('image/adventure3.png').convert_alpha(),
		)
		self.jump_audio = pygame.mixer.Sound('audio/jump.wav')  # 跳跃音效
		self.rect.size = self.adventure_img[0].get_size()
		self.x = 50  # 绘制玛丽的x坐标
		self.y = self.lowest_y  # 绘制玛丽的Y坐标
		self.rect.topleft = (self.x, self.y)

	# 跳状态
	def jump(self):
		self.jumpState = True

	# 玛丽移动
	def move(self):
		if self.jumpState:  # 当起跳的时候
			if self.rect.y >= self.lowest_y:  # 如果站在地上
				self.jumpValue = -5  # 以5个像素值向上移动
			if self.rect.y <= self.lowest_y - self.jumpHeight:  # 玛丽到达顶部回落
				self.jumpValue = 5  # 以5个像素值向下移动
			self.rect.y += self.jumpValue  # 通过循环改变玛丽的坐标
			if self.rect.y >= self.lowest_y:  # 如果玛丽回到地面
				self.jumpState = False  # 关闭跳跃状态

	# 绘制玛丽
	def draw_marie(self):
		# 匹配玛丽动图
		marieTndex = - next(self.marieIndexGen)
		# 绘制玛丽
		SCREEN.blit(self.adventure_img[marieTndex],
		            (self.x, self.rect.y))


def mainGame():
	score = 0  # 得分
	over = False  # 游戏结束标记
	global SCREEN, FPSCLOCK  # 将SCREEN, FPSCLOCK 两个变量全局化
	pygame.init()  # 经过初始化以后我们就可以尽情的使用pygame了
	# 使用Python时钟控制每个循环多长时间运行一次。在使用时钟前必须先创建Clock对象的一个实例
	FPSCLOCK = pygame.time.Clock()
	# 通常来说我们需要先创建个一个窗体，方便我们与程序的交互,设置窗体高和宽
	SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
	pygame.display.set_caption('玛丽冒险')  # 设置窗体标题
	# 创建地图对象
	bg1 = MyMap(0, 0)
	bg2 = MyMap(800, 0)
	# 创建玛丽对象
	marie = Marie()

	# 添加障碍物的时间
	addObstacleTimer = 0
	# 障碍物对象列表
	list = []

	while True:
		# 获取单击事件
		for event in pygame.event.get():
			# 如果点击了关闭窗体就将窗体关闭
			if event.type == QUIT:
				pygame.quit()  # 退出窗口
				sys.exit()  # 关闭窗口
			# 按下键盘上的空格键，开启跳跃的状态
			if event.type == KEYDOWN and event.key == K_SPACE:
				if marie.rect.y >= marie.lowest_y:  # 如果玛丽在地上
					marie.jump_audio.play()  # 播放玛丽跳跃音效
					marie.jump()  # 开启玛丽跳跃

		if over == False:
			# 绘制地图，起到更新地图的作用
			bg1.map_update()
			# 地图移动
			bg1.map_rolling()
			bg2.map_update()
			bg2.map_rolling()

			# 玛丽移动
			marie.move()
			# 绘制玛丽
			marie.draw_marie()

			# 计算障碍物间隔时间
			if addObstacleTimer >= 1300:
				r = random.randint(0, 100)
				if r > 40:
					# 创建障碍物对象
					obstacle = Obstacle()
					# j将障碍物对象添加到列表中
					list.append(obstacle)
				# 重置添加障碍物时间
				addObstacleTimer = 0

			# 循环遍历障碍物
			for i in range(len(list)):
				# 障碍物移动
				list[i].obstacle_move()
				# 绘制障碍物
				list[i].draw_obstacle()
		addObstacleTimer += 20  # 增加障碍物时间
		pygame.display.update()  # 更新整个窗体
		FPSCLOCK.tick(FPS)  # 循环应该多长时间运行一次


if __name__ == '__main__':
	mainGame()
