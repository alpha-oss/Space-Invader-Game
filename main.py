import pygame
import random
import math

from pygame import mixer

#To intialize pygame modulel
pygame.init()
clock=pygame.time.Clock()

#To set the game window
screen= pygame.display.set_mode((800,600))

#To change the logo , game name

pygame.display.set_caption("Space Invader")
icon=pygame.image.load('./Icons/spaceship1.png')
pygame.display.set_icon(icon)

#now to add image on our game window
playerimg=pygame.image.load('./Icons/spaceship1.png')
playerX=370
playerY=480
playerX_change=0

# BACKGROUND IMAGE OF GAME
backgroundimg = pygame.image.load('./Icons/space.png')

#BACKGROUND MUSIC 
mixer.music.load('./sounds/background.wav')
mixer.music.play(-1)

# enemy in game
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemy=6
for i in range(no_of_enemy):
    enemyimg.append(pygame.image.load('./Icons/enemy.png'))
    enemyX.append(random.randint(0,735))        
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# bullet in game
bulletimg=pygame.image.load('./Icons/bullet.png')
bulletX=0
bulletY=480
bulletY_change=40
bullet_state = "ready"

#SCORE
score_value=0
font = pygame.font.Font("freesansbold.ttf",35)

#GAME OVER DISPLAY STYLE
gameover = pygame.font.Font("freesansbold.ttf",74)

scoreX=10
scoreY=10

def show_score(x,y):
    score= font.render("Score:"+str(score_value),True,(0,255,0))
    screen.blit(score,(x,y))


def game_over():
    game=gameover.render("GAME OVER",True,(255,255,255))
    screen.blit(game,(200,250))


def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))


def isCollide(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow((enemyX-bulletX),2) + math.pow((enemyY-bulletY),2))
    if distance<27:
        return True
    else:
        return False

#To set the game window for longer time
running=True
while running:
    
    #NOW TO ADD RED GREEN AND BLUE COLOUR
    screen.fill((0,0,45))

    #BACKGROUNG IMAGE
    screen.blit(backgroundimg, (0,0))
    
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False
            

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                playerX_change= -6
            if event.key == pygame.K_RIGHT:
                playerX_change= 6
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                     bullet_sound=mixer.Sound('./sounds/laser.wav')
                     bullet_sound.play()
                     #so to get current x-coordinate of the spaceship
                     bulletX=playerX
                     fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.type== pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change=0
    
    #spaceship movement
    playerX+=playerX_change

    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    # enemy movement
    for i in range(no_of_enemy):

        #DISPLAY GAME OVER
        if enemyY[i]>440:
            for j in range(no_of_enemy):
                enemyY[i]=2000
            game_over()
            break




        enemyX[i] += enemyX_change[i]

        if enemyX[i]<=0:
            enemyX_change[i] = 7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]= -7         
            enemyY[i] += enemyY_change[i]

        
        #Collison part
        collison =isCollide(enemyX[i],enemyY[i],bulletX,bulletY)
        if collison:
            collide_sound=mixer.Sound('./sounds/explosion.wav')
            collide_sound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1
            
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)    
        
        enemy(enemyX[i],enemyY[i],i)

    # Bullet Movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    
    player(playerX,playerY)
    show_score(scoreX,scoreY)
    
    pygame.display.update()


      