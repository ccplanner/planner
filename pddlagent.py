#!/usr/bin/python2

import tworld as tw
import random
import downward
import ast
import os
import re
import config as cfg

verbose = False

class cacheing_pddl_agent:

    def __init__(self):
        self.moves=[] # list of moves to carry out moves.pop() is next move
        self.tick = 0
        global verbose
        verbose = cfg.opts.pddl_agent_verbose

    def get_move(self):
        """return a move"""
        if verbose: print "agent (move requested)"
        if verbose: print "agent (printing game status prior to move)"
        if verbose: print_game_status()
        self.tick += 1
        if len( self.moves ) > 0:
            move = self.moves.pop()
            if verbose: print "agent (cached move: %s)" % translate_tw_move(move)
            return move
        if verbose: print "agent (no cached moves)" 
        pddl_file_name = 'pddl/cc-agent%d.pddl' % self.tick
        pddl_file = open( pddl_file_name, 'w')
        produce_problem(pddl_file)
        pddl_file.close()
        if verbose:
            pddl_file = open( pddl_file_name, 'r')
            print "agent (printing problem PDDL, but skipping moves and walls and such)"
            depth = 0
            for line in pddl_file: 
                if re.search(r"^\(MOVE-DIR|^\(floor pos-|^pos-.*location$|^\(wall pos.*\)$", line) is None: 
                    opens = len(re.findall(r"\(",line))
                    closes = len(re.findall(r"\)",line))
                    if line.strip() != "": print "  " + ("  " * depth) + line.strip()
                    depth += opens - closes
            pddl_file.close()
        # get moves and translate them
        if verbose: print "agent (running planner)" 
        self.moves= map( translate_move, downward.run( pddl_file_name ))
        if verbose: print "agent (moves from planner: %s)" % map( translate_tw_move, self.moves)
        self.moves.reverse() # reverse to that moves.pop() returns next move
        move = self.moves.pop()
        if verbose: print "agent (move: %s)" % translate_tw_move(move)
        return move

def print_game_status():
    print "game (printing board, top tiles only)"
    print_board(9,9,False)
    x,y = tw.chips_pos()
    print "game (Keys R:%d B:%d Y:%d G:%d)" % tw.get_keys()
    print "game (Boots Ice:%d Suction:%d Fire:%d Water:%d)" % tw.get_boots()
    print "game (Player: %d,%d)" % (x, y)
    print "game (Chips left: %d)" % tw.chips_needed()

def print_board(x_max=32,y_max=32,print_bottom=True):
    """note x_max and y_max are then number of tiles printed in that 
        direction"""
    for y in range(y_max):
        print "  ", 
        for x in range(x_max):
            print "%2x|" % tw.get_tile(x,y)[0],
        print "\n",
        if print_bottom:
            print "  ",
            for x in range(x_max):
                print "%2x|" % tw.get_tile(x,y)[1],
            print "\n",

def translate_move( move):
    '''translate a move for fast downward to tile world'''
    if "slip" in move:
       return tw.WAIT
    if "slide-force-force" in move: # don't move when slide to preserve free move
       return tw.WAIT
    if "west" in move:
       return tw.WEST
    if "east" in move:
       return tw.EAST
    if "south" in move:
       return tw.SOUTH
    if "north" in move:
       return tw.NORTH
    assert "should never get here"

def translate_tw_move( move):
    '''translate a move for tile world to fast downward'''
    if move == tw.WAIT:
        return "wait (slip?)"
    if move == tw.WEST:
        return "west"
    if move == tw.EAST:
        return "east"
    if move == tw.SOUTH:
        return "south"
    if move == tw.NORTH:
        return "north"
    assert "should never get here"

tick = 0;
def pddl_agent():
    """Called by tile world to get a move"""
    global tick
    tick += 1
    pddl_file_name = 'pddl/cc-agent%d.pddl' % tick
    pddl_file = open( pddl_file_name, 'w')
    produce_problem(pddl_file)
    pddl_file.close()
    move_1= downward.run( pddl_file_name )[0]
    return translate_move( move_1 )

def produce_problem( out ):
    """produce the pddle for the board in it's current state"""
    print >> out, """(define (problem p01-%d-cc)
      (:domain chips-challenge)
      """ % tick
    max_num = tw.chips_needed() + 5
    produce_objects( out, max_num)
    produce_init( out, max_num)
    produce_goal( out)
    print >> out, ")"

def produce_objects( out, max_num ):
    print >> out, """(:objects
    dir-east - direction
    dir-north - direction
    dir-south - direction
    dir-west - direction
    red - color
    blue - color
    yellow - color
    green - color
    water - type
    fire - type
    ice - type
    slide - type
    """
    produce_numbers( out, max_num )
    produce_locations( out, 32, 32 )
    print >> out, ")"

def produce_numbers( out, num ):
    for n in range( num + 1):
        print >> out, "n%d - number" % n

def produce_locations( out, x_max, y_max ):
    ''' product locations'''
    for i in range( x_max ):
        for j in range( y_max ):
            print >> out, "pos-%d-%d - location" % (i,j )

def produce_init( out, max_num ):
    """Produce intial state"""
    print >> out, """(:init"""
    print >> out, "(chips-left n%d)" % tw.chips_needed()
    print >> out, "(switched-walls-open n0)" 
    print >> out, "(has-keys red n%d)" % tw.get_keys()[0] 
    print >> out, "(has-keys blue n%d)" % tw.get_keys()[1]
    print >> out, "(has-keys yellow n%d)" % tw.get_keys()[2]
    print >> out, "(has-keys green n%d)" % tw.get_keys()[3]
    if tw.get_boots()[0]: # ICE
	print >> out, "(has-boots ice)"
    if tw.get_boots()[1]: # SUCTION
	print >> out, "(has-boots slide)"
    if tw.get_boots()[2]: # FIRE
	print >> out, "(has-boots fire)"
    if tw.get_boots()[3]: # WATER
	print >> out, "(has-boots water)"
    produce_succesors(out, max_num) 
    produce_predicates(out, 32, 32)
    print >> out, ")"

def produce_succesors(out, num ):
    ''' Procude the successor prediciates up to num'''
    for n in range( num ):
        print >> out, "(successor n%d n%d)" % (n, n+1)

def produce_predicates( out, x_max, y_max ):
    ''' produce locations'''
    for i in range( x_max ):
        for j in range( y_max ):
            ################
            # TODO: improve this logic to be more readable
            # and maintinable
            #################
            treat_as_floor = (tw.Empty, tw.Exit, tw.HintButton, tw.Wall_North, tw.Wall_South, 
                            tw.Wall_East, tw.Wall_West, tw.Wall_Southeast)
            top, bot = tw.get_tile(i,j)
            if top in treat_as_floor:
                print >> out, "(floor pos-%d-%d)" % (i,j)
            elif top in (tw.HiddenWall_Perm, tw.HiddenWall_Temp, 
                         tw.BlueWall_Real, tw.BlueWall_Fake):
                print >> out, "(floor pos-%d-%d)" % (i,j)
            elif top == tw.Socket:
                print >> out, "(socket pos-%d-%d)" % (i,j)
            elif top in (tw.Chip_North, tw.Chip_West, tw.Chip_South, tw.Chip_East):
                print >> out, "(at pos-%d-%d)" % (i,j)
                if top == tw.Chip_East:
                    chip_dir = "dir-east"
                elif top == tw.Chip_West:
                    chip_dir = "dir-west"
                elif top == tw.Chip_South:
                    chip_dir = "dir-south"
                elif top == tw.Chip_North:
                    chip_dir = "dir-north"

                if bot in treat_as_floor:
                    print >> out, "(floor pos-%d-%d)" % (i,j)
                elif bot == tw.Wall:
                    print >> out, "(wall pos-%d-%d)" % (i,j)
                elif bot == tw.Ice:
                    print >> out, "(ice pos-%d-%d)" % (i,j)
                    print >> out, "(chip-state slipping)"
                    print >> out, "(slipping-dir %s)" % chip_dir
                elif bot == tw.SwitchWall_Open:
                    print >> out, "(switch-wall-open pos-%d-%d)" % (i,j)
                elif bot == tw.SwitchWall_Closed:
                    print >> out, "(switch-wall-closed pos-%d-%d)" % (i,j)
                elif bot == tw.Button_Green:
                    print >> out, "(green-button pos-%d-%d)" % (i,j)
                elif bot in (tw.Slide_North, tw.Slide_South, tw.Slide_East, tw.Slide_West):
                    print >> out, "(force-floor pos-%d-%d)" % (i,j)
                    print >> out, "(chip-state sliding)" #note not slipping
                    if bot == tw.Slide_North:
                        print >> out, "(slide-dir pos-%d-%d dir-north)" % (i,j)
                    elif bot == tw.Slide_South:
                        print >> out, "(slide-dir pos-%d-%d dir-south)" % (i,j)
                    elif bot == tw.Slide_East:
                        print >> out, "(slide-dir pos-%d-%d dir-east)" % (i,j)
                    elif bot == tw.Slide_West:
                        print >> out, "(slide-dir pos-%d-%d dir-west)" % (i,j)
            elif top == tw.ICChip:
                print >> out, "(chip pos-%d-%d)" % (i,j)
            elif top in (tw.Slide_North, tw.Slide_South, tw.Slide_East, tw.Slide_West):
                print >> out, "(force-floor pos-%d-%d)" % (i,j)
                if top == tw.Slide_North:
                    print >> out, "(slide-dir pos-%d-%d dir-north)" % (i,j)
                elif top == tw.Slide_South:
                    print >> out, "(slide-dir pos-%d-%d dir-south)" % (i,j)
                elif top == tw.Slide_East:
                    print >> out, "(slide-dir pos-%d-%d dir-east)" % (i,j)
                elif top == tw.Slide_West:
                    print >> out, "(slide-dir pos-%d-%d dir-west)" % (i,j)
            elif top == tw.Key_Red:
                print >> out, "(key pos-%d-%d red)" % (i,j)
            elif top == tw.Key_Blue:
                print >> out, "(key pos-%d-%d blue)" % (i,j)
            elif top == tw.Key_Yellow:
                print >> out, "(key pos-%d-%d yellow)" % (i,j)
            elif top == tw.Key_Green:
                print >> out, "(key pos-%d-%d green)" % (i,j)
            elif top == tw.Door_Red:
                print >> out, "(door pos-%d-%d red)" % (i,j)
            elif top == tw.Door_Blue:
                print >> out, "(door pos-%d-%d blue)" % (i,j)
            elif top == tw.Door_Yellow:
                print >> out, "(door pos-%d-%d yellow)" % (i,j)
            elif top == tw.Door_Green:
                print >> out, "(door pos-%d-%d green)" % (i,j)
            elif top == tw.Boots_Water:
                print >> out, "(boots pos-%d-%d water)" % (i,j)
            elif top == tw.Boots_Fire:
                print >> out, "(boots pos-%d-%d fire)" % (i,j)
            elif top == tw.Boots_Ice:
                print >> out, "(boots pos-%d-%d ice)" % (i,j)
            elif top == tw.Boots_Slide:
                print >> out, "(boots pos-%d-%d slide)" % (i,j)
            elif top == tw.Wall:
                print >> out, "(wall pos-%d-%d)" % (i,j)
            elif top == tw.Water:
                print >> out, "(water pos-%d-%d)" % (i,j)
            elif top == tw.Fire:
                print >> out, "(fire pos-%d-%d)" % (i,j)
            elif top == tw.PopupWall:
                print >> out, "(popup-wall pos-%d-%d)" % (i,j)                
            elif top == tw.Dirt:
                print >> out, "(dirt pos-%d-%d)" % (i, j)                
            elif top == tw.Burglar:
                print >> out, "(thief pos-%d-%d)" % (i, j)
            elif top == tw.Block_Static: #todo block north/etc
                print >> out, "(block pos-%d-%d)" % (i, j)
            elif top == tw.Bomb:
                print >> out, "(bomb pos-%d-%d)" % (i, j)
            elif top == tw.Gravel:
                print >> out, "(floor pos-%d-%d)" % (i, j)
                print >> out, "(gravel pos-%d-%d)" % (i, j)
            elif top == tw.Ice:
                print >> out, "(ice pos-%d-%d)" % (i,j)
            elif top in (tw.IceWall_Northeast, tw.IceWall_Northwest, tw.IceWall_Southeast, tw.IceWall_Southwest):
                print >> out, "(ice-wall pos-%d-%d)" % (i,j)
                if top == tw.IceWall_Northeast: # Open North and East
                    # slip in going south slip out going east
                    print >> out, "(ice-wall-dir pos-%d-%d dir-south dir-east)" % (i,j)
                    print >> out, "(ice-wall-dir pos-%d-%d dir-west dir-north)" % (i,j)
                elif top == tw.IceWall_Northwest: # Open North and West
                    print >> out, "(ice-wall-dir pos-%d-%d dir-south dir-west)" % (i,j)
                    print >> out, "(ice-wall-dir pos-%d-%d dir-east dir-north)" % (i,j)
                elif top == tw.IceWall_Southeast: # Open South and East
                    print >> out, "(ice-wall-dir pos-%d-%d dir-north dir-east)" % (i,j)
                    print >> out, "(ice-wall-dir pos-%d-%d dir-west dir-south)" % (i,j)
                elif top == tw.IceWall_Southwest: # Open South and West
                    print >> out, "(ice-wall-dir pos-%d-%d dir-north dir-west)" % (i,j)
                    print >> out, "(ice-wall-dir pos-%d-%d dir-east dir-south)" % (i,j)
            elif top == tw.SwitchWall_Open or bot == tw.SwitchWall_Open:
                print >> out, "(switch-wall-open pos-%d-%d)" % (i,j)
            elif top == tw.SwitchWall_Closed or bot == tw.SwitchWall_Closed:
                print >> out, "(switch-wall-closed pos-%d-%d)" % (i,j)
            elif top == tw.Button_Green or bot == tw.Button_Green:
                print >> out, "(green-button pos-%d-%d)" % (i,j)
            # set up movement
            if i != 0 and can_move_east_west(tw.get_tile(i-1,j),tw.get_tile(i,j)) :
                print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-east)" % (i-1,j, i,j)
                print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-west)" % (i,j, i-1,j)
            if j != 0 and can_move_north_south(tw.get_tile(i,j-1), tw.get_tile(i,j) ):
                print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-south)" % (i,j-1, i,j)
                print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-north)" % (i,j, i,j-1)

def can_move_east_west( (w_top, w_bot), (e_top, e_bot) ):
    """ if movement east to west is possible"""
    if both_walls( (w_top, w_bot), (e_top, e_bot) ):
        return False
    # west does not have a blocking tile
    # IceWall_Southwest is open to the south and west
    if  set((w_top, w_bot)).isdisjoint( (tw.Wall_East, tw.IceWall_Southwest, tw.IceWall_Northwest, tw.Wall_Southeast) ) and \
        set( (e_top, e_bot)).isdisjoint( (tw.Wall_West, tw.IceWall_Southeast, tw.IceWall_Northeast) ):
        return True
    else:
        return False

def can_move_north_south( n_tile, s_tile ):
    """ if movement north to south is possible n_tile and s_tile are (top, bot) tuples"""
    if both_walls( n_tile, s_tile ):
        return False
    # IceWall_Northeast is open to the north and east
    if  set( n_tile).isdisjoint( (tw.Wall_South, tw.IceWall_Northeast, tw.IceWall_Northwest, tw.Wall_Southeast) ) and \
        set( s_tile).isdisjoint( (tw.Wall_North, tw.IceWall_Southeast, tw.IceWall_Southwest) ):
        return True
    else:
        return False

def both_walls( (a_top, a_bot), (b_top, b_bot) ):
    """ if both a and b are walls movement between is impossible"""
    return (a_top == tw.Wall or a_bot == tw.Wall ) and \
           (b_bot == tw.Wall or b_bot == tw.Wall )

def produce_goal( out ):
    ''' product locations'''
    print >> out, "(:goal "
    for i in range( 32 ):
        for j in range( 32 ):
            top, bot = tw.get_tile(i,j)
            if top == tw.Exit :
                print >> out, "(at pos-%d-%d)" % (i,j)
    print >> out, ")"
