#!/usr/bin/python2

import tworld as tw
import random
import downward

def translate_move( move):
    '''translate a move for fast downward to tile world'''
    if "slip" in move:
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
    player-01 - player"""
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
            top, bot = tw.get_tile(i,j)
            if top == tw.Empty or top == tw.Exit or top == tw.HintButton:
                print >> out, "(floor pos-%d-%d)" % (i,j)
            elif top in (tw.HiddenWall_Perm, tw.HiddenWall_Temp, 
                         tw.BlueWall_Real, tw.BlueWall_Fake):
                print >> out, "(floor pos-%d-%d)" % (i,j)
            elif top == tw.Socket:
                print >> out, "(socket pos-%d-%d)" % (i,j)
            elif top in (tw.Chip_North, tw.Chip_West, tw.Chip_South, tw.Chip_East):
                print >> out, "(at player-01 pos-%d-%d)" % (i,j)
                if top == tw.Chip_East:
                    chip_dir = "dir-east"
                elif top == tw.Chip_West:
                    chip_dir = "dir-west"
                elif top == tw.Chip_South:
                    chip_dir = "dir-south"
                elif top == tw.Chip_North:
                    chip_dir = "dir-north"

                if bot == tw.Empty or bot == tw.Exit or bot == tw.HintButton:
                    print >> out, "(floor pos-%d-%d)" % (i,j)
                elif bot == tw.Wall:
                    print >> out, "(wall pos-%d-%d)" % (i,j)
                elif bot == tw.Ice:
                    print >> out, "(ice pos-%d-%d)" % (i,j)
                    print >> out, "(chip-state slipping)"
                    print >> out, "(slipping-dir %s)" % chip_dir
                elif top == tw.SwitchWall_Open or bot == tw.SwitchWall_Open:
                    print >> out, "(switch-wall-open pos-%d-%d)" % (i,j)
                elif top == tw.SwitchWall_Closed or bot == tw.SwitchWall_Closed:
                    print >> out, "(switch-wall-closed pos-%d-%d)" % (i,j)
                elif top == tw.Button_Green or bot == tw.Button_Green:
                    print >> out, "(green-button pos-%d-%d)" % (i,j)
            elif top == tw.ICChip:
                print >> out, "(chip pos-%d-%d)" % (i,j)
            elif top == tw.Wall:
                print >> out, "(wall pos-%d-%d)" % (i,j)
            elif top == tw.Water:
                print >> out, "(water pos-%d-%d)" % (i,j)
            elif top == tw.Fire:
                print >> out, "(fire pos-%d-%d)" % (i,j)
            elif top == tw.Ice:
                print >> out, "(ice pos-%d-%d)" % (i,j)
            elif top == tw.SwitchWall_Open or bot == tw.SwitchWall_Open:
                print >> out, "(switch-wall-open pos-%d-%d)" % (i,j)
            elif top == tw.SwitchWall_Closed or bot == tw.SwitchWall_Closed:
                print >> out, "(switch-wall-closed pos-%d-%d)" % (i,j)
            elif top == tw.Button_Green or bot == tw.Button_Green:
                print >> out, "(green-button pos-%d-%d)" % (i,j)
            if i != 0:
                print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-east)" % (i-1,j, i,j)
                print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-west)" % (i,j, i-1,j)
            if j != 0:
                print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-south)" % (i,j-1, i,j)
                print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-north)" % (i,j, i,j-1)

def produce_goal( out ):
    ''' product locations'''
    print >> out, "(:goal "
    for i in range( 32 ):
        for j in range( 32 ):
            top, bot = tw.get_tile(i,j)
            if top == tw.Exit :
                print >> out, "(at player-01 pos-%d-%d)" % (i,j)
    print >> out, ")"
