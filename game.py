#!/usr/bin/env python

import pygame
import sys
import os
import time
import noise
import random

pygame.init()
##settings

FPS = 60
RES = WIDTH, HEIGHT = 800, 600
CAPTION = "BizKit Raiderz"
PL_SPD = 3
PL_ACC_Y = 2 
TIMER_TIME = time.time()
MOMENTUM = 0
MOMEN = 4
CHUNK_SIZE = 8
FONTPATH = os.path.join("assets", "font", "HomeVideo-BLG6G.ttf")
FONT = pygame.font.Font(FONTPATH, 25)
FONT_TIMER = pygame.font.Font(FONTPATH, 17)
FHEIGHT = 28
FWIDTH = 270
FWIDTH_MAX = FWIDTH
SCALE_SIZE = (280, 36)

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
backbar = img_conv(os.path.join("assets", "backbar.png"))
transbar = img_conv(os.path.join("assets", "transparentbar.png"))
backbar = pygame.transform.scale(backbar, SCALE_SIZE)
transbar = pygame.transform.scale(transbar, SCALE_SIZE)

player_img = img_conv(os.path.join("assets","player.png"))
player_img = pygame.transform.scale(player_img, (player_img.get_width()*2, player_img.get_height()*2))
player_rect = pygame.Rect(WIDTH/2, -110, player_img.get_width(), player_img.get_height())

start_srn_img = img_conv(os.path.join("assets", "start_screen.png"))
background_img = img_conv(os.path.join("assets", "background.png"))

grass_img = img_conv(os.path.join("assets", "grass_block.png"))
dirt_img = img_conv(os.path.join("assets", "dirt.png"))
plant_img = img_conv(os.path.join("assets", "plant.png"))
stone_img = img_conv(os.path.join("assets", "stone.png"))
spike_img = img_conv(os.path.join("assets", "spike.png"))
big_spike_img = img_conv(os.path.join("assets", "big_spike.png"))

tile_index = {
    1:grass_img,
    2:dirt_img,
    3:plant_img,
    4:spike_img,
    5:big_spike_img,
    6:stone_img
                }

pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "star.png")).convert())
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

##main game loop

def draw_text(text, color, x, y, font = FONT, backcolor = None) -> pygame.Rect:
    """ Unlike other pygame's rect positioning, it positions the text, by taking the x and y as the center of the text. """

    textobj = font.render(text, 0, color, backcolor)
    textrect = textobj.get_rect()
    textrect.center = (x,y)
    screen.blit(textobj, textrect)

    return textrect

def take_damage(health):
    health -= 4
    health = max(health, 0)
    return health

def healthDisplay(HEALTH, M_HEALTH, backbar, transbar, colorf, rectf, FWIDTH, FWIDTH_MAX) -> None:
    screen.blit(backbar, (30, 30))
    pygame.draw.rect(screen, colorf, rectf)
    transbar.set_alpha(127)
    screen.blit(transbar, (30, 30))
    if int((HEALTH/M_HEALTH)*100) < 100:
        FWIDTH = max(int((HEALTH/M_HEALTH)*FWIDTH_MAX), 0)
        rectf.width = FWIDTH

def menu():
    while running:
        screen.fill("burlywood4")
        screen.blit(start_srn_img, (0,0))

        mx, my = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()

        challenge_text = draw_text("Glide For 3 minutes and you get THE BIZKIT!", "black", 3*WIDTH/8, HEIGHT/8, FONT_TIMER)

        play_rect_back = draw_text("    ","red3" , WIDTH/2,HEIGHT/2, FONT, "red3")
        play_rect = draw_text("PLAY","white" ,  WIDTH/2, HEIGHT/2, FONT)

        

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint((mx,my)):
                    main()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        
        clock.tick(FPS)
        pygame.display.flip()

def main():
    global START_TIME, player_rect , MOMENTUM, MOME
   
    TIMER = 0
    COLORF = "red3"
    RECTF = pygame.rect.Rect(35 ,34, FWIDTH, FHEIGHT)
    HEALTH = 80
    M_HEALTH = 80
    START_TIME = time.time()

    x_pos_0 = player_rect.x 
    
    while True:
      
        #end screen calc


        screen.fill("burlywood4")
        screen.blit(background_img, (0,0))
        dt = time.time() - START_TIME
        dt *= FPS
        START_TIME = time.time()

        TIMER = time.time() - TIMER_TIME

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

        player_rect, collision = move(player_rect, tile_rects, movement)

        if collision['Top'] == True:
            MOMENTUM = 0
            HEALTH = take_damage(HEALTH)
        if collision['Bottom'] == True:
            HEALTH = take_damage(HEALTH)
        if collision['Right'] == True:
            HEALTH = take_damage(HEALTH)

        if HEALTH == 0:
            x_distance = abs(player_rect.x - x_pos_0)
            end_screen(x_distance, TIMER )

        pygame.draw.rect(screen, "magenta", active_rect, width =2)
        player_draw(player_img, player_rect, active_rect, scroll)
        healthDisplay(HEALTH, M_HEALTH, backbar, transbar, COLORF, RECTF, FWIDTH, FWIDTH_MAX)
        
        time_text = draw_text(f"Time elapsed: {round(TIMER)}", "white", WIDTH-120, 30, FONT_TIMER )
        pygame.display.flip()
        clock.tick(FPS)

def end_screen(x_distance, timer):
    while running:
        screen.fill("burlywood4")

        mx, my = pygame.mouse.get_pos()

        if x_distance == 0 or x_distance < 10:
            challenge_text = draw_text("You Didn't Even MOVE!@?", "black", 3*WIDTH/8, HEIGHT/8, FONT_TIMER)
        if x_distance > 800 and timer >= 180:
            result = random.randint(1,3)
            if result == 1:
                challenge_text = draw_text("Now That is What I call Gliding!", "black", 3*WIDTH/8, HEIGHT/8, FONT_TIMER)
            elif result == 2:
                challenge_text = draw_text("COOL!", "black", 3*WIDTH/8, HEIGHT/8, FONT_TIMER)
            elif result == 3:
                challenge_text = draw_text("Good Work!", "black", 3*WIDTH/8, HEIGHT/8, FONT_TIMER)
        elif x_distance > 800 and timer < 180:
            challenge_text = draw_text("Hmm, you are fast but, sadly didn't last long!", "black", 3*WIDTH/8, HEIGHT/8, FONT_TIMER)
        elif x_distance < 800 and timer <180:
            challenge_text = draw_text("Hmm, Try Again!", "black", 3*WIDTH/8, HEIGHT/8, FONT_TIMER)

        play_rect_back = draw_text("    ","red3" , WIDTH/2,HEIGHT/2, FONT, "red3")
        play_rect = draw_text("QUIT","white" ,  WIDTH/2, HEIGHT/2, FONT)

        

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint((mx,my)):
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        
        clock.tick(FPS)
        pygame.display.flip()




def player_draw(PLAYER_IMG, PLAYER_RECT, ACTIVE_RECT, SCROLL):
    screen.blit(PLAYER_IMG, (player_rect.x - SCROLL[0], player_rect.y - SCROLL[1]))

def collisions(player_rect, tile_list):
    hit_list = []
    for tile in tile_list:
        if player_rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list    

def move(player_rect, tile_list, player_movement):
    collision = {'Top':False, 'Bottom':False, 'Left':False, 'Right':False}
    player_rect.x += player_movement[0]
    hit_list = collisions(player_rect, tile_list)
    for tile in hit_list:
        if player_movement[0] > 0:
            player_rect.right = tile.left
            collision['Right'] = True

        elif player_movement[0] < 0:
            player_rect.left = tile.right
            collision['Left'] = True


    player_rect.y += player_movement[1]
    hit_list = collisions(player_rect, tile_list)
    for tile in hit_list:
        if player_movement[1] > 0:
            player_rect.bottom = tile.top
            collision['Bottom'] = True

        if player_movement[1] < 0:
            player_rect.top = tile.bottom
            collision['Top'] = True

    return player_rect, collision

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
                tile_type = 6
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
    menu()
