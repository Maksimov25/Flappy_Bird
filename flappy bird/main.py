import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 80)

imgBG = pygame.image.load('images/background.png')
imgBird = pygame.image.load('images/bird.png')
imgPT = pygame.image.load('images/pipe_top.png')
imgPB = pygame.image.load('images/pipe_bottom.png')

pygame.mixer.music.load('sounds/zima-kholoda.mp3')
pygame.mixer.music.set_volume(0.1) # громкость музыки
pygame.mixer.music.play(-1) # зацикливаем музыку

sndFall = pygame.mixer.Sound('sounds/fall.wav')

py, sy, ay = HEIGHT // 2, 0, 0 # sy - скорость персонажа, ay - ускорение
player = pygame.Rect(WIDTH // 3, py, 34, 24) # создание прямоугольника игрока

frame = 0
state = 'start'
timer = 10
pipes =[]
bges = []
pipesScores = []
pipeSpeed = 3
pipeGateSize = 200 # размер прохода
pipeGatePos = HEIGHT // 2 # позиция прохода

bges.append(pygame.Rect(0, 0, 288, 600)) # добавление первого фона

lives = 3
scores = 0

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    press = pygame.mouse.get_pressed() # управление
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    frame = (frame + 0.2) % 4 # отрисовка кадров для смены анимаций
    pipeSpeed = 3 + scores // 100

    for i in range (len(bges) - 1, -1, -1):
        bg = bges[i]
        bg.x -= pipeSpeed // 2 # движение фонов

        if bg.right < 0:
            bges.remove(bg)

        if bges[len(bges) - 1].right <= WIDTH:
            bges.append(pygame.Rect(bges[len(bges) - 1].right, 0, 288, 600))


    for i in range (len(pipes) - 1, -1, -1):
        pipe = pipes[i]
        pipe.x -= pipeSpeed # делаем трубы не статичными

        if pipe.right < 0:
            pipes.remove(pipe) # удаление труб
            if pipe in pipesScores:
                pipesScores.remove(pipe)

    if state == 'start':
        if click and timer == 0 and len(pipes) == 0: # начало игры после пролета всех труб
            state = 'play'

        py += (HEIGHT // 2 - py) * 0.1 # возвращем при сталкновении птицу к центру экрана
        player.y = py

    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0

        py += sy  # механика падения
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200: # добавляем трубы
            pipes.append(pygame.Rect(WIDTH, 0, 52, pipeGatePos - pipeGateSize // 2))
            pipes.append(pygame.Rect(WIDTH, pipeGatePos + pipeGateSize // 2 , 52, HEIGHT - pipeGatePos + pipeGateSize // 2))

            pipeGatePos += randint(-100, 100) # смещение прохода для верхней трубы
            if pipeGatePos < pipeGateSize:
                pipeGatePos = pipeGateSize
            elif pipeGatePos > HEIGHT - pipeGateSize: # для нижней
                pipeGatePos = HEIGHT - pipeGateSize


        if player.top < 0 or player.bottom > HEIGHT: # проверка столкновений с верхом и низом
            state = 'fall'

        for pipe in pipes: # проверка столкновений с трубой
            if player.colliderect(pipe):
                state = 'fall'

            if pipe.right < player.left and pipe not in pipesScores:
                pipesScores.append(pipe)
                scores += 5 # добавление очков

    elif state == 'fall':
        sndFall.play()
        sy, ay = 0, 0
        pipeGatePos = HEIGHT // 2

        lives -= 1
        if lives > 0:
            state = 'start'
            timer = 60
        else:
            state = 'game over'
            timer = 180

    else:
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if timer == 0:
            play = False

    window.fill(pygame.Color('black'))
    for bg in bges:
        window.blit(imgBG, bg)

    for pipe in pipes:
        if pipe.y == 0:
            rect = imgPT.get_rect(bottomleft = pipe.bottomleft) # формируем новое положение для изображения
            window.blit(imgPT, rect) # вывод на экран изображения
        else:
            rect = imgPB.get_rect(topleft=pipe.topleft)  # формируем новое положение для изображения
            window.blit(imgPB, rect)

    image = imgBird.subsurface(34 * int(frame), 0, 34, 24) # формируем изображение
    image = pygame.transform.rotate(image, -sy * 2) # вращаем клюв птицы взаисимости от нахождения птицы в текущий момент
    window.blit(image, player) # вывод картинки птицы

    text = font1.render('Очки: ' + str(scores), 1, pygame.Color('black'))
    window.blit(text, (10, 10)) # вывод очков

    text = font1.render('Жизни: ' + str(lives), 1, pygame.Color('black'))
    window.blit(text, (10, HEIGHT - 30))  # вывод жизней

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()