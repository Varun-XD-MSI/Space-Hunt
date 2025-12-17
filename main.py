import pygame
import math
import random
from pygame import mixer

pygame.init()  # initialise pygame

screen = pygame.display.set_mode((800,600))  # creating screen

# adding background
background = pygame.image.load("back.png")

#bg music

songs = ["MissionImpossibleTheme.mp3","pirates.mp3"]
current_song = 0 
mixer.music.load(songs[current_song])
mixer.music.play(-1)  # to play it on loop

# title and icon
pygame.display.set_caption("Jadoo ke tatte")
icon = pygame.image.load("ufo-flying.png")
pygame.display.set_icon(icon)
# player placing 

playerimg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
PlayerX_change = 0

# enemy placing
enemyimg = pygame.image.load("ufo.png")
enemyX =  random.randint(0,735)
enemyY = random.randint(50,150)
enemyX_change = 0.3
enemyY_change = 40
# bullet placing
# ready -  we cant see the bullet
# fire - we can see the bullet

bulletimg = pygame.image.load("bullet.png")
bulletX =  0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

#score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score:" + str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))



def player(x,y):
    screen.blit(playerimg,(x,y))   # use to draw image of player in playing window
def enemy(x,y):
    screen.blit(enemyimg,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# game loop
running = True

while running:

    screen.fill((0,0,0))
    #background addition
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keyboard input controls and key pressed event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -0.3
                
            if event.key == pygame.K_RIGHT:
                PlayerX_change = +0.3

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bsound = mixer.Sound("laser1.wav")
                    bsound.play()
                
                    bulletX = playerX  
                    fire_bullet(bulletX,bulletY)
            if event.key == pygame.K_p:
                mixer.music.stop()  # stops current song

                current_song =  (current_song + 1)% len(songs) # move to the next song

                mixer.music.load(songs[current_song])
                mixer.music.play(-1)

               
        if(event.type==pygame.KEYUP):
            if(event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                print("Key is released")
                PlayerX_change = 0

    # RGB
    # screen.fill((0,0,0))   
    playerX += PlayerX_change
    if(playerX<=0):
        playerX = 0

    elif(playerX>736):
        playerX = 736
   # enemy movement
    enemyX += enemyX_change

    if(enemyX<=0):
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif(enemyX>736):
        enemyX_change = -0.3
        enemyY += enemyY_change

   
    
    # bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX ,bulletY)
        bulletY -= bulletY_change

    # collision
    collision = iscollision(enemyX,enemyY,bulletX,bulletY)
    if collision:
        explosion = mixer.Sound("boom.mp3")
        explosion.play()
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        
        
        enemyX =  random.randint(0,735)
        enemyY = random.randint(50,150)







    player(playerX,playerY)
    enemy(enemyX,enemyY)

    show_score(textX,textY)
    pygame.display.update()
