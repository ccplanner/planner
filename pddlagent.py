#!/usr/bin/python2

import tworld as tw
import random
import downward
import ast
import os
import re
import config as cfg
from stateworld import StateWorld

verbose = False

class cacheing_pddl_agent:

    def __init__(self):
        self.moves=[] # list of moves to carry out moves.pop() is next move
        self.tick = 0
        self.state = StateWorld()
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
        self.state.write_pddl(pddl_file)
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
