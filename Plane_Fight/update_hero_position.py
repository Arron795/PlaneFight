from email.mime import image
from socket import herror
from time import sleep
from turtle import Screen, update
import pygame
from plane_sprites import *

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

#定义rect记录飞机的初始位置
hero_rect = pygame.Rect(150,300,102,126)

#创建敌机的精灵
enemy = GameSprite("./images/enemy1.png")
enemy1 = GameSprite("./images/enemy1.png",3)

#创建敌机的精灵组
enemy_group = pygame.sprite.Group(enemy,enemy1)

#游戏循环
while True:

    #设置屏幕刷新帧率
    clock.tick(60)

    #监听事件
    for event in pygame.event.get():

        #判断事件类型是否为退出事件
        if  event.type == pygame.QUIT:

            print("退出游戏...")

            #quit 卸载所有模块
            pygame.quit()

            #终止程序
            exit()

    #修改飞机位置
    hero_rect.y -= 5

    #判断飞机位置
    if hero_rect.y <= -126:
        hero_rect.y = 700

    #调用blit方法绘制图像
    screen.blit(bg,(0,0))
    screen.blit(hero,hero_rect)

    #   让精灵组调用两个方法
    #   update - 让组中的所有精灵更新位置
    enemy_group.update()
    #   draw - 在screen上绘制所有的精灵
    enemy_group.draw(screen)

    #调用update方法更新显示
    pygame.display.update()

    print(i)
    i += 1

pygame.quit()




