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

default_message = 'Go get them gems!'

game_sprites = [0,
                pygame.image.load("Images/wall2.png"),
                pygame.image.load("Images/Arrows/ArrowLeft.png"),
                pygame.image.load("Images/Arrows/ArrowRight.png"),
                pygame.image.load("Images/Arrows/ArrowUp.png"),
                pygame.image.load("Images/Arrows/ArrowDown.png"),
                pygame.image.load("Images/Arrows/Gem.png"),]

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
    #gobject = 0
    is_dave = True
    name = 'Dave'
    startle_frog = True
    trigger_button = True
    solid_to_red_frog = False

# Dave action function called once per loop, so you can put goal checks and things in here
    def action(self):
        if game_state.min_score_hit:
            game_state.level_finished = True

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

class Arrow_Left(Thing):
    def __init__(self):
        self.sprite = 2
        self.move_speed = 1

    def action(self):
        if look(game_state.WEST, self.x, self.y).empty == True:
            move(game_state.WEST, self, self.x, self.y)

class Arrow_Right(Thing):
    def __init__(self):
        self.sprite = 3
        self.move_speed = 1

    def action(self):
        if look(game_state.EAST, self.x, self.y).empty == True:
            move(game_state.EAST, self, self.x, self.y)

class Arrow_Up(Thing):
    def __init__(self):
        self.sprite = 4
        self.move_speed = 1

    def action(self):
        if look(game_state.NORTH, self.x, self.y).empty == True:
            move(game_state.NORTH, self, self.x, self.y)

class Arrow_Down(Thing):
    def __init__(self):
        self.sprite = 5
        self.move_speed = 1

    def action(self):
        if look(game_state.SOUTH, self.x, self.y).empty == True:
            move(game_state.SOUTH, self, self.x, self.y)

class Gem(Thing):
    def __init__(self):
        self.sprite = 6
        self.solid = False

    def hit(self, hitby):

        if hitby.is_dave:
            game_state.score +=1

#################################

game_objects = [Blank(),    # Leave Blank where it is
                Wall(),     # There must be a Wall object for the unseen outer wall
                Arrow_Left(),
                Arrow_Right(),
                Arrow_Up(),
                Arrow_Down(),
                Gem()]

#################################
