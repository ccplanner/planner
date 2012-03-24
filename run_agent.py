#!/usr/bin/python2
# For running planner

import pddlagent as pa
import tworld

last_pos = None
last_move = None
skiped_moves = 0
def wrapper_agent():
    '''A wrapper agent that has memory, to deal with fast ticks'''
    global last_pos, last_move, skiped_moves
    if skiped_moves >= 4 or tworld.chips_pos() != last_pos:
        skiped_moves = 0
        if tworld.get_tile( *tworld.chips_pos() )[1] == tworld.Ice:
            return tworld.WAIT
        last_pos= tworld.chips_pos()
        last_move=pa.pddl_agent()
    else:
        skiped_moves += 1
    return last_move

tworld.set_agent( wrapper_agent )
#tworld.load_level('classical.dac',20)
tworld.load_level('easy.dac',20)
