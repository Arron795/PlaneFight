from email.mime import image
from socket import herror
from time import sleep
from turtle import update
import pygame

pygame.init()

screen = pygame.display.set_mode((480,700))          #(480,700)是一整个元组 作为一个size的参数

#绘制背景图像
#1、 加载图像数据
bg = pygame.image.load("./images/background.png")

#2、 blit 绘制图像
screen.blit(bg,(0,0))

#3、 update更新屏幕显示
#pygame.display.update()

#显示英雄图像
hero = pygame.image.load("./images/me1.png")
screen.blit(hero,(200,500))
pygame.display.update()     ##只需要再所有blit绘制图像后 调用一次display.update()即可

#sleep(2)       延时2秒

#创建游戏时钟对象
clock = pygame.time.Clock()
i  = 0

#游戏循环
while True:

    #设置屏幕刷新帧率
    clock.tick(60)

    print(i)
    i += 1

pygame.quit()




