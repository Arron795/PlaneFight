from email.mime import image
from socket import herror
from time import sleep
from turtle import update
import pygame

pygame.init()

screen = pygame.display.set_mode((480,700))          #(480,700)��һ����Ԫ�� ��Ϊһ��size�Ĳ���

#���Ʊ���ͼ��
#1�� ����ͼ������
bg = pygame.image.load("./images/background.png")

#2�� blit ����ͼ��
screen.blit(bg,(0,0))

#3�� update������Ļ��ʾ
#pygame.display.update()

#��ʾӢ��ͼ��
hero = pygame.image.load("./images/me1.png")
screen.blit(hero,(200,500))
pygame.display.update()     ##ֻ��Ҫ������blit����ͼ��� ����һ��display.update()����

#sleep(2)       ��ʱ2��

#������Ϸʱ�Ӷ���
clock = pygame.time.Clock()
i  = 0

#��Ϸѭ��
while True:

    #������Ļˢ��֡��
    clock.tick(60)

    print(i)
    i += 1

pygame.quit()




