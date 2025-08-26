#!/usr/bin/env python

import pygame
import sys
import os
import time
##Game Jam GAme!!!
## SO NERVOUS!!

##settings

FPS = 60
RES = WIDTH, HEIGHT = 800, 600
CAPTION = "OverDrive"
PL_POS = [int(WIDTH/2),int(HEIGHT/2)]
PL_SPD = 3
PL_ACC_Y = 2 
START_TIME = time.time()
Y_MOMENTUM = 0

running = False

##some things

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
active_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

player_img = pygame.image.load(os.path.join("assets","man.png")).convert()
player_img.set_colorkey("black")
player_rect = player_img.get_rect()

pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "star.png")).convert())
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

##main game loop



def main():
    global START_TIME

    while running:
       
        dt = time.time() - START_TIME
        dt *= FPS
        START_TIME = time.time()

        screen.fill("grey")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
        
        ##Player moevment
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            PL_POS[1] -= PL_SPD*dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            PL_POS[1] += PL_SPD*dt

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            PL_POS[0] -= PL_SPD*dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            PL_POS[0] += PL_SPD*dt
        
        if keys[pygame.K_SPACE]:
            PL_POS[1] -= PL_SPD*dt

        pygame.draw.rect(screen, "magenta", active_rect, width =2)
        player_draw(player_img, player_rect, PL_POS, active_rect)
        PL_POS[1] = gravity(Y_MOMENTUM, PL_POS[1], PL_ACC_Y)
        pygame.display.flip()
        clock.tick(FPS)


def player_draw(PLAYER_IMG, PLAYER_RECT, PLAYER_POS, ACTIVE_RECT):
    PLAYER_RECT.center = PLAYER_POS[0], PLAYER_POS[1]
    
    #Boundry collision system
    if PLAYER_RECT.x + PLAYER_RECT.width > ACTIVE_RECT.width:
        PLAYER_RECT.x =  ACTIVE_RECT.width - PLAYER_RECT.width 

    if PLAYER_RECT.y + PLAYER_RECT.height > ACTIVE_RECT.height:
        PLAYER_RECT.y = ACTIVE_RECT.height - PLAYER_RECT.height

    if PLAYER_RECT.x < ACTIVE_RECT.x:
        PLAYER_RECT.x = ACTIVE_RECT.x

    if PLAYER_RECT.y < ACTIVE_RECT.y:
        PLAYER_RECT.y = ACTIVE_RECT.y

    ##Helps to keep Player_pos and Player_rect' position same
    if PLAYER_POS[0] + (PLAYER_RECT.width/2) > ACTIVE_RECT.width:
        PLAYER_POS[0] = ACTIVE_RECT.width - PLAYER_RECT.width/2
    if PLAYER_POS[1] + (PLAYER_RECT.height/2) > ACTIVE_RECT.height:
        PLAYER_POS[1] = ACTIVE_RECT.height - PLAYER_RECT.height/2

    if PLAYER_POS[0] - (PLAYER_RECT.width/2) < ACTIVE_RECT.x:
        PLAYER_POS[0] = ACTIVE_RECT.x + PLAYER_RECT.width/2
    if PLAYER_POS[1] - (PLAYER_RECT.height/2) < ACTIVE_RECT.y:
        PLAYER_POS[1] = ACTIVE_RECT.y + PLAYER_RECT.height/2


    
    screen.blit(PLAYER_IMG, player_rect)

def gravity(y_momentum, player_pos_y, player_acc_y ):
    y_momentum += player_acc_y
    player_pos_y += y_momentum
    return player_pos_y



def terminate():
    pygame.quit()
    sys.exit()

def img_conv(path_to_image):
    img = pygame.image.load(path_to_image).convert()
    img.set_colorkey("black")

if __name__ == "__main__":
    running = True
    main()
