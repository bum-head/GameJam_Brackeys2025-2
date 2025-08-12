#!/usr/bin/env python

import pygame
import sys
import os

##Game Jam GAme!!!
## SO NERVOUS!!

##settings

FPS = 60
RES = WIDTH, HEIGHT = 800, 600
CAPTION = "OverDrive"

running = False

##some things

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "star.png")).convert())
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

##main game loop



def main():
    while running:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()

def img_conv(path_to_image):
    img = pygame.image.load(path_to_image).convert()
    img.set_colorkey("black")

if __name__ == "__main__":
    running = True
    main()
