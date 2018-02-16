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

import pygame, copy

game_state = None
game_objects = None
Dave = None
Wall = None

def fn_init_defs(gs, go, dv, wl):
    global game_state, game_objects, Dave, Wall
    game_state = gs
    game_objects = go
    Dave = dv
    Wall = wl

def look(direction, x, y):

    if direction == game_state.EAST:
        if x < game_state.LEVEL_WIDTH - 1:

            if game_state.game_map[x+1][y].gobject > 0:
                
                return game_state.game_map[x+1][y]
            
            elif (game_state.dave_x, game_state.dave_y) == (x+1, y) or \
                 (game_state.dave_dest_x, game_state.dave_dest_y) == (x+1, y):
                
                return Dave()
                
            else:
                return game_state.game_map[x+1][y]
        else:
            return Wall()

    if direction == game_state.WEST:
        if x > 0:

            if game_state.game_map[x-1][y].gobject > 0:
                
                return game_state.game_map[x-1][y]
            
            elif (game_state.dave_x, game_state.dave_y) == (x - 1, y) or \
                 (game_state.dave_dest_x, game_state.dave_dest_y) == (x - 1, y):

                return Dave()
                
            else:
                return game_state.game_map[x-1][y]
        else:
            return Wall()

    if direction == game_state.NORTH:
        if y > 0:

            if game_state.game_map[x][y-1].gobject > 0:
                
                return game_state.game_map[x][y-1]
            
            elif (game_state.dave_x, game_state.dave_y) == (x, y - 1) or \
                 (game_state.dave_dest_x, game_state.dave_dest_y) == (x, y - 1):

                return Dave()
                
            else:
                return game_state.game_map[x][y-1]
        else:
            return Wall()
    
    if direction == game_state.SOUTH:
        if y < game_state.LEVEL_HEIGHT - 1:

            if game_state.game_map[x][y+1].gobject > 0:
                
                return game_state.game_map[x][y+1]
            
            elif (game_state.dave_x, game_state.dave_y) == (x, y + 1) or \
                 (game_state.dave_dest_x, game_state.dave_dest_y) == (x, y + 1):
                
                return Dave()
                
            else:
                return game_state.game_map[x][y+1]
        else:
            return Wall()

    if direction == game_state.NE:
        if y > 0 and x < game_state.LEVEL_WIDTH - 1:
            if game_state.game_map[x+1][y-1].gobject > 0:
                
                return game_state.game_map[x+1][y-1]
            
            elif (game_state.dave_x, game_state.dave_y) == (x+1, y - 1) or \
                 (game_state.dave_dest_x, game_state.dave_dest_y) == (x+1, y - 1):

                return Dave()
                
            else:
                return game_state.game_map[x+1][y-1]
        else:
            return Wall()

    if direction == game_state.SE:
        if y < game_state.LEVEL_HEIGHT - 1 and x < game_state.LEVEL_WIDTH - 1:
            if game_state.game_map[x+1][y+1].gobject > 0:
                
                return game_state.game_map[x+1][y+1]
            
            elif (game_state.dave_x, game_state.dave_y) == (x+1, y + 1) or \
                 (game_state.dave_dest_x, game_state.dave_dest_y) == (x+1, y + 1):

                return Dave()
                
            else:
                return game_state.game_map[x+1][y+1]
        else:
            return Wall()

    if direction == game_state.SW:
        if y < game_state.LEVEL_HEIGHT - 1 and x > 0:
            if game_state.game_map[x-1][y+1].gobject > 0:
                
                return game_state.game_map[x-1][y+1]
            
            elif (game_state.dave_x, game_state.dave_y) == (x-1, y + 1) or \
                 (game_state.dave_dest_x, game_state.dave_dest_y) == (x-1, y + 1):

                return Dave()
                
            else:
                return game_state.game_map[x-1][y+1]
        else:
            return Wall()

    if direction == game_state.NW:
        if y > 0 and x > 0:
            if game_state.game_map[x-1][y-1].gobject > 0:
                
                return game_state.game_map[x-1][y-1]
            
            elif (game_state.dave_x, game_state.dave_y) == (x-1, y - 1) or \
                 (game_state.dave_dest_x, game_state.dave_dest_y) == (x-1, y - 1):

                return Dave()
                
            else:
                return game_state.game_map[x-1][y-1]
        else:
            return Wall() 
# If none of the above
    #return game_state.game_map[x][y]   
    if game_state.game_map[x][y].gobject > 0:
        
        return game_state.game_map[x][y]
    
    elif (game_state.dave_x, game_state.dave_y) == (x, y) or \
         (game_state.dave_dest_x, game_state.dave_dest_y) == (x, y):
        
        return Dave()
        
    else:
        return game_state.game_map[x][y]


def move(direction, obj, x, y):
    if obj.moving == 0:
        if direction == game_state.NORTH:
            
            obj.moving = game_state.NORTH

            if game_state.game_map[x][y-1].being_moved_into > 0:

                hitting_object = game_state.game_map[x][y-1]
                
                if game_state.game_map[x][y-1].being_moved_into == game_state.EAST:
                    game_state.game_map[x][y-1] = game_state.game_map[x+1][y-1]
                    game_state.game_map[x][y-1].moving = 0
                    game_state.game_map[x][y-1].x = x
                    game_state.game_map[x][y-1].y = y-1
                    game_state.game_map[x+1][y-1] = copy.deepcopy(game_objects[0])
                    
                if game_state.game_map[x][y-1].being_moved_into == game_state.WEST:
                    game_state.game_map[x][y-1] = game_state.game_map[x-1][y-1]
                    game_state.game_map[x][y-1].moving = 0
                    game_state.game_map[x][y-1].x = x
                    game_state.game_map[x][y-1].y = y-1
                    game_state.game_map[x-1][y-1] = copy.deepcopy(game_objects[0])

                if game_state.game_map[x][y-1].being_moved_into == game_state.NORTH:
                    game_state.game_map[x][y-1] = game_state.game_map[x][y-2]
                    game_state.game_map[x][y-1].moving = 0
                    game_state.game_map[x][y-1].x = x
                    game_state.game_map[x][y-1].y = y-1
                    game_state.game_map[x][y-2] = copy.deepcopy(game_objects[0])

                hitting_object.hit(game_state.game_map[x][y-1])

            # Only set certain flags if space is blank
            if game_state.game_map[x][y-1].gobject == 0:
                game_state.game_map[x][y-1].solid = obj.solid
                game_state.game_map[x][y-1].squash = obj.squash
                game_state.game_map[x][y-1].name = obj.name
                
            game_state.game_map[x][y-1].empty = False
            game_state.game_map[x][y-1].being_moved_into = game_state.SOUTH
            #game_state.game_map[x][y-1].sprite = 1
            game_state.game_map[x][y-1].move_speed = 0
            obj.forward = game_state.NORTH
            obj.backward = game_state.SOUTH
            obj.left = game_state.WEST
            obj.right = game_state.EAST

        if direction == game_state.EAST:
            
            obj.moving = game_state.EAST

            if game_state.game_map[x+1][y].being_moved_into > 0:

                hitting_object = game_state.game_map[x+1][y]
                
                if game_state.game_map[x+1][y].being_moved_into == game_state.EAST:
                    game_state.game_map[x+1][y] = game_state.game_map[x+2][y]
                    game_state.game_map[x+1][y].moving  = 0
                    game_state.game_map[x+1][y].x = x+1
                    game_state.game_map[x+1][y].y = y
                    game_state.game_map[x+2][y] = copy.deepcopy(game_objects[0])

                if game_state.game_map[x+1][y].being_moved_into == game_state.NORTH:
                    game_state.game_map[x+1][y] = game_state.game_map[x+1][y-1]
                    game_state.game_map[x+1][y].moving  = 0
                    game_state.game_map[x+1][y].x = x+1
                    game_state.game_map[x+1][y].y = y
                    game_state.game_map[x+1][y-1] = copy.deepcopy(game_objects[0])

                if game_state.game_map[x+1][y].being_moved_into == game_state.SOUTH:
                    game_state.game_map[x+1][y] = game_state.game_map[x+1][y+1]
                    game_state.game_map[x+1][y].moving  = 0
                    game_state.game_map[x+1][y].x = x+1
                    game_state.game_map[x+1][y].y = y
                    game_state.game_map[x+1][y+1] = copy.deepcopy(game_objects[0])

                hitting_object.hit(game_state.game_map[x+1][y])

            if game_state.game_map[x+1][y].gobject == 0:
                game_state.game_map[x+1][y].solid = obj.solid
                game_state.game_map[x+1][y].squash = obj.squash
                game_state.game_map[x+1][y].name = obj.name
                
            game_state.game_map[x+1][y].empty = False
            game_state.game_map[x+1][y].being_moved_into = game_state.WEST
            #game_state.game_map[x+1][y].sprite = 1
            game_state.game_map[x+1][y].move_speed = 0
            obj.forward = game_state.EAST
            obj.backward = game_state.WEST
            obj.left = game_state.NORTH
            obj.right = game_state.SOUTH

        if direction == game_state.SOUTH:
            
            obj.moving = game_state.SOUTH

            if game_state.game_map[x][y+1].being_moved_into > 0:

                hitting_object = game_state.game_map[x][y+1]
                
                if game_state.game_map[x][y+1].being_moved_into == game_state.EAST:
                    game_state.game_map[x][y+1] = game_state.game_map[x+1][y+1]
                    game_state.game_map[x][y+1].moving = 0
                    game_state.game_map[x][y+1].x = x
                    game_state.game_map[x][y+1].y = y+1
                    game_state.game_map[x+1][y+1] = copy.deepcopy(game_objects[0])
                    
                if game_state.game_map[x][y+1].being_moved_into == game_state.WEST:
                    game_state.game_map[x][y+1] = game_state.game_map[x-1][y+1]
                    game_state.game_map[x][y+1].moving = 0
                    game_state.game_map[x][y+1].x = x
                    game_state.game_map[x][y+1].y = y+1
                    game_state.game_map[x-1][y+1] = copy.deepcopy(game_objects[0])

                if game_state.game_map[x][y+1].being_moved_into == game_state.SOUTH:
                    game_state.game_map[x][y+1] = game_state.game_map[x][y+2]
                    game_state.game_map[x][y+1].moving = 0
                    game_state.game_map[x][y+1].x = x
                    game_state.game_map[x][y+1].y = y+1
                    game_state.game_map[x][y+2] = copy.deepcopy(game_objects[0])

                hitting_object.hit(game_state.game_map[x][y+1])

            if game_state.game_map[x][y+1].gobject == 0:
                game_state.game_map[x][y+1].solid = obj.solid
                game_state.game_map[x][y+1].squash = obj.squash
                game_state.game_map[x][y+1].name = obj.name
                
            game_state.game_map[x][y+1].empty = False    
            game_state.game_map[x][y+1].being_moved_into = game_state.NORTH
            #game_state.game_map[x][y+1].sprite = 1
            game_state.game_map[x][y+1].move_speed = 0
            obj.forward = game_state.SOUTH
            obj.backward = game_state.NORTH
            obj.left = game_state.EAST
            obj.right = game_state.WEST

        if direction == game_state.WEST:
            
            obj.moving = game_state.WEST

            if game_state.game_map[x-1][y].being_moved_into > 0:

                hitting_object = game_state.game_map[x - 1][y]
                
                if game_state.game_map[x-1][y].being_moved_into == game_state.WEST:
                    game_state.game_map[x-1][y] = game_state.game_map[x-2][y]
                    game_state.game_map[x-1][y].moving = 0
                    game_state.game_map[x-1][y].x = x-1
                    game_state.game_map[x-1][y].y = y
                    game_state.game_map[x-2][y] = copy.deepcopy(game_objects[0])

                if game_state.game_map[x-1][y].being_moved_into == game_state.NORTH:
                    game_state.game_map[x-1][y] = game_state.game_map[x-1][y-1]
                    game_state.game_map[x-1][y].moving = 0
                    game_state.game_map[x-1][y].x = x-1
                    game_state.game_map[x-1][y].y = y
                    game_state.game_map[x-1][y-1] = copy.deepcopy(game_objects[0])

                if game_state.game_map[x-1][y].being_moved_into == game_state.SOUTH:
                    game_state.game_map[x-1][y] = game_state.game_map[x-1][y+1]
                    game_state.game_map[x-1][y].moving = 0
                    game_state.game_map[x-1][y].x = x-1
                    game_state.game_map[x-1][y].y = y
                    game_state.game_map[x-1][y+1] = copy.deepcopy(game_objects[0])

                hitting_object.hit(game_state.game_map[x - 1][y])

            if game_state.game_map[x-1][y].gobject == 0:
                game_state.game_map[x-1][y].solid = obj.solid
                game_state.game_map[x-1][y].squash = obj.squash
                game_state.game_map[x-1][y].name = obj.name
                
            game_state.game_map[x-1][y].empty = False
            game_state.game_map[x-1][y].being_moved_into = game_state.EAST
            #game_state.game_map[x-1][y].sprite = 1
            game_state.game_map[x-1][y].move_speed = 0
            obj.forward = game_state.WEST
            obj.backward = game_state.EAST
            obj.left = game_state.SOUTH
            obj.right = game_state.NORTH

def change(obj1, obj2):
    for x_counter in range(game_state.LEVEL_WIDTH):
        for y_counter in range(game_state.LEVEL_HEIGHT):
            if game_state.game_map[x_counter][y_counter].gobject == game_state.obj_names[obj1]:
                
                if game_state.game_map[x_counter][y_counter].moving:
                    if game_state.game_map[x_counter][y_counter].forward == game_state.NORTH:
                        game_state.game_map[x_counter][y_counter-1] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter-1].gobject])
                    elif game_state.game_map[x_counter][y_counter].forward == game_state.EAST:
                        game_state.game_map[x_counter+1][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter+1][y_counter].gobject])
                    elif game_state.game_map[x_counter][y_counter].forward == game_state.SOUTH:
                        game_state.game_map[x_counter][y_counter+1] = copy.deepcopy(game_objects[game_state.game_map[x_counter][y_counter+1].gobject])
                    elif game_state.game_map[x_counter][y_counter].forward == game_state.WEST:
                        game_state.game_map[x_counter-1][y_counter] = copy.deepcopy(game_objects[game_state.game_map[x_counter-1][y_counter].gobject])

                game_state.game_map[x_counter][y_counter] = copy.deepcopy(game_objects[game_state.obj_names[obj2]])
                game_state.game_map[x_counter][y_counter].x = x_counter
                game_state.game_map[x_counter][y_counter].y = y_counter

def dave_is_to(direction, x, y):
    if direction == game_state.NORTH:
        if y > game_state.dave_y:
            return True

    if direction == game_state.SOUTH:
        if y < game_state.dave_y:
            return True

    if direction == game_state.EAST:
        if x < game_state.dave_x:
            return True

    if direction == game_state.WEST:
        if x > game_state.dave_x:
            return True

    return False

def create(obj, direction, x, y):

    if direction == game_state.NORTH:
        dx = x
        dy = y - 1
    elif direction == game_state.SOUTH:
        dx = x
        dy = y + 1
    elif direction == game_state.EAST:
        dx = x + 1
        dy = y
    elif direction == game_state.WEST:
        dx = x - 1
        dy = y
    elif direction == game_state.NE:
        dx = x + 1
        dy = y - 1
    elif direction == game_state.SE:
        dx = x + 1
        dy = y + 1
    elif direction == game_state.SW:
        dx = x - 1
        dy = y + 1
    elif direction == game_state.NW:
        dx = x - 1
        dy = y - 1
    else:
        dx = x
        dy = y

    hitting_object = game_state.game_map[dx][dy]

#    if game_state.game_map[dx][dy].being_moved_into > 0:
#        
#        if game_state.game_map[dx][dy].being_moved_into == game_state.NORTH:
#            game_state.game_map[dx][dy] = game_state.game_map[dx][dy-1]
#            game_state.game_map[dx][dy].moving = 0
#            game_state.game_map[dx][dy-1] = copy.deepcopy(game_objects[0])
#            
#        if game_state.game_map[dx][dy].being_moved_into == game_state.EAST:
#            game_state.game_map[dx][dy] = game_state.game_map[dx+1][dy]
#            game_state.game_map[dx][dy].moving = 0
#            game_state.game_map[dx+1][dy] = copy.deepcopy(game_objects[0])
#            
#        if game_state.game_map[dx][dy].being_moved_into == game_state.SOUTH:
#            game_state.game_map[dx][dy] = game_state.game_map[dx][dy+1]
#            game_state.game_map[dx][dy].moving = 0
#            game_state.game_map[dx][dy+1] = copy.deepcopy(game_objects[0])
#            
#        if game_state.game_map[dx][dy].being_moved_into == game_state.WEST:
#            game_state.game_map[dx][dy] = game_state.game_map[dx-1][dy]
#            game_state.game_map[dx][dy].moving = 0
#            game_state.game_map[dx-1][dy] = copy.deepcopy(game_objects[0])
#
#        hitting_object.hit(game_state.game_map[dx][dy], dx, dy)
#
#        hitting_object = game_state.game_map[dx][dy]

    if hitting_object.moving:
        if hitting_object.forward == game_state.NORTH:
            #game_state.game_map[dx][dy - 1] = copy.deepcopy(game_objects[game_state.game_map[dx][dy - 1].gobject])
            reset_flags(dx, dy-1)
        elif hitting_object.forward == game_state.EAST:
            #game_state.game_map[dx+1][dy] = copy.deepcopy(game_objects[game_state.game_map[dx+1][dy].gobject])
            reset_flags(dx + 1, dy)
        elif hitting_object.forward == game_state.SOUTH:
            #game_state.game_map[dx][dy + 1] = copy.deepcopy(game_objects[game_state.game_map[dx][dy + 1].gobject])
            reset_flags(dx, dy+1)
        elif hitting_object.forward == game_state.WEST:
            #game_state.game_map[dx-1][dy] = copy.deepcopy(game_objects[game_state.game_map[dx-1][dy].gobject])
            reset_flags(dx - 1, dy)

            
    game_state.game_map[dx][dy] = copy.deepcopy(game_objects[game_state.obj_names[obj]])
    game_state.game_map[dx][dy].x = dx
    game_state.game_map[dx][dy].y = dy

    hitting_object.hit(game_state.game_map[dx][dy])

    game_state.game_map[dx][dy].being_moved_into = hitting_object.being_moved_into
    


def transport(hitby, tself, x, y):
    
        if hitby.is_dave:
        
            #font = pygame.font.Font(None, 35)
            #text = font.render('Transporting!', True, (255, 255, 255), (0, 0, 0))
            #text_rect = text.get_rect()
            #text_rect.centerx = screen.get_rect().centerx
            #text_rect.centery = screen.get_rect().centery
            
            #screen.blit(text, text_rect)
            #pygame.display.flip()

            game_state.transporting = True
            
            #pygame.time.wait(1000)
            game_state.dave_x = game_state.dave_dest_x = tself.target[0]
            game_state.dave_y = game_state.dave_dest_y = tself.target[1]
            
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

            Dave_hit()
            
        else:
            
            if game_state.game_map[tself.target[0]][tself.target[1]].being_moved_into > 0:
                
                if game_state.game_map[tself.target[0]][tself.target[1]].being_moved_into == game_state.NORTH:
                    game_state.game_map[tself.target[0]][tself.target[1]] = game_state.game_map[tself.target[0]][tself.target[1]-1]
                    game_state.game_map[tself.target[0]][tself.target[1]].moving = 0
                    game_state.game_map[tself.target[0]][tself.target[1]-1] = copy.deepcopy(game_objects[0])
                    
                if game_state.game_map[tself.target[0]][tself.target[1]].being_moved_into == game_state.EAST:
                    game_state.game_map[tself.target[0]][tself.target[1]] = game_state.game_map[tself.target[0]+1][tself.target[1]]
                    game_state.game_map[tself.target[0]][tself.target[1]].moving = 0
                    game_state.game_map[tself.target[0]+1][tself.target[1]] = copy.deepcopy(game_objects[0])
                    
                if game_state.game_map[tself.target[0]][tself.target[1]].being_moved_into == game_state.SOUTH:
                    game_state.game_map[tself.target[0]][tself.target[1]] = game_state.game_map[tself.target[0]][tself.target[1]+1]
                    game_state.game_map[tself.target[0]][tself.target[1]].moving = 0
                    game_state.game_map[tself.target[0]][tself.target[1]+1] = copy.deepcopy(game_objects[0])
                    
                if game_state.game_map[tself.target[0]][tself.target[1]].being_moved_into == game_state.WEST:
                    game_state.game_map[tself.target[0]][tself.target[1]] = game_state.game_map[tself.target[0]-1][tself.target[1]]
                    game_state.game_map[tself.target[0]][tself.target[1]].moving = 0
                    game_state.game_map[tself.target[0]-1][tself.target[1]] = copy.deepcopy(game_objects[0])
                    
            hitting_object = game_state.game_map[tself.target[0]][tself.target[1]]

            # Top line creates a new object, bottom line copies old one
            #game_state.game_map[tself.target[0]][tself.target[1]] = copy.deepcopy(game_objects[hitby.gobject])
            game_state.game_map[tself.target[0]][tself.target[1]] = copy.deepcopy(game_state.game_map[x][y])
            game_state.game_map[tself.target[0]][tself.target[1]].x = tself.target[0]
            game_state.game_map[tself.target[0]][tself.target[1]].y = tself.target[1]

            hitting_object.hit(game_state.game_map[tself.target[0]][tself.target[1]])

            if hitting_object.moving:
                if hitting_object.forward == game_state.NORTH:
                    #game_state.game_map[tself.target[0]][tself.target[1] - 1] = copy.deepcopy(game_objects[game_state.game_map[tself.target[0]][tself.target[1] - 1].gobject])
                    reset_flags(tself.target[0], tself.target[1] - 1)
                elif hitting_object.forward == game_state.EAST:
                    #game_state.game_map[tself.target[0]+1][tself.target[1]] = copy.deepcopy(game_objects[game_state.game_map[tself.target[0]+1][tself.target[1]].gobject])
                    reset_flags(tself.target[0]+1, tself.target[1])
                elif hitting_object.forward == game_state.SOUTH:
                    #game_state.game_map[tself.target[0]][tself.target[1] + 1] = copy.deepcopy(game_objects[game_state.game_map[tself.target[0]][tself.target[1] + 1].gobject])
                    reset_flags(tself.target[0], tself.target[1] + 1)
                elif hitting_object.forward == game_state.WEST:
                    #game_state.game_map[tself.target[0]-1][tself.target[1]] = copy.deepcopy(game_objects[game_state.game_map[tself.target[0]-1][tself.target[1]].gobject])
                    reset_flags(tself.target[0]-1, tself.target[1])

def reset_flags(x, y):
    game_state.game_map[x][y].solid = game_objects[game_state.game_map[x][y].gobject].solid
    game_state.game_map[x][y].squash = game_objects[game_state.game_map[x][y].gobject].squash
    game_state.game_map[x][y].name = game_objects[game_state.game_map[x][y].gobject].name
    game_state.game_map[x][y].empty = game_objects[game_state.game_map[x][y].gobject].empty
    game_state.game_map[x][y].being_moved_into = 0
    game_state.game_map[x][y].move_speed = game_objects[game_state.game_map[x][y].gobject].move_speed
    game_state.game_map[x][y].ignore = False


def Dave_hit():

    hitting_object = game_state.game_map[game_state.dave_x][game_state.dave_y]

    if game_state.game_map[game_state.dave_x][game_state.dave_y].moving:
        if game_state.game_map[game_state.dave_x][game_state.dave_y].forward == game_state.NORTH:
            #game_state.game_map[game_state.dave_x][game_state.dave_y-1] = copy.deepcopy(game_objects[game_state.game_map[game_state.dave_x][game_state.dave_y-1].gobject])
            reset_flags(game_state.dave_x, game_state.dave_y - 1)
            
        elif game_state.game_map[game_state.dave_x][game_state.dave_y].forward == game_state.EAST:
            #game_state.game_map[game_state.dave_x+1][game_state.dave_y] = copy.deepcopy(game_objects[game_state.game_map[game_state.dave_x+1][game_state.dave_y].gobject])
            reset_flags(game_state.dave_x + 1, game_state.dave_y)
            
        elif game_state.game_map[game_state.dave_x][game_state.dave_y].forward == game_state.SOUTH:
            #game_state.game_map[game_state.dave_x][game_state.dave_y+1] = copy.deepcopy(game_objects[game_state.game_map[game_state.dave_x][game_state.dave_y+1].gobject])
            reset_flags(game_state.dave_x, game_state.dave_y + 1)
            
        elif game_state.game_map[game_state.dave_x][game_state.dave_y].forward == game_state.WEST:
            #game_state.game_map[game_state.dave_x-1][game_state.dave_y] = copy.deepcopy(game_objects[game_state.game_map[game_state.dave_x-1][game_state.dave_y].gobject])
            reset_flags(game_state.dave_x - 1, game_state.dave_y)



    game_state.game_map[game_state.dave_x][game_state.dave_y] = copy.deepcopy(game_objects[0])

    hitting_object.hit(Dave())
