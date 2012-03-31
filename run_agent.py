#!/usr/bin/python2
# For running planner

import pddlagent as pa
import tworld

agent = pa.cacheing_pddl_agent()

class wrapper_agent:
    def __init__(self, get_move_func ):
        self.last_pos = None
        self.last_move = None
        self.skiped_moves = 0
        self.wrapped_get_move = get_move_func

    def get_move(self):
        '''A wrapper agent that has memory, to deal with fast ticks'''
        if self.skiped_moves >= 4 or tworld.chips_pos() != self.last_pos:
            self.skiped_moves = 0
            if tworld.get_tile( *tworld.chips_pos() )[1] == tworld.Ice:
                return tworld.WAIT
            self.last_pos= tworld.chips_pos()
            #last_move=pa.pddl_agent()
            self.last_move=agent.get_move()
        else:
            self.skiped_moves += 1
        return self.last_move

#wagent = wrapper_agent( pa.pddlagent )
wagent = wrapper_agent( agent.get_move )
tworld.set_agent( wagent.get_move )
tworld.load_level('classical.dac',1)
#tworld.load_level('CCLP3.dac',5)
#tworld.load_level('keys.dac',1)
