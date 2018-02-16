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

import pygame
from CTfns import *

game_state = None

def init_defs(gs):
    global game_state
    game_state = gs

default_message = 'Grab those frogs!'

game_sprites = [0,
                pygame.image.load("Images/wall2.png"),
                pygame.image.load("Images/smiley.png"),
                pygame.image.load("Images/frog.png"),
                pygame.image.load("Images/box.png"),
                pygame.image.load("Images/chopper.png"),
                pygame.image.load("Images/transporter.png"),
                pygame.image.load("Images/grass.png"),
                pygame.image.load("Images/transporter2.png"),
                pygame.image.load("Images/transporter3.png"),
                pygame.image.load("Images/frog_down.png"),
                pygame.image.load("Images/frog_back1.png"),
                pygame.image.load("Images/frog_back2.png"),
                pygame.image.load("Images/frog_side1.png"),
                pygame.image.load("Images/frog_side2.png"),
                pygame.image.load("Images/frog_side3.png"),
                pygame.image.load("Images/frog_side4.png"),
                pygame.image.load("Images/red_frog.png"),
                pygame.image.load("Images/red_frog_down.png"),
                pygame.image.load("Images/red_frog_back1.png"),
                pygame.image.load("Images/red_frog_back2.png"),
                pygame.image.load("Images/red_frog_side1.png"),
                pygame.image.load("Images/red_frog_side2.png"),
                pygame.image.load("Images/red_frog_side3.png"),
                pygame.image.load("Images/red_frog_side4.png"),
                pygame.image.load("Images/button_on.png"),
                pygame.image.load("Images/button_off.png"),
                pygame.image.load("Images/gate.png"),
                pygame.image.load("Images/apple.png"),
                pygame.image.load("Images/turret_vert_on.png"),
                pygame.image.load("Images/turret_horiz_on.png"),
                0,0,
                pygame.image.load("Images/laser_vert.png"),
                pygame.image.load("Images/laser_horiz.png"),
                pygame.image.load("Images/key.png"),
                pygame.image.load("Images/lock.png"),
                pygame.image.load("Images/bush.png"),
                pygame.image.load("Images/wall3.png"),
                pygame.image.load("Images/wall4.png"),
                pygame.image.load("Images/rock.png")]

game_sprites[31] = pygame.transform.flip(game_sprites[29], False, True)
game_sprites[32] = pygame.transform.flip(game_sprites[30], True, False)

class Thing:

    gobject = 1
    name = 0
    sprite = 1
    x = y = 0
    solid = True
    squash = False
    ignore = False
    h_push = False
    v_push = False
    moving = 0
    being_moved_into = 0
    moved = 0
    forward = 1
    backward = 3
    left = 4
    right = 2
    move_counter = 0
    move_speed = 0
    is_dave = False
    empty = False
    needs_target = False
    target = 0
    animation = 0
    anim_frame = 0
    anim_timer = 0
    trigger_button = False
    solid_to_red_frog = True
    break_box = False

    startle_frog = False

    def hit(self, hitby):
        return

    def action(self):
        return

    def check_squash(self, obj):
        return self.squash

class Dave(Thing):
    gobject = 0
    is_dave = True
    name = 'Dave'
    startle_frog = True
    trigger_button = True
    solid_to_red_frog = False

# Dave action function called once per loop, so you can put goal checks and things in here
    def action(self):
        if game_state.min_score_hit:
            game_state.message = 'Get to the Chopper!'
            col_a, col_b, col_c = game_state.bg_col
            if game_state.bg_col[0] < 255:
                col_a += 2
                if col_a > 255:
                    col_a = 255
            if game_state.bg_col[1] < 220:
                col_b += 2
                if col_b > 220:
                    col_b = 220
            if game_state.bg_col[2] > 150:
                col_c -= 2
                if col_c < 150:
                    col_c = 150
            game_state.bg_col = col_a, col_b, col_c
            
class Blank(Thing):
    def __init__(self):
        self.gobject = 0
        self.name = 'Blank'
        self.sprite = 0
        self.solid = False
        self.squash = True
        self.empty = True

        self.solid_to_red_frog = False

class Wall(Thing):
    def __init__(self):
        self.break_box = True
        self.name = 'Wall'

class Smiley(Thing):    
    def __init__(self):
        self.gobject = 2
        self.name = 'Smiley'
        self.sprite = 2
        self.h_push = True
        self.v_push = True
        self.move_speed = 2
        self.trigger_button = True
        self.break_box = True
        
    def action(self):
        x = self.x
        y = self.y
        
        if self.moving > 0 or self.moved:
            self.startle_frog = True
        else:
            self.startle_frog = False

        if self.moved > 0:
            #if look(self.moved, x, y).empty or look(self.moved, x, y).name == 'Frog' or look(self.moved, x, y).name == 'Startled_Frog' \
            #                                or look(self.moved, x, y).name == 'Red_Frog' or look(self.moved, x, y).name == 'Angry_Red_Frog'\
            #                                or look(self.moved, x, y).name == 'Transporter' or look(self.moved, x, y).name == 'Laser':
            if look(self.moved, x, y).empty or look(self.moved, x, y).name in ['Frog','Startled_Frog','Red_Frog','Angry_Red_Frog','Transporter','Laser']:
                move(self.moved, self, x, y)
            if look(self.moved, x, y).name == 'Box':
                create('Frog', self.moved, x, y)

        return

class Calm_Frog(Thing):
    def __init__(self):
        self.gobject = 3
        self.name = 'Frog'
        self.sprite = 3
        self.animation = [(3, 100), (13, 10), (15, 10)]
        self.solid = False
        #self.squash = True

    def hit(self, hitby):
    
        if hitby.is_dave:
            game_state.score +=1


    def action(self):
        x = self.x
        y = self.y
        
        if look(game_state.NORTH, x, y).startle_frog or look(game_state.SOUTH, x, y).startle_frog \
           or look(game_state.EAST, x, y).startle_frog or look(game_state.WEST, x, y).startle_frog:
            create('Startled_Frog', 0, x, y)

    def check_squash(self, obj):
        if obj.name in ['Box', 'Chopper', 'Key']:
            return False
        else:
            return True

class Startled_Frog(Thing):
    def __init__(self):
        self.gobject = 4
        self.name = 'Startled_Frog'
        self.sprite = 10
        self.solid = False
        #self.squash = True
        self.startle_frog = True
        self.trigger_button = True
        
        self.move_speed = 1

    def hit(self, hitby):
        if hitby.is_dave:
            game_state.score +=1

    def action(self):
        x = self.x
        y = self.y
        
        if look(self.left, x, y).empty:
            move(self.left, self, x, y)
        elif look(self.forward, x, y).empty:
            move(self.forward, self, x, y)
        elif look(self.right, x, y).empty:
            move(self.right, self, x, y)
        elif look(self.backward, x, y).empty:
            move(self.backward, self, x, y)

        if self.forward == game_state.NORTH:
            self.animation = [(11, 8), (12, 8)]
        elif self.forward == game_state.EAST:
            self.animation = [(15, 4), (16, 8)]
        elif self.forward == game_state.SOUTH:
            self.animation = [(3, 8), (10, 8)]
        elif self.forward == game_state.WEST:
            self.animation = [(13, 4), (14, 8)]
            
    def check_squash(self, obj):
        if obj.name in ['Box', 'Chopper', 'Key']:
            return False
        else:
            return True


class Box(Thing):
    def __init__(self):
        self.gobject = 5
        self.name = 'Box'
        self.sprite = 4
        self.h_push = True
        self.v_push = True
        self.move_speed = 1

    #def hit(self, hitby, x, y):
    #    if hitby.gobject == 2:
    #        create("Frog", 0, x, y)

    def action(self):
        x = self.x
        y = self.y
        
        #if dave_is_to(game_state.SOUTH, x, y):
        #if look(game_state.SOUTH, x, y).is_dave:
        #    if game_state.use_key == True:
        #        create('Smiley', game_state.NORTH, x, y)
        if self.moving > 0 or self.moved:
            self.startle_frog = True
        else:
            self.startle_frog = False
            
        if self.moved == game_state.SOUTH and look(game_state.SOUTH, x, y).break_box == True:
            create('Frog', 0, x, y)
            
        if look(game_state.SOUTH, x, y).empty == True:
            move(game_state.SOUTH, self, x, y)



class Chopper(Thing):
    def __init__(self):
        self.gobject = 6
        self.name = 'Chopper'
        self.sprite = 5
        self.h_push = True
        self.v_push = True
        self.move_speed = 1

#    def hit(self, hitby, x, y):
#        change('Box', 'Frog')

    def hit(self, hitby):
        if hitby.is_dave and game_state.min_score_hit:
            game_state.level_finished = True
            
        
    def action(self):
        if game_state.min_score_hit:        
            self.solid = False

class Transporter(Thing):
    def __init__(self):
        self.gobject = 7
        self.name = 'Transporter'
        self.sprite = 6
        self.animation = [(6, 4), (8, 4), (9, 4)]
        self.solid = False
        self.needs_target = True
        self.squash = True

    def hit(self, hitby):
        x = self.x
        y = self.y
        

        transport(hitby, self, x, y)
        
# Keep this part in for regenerating transporters
        create("Transporter", 0, x, y)
        game_state.game_map[x][y].target = self.target

class Grass(Thing):
    def __init__(self):
        self.gobject = 8
        self.sprite = 7
        self.solid = False
        
class Red_Frog(Thing):
    def __init__(self):
        self.name = 'Red_Frog'
        self.gobject = 9
        self.sprite = 17
        self.solid = False
        self.squash = True

    def action(self):
        x = self.x
        y = self.y
        

        if look(game_state.NORTH, x, y).startle_frog or look(game_state.SOUTH, x, y).startle_frog \
           or look(game_state.EAST, x, y).startle_frog or look(game_state.WEST, x, y).startle_frog:
            create('Angry_Red_Frog', 0, x, y)

    def check_squash(self, obj):
        if obj.name in ['Box', 'Chopper', 'Key']:
            return False
        else:
            return True

class Angry_Red_Frog(Thing):
    def __init__(self):
        self.name = 'Angry_Red_Frog'
        self.gobject = 10
        self.sprite = 18
        self.animation = [(17, 8), (18, 8)]
        self.solid = False
        self.squash = True
        self.move_speed = 1
        self.startle_frog = True
        self.trigger_button = True

    def action(self):
        x = self.x
        y = self.y
        

        if look(self.forward, x, y).name == 'Apple' and look(self.forward, x, y).being_moved_into == 0:
            look(self.forward, x, y).eat()
            return
        if look(self.left, x, y).name == 'Apple' and look(self.left, x, y).being_moved_into == 0:
            look(self.left, x, y).eat()
            return
        if look(self.backward, x, y).name == 'Apple' and look(self.backward, x, y).being_moved_into == 0:
            look(self.backward, x, y).eat()
            return
        if look(self.right, x, y).name == 'Apple' and look(self.right, x, y).being_moved_into == 0:
            look(self.right, x, y).eat()
            return
        
        if dave_is_to(game_state.NORTH, x, y):
            if look(game_state.NORTH, x, y).solid_to_red_frog == False and look(game_state.NORTH, x, y).being_moved_into == 0:
                move(game_state.NORTH, self, x, y)
                self.animation = [(19, 8), (20, 8)]
        if dave_is_to(game_state.SOUTH, x, y):
            if look(game_state.SOUTH, x, y).solid_to_red_frog == False and look(game_state.SOUTH, x, y).being_moved_into == 0:
                move(game_state.SOUTH, self, x, y)
                self.animation = [(17, 8), (18, 8)]
        if dave_is_to(game_state.EAST, x, y):
            if look(game_state.EAST, x, y).solid_to_red_frog == False and look(game_state.EAST, x, y).being_moved_into == 0:
                move(game_state.EAST, self, x, y)
                self.animation = [(23, 8), (24, 8)]
        if dave_is_to(game_state.WEST, x, y):
            if look(game_state.WEST, x, y).solid_to_red_frog == False and look(game_state.WEST, x, y).being_moved_into == 0:
                move(game_state.WEST, self, x, y)
                self.animation = [(21, 8), (22, 8)]

    def hit(self, hitby):
        if hitby.is_dave:
            game_state.kill_dave = True

    def check_squash(self, obj):
        if obj.name in ['Box', 'Chopper', 'Key']:
            return False
        else:
            return True

class Button_On(Thing):
    def __init__(self):
        self.gobject = 11
        self.sprite = 25
        self.needs_target = True
        self.target = (0,0)
        self.initialise = True
        self.break_box = True
        

        

    def action(self):
        x = self.x
        y = self.y
        
        if self.initialise == True:
            self.initialise = False
            if look(0, self.target[0], self.target[1]).name == 'Gate':
                self.sprite = 25
            else:
                self.sprite = 26
                
        if (look(game_state.NORTH, x, y).trigger_button == True or look(game_state.SOUTH, x, y).trigger_button == True or \
           look(game_state.EAST, x, y).trigger_button == True or look(game_state.WEST, x, y).trigger_button == True):
            if look(0, self.target[0], self.target[1]).empty == True and look(0, self.target[0], self.target[1]).is_dave == False \
               or look(0, self.target[0], self.target[1]).name == 'Laser':
                create('Gate', 0, self.target[0], self.target[1])
                self.sprite = 25
        else:
            if look(0, self.target[0], self.target[1]).name == 'Gate':
                create('Blank', 0, self.target[0], self.target[1])
                self.sprite = 26

class Button_Off(Thing):
    def __init__(self):
        self.gobject = 12
        self.sprite = 26
        self.needs_target = True
        self.break_box = True

    def action(self):
        x = self.x
        y = self.y
        
        if (look(game_state.NORTH, x, y).trigger_button == True or look(game_state.SOUTH, x, y).trigger_button == True or \
           look(game_state.EAST, x, y).trigger_button == True or look(game_state.WEST, x, y).trigger_button == True):
            if look(0, self.target[0], self.target[1]).name == 'Gate':
                create('Blank', 0, self.target[0], self.target[1])
                self.sprite = 25
        else:
            if (look(0, self.target[0], self.target[1]).empty == True and look(0, self.target[0], self.target[1]).is_dave == False) \
               or look(0, self.target[0], self.target[1]).name == 'Laser':
                create('Gate', 0, self.target[0], self.target[1])
                self.sprite = 26

class Gate(Thing):
    def __init__(self):
        self.gobject = 13
        self.name = 'Gate'
        self.sprite = 27
        self.break_box = True

class Apple(Thing):
    def __init__(self):
        self.gobject = 14
        self.name = 'Apple'
        self.sprite = 28
        self.h_push = True
        self.move_speed = 4
        self.life = 60

    def action(self):
        x = self.x
        y = self.y
        
        if self.moving > 0 or self.moved:
            self.startle_frog = True
        else:
            self.startle_frog = False
        
        if look(game_state.SOUTH, x, y).empty or look(game_state.SOUTH, x, y).name in ['Frog','Startled_Frog','Red_Frog','Angry_Red_Frog','Laser']:
            move(game_state.SOUTH, self, x, y)
                     
        elif look(game_state.SOUTH, x, y).name == 'Apple' and \
                 (look(game_state.SW, x, y).empty == True or look(game_state.SW, x, y).name in ['Frog','Startled_Frog','Red_Frog','Angry_Red_Frog','Laser']) and \
                 (look(game_state.WEST, x, y).empty == True or look(game_state.WEST, x, y).name in ['Frog','Startled_Frog','Red_Frog','Angry_Red_Frog','Laser']):
            move(game_state.WEST, self, x, y)

        elif look(game_state.SOUTH, x, y).name == 'Apple' and \
                 (look(game_state.SE, x, y).empty == True or look(game_state.SE, x, y).name in ['Frog','Startled_Frog','Red_Frog','Angry_Red_Frog','Laser']) and \
                 (look(game_state.EAST, x, y).empty == True or look(game_state.EAST, x, y).name in ['Frog','Startled_Frog','Red_Frog','Angry_Red_Frog','Laser']):
            move(game_state.EAST, self, x, y)

        if self.moved == game_state.SOUTH and look(game_state.SOUTH, x, y).is_dave:
            game_state.kill_dave = True

    def eat(self):

        self.life -= 1
        if self.life < 0:
            create('Blank', 0, self.x, self.y)

class Turret_N(Thing):
    def __init__(self):
        self.gobject = 15
        self.name = 'Turret_N'
        self.sprite = 29

    def action(self):
        if look(game_state.NORTH, self.x, self.y).name not in ['Wall', 'Smiley', 'Gate', 'Laser', 'Lock', 'Turret_N', 'Turret_S', 'Turret_E', 'Turret_W']:

            create('Laser', game_state.NORTH, self.x, self.y)
            look(game_state.NORTH, self.x, self.y).forward = game_state.NORTH
            #look(game_state.NORTH, self.x, self.y).backward = game_state.SOUTH
            #look(game_state.NORTH, self.x, self.y).left = game_state.WEST
            #look(game_state.NORTH, self.x, self.y).right = game_state.EAST

class Turret_E(Thing):
    def __init__(self):
        self.gobject = 16
        self.name = 'Turret_E'
        self.sprite = 30

    def action(self):
        if look(game_state.EAST, self.x, self.y).name not in ['Wall', 'Smiley', 'Gate', 'Laser', 'Lock', 'Turret_N', 'Turret_S', 'Turret_E', 'Turret_W']:

            create('Laser', game_state.EAST, self.x, self.y)
            look(game_state.EAST, self.x, self.y).forward = game_state.EAST
            look(game_state.EAST, self.x, self.y).sprite = 34

class Turret_S(Thing):
    def __init__(self):
        self.gobject = 17
        self.name = 'Turret_S'
        self.sprite = 31
        
    def action(self):
        if look(game_state.SOUTH, self.x, self.y).name not in ['Wall', 'Smiley', 'Gate', 'Laser', 'Lock', 'Turret_N', 'Turret_S', 'Turret_E', 'Turret_W']:

            create('Laser', game_state.SOUTH, self.x, self.y)
            look(game_state.SOUTH, self.x, self.y).forward = game_state.SOUTH
            
class Turret_W(Thing):
    def __init__(self):
        self.gobject = 18
        self.name = 'Turret_W'
        self.sprite = 32

    def action(self):
        if look(game_state.WEST, self.x, self.y).name not in ['Wall', 'Smiley', 'Gate', 'Laser', 'Lock', 'Turret_N', 'Turret_S', 'Turret_E', 'Turret_W']:

            create('Laser', game_state.WEST, self.x, self.y)
            look(game_state.WEST, self.x, self.y).forward = game_state.WEST
            look(game_state.WEST, self.x, self.y).sprite = 34
            
class Laser(Thing):
    def __init__(self):
        self.gobject = 19
        self.name = 'Laser'
        self.sprite = 33
        self.squash = True
        self.solid = False

    def hit(self, hitby):
        if hitby.is_dave:
            game_state.kill_dave = True

    def action(self):
        if self.forward == game_state.NORTH:
            if (look(game_state.SOUTH, self.x, self.y).name == 'Turret_N' or \
               (look(game_state.SOUTH, self.x, self.y).name == 'Laser' and look(game_state.SOUTH, self.x, self.y).forward == game_state.NORTH)):
                if look(game_state.NORTH, self.x, self.y).name not in ['Wall', 'Smiley', 'Gate', 'Laser', 'Lock', 'Turret_N', 'Turret_S', 'Turret_E', 'Turret_W']:
                #if look(game_state.NORTH, self.x, self.y).name != 'Wall' and look(game_state.NORTH, self.x, self.y).name != 'Smiley' \
                #   and look(game_state.NORTH, self.x, self.y).name != 'Gate' and look(game_state.NORTH, self.x, self.y).name != 'Laser'\
                #   and look(game_state.NORTH, self.x, self.y).name != 'Lock':
                    create('Laser', game_state.NORTH, self.x, self.y)
                    look(game_state.NORTH, self.x, self.y).forward = game_state.NORTH
            else:
                create('Blank', 0, self.x, self.y)
                return
                            
        elif self.forward == game_state.EAST:
            self.ignore = True
            if (look(game_state.WEST, self.x, self.y).name == 'Turret_E' or \
               (look(game_state.WEST, self.x, self.y).name == 'Laser' and look(game_state.WEST, self.x, self.y).forward == game_state.EAST)):
                if look(game_state.EAST, self.x, self.y).name not in ['Wall', 'Smiley', 'Gate', 'Laser', 'Lock', 'Turret_N', 'Turret_S', 'Turret_E', 'Turret_W']:
                    create('Laser', game_state.EAST, self.x, self.y)
                    look(game_state.EAST, self.x, self.y).forward = game_state.EAST
                    look(game_state.EAST, self.x, self.y).sprite = 34
                    look(game_state.EAST, self.x, self.y).ignore = True
            else:
                create('Blank', 0, self.x, self.y)
                
                
        elif self.forward == game_state.SOUTH:
            self.ignore = True
            if (look(game_state.NORTH, self.x, self.y).name == 'Turret_S' or \
               (look(game_state.NORTH, self.x, self.y).name == 'Laser' and look(game_state.NORTH, self.x, self.y).forward == game_state.SOUTH)):
                if look(game_state.SOUTH, self.x, self.y).name not in ['Wall', 'Smiley', 'Gate', 'Laser', 'Lock', 'Turret_N', 'Turret_S', 'Turret_E', 'Turret_W']:
                    create('Laser', game_state.SOUTH, self.x, self.y)
                    look(game_state.SOUTH, self.x, self.y).forward = game_state.SOUTH
                    look(game_state.SOUTH, self.x, self.y).ignore = True
            else:
                create('Blank', 0, self.x, self.y)
                
        elif self.forward == game_state.WEST:
            if (look(game_state.EAST, self.x, self.y).name == 'Turret_W' or \
               (look(game_state.EAST, self.x, self.y).name == 'Laser' and look(game_state.EAST, self.x, self.y).forward == game_state.WEST)):
                if look(game_state.WEST, self.x, self.y).name not in ['Wall', 'Smiley', 'Gate', 'Laser', 'Lock', 'Turret_N', 'Turret_S', 'Turret_E', 'Turret_W']:
                    create('Laser', game_state.WEST, self.x, self.y)
                    look(game_state.WEST, self.x, self.y).forward = game_state.WEST
                    look(game_state.WEST, self.x, self.y).sprite = 34
            else:
                create('Blank', 0, self.x, self.y)

class Key(Thing):
    def __init__(self):
        self.gobject = 20
        self.name = 'Key'
        self.sprite = 35
        self.h_push = True
        self.v_push = True
        self.move_speed = 1

class Lock(Thing):
    def __init__(self):
        self.gobject = 21
        self.name = 'Lock'
        self.sprite = 36

    def hit(self, hitby):
        create('Blank', 0, self.x, self.y)

    def check_squash(self, obj):
        if obj.name == 'Key':
            return True
        else:
            return False

class Bush(Thing):
    def __init__(self):
        self.gobject = 22
        self.sprite = 37

    def action(self):
        if game_state.player_moving == 0 and (look(game_state.NORTH, self.x, self.y).is_dave or look(game_state.SOUTH, self.x, self.y).is_dave or\
                                              look(game_state.WEST, self.x, self.y).is_dave or look(game_state.EAST, self.x, self.y).is_dave)\
                                         and game_state.use_key == True:
            create('Blank', 0, self.x, self.y)


class Wall2(Thing):
    def __init__(self):
        self.break_box = True
        self.sprite = 38
        self.name = 'Wall'

class Wall3(Thing):
    def __init__(self):
        self.break_box = True
        self.sprite = 39
        self.name = 'Wall'

class Rock(Thing):
    def __init__(self):
        self.break_box = True
        self.sprite = 40
        self.name = 'Wall'
#################################

game_objects = [Blank(),    # Leave Blank where it is
                Wall(),     # There must be a Wall object for the unseen outer wall
                Smiley(),
                Calm_Frog(),
                Startled_Frog(),
                Box(),
                Chopper(),
                Transporter(),
                Grass(),
                Red_Frog(),
                Angry_Red_Frog(),
                Button_On(),
                Button_Off(),
                Gate(),
                Apple(),
                Turret_N(),
                Turret_E(),
                Turret_S(),
                Turret_W(),
                Laser(),
                Key(),
                Lock(),
                Bush(),
                Wall2(),
                Wall3(),
                Rock()]

#################################

