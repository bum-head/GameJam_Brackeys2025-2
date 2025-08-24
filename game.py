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
PL_POS = [0,0]
PL_SPD = 3
START_TIME = time.time()

running = False

##some things

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

player_img = pygame.image.load(os.path.join("assets","man.png")).convert()
player_img.set_colorkey("white")

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
       
        player_draw(player_img, PL_POS)
        pygame.display.flip()
        clock.tick(FPS)


def player_draw(PLAYER_IMG, PLAYER_POS):
    player_rect = PLAYER_IMG.get_rect()
    player_rect.center = PLAYER_POS[0], PLAYER_POS[1]

    screen.blit(PLAYER_IMG, player_rect)



def terminate():
    pygame.quit()
    sys.exit()

def img_conv(path_to_image):
    img = pygame.image.load(path_to_image).convert()
    img.set_colorkey("black")

if __name__ == "__main__":
    running = True
    main()
