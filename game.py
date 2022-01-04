import pygame
import random
import math
from pygame import mixer


# Initialize the pygame
import pygame.sprite

pygame.init()

# Create the screen
# h, w or x, y axis
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('background.png')

# Title of the screen and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)


# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


# Enemy
# For multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
# Won't use it x direc
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Font

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # Appear on the center of spaceship
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False



# Game Loop
running = True

while running:
    # rgb 
    screen.fill((0, 0, 0))
    # bcg image
    screen.blit(background, (0, 0))
    # playerX += 0.2


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystoke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current X coridnate of the ufo
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    

    
    # Checnking for boundaries of spaceship so it doesnt go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    # Enemy movement    
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
























