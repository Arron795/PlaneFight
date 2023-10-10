﻿from email.mime import image
from lzma import PRESET_DEFAULT
from pickle import FRAME
import random
import pygame


#常量定义用全大写字母，因为python里没有真正意义上的常量，都是动态变量，于是用约定俗成的全大写代表常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
FRAME_PER_SEC = 60
CREATE_ENEMY_EVENT = pygame.USEREVENT
CREATE_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
        """飞机大战游戏精灵"""

        def __init__(self,image_name,speed = 1):
           
           #调用父类的初始化方法，切记在初始化子类的时候要有这一步！
           super().__init__()

           #定义对象属性
           self.image = pygame.image.load(image_name)
           self.rect = self.image.get_rect()
           self.speed = speed

        def update(self):
            #在屏幕的垂直方向上移动
            self.rect.y += self.speed

class Background (GameSprite):
    """游戏背景精灵"""
    def __init__(self,is_alt = False):
        #1、调用父类方法实现精灵的创建
        super().__init__("./images/background.png")

        #2、判断是否交替图像，如果是，需要设置为True
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
       
        #1、调用父类方法实现
        super().update()

        #2、判断是否移出屏幕
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -SCREEN_RECT.height

class Enemy(GameSprite):
    """敌机精灵"""
    def __init__(self):
        #1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./images/enemy1.png")
        
        #2.指定敌机的初始随机速度
        self.speed = random.randint(1,3)

        #3.指定敌机的初始随机位置
        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)

        self.isboom = False


    def update(self):
        
        #1.调用父类方法，保持垂直方向飞行
        super().update()

        #2.判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            print("敌机飞出屏幕...")

            #kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()

        #
        if self.isboom:
            for i in (1,2,3,4):
                self.image = pygame.image.load("./images/enemy1_down"+str(i)+".png")



    def __del__(self):
        #print("敌机挂了 %s" % self.rect)
        self.kill()



class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):

        #1.调用父类方法，设置image 和 speed
        super().__init__("./images/me1.png",0)

        #2.设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        #3.创建子弹的精灵组
        
        self.bullets = pygame.sprite.Group()
     
    def update(self):
        
        #英雄在水平方向移动
        self.rect.x += self.speed

        #控制英雄不能离开屏幕
        if  self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("发射子弹biubiubiu")
        for i in (0,1,2):
                
            #1.创建子弹精灵
            bullet = Bullet()

            #2.设置子弹精灵位置
            bullet.rect.bottom = self.rect.y  - 20 * i
            bullet.rect.centerx = self.rect.centerx
        
            #3.将精灵添加到精灵组
            self.bullets.add(bullet)

class Bullet(GameSprite):
    """子弹精灵"""
    
    def __init__(self):

        #调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./images/bullet1.png",-2)
        
        #调用父类方法，让子弹垂直方向飞行
    def update(self):
        super().update()

        if self.rect.bottom < 0:
            self.kill()                 ##记得销毁子弹！
            

    def __del__(self):
        print("子弹飞出屏幕ovo")
             
