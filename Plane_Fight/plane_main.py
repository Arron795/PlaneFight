from json.tool import main
from multiprocessing.spawn import _main
from tkinter.tix import MAIN
import pygame
from plane_sprites import * 

class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self) -> None:
       print("游戏初始化...")

       #1.创建游戏窗口
       self.screen = pygame.display.set_mode(SCREEN_RECT.size)
       #2.创建游戏的时钟
       self.clock = pygame.time.Clock()
       #3.调用私有方法，精灵和精灵组的创建
       self.__create_sprites()

       #4.设置定时器事件   - 创建敌机 1s  即  1000ms
       pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
       pygame.time.set_timer(CREATE_FIRE_EVENT,500)


    def __create_sprites(self):
        # 创建背景精灵和精灵组

        #bg1 = Background("./images/background.png")
        #bg2 = Background("./images/background.png")
        #bg2.rect.y = -bg2.rect.height
        bg1 = Background()      #默认是False,第一张图片和游戏窗口大小重合
        bg2 = Background(True)  #设为True后，第二张图片在游戏窗口往上距离原点窗口长度位置开始

        self.back_group = pygame.sprite.Group(bg1,bg2)

        #创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        #创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
     

        
    def start_game(self):
        print("游戏开始!!")

        while True:
            #1、设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #2、事件监听
            self.__event_handler()
            #3、碰撞检测
            self.__check_collide()              ##记得加括号！！
            #4、更新/绘制精灵组
            self.__update_sprites()
            #5、更新显示
            pygame.display.update()
            

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           ##这里是pygame.QUIT 不是 event.QUIT
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出场！")

                #创建敌机精灵
                enemy = Enemy()
                #将敌机精灵添加到敌机精灵组中
                self.enemy_group.add(enemy)

                #*如果用事件监听做按键操作，那么将会出现按下之后只会执行一次操作，不会持续执行
                #*因此用键盘模块做按键操作更好，可以持续输出按键操作


            elif event.type == CREATE_FIRE_EVENT:
                self.hero.fire()



        #使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        #判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        enemies = pygame.sprite.groupcollide(self.hero_group,self.enemy_group,False,True)

        if len(enemies)>0:
            self.hero.kill();

            PlaneGame.__game_over();


    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
      
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod       #静态方法
    def __game_over():
        print("游戏结束！")
        
        pygame.quit()
        exit()


if __name__ == '__main__':
    
    #创建游戏对象
    game = PlaneGame()

    #启动游戏
    game.start_game()

