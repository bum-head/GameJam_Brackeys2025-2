#!/usr/bin/env python

import pygame
import sys
import os
import time
import noise


##settings

FPS = 60
RES = WIDTH, HEIGHT = 800, 600
CAPTION = "OverDrive"
PL_POS = [int(WIDTH/2),int(HEIGHT/2)]
PL_SPD = 3
PL_ACC_Y = 2 
START_TIME = time.time()
Y_MOMENTUM = 0
CHUNK_SIZE = 8

running = False
true_scroll = [0, 0]
movement = [0, 0]
game_map = {}

##some things
def img_conv(path_to_image):
    img = pygame.image.load(path_to_image).convert()
    img.set_colorkey("black")
    return img

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
active_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

player_img = img_conv(os.path.join("assets","man.png"))
player_rect = player_img.get_rect()

grass_img = img_conv(os.path.join("assets", "grass_block.png"))
dirt_img = img_conv(os.path.join("assets", "dirt.png"))
plant_img = img_conv(os.path.join("assets", "plant.png"))

tile_index = {
    1:grass_img,
    2:dirt_img,
    3:plant_img
                }


pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "star.png")).convert())
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

##main game loop



def main():
    global START_TIME, movement

    while running:
       
        dt = time.time() - START_TIME
        dt *= FPS
        START_TIME = time.time()

        true_scroll[0] += (player_rect.x - true_scroll[0] - (int(WIDTH/4)+int(player_rect.width/2)) )/20
        true_scroll[1] += (player_rect.y - true_scroll[1] - (int(HEIGHT/4)+int(player_rect.height/2)) )/20
        
        scroll = true_scroll.copy()
        scroll[0], scroll[1] = int(scroll[0]), int(scroll[1])

        tile_rects = []
        for y in range(4):
            for x in range(5):
                target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
                target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))

                target_chunk = str(target_x) + ";" + str(target_y)

                if target_chunk not in game_map:
                    game_map[target_chunk] = generate_chunk(target_x, target_y)
                for tile in game_map[target_chunk]:
                    screen.blit(tile_index[tile[1]], (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))
                    if tile[1] in [1,2]:
                        tile_rects.append(pygame.Rect(tile[0][0]*16, tile[0][1]*16, 16, 16))
        

        screen.fill("lightblue")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
        
        ##Player moevment
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement[1] -= PL_SPD*dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement[1] += PL_SPD*dt

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement[0] -= PL_SPD*dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement[0] += PL_SPD*dt
        
        if keys[pygame.K_SPACE]:
            movement[1] -= PL_SPD*dt

        pygame.draw.rect(screen, "magenta", active_rect, width =2)
        #player_draw(player_img, player_rect, PL_POS, active_rect, scroll)
        movement[1] = gravity(Y_MOMENTUM, PL_POS[1], PL_ACC_Y)

        screen.blit(player_img, (0-scroll[0],0-scroll[1]))
        pygame.display.flip()
        clock.tick(FPS)


def player_draw(PLAYER_IMG, PLAYER_RECT, PLAYER_POS, ACTIVE_RECT, SCROLL):
    PLAYER_RECT.center = PLAYER_POS[0], PLAYER_POS[1]
    
    #Boundry collision system
#    if PLAYER_RECT.x + PLAYER_RECT.width > ACTIVE_RECT.width:
#        PLAYER_RECT.x =  ACTIVE_RECT.width - PLAYER_RECT.width 

#    if PLAYER_RECT.y + PLAYER_RECT.height > ACTIVE_RECT.height:
#        PLAYER_RECT.y = ACTIVE_RECT.height - PLAYER_RECT.height

#    if PLAYER_RECT.x < ACTIVE_RECT.x:
#        PLAYER_RECT.x = ACTIVE_RECT.x

#    if PLAYER_RECT.y < ACTIVE_RECT.y:
#        PLAYER_RECT.y = ACTIVE_RECT.y

    ##Helps to keep Player_pos and Player_rect' position same
#    if PLAYER_POS[0] + (PLAYER_RECT.width/2) > ACTIVE_RECT.width:
#        PLAYER_POS[0] = ACTIVE_RECT.width - PLAYER_RECT.width/2
    if PLAYER_POS[1] + (PLAYER_RECT.height/2) > ACTIVE_RECT.height:
        PLAYER_POS[1] = ACTIVE_RECT.height - PLAYER_RECT.height/2

#    if PLAYER_POS[0] - (PLAYER_RECT.width/2) < ACTIVE_RECT.x:
#        PLAYER_POS[0] = ACTIVE_RECT.x + PLAYER_RECT.width/2
    if PLAYER_POS[1] - (PLAYER_RECT.height/2) < ACTIVE_RECT.y:
        PLAYER_POS[1] = ACTIVE_RECT.y + PLAYER_RECT.height/2


    
    screen.blit(PLAYER_IMG, (player_rect.x - SCROLL[0], player_rect.y - SCROLL[1]))

def collisions(player_rect, tile_list):
    hit_list = []
    for tile in tile_list:
        if player_rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list
    

def move(player_rect, tile_list, player_movement):

    player_rect.x += movement[0]
    hit_list = collisions(player_rect, tile_rect)
    for tile in hit_list:
        if movement[0] > 0:
            player_rect.right = tile.left

        elif movement[0] < 0:
            player_rect.left = tile.right


    player_rect.y += movemnt[1]
    hit_list = collisions(player_rect, tile_rect)
    for tile in hit_list:
        if movement[1] > 0:
            player_rect.bottom = tile.top

        if movement[1] < 0:
            player_rect.top = tile.bottom

    return player_rect

def gravity(y_momentum, player_pos_y, player_acc_y ):
    y_momentum += player_acc_y
    player_pos_y += y_momentum
    return player_pos_y

def generate_chunk(x, y):
    chunk_data = []

    for x_pos in range(CHUNK_SIZE):
        for y_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos

            tile_type = 0

            height = int(noise.pnoise1(target_x * 0.1, repeat=999999999) * 6) # change the * 6 to a higher or lower number to increase or reduce the terrain height
            if target_y > 8 - height:
                tile_type = 2
                chunk_data.append([[target_x, target_y], tile_type])
            elif target_y == 8 - height:
                tile_type = 1
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    running = True
    main()
