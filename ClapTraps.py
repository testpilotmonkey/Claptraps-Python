#!/usr/bin/env python

#    Copyright 2010 testpilotmonkey (testpilotmonkey@gmail.com)
#
#    This file is part of ClapTraps.
#
#    ClapTraps is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ClapTraps is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ClapTraps.  If not, see <http://www.gnu.org/licenses/>.


import pygame, sys, traceback, pickle, copy, os

from CTfns import fn_init_defs, look, move, reset_flags, Dave_hit

sys.path.append('.') # Needed to make py2exe work properly
sys.path.append('Defs')
pygame.init()

icon = pygame.image.load('Images/icon.png')
pygame.display.set_icon(icon)

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ClapTraps')

class Game_State:
    def __init__(self):
        self.score = 0
        self.LEVEL_WIDTH = 16
        self.LEVEL_HEIGHT = 12
        self.NORTH = 1
        self.EAST = 2
        self.SOUTH = 3
        self.WEST = 4
        self.NE = 5
        self.SE = 6
        self.SW = 7
        self.NW = 8
        self.game_map = []
        self.dave_x = 0
        self.dave_y = 0
        self.dave_dest_x = 0
        self.dave_dest_y = 0
        self.x_offset = 0
        self.y_offset = 0
        self.player_moving = 0
        self.kill_dave = False
        self.obj_names = {}
        self.use_key = False
        self.level_number = 0
        self.min_score_hit = False
        self.level_finished = False
        self.lives = 3
        self.transporting = False
        self.message = 'Blank!'
        self.bg_col = 150, 150, 255
        self.play_music = True
        self.default_message = 'Grab those frogs!'
        self.keys = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]

        # This is set after all objects are defined
        self.NO_OF_OBJECTS = 0

        self.target_img = pygame.image.load("Images/target.png")
        

game_state = Game_State()
game_objects = game_sprites = Dave = None

# Load preferences
prefs_file = open('CTprefs', "rb")
game_prefs = pickle.load(prefs_file)
game_state.keys = game_prefs[0]
game_state.play_music = game_prefs[1]
prefs_file.close()


def load_defs(defs_name):

    global game_objects, game_sprites, Dave

    CTdefs = __import__(defs_name)

    CTdefs.init_defs(game_state)
    game_objects = CTdefs.game_objects
    game_sprites = CTdefs.game_sprites
    Dave = CTdefs.Dave
    game_state.default_message = CTdefs.default_message

    for counter in range(len(game_objects)):
        game_objects[counter].gobject = counter

    game_state.NO_OF_OBJECTS = len(game_objects) - 1

    for obj in game_objects:
        if obj.name != 0:
            game_state.obj_names[obj.name] = obj.gobject
            
    # Functions taken from here
    fn_init_defs(game_state, game_objects, Dave, CTdefs.Wall)


sprite_dave = [pygame.image.load("Images/dave2.png"),
              pygame.image.load("Images/dave_run1.png"),
              pygame.image.load("Images/dave_run2.png"),
              pygame.image.load("Images/dave_run3.png"),
              pygame.image.load("Images/dave_run2.png"),
              pygame.image.load("Images/dave_run4.png"),
              pygame.image.load("Images/dave_run5.png"),
              pygame.image.load("Images/dave_run6.png"),
              pygame.image.load("Images/dave_run5.png"),
              pygame.image.load("Images/dave_run_v1.png"),
              pygame.image.load("Images/dave_run_v2.png"),
              pygame.image.load("Images/dave_run_v3.png"),
              pygame.image.load("Images/dave_run_v4.png")]

#sprite_dave[5] = pygame.transform.flip(sprite_dave[1], True, False)
#sprite_dave[6] = pygame.transform.flip(sprite_dave[2], True, False)
#sprite_dave[7] = pygame.transform.flip(sprite_dave[3], True, False)
#sprite_dave[8] = pygame.transform.flip(sprite_dave[4], True, False)



def render_text(input_text, y_pos):
    font = pygame.font.Font("eartm.ttf", 35)

    text = font.render(input_text, True, (0, 0, 0), (150, 150, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx + 2
    #text_rect.centery = screen.get_rect().centery
    text_rect.centery = y_pos + 2
    screen.blit(text, text_rect, None, pygame.BLEND_MULT)
    
    text = font.render(input_text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    #text_rect.centery = screen.get_rect().centery
    text_rect.centery = y_pos
    screen.blit(text, text_rect)
    #pygame.display.flip()



def status_screen():
    #game_state.bg_col = 150, 150, 255
    screen.fill(game_state.bg_col)
    prompt_rect = pygame.Rect(0, 0, 400, 200)
    prompt_rect.centerx = screen.get_rect().centerx
    prompt_rect.centery = screen.get_rect().centery
    pygame.draw.rect(screen, (0, 0, 0), prompt_rect)
    render_text('Level ' + str(game_state.level_number + 1), 120)
    render_text(game_state.message, 180)
    render_text('Score: ' + str(game_state.score), 240)
    render_text('Target Score: ' + str(game_data.minimum_score[game_state.level_number]), 270)
    render_text('Lives: ' + str(game_state.lives), 300)
    pygame.display.flip()
    while(1):
        wait_event = pygame.event.wait()
        if wait_event.type == pygame.KEYDOWN:
            if wait_event.key == pygame.K_SPACE:
                return True
            if wait_event.key == pygame.K_ESCAPE:
                return False
            else:
                pass

class Game_Data:
    def __init__(self):
        # The level_map data structure: level_map[x][y] = [gobject(, target)]
        self.level_map = [[[[0,0] for i in range(12)] for j in range(16)]]
        self.dave_pos = [(0,0)]
        self.level_size = [(16, 12)]
        self.minimum_score = [0]
        self.def_file = None

#game_data = Game_Data()
        
#data_file = file(r"game_data.dat", "rb")
#game_data = pickle.load(data_file)
#data_file.close()


game_data = None

def game():

    #game_state.score = 0
    game_state.min_score_hit = False
    game_state.level_finished = False

    old_screen = pygame.Surface((640, 480))
    old_rect = old_screen.get_rect()

# Copy level data to working data

    game_state.LEVEL_WIDTH = game_data.level_size[game_state.level_number][0]
    game_state.LEVEL_HEIGHT = game_data.level_size[game_state.level_number][1]

    game_state.game_map = []
    temp_list = []

    for x_counter in range(game_state.LEVEL_WIDTH):
        for y_counter in range(game_state.LEVEL_HEIGHT):     
            temp_list.append(copy.deepcopy(game_objects[game_data.level_map[game_state.level_number][x_counter][y_counter][0]]))
            temp_list[-1].target = copy.deepcopy(game_data.level_map[game_state.level_number][x_counter][y_counter][1])
            temp_list[-1].x = x_counter
            temp_list[-1].y = y_counter
            #temp_list.append(game_data.level_map[x_counter][y_counter])
        game_state.game_map.append(copy.deepcopy(temp_list))
        temp_list = []

    game_state.dave_x = game_state.dave_dest_x = game_data.dave_pos[game_state.level_number][0]
    game_state.dave_y = game_state.dave_dest_y = game_data.dave_pos[game_state.level_number][1]

#################################

    frames = 0
    ticks = pygame.time.get_ticks()
    GameClock = pygame.time.Clock()

    player_rect = pygame.Rect(0, 0, 40, 40)

    game_state.x_offset = game_state.dave_x - 5
    if game_state.x_offset < 0:
        game_state.x_offset = 0
    if game_state.x_offset > game_state.LEVEL_WIDTH - 16:
        game_state.x_offset = game_state.LEVEL_WIDTH - 16
        
    game_state.y_offset = game_state.dave_y - 5
    if game_state.y_offset < 0:
        game_state.y_offset = 0
    if game_state.y_offset > game_state.LEVEL_HEIGHT - 12:
        game_state.y_offset = game_state.LEVEL_HEIGHT - 12
        
    program_quit = False
    player_right = player_left = player_up = player_down = 0
    player_dir = 0
    game_state.player_moving = 0
    player_move_counter_horiz = 0
    scroll_horiz = False
    scroll_horiz_comp = False
    player_move_counter_vert = 0
    scroll_vert = False
    scroll_vert_comp = False

    dave_frame = 0
    anim_counter = 0
    dave_wait = 0


    while(1):
# Process inputs
        for event in pygame.event.get():          
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                program_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == game_state.keys[0]:
                    player_right = 1
                    #player_left = 0
                if event.key == game_state.keys[1]:
                    #player_right = 0
                    player_left = 1
                if event.key == game_state.keys[2]:
                    player_up = 1
                    #player_down = 0
                if event.key == game_state.keys[3]:
                    #player_up = 0
                    player_down = 1
                if event.key == game_state.keys[4]:
                    game_state.use_key = True
                    
                if event.key == pygame.K_TAB:
                    game_state.use_key = False
                    player_right = player_left = player_up = player_down = 0
                    if status_screen() == False:
                        program_quit = True

                #if event.key == pygame.K_w:
                #    return True

            if event.type == pygame.KEYUP:
                if event.key == game_state.keys[0]:
                    player_right = 0
                    #player_left = 0
                if event.key == game_state.keys[1]:
                    #player_right = 0
                    player_left = 0
                if event.key == game_state.keys[2]:
                    player_up = 0
                    #player_down = 0
                if event.key == game_state.keys[3]:
                    #player_up = 0
                    player_down = 0
                if event.key == game_state.keys[4]:
                    game_state.use_key = False

        if player_right:
            player_dir = game_state.EAST
        elif player_left:
            player_dir = game_state.WEST
        elif player_up:
            player_dir = game_state.NORTH
        elif player_down:
            player_dir = game_state.SOUTH
        else:
            player_dir = 0
            
# Exit to menu
        if program_quit == True:
            game_state.bg_col = 150, 150, 255
            screen.fill(game_state.bg_col)

            render_text('Quit Y/N?', 240)

            pygame.display.flip()
            while(1):
                wait_event = pygame.event.wait()
                if wait_event.type == pygame.KEYDOWN:
                    if wait_event.key == pygame.K_y:
                        return False
                    elif wait_event.key == pygame.K_n:
                        program_quit = False
                        break
                    else:
                        pass
            

        
        
# Move Player
        if not game_state.player_moving:
            
            if player_dir == game_state.EAST and game_state.dave_x < game_state.LEVEL_WIDTH - 1:
                if game_state.game_map[game_state.dave_x + 1][game_state.dave_y].solid == False:
                    
                    game_state.player_moving = game_state.EAST
                    game_state.dave_dest_x, game_state.dave_dest_y = game_state.dave_x + 1, game_state.dave_y
                    
                    if game_state.dave_x - game_state.x_offset > 8 and game_state.x_offset < game_state.LEVEL_WIDTH - 16:
                        #game_state.x_offset += 1
                        scroll_horiz = True
        # Push Horizontally
                elif game_state.game_map[game_state.dave_x + 1][game_state.dave_y].h_push == True \
                        and game_state.dave_x < game_state.LEVEL_WIDTH - 2 \
                        and game_state.game_map[game_state.dave_x + 2][game_state.dave_y].check_squash(game_state.game_map[game_state.dave_x + 1][game_state.dave_y]) == True:
                        #and game_state.game_map[game_state.dave_x + 2][game_state.dave_y].squash == True:

                        #game_state.game_map[game_state.dave_x + 2][game_state.dave_y].move_speed = 0
                        move(game_state.EAST,
                             game_state.game_map[game_state.dave_x + 1][game_state.dave_y],
                             game_state.dave_x + 1, game_state.dave_y)

                        game_state.player_moving = game_state.EAST
                        game_state.dave_dest_x, game_state.dave_dest_y = game_state.dave_x + 1, game_state.dave_y
                        
                        if game_state.dave_x - game_state.x_offset > 8 and game_state.x_offset < game_state.LEVEL_WIDTH - 16:
                            #game_state.x_offset += 1
                            scroll_horiz = True

                    
            if player_dir == game_state.WEST and game_state.dave_x > 0:
                if game_state.game_map[game_state.dave_x - 1][game_state.dave_y].solid == False:

                    game_state.player_moving = game_state.WEST
                    game_state.dave_dest_x, game_state.dave_dest_y = game_state.dave_x - 1, game_state.dave_y
                    
                    if game_state.dave_x - game_state.x_offset < 7 and game_state.x_offset > 0:
                        scroll_horiz = True
                        scroll_horiz_comp = True

             # Push Horizontally
                elif game_state.game_map[game_state.dave_x - 1][game_state.dave_y].h_push == True \
                        and game_state.dave_x > 1 \
                        and game_state.game_map[game_state.dave_x - 2][game_state.dave_y].check_squash(game_state.game_map[game_state.dave_x - 1][game_state.dave_y]) == True:
                        #and game_state.game_map[game_state.dave_x - 2][game_state.dave_y].squash == True:
                            
                        #game_state.game_map[game_state.dave_x - 2][game_state.dave_y].move_speed = 0
                        move(game_state.WEST,
                             game_state.game_map[game_state.dave_x - 1][game_state.dave_y],
                             game_state.dave_x - 1, game_state.dave_y)

                        game_state.player_moving = game_state.WEST
                        game_state.dave_dest_x, game_state.dave_dest_y = game_state.dave_x - 1, game_state.dave_y
                        
                        if game_state.dave_x - game_state.x_offset < 7 and game_state.x_offset > 0:
                            scroll_horiz = True
                            scroll_horiz_comp = True

                
            if player_dir == game_state.NORTH and game_state.dave_y > 0:
                if game_state.game_map[game_state.dave_x][game_state.dave_y - 1].solid == False:

                    game_state.player_moving = game_state.NORTH
                    game_state.dave_dest_x, game_state.dave_dest_y = game_state.dave_x, game_state.dave_y - 1

                    
                    if game_state.dave_y - game_state.y_offset < 5 and game_state.y_offset > 0:
                        #game_state.y_offset -= 1
                        scroll_vert = True
                        scroll_vert_comp = True

             # Push Vertically
                elif game_state.game_map[game_state.dave_x][game_state.dave_y - 1].v_push == True \
                        and game_state.dave_y > 1 \
                        and game_state.game_map[game_state.dave_x][game_state.dave_y - 2].check_squash(game_state.game_map[game_state.dave_x][game_state.dave_y - 1]) == True:

                        #game_state.game_map[game_state.dave_x][game_state.dave_y - 2].move_speed = 0
    
                        move(game_state.NORTH,
                             game_state.game_map[game_state.dave_x][game_state.dave_y - 1],
                             game_state.dave_x, game_state.dave_y - 1)

                        game_state.player_moving = game_state.NORTH
                        game_state.dave_dest_x, game_state.dave_dest_y = game_state.dave_x, game_state.dave_y - 1

                        
                        if game_state.dave_y - game_state.y_offset < 5 and game_state.y_offset > 0:
                            #game_state.y_offset -= 1
                            scroll_vert = True
                            scroll_vert_comp = True
                    
            if player_dir == game_state.SOUTH and game_state.dave_y < game_state.LEVEL_HEIGHT - 1:
                if game_state.game_map[game_state.dave_x][game_state.dave_y + 1].solid == False:

                    game_state.player_moving = game_state.SOUTH
                    game_state.dave_dest_x, game_state.dave_dest_y = game_state.dave_x, game_state.dave_y + 1
                    
                    if game_state.dave_y - game_state.y_offset > 6 and game_state.y_offset < game_state.LEVEL_HEIGHT - 12:
                        #game_state.y_offset += 1
                        scroll_vert = True

             # Push Vertically
                elif game_state.game_map[game_state.dave_x][game_state.dave_y + 1].v_push == True \
                        and game_state.dave_y < game_state.LEVEL_HEIGHT - 2 \
                        and game_state.game_map[game_state.dave_x][game_state.dave_y + 2].check_squash(game_state.game_map[game_state.dave_x][game_state.dave_y + 1]) == True:

                        #game_state.game_map[game_state.dave_x][game_state.dave_y + 2].move_speed = 0

                        move(game_state.SOUTH,
                             game_state.game_map[game_state.dave_x][game_state.dave_y + 1],
                             game_state.dave_x, game_state.dave_y + 1)

                        game_state.player_moving = game_state.SOUTH
                        game_state.dave_dest_x, game_state.dave_dest_y = game_state.dave_x, game_state.dave_y + 1
                        
                        if game_state.dave_y - game_state.y_offset > 6 and game_state.y_offset < game_state.LEVEL_HEIGHT - 12:
                            #game_state.y_offset += 1
                            scroll_vert = True
                    

        if game_state.player_moving == game_state.EAST:
            player_move_counter_horiz += 1
            
            if anim_counter == 0:
                dave_frame +=1
            if dave_frame > 4:
                dave_frame = 1
            dave_wait = 10
            
            if player_move_counter_horiz == 4:
                player_move_counter_horiz = 0
                game_state.player_moving = 0
                game_state.dave_x += 1
                                
                if scroll_horiz:
                    scroll_horiz = False
                    game_state.x_offset += 1
                    
# Let Dave hit objects
                if game_state.game_map[game_state.dave_x][game_state.dave_y].solid == False:
                    Dave_hit()

                
        if game_state.player_moving == game_state.WEST:
            player_move_counter_horiz -= 1
            
            if dave_frame < 4:
                dave_frame = 4
            if anim_counter == 0:
                dave_frame +=1
            if dave_frame > 8:
                dave_frame = 5
            dave_wait = 10
            
            if player_move_counter_horiz == -4:
                player_move_counter_horiz = 0
                game_state.player_moving = 0
                game_state.dave_x -= 1
                
                if scroll_horiz:
                    scroll_horiz = False
                    scroll_horiz_comp = False
                    game_state.x_offset -= 1
                    
# Let Dave hit objects
                if game_state.game_map[game_state.dave_x][game_state.dave_y].solid == False:
                    Dave_hit()


        if game_state.player_moving == game_state.NORTH:
            player_move_counter_vert -= 1

            if dave_frame < 11:
                dave_frame = 11
            if anim_counter == 0:
                dave_frame +=1
            if dave_frame > 12:
                dave_frame = 11
            dave_wait = 10

            if player_move_counter_vert == -4:
                player_move_counter_vert = 0
                game_state.player_moving = 0
                game_state.dave_y -= 1
                
                if scroll_vert:
                    scroll_vert = False
                    scroll_vert_comp = False
                    game_state.y_offset -= 1
                    
# Let Dave hit objects
                if game_state.game_map[game_state.dave_x][game_state.dave_y].solid == False:
                    Dave_hit()
                

        if game_state.player_moving == game_state.SOUTH:
            player_move_counter_vert += 1

            if dave_frame < 9:
                dave_frame = 9
            if anim_counter == 0:
                dave_frame +=1
            if dave_frame > 10:
                dave_frame = 9
            dave_wait = 10

            if player_move_counter_vert == 4:
                player_move_counter_vert = 0
                game_state.player_moving = 0
                game_state.dave_y += 1
                
                if scroll_vert:
                    scroll_vert = False
                    game_state.y_offset += 1
                    
# Let Dave hit objects
                if game_state.game_map[game_state.dave_x][game_state.dave_y].solid == False:
                    Dave_hit()
                
# If Dave's standing still (but not just moved) hit objects beneath him
        if dave_wait < 8:
            Dave_hit()


# Perform sprite actions

        for y_counter in range(game_state.LEVEL_HEIGHT): 
            for x_counter in range(game_state.LEVEL_WIDTH):
               
                current_sprite = game_state.game_map[x_counter][y_counter]

                if x_counter == game_state.dave_x and y_counter == game_state.dave_y and current_sprite.solid == False:
                    Dave_hit()

                # Animate sprite
                if current_sprite.animation != 0:
                    if current_sprite.anim_timer < current_sprite.animation[current_sprite.anim_frame][1] - 1:
                        current_sprite.anim_timer += 1
                    else:
                        current_sprite.anim_timer = 0
                        current_sprite.anim_frame += 1
                        if current_sprite.anim_frame == len(current_sprite.animation):
                            current_sprite.anim_frame = 0
                            
                    current_sprite.sprite = current_sprite.animation[current_sprite.anim_frame][0]
                        

                if current_sprite.ignore == False:
                    
                    current_sprite.action()
                    
                    if current_sprite.moved > 0:
                        current_sprite.moved = 0
                else:
                    current_sprite.ignore = False

                if current_sprite.moving > 0:
                    current_sprite.move_counter += current_sprite.move_speed
                    if current_sprite.move_counter > 3:
                        
                        if current_sprite.moving == game_state.NORTH:

                            hitting_object = game_state.game_map[x_counter][y_counter - 1]

                            game_state.game_map[x_counter][y_counter - 1] = copy.deepcopy(game_state.game_map[x_counter][y_counter])
                            game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[0])
                            #game_state.game_map[x_counter][y_counter - 1].ignore = True
                            game_state.game_map[x_counter][y_counter - 1].x = x_counter
                            game_state.game_map[x_counter][y_counter - 1].y = y_counter - 1
                            game_state.game_map[x_counter][y_counter - 1].move_counter = 0
                            game_state.game_map[x_counter][y_counter - 1].moving = 0
                            
                            game_state.game_map[x_counter][y_counter - 1].moved = game_state.NORTH
                            # Blank above line and uncomment below if multiple Repton shuffles shouldn't kill
                            #if y_counter > 1 and \
                            #   game_state.game_map[x_counter][y_counter-2].gobject == 0:
                            #    game_state.game_map[x_counter][y_counter-1].moved = game_state.NORTH

                            hitting_object.hit(game_state.game_map[x_counter][y_counter - 1])

                            if hitting_object.moving:
                                if hitting_object.forward == game_state.NORTH:
                                    #game_state.game_map[x_counter][y_counter - 2] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter - 2].gobject])
                                    reset_flags(x_counter, y_counter - 2)
                                elif hitting_object.forward == game_state.EAST:
                                    #game_state.game_map[x_counter+1][y_counter - 1] = copy.deepcopy(game_objects[game_state.game_map[x_counter+1][y_counter - 1].gobject])
                                    reset_flags(x_counter + 1, y_counter - 1)
                                elif hitting_object.forward == game_state.SOUTH:
                                    #game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter].gobject])
                                    reset_flags(x_counter, y_counter)
                                elif hitting_object.forward == game_state.WEST:
                                    #game_state.game_map[x_counter-1][y_counter - 1] = copy.deepcopy(game_objects[game_state.game_map[x_counter-1][y_counter - 1].gobject])
                                    reset_flags(x_counter - 1, y_counter - 1)

               
                        if current_sprite.moving == game_state.SOUTH:

                            hitting_object = game_state.game_map[x_counter][y_counter + 1]

                            game_state.game_map[x_counter][y_counter+1] = copy.deepcopy(game_state.game_map[x_counter][y_counter])
#                            game_state.game_map[x_counter][y_counter+1] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter].object])
                            game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[0])
                            game_state.game_map[x_counter][y_counter+1].ignore = True
                            game_state.game_map[x_counter][y_counter+1].x = x_counter
                            game_state.game_map[x_counter][y_counter+1].y = y_counter + 1
                            game_state.game_map[x_counter][y_counter+1].move_counter = 0
                            game_state.game_map[x_counter][y_counter+1].moving = 0
                            
                            game_state.game_map[x_counter][y_counter+1].moved = game_state.SOUTH
                            # Blank above line and uncomment below if multiple Repton shuffles shouldn't kill
                            #if y_counter < game_state.LEVEL_WIDTH - 2 and \
                            #   game_state.game_map[x_counter][y_counter+2].gobject == 0:
                            #    game_state.game_map[x_counter][y_counter+1].moved = game_state.SOUTH

                            hitting_object.hit(game_state.game_map[x_counter][y_counter + 1])
                
                            if hitting_object.moving:
                                if hitting_object.forward == game_state.NORTH:
                                    #game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter].gobject])
                                    reset_flags(x_counter, y_counter)
                                elif hitting_object.forward == game_state.EAST:
                                    #game_state.game_map[x_counter+1][y_counter + 1] = copy.deepcopy(game_objects[game_state.game_map[x_counter+1][y_counter + 1].gobject])
                                    reset_flags(x_counter + 1, y_counter + 1)
                                elif hitting_object.forward == game_state.SOUTH:
                                    #game_state.game_map[x_counter][y_counter + 2] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter + 2].gobject])
                                    reset_flags(x_counter, y_counter + 2)
                                elif hitting_object.forward == game_state.WEST:
                                    #game_state.game_map[x_counter-1][y_counter + 1] = copy.deepcopy(game_objects[game_state.game_map[x_counter-1][y_counter + 1].gobject])
                                    reset_flags(x_counter - 1, y_counter + 1)


                        if current_sprite.moving == game_state.EAST:

                            hitting_object = game_state.game_map[x_counter + 1][y_counter]

                            game_state.game_map[x_counter + 1][y_counter] = copy.deepcopy(game_state.game_map[x_counter][y_counter])
#                            game_state.game_map[x_counter+1][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter].object])
                            game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[0])
                            game_state.game_map[x_counter+1][y_counter].ignore = True
                            game_state.game_map[x_counter+1][y_counter].x = x_counter + 1
                            game_state.game_map[x_counter+1][y_counter].y = y_counter
                            game_state.game_map[x_counter + 1][y_counter].move_counter = 0
                            game_state.game_map[x_counter + 1][y_counter].moving = 0
                            
                            game_state.game_map[x_counter + 1][y_counter].moved = game_state.EAST
                            # Blank above line and uncomment below if multiple Repton shuffles shouldn't kill
                            #if x_counter < game_state.LEVEL_HEIGHT - 2 and \
                            #   game_state.game_map[x_counter + 2][y_counter].gobject == 0:
                            #    game_state.game_map[x_counter + 1][y_counter].moved = game_state.EAST

                            hitting_object.hit(game_state.game_map[x_counter + 1][y_counter])

                
                            if hitting_object.moving:
                                if hitting_object.forward == game_state.NORTH:
                                    #game_state.game_map[x_counter + 1][y_counter-1] = copy.deepcopy(game_objects[game_state.game_map[x_counter + 1][y_counter-1].gobject])
                                    reset_flags(x_counter + 1, y_counter - 1)
                                elif hitting_object.forward == game_state.EAST:
                                    #game_state.game_map[x_counter + 2][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter + 2][y_counter].gobject])
                                    reset_flags(x_counter + 2, y_counter)
                                elif hitting_object.forward == game_state.SOUTH:
                                    #game_state.game_map[x_counter + 1][y_counter+1] = copy.deepcopy(game_objects[game_state.game_map[x_counter + 1][y_counter+1].gobject])
                                    reset_flags(x_counter + 1, y_counter + 1)
                                elif hitting_object.forward == game_state.WEST:
                                    #game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter].gobject])
                                    reset_flags(x_counter, y_counter)

                   
                        if current_sprite.moving == game_state.WEST:

                            hitting_object = game_state.game_map[x_counter - 1][y_counter]

                            game_state.game_map[x_counter - 1][y_counter] = copy.deepcopy(game_state.game_map[x_counter][y_counter])
#                            game_state.game_map[x_counter-1][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter].object])
                            game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[0])
                            #game_state.game_map[x_counter - 1][y_counter].ignore = True
                            game_state.game_map[x_counter - 1][y_counter].x = x_counter - 1
                            game_state.game_map[x_counter - 1][y_counter].y = y_counter
                            game_state.game_map[x_counter - 1][y_counter].move_counter = 0
                            game_state.game_map[x_counter - 1][y_counter].moving = 0
                            
                            game_state.game_map[x_counter - 1][y_counter].moved = game_state.WEST
                            # Blank above line and uncomment below if multiple Repton shuffles shouldn't kill
                            #if x_counter > 1 and \
                            #   game_state.game_map[x_counter - 2][y_counter].gobject == 0:
                            #    game_state.game_map[x_counter - 1][y_counter].moved = game_state.WEST

                            hitting_object.hit(game_state.game_map[x_counter - 1][y_counter])
                
                            if hitting_object.moving:
                                if hitting_object.forward == game_state.NORTH:
                                    #game_state.game_map[x_counter - 1][y_counter-1] = copy.deepcopy(game_objects[game_state.game_map[x_counter - 1][y_counter-1].gobject])
                                    reset_flags(x_counter - 1, y_counter - 1)
                                elif hitting_object.forward == game_state.EAST:
                                    #game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter].gobject])
                                    reset_flags(x_counter, y_counter)
                                elif hitting_object.forward == game_state.SOUTH:
                                    #game_state.game_map[x_counter - 1][y_counter+1] = copy.deepcopy(game_objects[game_state.game_map[x_counter - 1][y_counter+1].gobject])
                                    reset_flags(x_counter - 1, y_counter + 1)
                                elif hitting_object.forward == game_state.WEST:
                                    #game_state.game_map[x_counter - 2][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter - 2][y_counter].gobject])
                                    reset_flags(x_counter - 2, y_counter)

# Kill Dave: oh no!
                        
        if game_state.kill_dave == True:
            game_state.kill_dave = False
            game_state.lives -= 1
            
            game_state.use_key = False
            player_right = player_left = player_up = player_down = 0
            game_state.dave_x = game_state.dave_dest_x = game_data.dave_pos[game_state.level_number][0]
            game_state.dave_y = game_state.dave_dest_y = game_data.dave_pos[game_state.level_number][1]
            player_move_counter_horiz = player_move_counter_vert = 0
            game_state.player_moving = 0
            scroll_horiz = scroll_vert = False

            game_state.transporting = False
            if game_state.min_score_hit == True:
                game_state.bg_col = 255, 220, 150
            else:
                game_state.bg_col = 150, 150, 255

            game_state.x_offset = game_state.dave_x - 5
            if game_state.x_offset < 0:
                game_state.x_offset = 0
            if game_state.x_offset > game_state.LEVEL_WIDTH - 16:
                game_state.x_offset = game_state.LEVEL_WIDTH - 16
                
            game_state.y_offset = game_state.dave_y - 5
            if game_state.y_offset < 0:
                game_state.y_offset = 0
            if game_state.y_offset > game_state.LEVEL_HEIGHT - 12:
                game_state.y_offset = game_state.LEVEL_HEIGHT - 12
            
            if game_state.lives == 0:
                render_text('Poor Dave', 240)
                pygame.display.flip()
                while(1):
                    wait_event = pygame.event.wait()
                    if wait_event.type == pygame.KEYDOWN:
                        if wait_event.key == pygame.K_SPACE:
                            break
                        else:
                            pass
                return False
            else:
                render_text('Watch out Dave! That killed you!', 240)
                pygame.display.flip()
                while(1):
                    wait_event = pygame.event.wait()
                    if wait_event.type == pygame.KEYDOWN:
                        if wait_event.key == pygame.K_SPACE:
                            break
                        else:
                            pass

            if status_screen() == False:
                program_quit = True

# Transport-out effect       
        if game_state.transporting == True:
            old_screen.blit(screen, old_rect)
            
            for col_val in range(16):
                game_state.bg_col = 255 - col_val * 16, 255 - col_val * 16, 255 - col_val * 16
                screen.fill(game_state.bg_col)
                screen.blit(old_screen, old_rect, None, pygame.BLEND_MIN)
                pygame.display.flip()
                #game_state.transporting = False
            game_state.bg_col = 150, 150, 255

        screen.fill(game_state.bg_col)

# Draw map
        for y_counter in range(12 + scroll_vert):
            for x_counter in range(16 + scroll_horiz):

                map_sprite = game_state.game_map[x_counter - scroll_horiz_comp + game_state.x_offset][y_counter - scroll_vert_comp + game_state.y_offset]

                if map_sprite.sprite > 0:
                    if map_sprite.moving == game_state.NORTH:
                        
                        screen.blit(game_sprites[map_sprite.sprite]
                        ,((x_counter - scroll_horiz_comp) * 40 - (player_move_counter_horiz * 10) * scroll_horiz
                        , (y_counter - scroll_vert_comp) * 40 - \
                          (player_move_counter_vert * 10) * scroll_vert - map_sprite.move_counter * 10))

                    elif map_sprite.moving == game_state.EAST:
                        
                        screen.blit(game_sprites[map_sprite.sprite]
                        ,((x_counter - scroll_horiz_comp) * 40 - \
                          (player_move_counter_horiz * 10) * scroll_horiz + map_sprite.move_counter * 10
                        , (y_counter - scroll_vert_comp) * 40 - (player_move_counter_vert * 10) * scroll_vert))

                    elif map_sprite.moving == game_state.SOUTH:
                        
                        screen.blit(game_sprites[map_sprite.sprite]
                        ,((x_counter - scroll_horiz_comp) * 40 - (player_move_counter_horiz * 10) * scroll_horiz
                        , (y_counter - scroll_vert_comp) * 40 - \
                          (player_move_counter_vert * 10) * scroll_vert + map_sprite.move_counter * 10))

                    elif map_sprite.moving == game_state.WEST:
                        
                        screen.blit(game_sprites[map_sprite.sprite]
                        ,((x_counter - scroll_horiz_comp) * 40 - \
                          (player_move_counter_horiz * 10) * scroll_horiz - map_sprite.move_counter * 10
                        , (y_counter - scroll_vert_comp) * 40 - (player_move_counter_vert * 10) * scroll_vert))

                    else:

                        screen.blit(game_sprites[map_sprite.sprite]
                        ,((x_counter - scroll_horiz_comp) * 40 - (player_move_counter_horiz * 10) * scroll_horiz
                        , (y_counter - scroll_vert_comp) * 40 - (player_move_counter_vert * 10) * scroll_vert))
                        

# Draw player
        player_rect.left = (game_state.dave_x - game_state.x_offset) * 40 + (player_move_counter_horiz * 10) * (not scroll_horiz)
        player_rect.top = (game_state.dave_y - game_state.y_offset) * 40 + (player_move_counter_vert * 10) * (not scroll_vert) 
        screen.blit(sprite_dave[dave_frame], player_rect)

# Transport-in effect
        if game_state.transporting == True:
            old_screen.blit(screen, old_rect)
            
            for col_val in range(16):
                game_state.bg_col = col_val * 16, col_val * 16, col_val * 16
                screen.fill(game_state.bg_col)
                screen.blit(old_screen, old_rect, None, pygame.BLEND_ADD)
                pygame.display.flip()
                game_state.transporting = False
            if game_state.min_score_hit == True:
                game_state.bg_col = 255, 220, 150
            else:
                game_state.bg_col = 150, 150, 255
            
        
        pygame.display.flip()
        frames += 1

        if dave_wait > 0:
            dave_wait -= 1
        elif dave_wait == 0:
            dave_frame = 0

        
        anim_counter += 1
        if anim_counter > 2:
            anim_counter = 0



# Dave action function is used for any goal checks etc.
        Dave().action()

# If minimum score hit, set game_state.min_score_hit flag
        if game_state.score > game_data.minimum_score[game_state.level_number] - 1:
            game_state.min_score_hit = True
# If level has been completed, this flag will be set
        if game_state.level_finished:
            return True

        
        GameClock.tick(30)

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))

    return True

def editor(level_file_name):

    game_state.bg_col = 150, 200, 200

    frames = 0
    ticks = pygame.time.get_ticks()
    EditorClock = pygame.time.Clock()

    mouse_rect = pygame.Rect(0, 0, 20, 20)

    x_offset = y_offset = 0
    program_quit = False

# Copy level data to working data
    editor_level_number = 0 
    game_state.LEVEL_WIDTH = game_data.level_size[editor_level_number][0]
    game_state.LEVEL_HEIGHT = game_data.level_size[editor_level_number][1]
    editor_dave_pos = copy.deepcopy(game_data.dave_pos[editor_level_number])
    editor_level_map = copy.deepcopy(game_data.level_map[editor_level_number])

    
    placing_target = False
    original_x = original_y = 0
    target_x = target_y = -40
    flasher = 0

    sprite_no = 1

    prev_mouse_x = prev_mouse_y = -1

    check_if_save = False

    while(1):
# Process inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                program_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and x_offset < game_state.LEVEL_WIDTH - 16:
                    x_offset += 1
                if event.key == pygame.K_LEFT and x_offset > 0:
                    x_offset -= 1
                if event.key == pygame.K_UP and y_offset > 0:
                    y_offset -= 1
                if event.key == pygame.K_DOWN and y_offset < game_state.LEVEL_HEIGHT - 12:
                    y_offset += 1
                if event.key == pygame.K_SPACE:
                    editor_dave_pos = ((mouse_rect.left - mouse_rect.left % 40)/40 + x_offset, (mouse_rect.top - mouse_rect.top % 40)/40 + y_offset)
                    check_if_save = True
                if placing_target == False:
                    if event.key == pygame.K_z and sprite_no > 1:
                        sprite_no -=1
                        flasher = 0
                    if event.key == pygame.K_x and sprite_no < game_state.NO_OF_OBJECTS:
                        sprite_no +=1
                        flasher = 0
                prev_mouse_x = prev_mouse_y = -1

                if event.key == pygame.K_w and editor_level_number < len(game_data.level_map) - 1 and placing_target == False:
                    if check_if_save == True:
                        render_text('Save current level? Y/N', 240)
                        pygame.display.flip()
                        while(1):
                            wait_event = pygame.event.wait()

                            if wait_event.type == pygame.KEYDOWN:
                            
                                if wait_event.key == pygame.K_y:
                                    game_data.dave_pos[editor_level_number] = editor_dave_pos
                                    game_data.level_map[editor_level_number] = editor_level_map
                                    game_data.level_size[editor_level_number] = [game_state.LEVEL_WIDTH, game_state.LEVEL_HEIGHT]
                                    
                                    data_file = open(level_file_name, "wb")
                                    pickle.dump(game_data, data_file)
                                    data_file.close()
                                    
                                    break
                                elif wait_event.key == pygame.K_n:
                                    
                                    break
                                else:
                                    pass
                    check_if_save = False
                    editor_level_number += 1
                    game_state.LEVEL_WIDTH = game_data.level_size[editor_level_number][0]
                    game_state.LEVEL_HEIGHT = game_data.level_size[editor_level_number][1]
                    editor_dave_pos = copy.deepcopy(game_data.dave_pos[editor_level_number])
                    editor_level_map = copy.deepcopy(game_data.level_map[editor_level_number])
                    x_offset = y_offset = 0
                    target_x = target_y = -40

                if event.key == pygame.K_q and editor_level_number > 0 and placing_target == False:
                    if check_if_save == True:
                        render_text('Save current level? Y/N', 240)
                        pygame.display.flip()
                        while(1):
                            wait_event = pygame.event.wait()

                            if wait_event.type == pygame.KEYDOWN:
                            
                                if wait_event.key == pygame.K_y:
                                    game_data.dave_pos[editor_level_number] = editor_dave_pos
                                    game_data.level_map[editor_level_number] = editor_level_map
                                    game_data.level_size[editor_level_number] = [game_state.LEVEL_WIDTH, game_state.LEVEL_HEIGHT]
                                    
                                    data_file = open(level_file_name, "wb")
                                    pickle.dump(game_data, data_file)
                                    data_file.close()
                                    
                                    break
                                elif wait_event.key == pygame.K_n:
                                    
                                    break
                                else:
                                    pass
                    check_if_save = False
                    editor_level_number -= 1
                    game_state.LEVEL_WIDTH = game_data.level_size[editor_level_number][0]
                    game_state.LEVEL_HEIGHT = game_data.level_size[editor_level_number][1]
                    editor_dave_pos = copy.deepcopy(game_data.dave_pos[editor_level_number])
                    editor_level_map = copy.deepcopy(game_data.level_map[editor_level_number])
                    x_offset = y_offset = 0
                    target_x = target_y = -40

                if event.key == pygame.K_s and placing_target == False:

                    check_if_save = True
                    
                    prompt_rect = pygame.Rect(0, 0, 400, 200)
                    prompt_rect.centerx = screen.get_rect().centerx
                    prompt_rect.centery = screen.get_rect().centery

                    
                    
                    while(1):
                        pygame.draw.rect(screen, (0, 0, 0), prompt_rect)
                        render_text('Set Minimum Score', 210)
                        render_text(str(game_data.minimum_score[editor_level_number]), 240)
                        render_text('Up/Down to change, Return to set', 270)
                        pygame.display.flip()
                        
                        wait_event = pygame.event.wait()
                        if wait_event.type == pygame.KEYDOWN:
                            if wait_event.key == pygame.K_RETURN:
                                break
                            elif wait_event.key == pygame.K_UP:
                                    game_data.minimum_score[editor_level_number] += 1
                            elif wait_event.key == pygame.K_DOWN and game_data.minimum_score[editor_level_number] > 1:
                                    game_data.minimum_score[editor_level_number] -= 1
                            #else:
                            #    pass

                if event.key == pygame.K_t and placing_target == False:

                    if check_if_save == True:
                        render_text('Save current level? Y/N', 240)
                        pygame.display.flip()
                        while(1):
                            wait_event = pygame.event.wait()

                            if wait_event.type == pygame.KEYDOWN:
                            
                                if wait_event.key == pygame.K_y:
                                    game_data.dave_pos[editor_level_number] = editor_dave_pos
                                    game_data.level_map[editor_level_number] = editor_level_map
                                    game_data.level_size[editor_level_number] = [game_state.LEVEL_WIDTH, game_state.LEVEL_HEIGHT]
                                    
                                    data_file = open(level_file_name, "wb")
                                    pickle.dump(game_data, data_file)
                                    data_file.close()
                                    break
                                elif wait_event.key == pygame.K_n:
                                    
                                    break
                                else:
                                    pass
                                
                    check_if_save = False 
                    game_state.level_number = editor_level_number
                    game_state.score = 0
                    game_state.lives = 3
                    game_state.bg_col = 150, 150, 255
                    game_state.message = 'Testing!'
                    status_screen()
                    game()
                    game_state.bg_col = 150, 200, 200
                    game_state.message = 'Testing Complete!'
                    status_screen()
                    target_x = target_y = -40

# -------------- Create new map -----------------
                if event.key == pygame.K_n and placing_target == False:

                    target_x = target_y = -40

                    create_new_map = False

                    new_map_x = new_map_y = 32

                    prompt_rect = pygame.Rect(0, 0, 400, 200)
                    prompt_rect.centerx = screen.get_rect().centerx
                    prompt_rect.centery = screen.get_rect().centery
                    pygame.draw.rect(screen, (0, 0, 0), prompt_rect)
                    render_text('New Map:', 160)
                    render_text('Q/W - change width', 190)
                    render_text('A/S - change height', 220)
                    render_text(' Size: ' + str(new_map_x) + ' x '+ str(new_map_y) + ' ', 250)
                    render_text('Return - Set size', 280)
                    render_text('Esc - Cancel', 310)
                    pygame.display.flip()

                    
                    while(1):
                        wait_event = pygame.event.wait()

                        if wait_event.type == pygame.KEYDOWN:
                        
                            #if wait_event.key == pygame.K_1:      
                            #    game_state.LEVEL_WIDTH = 16
                            #    game_state.LEVEL_HEIGHT = 12
                            #    create_new_map = True
                            #    break
                            
                            #elif wait_event.key == pygame.K_2:      
                            #    game_state.LEVEL_WIDTH = 32
                            #    game_state.LEVEL_HEIGHT = 32
                            #    create_new_map = True
                            #    break
                            
                            #elif wait_event.key == pygame.K_3:      
                            #    game_state.LEVEL_WIDTH = 64
                            #    game_state.LEVEL_HEIGHT = 64
                            #    create_new_map = True
                            #    break
                                                    
                            if wait_event.key == pygame.K_ESCAPE:
                                break

                            elif wait_event.key == pygame.K_q:
                                if new_map_x > 16:
                                    new_map_x -= 1
                                    
                            elif wait_event.key == pygame.K_w:
                                if new_map_x < 64 :
                                    new_map_x += 1
                                    
                            elif wait_event.key == pygame.K_a:
                                if new_map_y > 12:
                                    new_map_y -= 1
                                    
                            elif wait_event.key == pygame.K_s:
                                if new_map_y < 64:
                                    new_map_y += 1

                            elif wait_event.key == pygame.K_RETURN:      
                                create_new_map = True
                                break
                                    
                            else:
                                pass
                        else:
                            pass

                        render_text(' Size: ' + str(new_map_x) + ' x '+ str(new_map_y) + ' ', 250)
                        pygame.display.flip()

                        
                    if create_new_map == True:
                        prompt_rect = pygame.Rect(0, 0, 400, 200)
                        prompt_rect.centerx = screen.get_rect().centerx
                        prompt_rect.centery = screen.get_rect().centery
                        pygame.draw.rect(screen, (0, 0, 0), prompt_rect)
                        render_text('R: Replace current map', 210)
                        render_text('I: Insert after other maps', 240)
                        render_text('Esc - Cancel', 270)
                        pygame.display.flip()

                        while(1):
                            wait_event = pygame.event.wait()

                            if wait_event.type == pygame.KEYDOWN:
                            
                                if wait_event.key == pygame.K_r:      
                                    break
                                
                                elif wait_event.key == pygame.K_i:
                                    if check_if_save == True:
                                        prompt_rect = pygame.Rect(0, 0, 400, 200)
                                        prompt_rect.centerx = screen.get_rect().centerx
                                        prompt_rect.centery = screen.get_rect().centery
                                        pygame.draw.rect(screen, (0, 0, 0), prompt_rect)
                                        render_text('Save current level? Y/N', 240)
                                        pygame.display.flip()
                                        while(1):
                                            wait_event = pygame.event.wait()

                                            if wait_event.type == pygame.KEYDOWN:
                                            
                                                if wait_event.key == pygame.K_y:
                                                    game_data.dave_pos[editor_level_number] = editor_dave_pos
                                                    game_data.level_map[editor_level_number] = editor_level_map
                                                    game_data.level_size[editor_level_number] = [game_state.LEVEL_WIDTH, game_state.LEVEL_HEIGHT]
                                                    
                                                    data_file = open(level_file_name, "wb")
                                                    pickle.dump(game_data, data_file)
                                                    data_file.close()
                                                    
                                                    break
                                                elif wait_event.key == pygame.K_n:
                                                    
                                                    break
                                                else:
                                                    pass
                                    check_if_save = False
                                    #print len(game_data.level_map)
                                    editor_level_number = len(game_data.level_map)
                                    game_state.LEVEL_WIDTH = new_map_x
                                    game_state.LEVEL_HEIGHT = new_map_y
                                    game_data.level_map.append([[[0,0] for i in range(game_state.LEVEL_HEIGHT)] for j in range(game_state.LEVEL_WIDTH)])
                                    game_data.dave_pos.append((0, 0))
                                    game_data.level_size.append([game_state.LEVEL_WIDTH, game_state.LEVEL_HEIGHT])
                                    game_data.minimum_score.append(1)
                                    break
                                                        
                                elif wait_event.key == pygame.K_ESCAPE:
                                    create_new_map = False
                                    break
                                
                                else:
                                    pass
                            else:
                                pass

                    if create_new_map == True:
                        
                        game_state.LEVEL_WIDTH = new_map_x
                        game_state.LEVEL_HEIGHT = new_map_y
                                    
                        editor_level_map = [[[0,0] for i in range(game_state.LEVEL_HEIGHT)] for j in range(game_state.LEVEL_WIDTH)]
                            
                        editor_dave_pos = (0,0)
                        game_data.minimum_score[editor_level_number] = 1
                        x_offset = y_offset = 0
# -------------------------------------------------

# Exit to menu
        if program_quit == True:
            break

        screen.fill(game_state.bg_col)

# Place sprite

        mouse_x = (mouse_rect.left - mouse_rect.left % 40)/40 + x_offset
        mouse_y = (mouse_rect.top - mouse_rect.top % 40)/40 + y_offset

        mouse_buttons = pygame.mouse.get_pressed()
        
        if mouse_buttons[0] == 1 and (prev_mouse_x != mouse_x or prev_mouse_y != mouse_y):
            if game_objects[sprite_no].needs_target == False:
                editor_level_map[mouse_x][mouse_y] = [sprite_no, 0]
                check_if_save = True
            else:
                if placing_target == False:
                    editor_level_map[mouse_x][mouse_y] = [sprite_no, 0]
                    original_x = mouse_x
                    original_y = mouse_y
                    placing_target = True
                    check_if_save = True
                else:
                    editor_level_map[original_x][original_y][1] = (mouse_x, mouse_y)
                    placing_target = False
                    check_if_save = True

            prev_mouse_x = mouse_x
            prev_mouse_y = mouse_y
            target_x = target_y = -40
                    
        if mouse_buttons[2] == 1 and placing_target == False:
            editor_level_map[mouse_x][mouse_y] = [0, 0]
            prev_mouse_x = prev_mouse_y = -1
            check_if_save = True
            target_x = target_y = -40
            


# Draw map
        for y_counter in range(12):
            for x_counter in range(16):
                #print x_counter + x_offset, y_counter + y_offset
                map_sprite = editor_level_map[x_counter + x_offset][y_counter + y_offset][0]
                if map_sprite > 0:
                    screen.blit(game_sprites[game_objects[map_sprite].sprite], (x_counter * 40, y_counter * 40))

# Draw target
        if editor_level_map[mouse_x][mouse_y][1] != 0:
            target_x = editor_level_map[mouse_x][mouse_y][1][0] * 40
            target_y = editor_level_map[mouse_x][mouse_y][1][1] * 40
            #screen.blit(game_state.target_img, (editor_level_map[mouse_x][mouse_y][1][0] * 40, editor_level_map[mouse_x][mouse_y][1][1] * 40))
        if flasher > 30:
            screen.blit(game_state.target_img, (target_x - x_offset * 40, target_y - y_offset * 40))
            

# Draw cursor
        mouse_rect.topleft = pygame.mouse.get_pos()
        mouse_rect.left = (mouse_rect.left - mouse_rect.left % 40)
        mouse_rect.top = (mouse_rect.top - mouse_rect.top % 40)
        if flasher < 30:
            if placing_target == True:
                screen.blit(game_state.target_img, mouse_rect)
            else:
                screen.blit(game_sprites[game_objects[sprite_no].sprite], mouse_rect)
        
# Draw Dave
        screen.blit(sprite_dave[0], ((editor_dave_pos[0] - x_offset) * 40, (editor_dave_pos[1] - y_offset) * 40))

        
        
        pygame.display.flip()
        frames = frames+1
        flasher += 1
        if flasher > 60:
            flasher = 0
        
        EditorClock.tick(60)

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))
    

# Save Data

#    game_data.dave_pos[editor_level_number] = editor_dave_pos
#    game_data.level_map[editor_level_number] = editor_level_map
#    game_data.level_size[editor_level_number] = [game_state.LEVEL_WIDTH, game_state.LEVEL_HEIGHT]
#    
#    data_file = file(r"game_data.dat", "w")
#    pickle.dump(game_data, data_file)
#    data_file.close()
    if check_if_save == True:
        
        render_text('Save current level? Y/N', 240)
        pygame.display.flip()
        while(1):
            wait_event = pygame.event.wait()

            if wait_event.type == pygame.KEYDOWN:
            
                if wait_event.key == pygame.K_y:
                    game_data.dave_pos[editor_level_number] = editor_dave_pos
                    game_data.level_map[editor_level_number] = editor_level_map
                    game_data.level_size[editor_level_number] = [game_state.LEVEL_WIDTH, game_state.LEVEL_HEIGHT]
                    
                    data_file = open(level_file_name, "wb")
                    pickle.dump(game_data, data_file)
                    data_file.close()
                    break
                elif wait_event.key == pygame.K_n:
                    
                    break
                else:
                    pass

def main():

    global game_data
    program_quit = False
    title_screen = pygame.image.load("Images/Title-Screen.png")
    stretched_title_screen = pygame.transform.scale(title_screen, (640, 480))

    title_rect = stretched_title_screen.get_rect()

#    for col_val in range(32):
#        bg_col = col_val * 8, col_val * 8, col_val * 8
#        screen.fill(bg_col)
#        screen.blit(stretched_title_screen, title_rect, None, pygame.BLEND_MIN)
#        pygame.display.flip()

    sound_twiddle = pygame.mixer.Sound('Music/Twiddle.wav')
    pygame.mixer.music.load('Music/CT Title.ogg')

    menu_tick = pygame.time.get_ticks()
    menu_items = ['1 for user levels', '2 for editor', 'M to toggle music', 'R to redefine keys', 'Esc to exit']
    menu_counter = 0


    while(1):

        if game_state.play_music and pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(-1)
        
        game_state.level_number = 0

        if pygame.time.get_ticks() - menu_tick > 1000:
            menu_tick = pygame.time.get_ticks()
            menu_counter += 1
            if menu_counter > len(menu_items) - 1:
                menu_counter = 0

        screen.blit(stretched_title_screen, title_rect)
        
        render_text('Version 1.1', 460)
        render_text('Press Space to Play!', 260)
        render_text(menu_items[menu_counter], 420)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                program_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    game_state.bg_col = 150, 150, 255
                    screen.fill(game_state.bg_col)
                    
                    render_text('Select episode:', 180)
                    render_text('1 - Pond of Pondering', 220)
                    render_text('2 - Swamp of Sussing', 260)
                    render_text('3 - Bog of Bewilderment', 300)
                    pygame.display.flip()
                    
                    while(1):
                        wait_event = pygame.event.wait()
                        if wait_event.type == pygame.KEYDOWN:
                            if wait_event.key == pygame.K_1:
                                game_filename = "game_data1.dat"
                                intro_text = ['Dave dreamed of a frog farm,',\
                                              'where he would tend his flock',\
                                              'amid the soft ribbiting.',\
                                              'But Dave needs frogs!']

                                outro_text = ['Dave collected his frogs',\
                                              'at the end of a hard day',\
                                              'and went back home.',\
                                              'Goodnight Dave!']
                                break
                            if wait_event.key == pygame.K_2:
                                game_filename = "game_data2.dat"
                                intro_text = ['Dave had some frogs,',\
                                              'but not enough',\
                                              'to start his farm.',\
                                              'Get more frogs!']

                                outro_text = ['There were now many frogs',\
                                              'Hopping around his feet',\
                                              'and Dave smiled.',\
                                              'Dave likes frogs!']
                                break
                            if wait_event.key == pygame.K_3:
                                game_filename = "game_data3.dat"
                                intro_text = ['The frogs seemed to want friends',\
                                              'to play with',\
                                              'on the farm.',\
                                              'Lots of frogs!']

                                outro_text = ['His dream come true,',\
                                              'Dave rested his feet',\
                                              'and listened to the croaks.',\
                                              'Well done Dave!']
                                break
                            else:
                                pass

                    data_file = open(game_filename, "rb")
                    game_data = pickle.load(data_file)
                    data_file.close()

                    print game_data.def_file
                    load_defs(game_data.def_file[:-3])

                    game_state.lives = 3
                    game_state.score = 0
                    game_state.bg_col = 150, 150, 255
                    screen.fill(game_state.bg_col)
                    render_text(intro_text[0], 180)
                    render_text(intro_text[1], 220)
                    render_text(intro_text[2], 260)
                    render_text(intro_text[3], 300)
                    pygame.display.flip()
                    
                    pygame.mixer.music.stop()
                    if game_state.play_music:
                        sound_twiddle.play()
                    
                    while(1):
                        wait_event = pygame.event.wait()
                        if wait_event.type == pygame.KEYDOWN:
                            if wait_event.key == pygame.K_SPACE:
                                
                                break
                            else:
                                pass
                            
                    game_state.message = game_state.default_message
                    
                    if status_screen() == False:
                        break
                                
                    while(1):

                        if game_state.play_music:
                            pygame.mixer.music.load('Music/CT Game 1.ogg')
                            pygame.mixer.music.play(-1)
                        return_val = game()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('Music/CT Title.ogg')
                        game_state.bg_col = 150, 150, 255
                        game_state.message = game_state.default_message
                        
                        if return_val == False:
                            game_state.bg_col = 150, 150, 255
                            screen.fill(game_state.bg_col)
                            render_text('Retry Y/N?', 240)
                            pygame.display.flip()
                            retry = True
                            while(1):
                                wait_event = pygame.event.wait()
                                if wait_event.type == pygame.KEYDOWN:
                                    if wait_event.key == pygame.K_y:
                                        game_state.lives = 3
                                        game_state.score = 0
                                        break
                                    if wait_event.key == pygame.K_n:
                                        retry = False
                                        break
                                    else:
                                        pass
                            if retry == False:
                                break

                            if status_screen() == False:
                                break
                            
                        else:
                            game_state.level_number += 1
                            game_state.score = 0
                            if game_state.level_number > len(game_data.level_map) - 1:
                                game_state.bg_col = 150, 150, 255
                                screen.fill(game_state.bg_col)
                                render_text(outro_text[0], 180)
                                render_text(outro_text[1], 220)
                                render_text(outro_text[2], 260)
                                render_text(outro_text[3], 300)
                                pygame.display.flip()
                                if game_state.play_music:
                                    sound_twiddle.play()
                                
                                while(1):
                                    wait_event = pygame.event.wait()
                                    if wait_event.type == pygame.KEYDOWN:
                                        if wait_event.key == pygame.K_SPACE:
                                            break
                                        else:
                                            pass
                                break
                            prompt_rect = pygame.Rect(0, 0, 300, 100)
                            prompt_rect.centerx = screen.get_rect().centerx
                            prompt_rect.centery = screen.get_rect().centery
                            pygame.draw.rect(screen, (0, 0, 0), prompt_rect)
                            render_text('Level Complete!', 210)
                            render_text('Press Space', 270)
                            pygame.display.flip()
                            if game_state.play_music:
                                sound_twiddle.play()
                            while(1):
                                wait_event = pygame.event.wait()
                                if wait_event.type == pygame.KEYDOWN:
                                    if wait_event.key == pygame.K_SPACE:
                                        
                                        break
                                    else:
                                        pass

                            if status_screen() == False:
                                break
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    
                    level_list = os.listdir('Levels')
                    file_number = 0

                    
                    while(1):
                        wait_event = pygame.event.wait()
                        if wait_event.type == pygame.KEYDOWN:
                            if wait_event.key == pygame.K_RETURN:                             
                                break
                            elif wait_event.key == pygame.K_DOWN:
                                file_number += 1
                                if file_number > len(level_list) - 1:
                                    file_number = len(level_list) - 1
                            elif wait_event.key == pygame.K_UP:
                                file_number -= 1
                                if file_number < 0:
                                    file_number = 0
                            else:
                                pass
                            
                        screen.fill(game_state.bg_col)
                        render_text("Play which level set?", 220)
                        render_text(level_list[file_number][:-4], 250)
                        pygame.display.flip()

                    data_file = open("Levels/" + level_list[file_number], "rb")
                    game_data = pickle.load(data_file)
                    data_file.close()

                    print game_data.def_file
                    load_defs(game_data.def_file[:-3])

                    game_state.lives = 3
                    game_state.score = 0
                    game_state.bg_col = 150, 150, 255
                    screen.fill(game_state.bg_col)
                    render_text('Playing user levels', 240)
                    pygame.display.flip()

                    pygame.mixer.music.stop()
                    if game_state.play_music:
                        sound_twiddle.play()
                    
                    while(1):
                        wait_event = pygame.event.wait()
                        if wait_event.type == pygame.KEYDOWN:
                            if wait_event.key == pygame.K_SPACE:
                                
                                break
                            else:
                                pass
                            
                    game_state.message = game_state.default_message
                    
                    
                    if status_screen() == False:
                        break
                                
                    while(1):

                        if game_state.play_music:
                            pygame.mixer.music.load('Music/CT Game 1.ogg')
                            pygame.mixer.music.play(-1)
                        return_val = game()
                        game_state.bg_col = 150, 150, 255
                        game_state.message = game_state.default_message
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('Music/CT Title.ogg')
                        
                        if return_val == False:
                            game_state.bg_col = 150, 150, 255
                            screen.fill(game_state.bg_col)
                            render_text('Retry Y/N?', 240)
                            pygame.display.flip()
                            retry = True
                            while(1):
                                wait_event = pygame.event.wait()
                                if wait_event.type == pygame.KEYDOWN:
                                    if wait_event.key == pygame.K_y:
                                        game_state.lives = 3
                                        game_state.score = 0
                                        break
                                    if wait_event.key == pygame.K_n:
                                        retry = False
                                        break
                                    else:
                                        pass
                            if retry == False:
                                break

                            if status_screen() == False:
                                break
                        else:
                            game_state.level_number += 1
                            game_state.score = 0
                            if game_state.level_number > len(game_data.level_map) - 1:
                                game_state.bg_col = 150, 150, 255
                                screen.fill(game_state.bg_col)

                                render_text('User levels completed', 240)
                                if game_state.play_music:
                                    sound_twiddle.play()

                                pygame.display.flip()
                                while(1):
                                    wait_event = pygame.event.wait()
                                    if wait_event.type == pygame.KEYDOWN:
                                        if wait_event.key == pygame.K_SPACE:
                                            break
                                        else:
                                            pass
                                break
                            prompt_rect = pygame.Rect(0, 0, 300, 100)
                            prompt_rect.centerx = screen.get_rect().centerx
                            prompt_rect.centery = screen.get_rect().centery
                            pygame.draw.rect(screen, (0, 0, 0), prompt_rect)
                            render_text('Level Complete!', 210)
                            render_text('Press Space', 270)
                            pygame.display.flip()
                            if game_state.play_music:
                                sound_twiddle.play()
                            while(1):
                                wait_event = pygame.event.wait()
                                if wait_event.type == pygame.KEYDOWN:
                                    if wait_event.key == pygame.K_SPACE:
                                        
                                        break
                                    else:
                                        pass

                            if status_screen() == False:
                                break



                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:

                    level_list = os.listdir('Levels')
                    file_number = 0
                    new_level_set = False

                    
                    while(1):
                        wait_event = pygame.event.wait()
                        if wait_event.type == pygame.KEYDOWN:
                            if wait_event.key == pygame.K_RETURN:                             
                                break
                            elif wait_event.key == pygame.K_DOWN:
                                file_number += 1
                                if file_number > len(level_list) - 1:
                                    file_number = len(level_list) - 1
                            elif wait_event.key == pygame.K_UP:
                                file_number -= 1
                                if file_number < 0:
                                    file_number = 0
                            elif wait_event.key == pygame.K_n:
                                new_level_set = True
                                break
                            else:
                                pass
                            
                        screen.fill(game_state.bg_col)
                        render_text("Edit which level set?", 220)
                        render_text(level_list[file_number][:-4], 250)
                        render_text("or press N for new", 310)
                        pygame.display.flip()

                    pygame.mixer.music.stop()
                    
                    if new_level_set == True:
                        new_level_name = ""
                        while(1):

                            screen.fill(game_state.bg_col)
                            render_text("Input name:", 220)
                            render_text(new_level_name, 250)
                            pygame.display.flip()
 
                            wait_event = pygame.event.wait()
                            if wait_event.type == pygame.KEYDOWN:
                                if wait_event.key == pygame.K_RETURN:                             
                                    break
                                elif wait_event.key == pygame.K_BACKSPACE:                             
                                    new_level_name = new_level_name[:-1]
                                else:
                                    new_level_name += wait_event.unicode
################################################ Set definitions for map set
                        temp_list = os.listdir('Defs')
                        def_list = []
                        for item in temp_list:
                            if item[-3:] == '.py':
                                def_list.append(item)
                        def_file_number = 0
                                    
                        while(1):
                            wait_event = pygame.event.wait()
                            if wait_event.type == pygame.KEYDOWN:
                                if wait_event.key == pygame.K_RETURN:                             
                                    break
                                elif wait_event.key == pygame.K_DOWN:
                                    def_file_number += 1
                                    if def_file_number > len(def_list) - 1:
                                        def_file_number = len(def_list) - 1
                                elif wait_event.key == pygame.K_UP:
                                    def_file_number -= 1
                                    if def_file_number < 0:
                                        def_file_number = 0
                                else:
                                    pass
                          
                            screen.fill(game_state.bg_col)
                            render_text("Use which rule definitions?", 220)
                            render_text(def_list[def_file_number][:-3], 250)
                            pygame.display.flip()
#################################################                                      
                        game_data = Game_Data()

                        game_data.def_file = def_list[def_file_number]

                        load_defs(game_data.def_file[:-3])
                        
                        pygame.key.set_repeat(500, 100)
                        editor("Levels/" + new_level_name + ".lev")
                        pygame.key.set_repeat()
                    else:
                        data_file = open("Levels/" + level_list[file_number], "rb")
                        game_data = pickle.load(data_file)
                        data_file.close()

                        load_defs(game_data.def_file[:-3])
                        
                        pygame.key.set_repeat(500, 100)
                        editor("Levels/" + level_list[file_number])
                        pygame.key.set_repeat()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if game_state.play_music:
                        game_state.play_music = False
                        pygame.mixer.music.stop()
                    else:
                        game_state.play_music = True
                        pygame.mixer.music.play(-1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    key_names = ['right', 'left', 'up', 'down', 'use']

                    for key_no in range(5):
                            
                        screen.fill(game_state.bg_col)
                        render_text("Press key for " + key_names[key_no], 220)
                        pygame.display.flip()

                        while(1):
                            wait_event = pygame.event.wait()
                            if wait_event.type == pygame.KEYDOWN:
                                game_state.keys[key_no] = wait_event.key
                                break


                      


        if program_quit == True:

            #Save preferences
            prefs_file = open('CTprefs', "wb")
            pickle.dump([game_state.keys, game_state.play_music], prefs_file)
            prefs_file.close()
            
            break

    pygame.quit ()



if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        tb = sys.exc_info()[2]
        traceback.print_exception(e.__class__, e, tb)
    pygame.quit()
