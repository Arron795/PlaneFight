import sys
import pygame

pygame.init()
from plane_sprites import *
# **************************************************************
# FileName: plane_main.py***************************************
# Author:  Junieson *********************************************
# Version:  2019.8.12 ******************************************
# ****************************************************************
class PlaneGame(object):
    """�ɻ���ս����Ϸ"""

    def __init__(self):
        print("��Ϸ��ʼ��")

        # 1. ������Ϸ�Ĵ���
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # ������������
        self.canvas_over = CanvasOver(self.screen)
        # 2. ������Ϸ��ʱ��
        self.clock = pygame.time.Clock()
        # 3. ����˽�з���������;�����Ĵ���
        self.__create_sprites()
        # ��������
        self.score = GameScore()
        # �������ָ��
        self.index = 0
        # ����bgm
        self.bg_music = pygame.mixer.Sound("./music/game_music.ogg")
        self.bg_music.set_volume(0.3)
        self.bg_music.play(-1)
        # ��Ϸ��������
        self.game_over = False
        # 4. ���ö�ʱ���¼� - �����л���1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, random.randint(1000, 2000))
        pygame.time.set_timer(HERO_FIRE_EVENT, 400)
        pygame.time.set_timer(BUFF1_SHOW_UP, random.randint(10000, 20000))
        pygame.time.set_timer(BUFF2_SHOW_UP, random.randint(20000, 40000))
        pygame.time.set_timer(ENEMY_FIRE_EVENT, 2000)

    def __create_sprites(self):

        # ������������;�����
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # �����л��ľ�����

        self.enemy_group = pygame.sprite.Group()

        # ����Ӣ�۵ľ���;�����
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        # �����о��ӵ���
        self.enemy_bullet_group = pygame.sprite.Group()

        # Ѫ���б�
        self.bars = []
        self.bars.append(self.hero.bar)

        # ����buff��
        self.buff1_group = pygame.sprite.Group()

        # ��������boom��
        self.enemy_boom = pygame.sprite.Group()

        # bomb�б�
        self.bombs = []

    def start_game(self):
        print("��Ϸ��ʼ...")

        while True:
            # 1. ����ˢ��֡��
            self.clock.tick(FRAME_PER_SEC)
            # 2. �¼�����
            self.__event_handler()
            # 3. ��ײ���
            self.__check_collide()
            # 4. ����/���ƾ�����
            self.__update_sprites()

            # �Ƿ�Ҫ������Ϸ

            if self.game_over:
                self.canvas_over.update()

            # 5. ������ʾ
            pygame.display.update()

    def __event_handler(self):  # �¼����

        if self.score.getvalue() > 200+500*self.index:
            self.boss = Boss()
            self.enemy_group.add(self.boss)
            self.bars.append(self.boss.bar)
            self.index += 1

        for event in pygame.event.get():
            # �ж��Ƿ��˳���Ϸ
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == CREATE_ENEMY_EVENT:
                # �����л����齫�л�������ӵ��л�������
                if self.score.getvalue() < 20:
                    enemy = Enemy()
                else:
                    if random.randint(0, 100) % 4:
                        enemy = Enemy()
                    else:
                        enemy = Enemy(2)

                self.enemy_group.add(enemy)
                self.bars.append(enemy.bar)

            elif event.type == HERO_FIRE_EVENT:
                for hero in self.hero_group:
                    hero.fire()
            elif event.type == BUFF1_SHOW_UP:
                buff1 = Buff1()
                self.buff1_group.add(buff1)
            elif event.type == BUFF2_SHOW_UP:
                if self.hero.bar.color == color_red:#�������
                    buff = Buff3()
                else:
                    buff= Buff2()
                self.buff1_group.add(buff)
            elif event.type == ENEMY_FIRE_EVENT:
                for enemy in self.enemy_group:
                    if enemy.number >= 2:
                        enemy.fire()
                        for bullet in enemy.bullets:
                            self.enemy_bullet_group.add(bullet)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bomb_throw()
            else:
                if self.game_over == True:
                    flag = self.canvas_over.event_handler(event)
                    if flag == 1:
                        self.__start__()
                    elif flag == 0:
                        pygame.quit()
                        sys.exit()

        # ʹ�ü����ṩ�ķ�����ȡ���̰��� - ����Ԫ��
        keys_pressed = pygame.key.get_pressed()
        # �ж�Ԫ���ж�Ӧ�İ�������ֵ 1
        if keys_pressed[pygame.K_RIGHT]:
            self.heros_move(5)
        elif keys_pressed[pygame.K_LEFT]:
            self.heros_move(-5)
        elif keys_pressed[pygame.K_UP]:
            self.heros_move(0, -5)
        elif keys_pressed[pygame.K_DOWN]:
            self.heros_move(0, 5)
        else:
            self.heros_move(0, 0)

    def heros_move(self, x=0, y=0):
        self.hero.speedx = x
        self.hero.speedy = y

    def bomb_throw(self):
        music_use_bomb = pygame.mixer.Sound("./music/use_bomb.wav")
        if self.hero.bomb > 0:
            music_use_bomb.play()
            self.hero.bomb -= 1
            self.bombs.pop()
            for enemy in self.enemy_group:
                if enemy.number < 3:
                    enemy.bar.length = 0
                    enemy.isboom = True
                else:
                    enemy.injury = 20
                    enemy.isboom = True

    def __check_collide(self):

        # 1. �ӵ��ݻٵл�
        for enemy in self.enemy_group:
            for hero in self.hero_group:
                for bullet in hero.bullets:
                    if pygame.sprite.collide_mask(bullet, enemy):  # ������ײ�����Ծ�ȷ������ȥ��alpha���ֵ�����Ŷ
                        bullet.kill()
                        enemy.injury = bullet.hity
                        enemy.isboom = True
                        if enemy.bar.length <= 0:
                            self.enemy_group.remove(enemy)
                            self.enemy_boom.add(enemy)

        # 2. �л�ײ��Ӣ��
        for enemy in self.enemy_group:
            if pygame.sprite.collide_mask(self.hero, enemy):
                if enemy.number < 3:
                    enemy.bar.length = 0  # �л�ֱ����
                    self.hero.injury = self.hero.bar.value / 4  # Ӣ�۵��ķ�֮һ��Ѫ
                    if self.hero.buff1_num > 0:
                        self.hero.buff1_num -= 1
                        self.hero.music_degrade.play()
                    self.enemy_group.remove(enemy)
                    self.enemy_boom.add(enemy)
                    enemy.isboom = True
                else:
                    self.hero.bar.length = 0
                self.hero.isboom = True

        # �ӵ��ݻ�Ӣ��
        for bullet in self.enemy_bullet_group:
            if pygame.sprite.collide_mask(self.hero, bullet):
                bullet.kill()
                self.hero.injury = 1
                if self.hero.buff1_num > 0:
                    self.hero.music_degrade.play()
                    if self.hero.buff1_num == 5:
                        self.mate1.kill()
                        self.mate2.kill()
                    self.hero.buff1_num -= 1

                self.hero.isboom = True

        if not self.hero.alive():
            self.hero.rect.right = -10  # ��Ӣ���Ƴ���Ļ
            if self.hero.buff1_num == 5:
                self.mate1.rect.right = -10
                self.mate2.rect.right = -10
            self.game_over = True

        # 3.buff����
        for buff in self.buff1_group:
            if pygame.sprite.collide_mask(self.hero, buff):
                buff.music_get.play()
                if buff.speedy == 1:  # ���ٶ�������
                    if self.hero.buff1_num < 6:
                        self.hero.buff1_num += 1
                        self.hero.music_upgrade.play()
                        if self.hero.buff1_num == 5:
                            self.team_show()

                elif buff.speedy==2:
                    self.hero.bomb += 1
                    image = pygame.image.load("./images/bomb.png")
                    self.bombs.append(image)
                elif buff.speedy==3:
                    if self.hero.bar.length < self.hero.bar.weight*self.hero.bar.value:
                        self.hero.bar.length += self.hero.bar.weight*self.hero.bar.value
                buff.kill()

    def team_show(self):
        self.mate1 = Heromate(-1)
        self.mate2 = Heromate(1)
        self.mate1.image = pygame.image.load("./images/life.png")
        self.mate1.rect = self.mate1.image.get_rect()
        self.mate2.image = pygame.image.load("./images/life.png")
        self.mate2.rect = self.mate2.image.get_rect()
        self.hero_group.add(self.mate1)
        self.hero_group.add(self.mate2)

    # ���ָ���
    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.enemy_boom.update()
        self.enemy_boom.draw(self.screen)

        self.heros_update()
        self.hero_group.draw(self.screen)

        for hero in self.hero_group:
            hero.bullets.update()
            hero.bullets.draw(self.screen)

        self.buff1_group.update()
        self.buff1_group.draw(self.screen)

        self.bars_update()
        self.bombs_update()

        self.enemy_bullet_group.update()
        self.enemy_bullet_group.draw(self.screen)

        self.score_show()

    def heros_update(self):
        for hero in self.hero_group:
            if hero.number == 1:
                hero.rect.bottom = self.hero.rect.bottom
                hero.rect.left = self.hero.rect.right
            if hero.number == -1:
                hero.rect.bottom = self.hero.rect.bottom
                hero.rect.right = self.hero.rect.left
            hero.update()

    def bars_update(self):
        for bar in self.bars:
            if bar.length > 0:
                bar.update(self.screen)
            else:
                self.bars.remove(bar)

    def bullet_enemy_update(self):
        for enemy in self.enemy_group:
            enemy.bullets.update()
            enemy.bullets.draw(self.screen)

    def bombs_update(self):
        i = 1
        for bomb in self.bombs:
            self.screen.blit(bomb, (0, 700 - (bomb.get_rect().height) * i))
            i += 1

    def score_show(self):
        score_font = pygame.font.Font("./STCAIYUN.ttf", 33)
        image = score_font.render("SCORE:" + str(int(self.score.getvalue())), True, color_gray)
        rect = image.get_rect()
        rect.bottom, rect.right = 700, 480
        self.screen.blit(image, rect)

    @staticmethod
    def __start__():
        # ������Ϸ����
        game = PlaneGame()

        # ������Ϸ
        game.start_game()


if __name__ == '__main__':
    PlaneGame.__start__()

