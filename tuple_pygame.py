import pygame
from random import randint #генерация рандомных чисел в диапазоне
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT)) #создаем окно с картежем высоты и ширины экрана
clock = pygame.time.Clock() #контролируем кл/во кадров в секунду

#главный игровой цикл
play = True
while play:
    for event in pygame.event.get(): #возвращаем все события с последнего опроса и обрабатываем по очереди
        if event.type == pygame.QUIT:
            play = False

    pygame.display.update() #обновляем окно
    clock.tick(FPS)

pygame.quit()