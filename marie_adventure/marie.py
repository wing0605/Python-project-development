#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''==============================================
@Project -> File   ：Python项目开发实战入门 -> marie
@IDE    ：PyCharm
@Author ：Liu Yimin
@Date   ：2021-01-13 21:32
@Desc   ：
==============================================='''
import pygame                   # 将pygame库导入到Python程序中
from pygame.locals import *     # 导入pygame中的常量
import sys

SCREENWIDTH = 822               # 窗口宽度
SCREENHEIGHT = 199              # 窗口高度
FPS = 30                        # 更新画面的时间


def mainGame():
	score = 0                   # 得分
	over = False                # 游戏结束标记
	global SCREEN, FPSCLOCK     # 将SCREEN, FPSCLOCK 两个变量全局化
	pygame.init()               # 经过初始化以后我们就可以尽情的使用pygame了
	# 使用Python时钟控制每个循环多长时间运行一次。在使用时钟前必须先创建Clock对象的一个实例
	FPSCLOCK = pygame.time.Clock()
	# 通常来说我们需要先创建个一个窗体，方便我们与程序的交互,设置窗体高和宽
	SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
	pygame.display.set_caption('玛丽冒险')  # 设置窗体标题
	while True:
		# 获取单击事件
		for event in pygame.event.get():
			# 如果点击了关闭窗体就将窗体关闭
			if event.type == QUIT:
				pygame.quit()       # 退出窗口
				sys.exit()          # 关闭窗口
		pygame.display.update()     # 更新整个窗体
		FPSCLOCK.tick(FPS)          # 循环应该多长时间运行一次

if __name__ == '__main__':
    mainGame()

