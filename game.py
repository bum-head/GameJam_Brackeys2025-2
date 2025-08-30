#!/usr/bin/env python

import pygame
import sys
import os
import time
import noise
import random

##settings

FPS = 60
RES = WIDTH, HEIGHT = 800, 600
CAPTION = "OverDrive"
#PL_POS = [int(WIDTH/2),int(HEIGHT/2)]
PL_SPD = 3
PL_ACC_Y = 2 
START_TIME = time.time()
MOMENTUM = 0
MOMEN = 4
CHUNK_SIZE = 8

running = False
true_scroll = [0, 0]
game_map = {}

##some things
def img_conv(path_to_image):
    img = pygame.image.load(path_to_image).convert()
    img.set_colorkey("black")
    return img

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
active_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

player_img = img_conv(os.path.join("assets","player.png"))
player_img = pygame.transform.scale(player_img, (player_img.get_width()*2, player_img.get_height()*2))
player_rect = pygame.Rect(WIDTH/2, -100, player_img.width, player_img.height)


grass_img = img_conv(os.path.join("assets", "grass_block.png"))
dirt_img = img_conv(os.path.join("assets", "dirt.png"))
plant_img = img_conv(os.path.join("assets", "plant.png"))
spike_img = img_conv(os.path.join("assets", "spike.png"))
big_spike_img = img_conv(os.path.join("assets", "big_spike.png"))

tile_index = {
    1:grass_img,
    2:dirt_img,
    3:plant_img,
    4:spike_img,
    5:big_spike_img
                }


pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "star.png")).convert())
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

##main game loop



def main():
    global START_TIME, player_rect , MOMENTUM

    while running:
       
        screen.fill("burlywood4")
        dt = time.time() - START_TIME
        dt *= FPS
        START_TIME = time.time()

        true_scroll[0] += (player_rect.x - true_scroll[0] - (int(WIDTH/2)+int(player_rect.width/2)) + 40)/20
        true_scroll[1] += (player_rect.y - true_scroll[1] - (int(HEIGHT/2)+int(player_rect.height/2)) + 20)/20
        
        scroll = true_scroll.copy()
        scroll[0], scroll[1] = int(scroll[0]), int(scroll[1])

        tile_rects = []
        for y in range(7):
            for x in range(8):
                target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
                target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))

                target_chunk = str(target_x) + ";" + str(target_y)

                if target_chunk not in game_map:
                    game_map[target_chunk] = generate_chunk(target_x, target_y)
                for tile in game_map[target_chunk]:
                    screen.blit(tile_index[tile[1]], (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))
                    if tile[1] in [1,2]:
                        tile_rects.append(pygame.Rect(tile[0][0]*16, tile[0][1]*16, 16, 16))
                           


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
        
        movement = [0, 0]
        ##Player moevment
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement[1] -= int(PL_SPD*dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement[1] += int(PL_SPD*dt)

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement[0] -= int(PL_SPD*dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement[0] += int(PL_SPD*dt)
       
        if keys[pygame.K_l]:
            movement[0] += int(4*dt)

        if keys[pygame.K_SPACE]:
            MOMENTUM = 10

        if MOMENTUM > -5:
            MOMENTUM -= 3*dt/6

        movement[1] -= MOMENTUM - MOMEN*(dt/6)

        pygame.draw.rect(screen, "magenta", active_rect, width =2)
        player_draw(player_img, player_rect, active_rect, scroll)
        
        pygame.display.set_caption(f"({player_rect.x}, {player_rect.y})")
        #movement[1] += gravity(player_rect.y, PL_ACC_Y)
        player_rect = move(player_rect, tile_rects, movement)
        #screen.blit(pygame.transform.scale(display, RES), (0,0))
        screen.blit(player_img, (0-scroll[0],0-scroll[1]))   #An object not a player
        pygame.display.flip()
        clock.tick(FPS)


def player_draw(PLAYER_IMG, PLAYER_RECT, ACTIVE_RECT, SCROLL):
    screen.blit(PLAYER_IMG, (player_rect.x - SCROLL[0], player_rect.y - SCROLL[1]))

def collisions(player_rect, tile_list):
    hit_list = []
    for tile in tile_list:
        if player_rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list    

def move(player_rect, tile_list, player_movement):

    player_rect.x += player_movement[0]
    hit_list = collisions(player_rect, tile_list)
    for tile in hit_list:
        if player_movement[0] > 0:
            player_rect.right = tile.left

        elif player_movement[0] < 0:
            player_rect.left = tile.right


    player_rect.y += player_movement[1]
    hit_list = collisions(player_rect, tile_list)
    for tile in hit_list:
        if player_movement[1] > 0:
            player_rect.bottom = tile.top

        if player_movement[1] < 0:
            player_rect.top = tile.bottom

    return player_rect

def gravity(player_pos_y, player_acc_y ):
    player_pos_y += player_acc_y
    return player_pos_y

def generate_chunk(x, y):
    chunk_data = []

    for x_pos in range(CHUNK_SIZE):
        for y_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos

            tile_type = 0

            height = int(noise.pnoise1(target_x * 0.1, repeat=999999999) * 11) # change the * 6 to a higher or lower number to increase or reduce the terrain height
            if target_y > 15 - height:
                tile_type = 2
            elif target_y == 15 - height:
                tile_type = 1
            elif target_y == 14 - height:
                if random.randint(1,5) == 1:
                    tile_type = 3
            
            depth = int(noise.pnoise1(target_x * 0.2, repeat=999999999) * 8)
            if target_y < -10 - depth:
                tile_type = 2
            elif target_y == -10 - depth:
                tile_type = 1
            elif target_y == -9 - depth:
                if random.randint(1,5) == 1:
                    tile_type = 4
                if random.randint(1,7) == 1:
                    tile_type = 5
            
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])


    return chunk_data

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    running = True
    main()
