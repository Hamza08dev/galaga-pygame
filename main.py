import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 650))

background = pygame.image.load('galaga_bg.png')

player_img = pygame.image.load('spaceship.png')
playerX = 360
playerY = 480
playerX_change = 0

enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(17)

bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def Is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Score

Score_value = 0
font = pygame.font.Font('Benguiat Bold.ttf', 28)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score:" + str(Score_value), True, (80, 20, 100))
    screen.blit(score, (x, y))


running = True
while True:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5
            if event.key == pygame.K_LEFT:
                playerX_change = -2.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0


    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    playerX += playerX_change

    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = +4
            enemyX[i] = 0
            enemyY[i] += enemyY_change[i]

        collision = Is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            Score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    show_score(textX, textY)
    player(playerX, playerY)

    pygame.display.update()
