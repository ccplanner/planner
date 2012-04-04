#!/usr/bin/python2
# For running planner

from __future__ import division
import pddlagent as pa
import tworld
import time
import sys
import config
from optparse import OptionParser

DEFAULT_LEVEL_SET="classical.dac"

usage = "usage: python %s [options] file" % sys.argv[0]
parser = OptionParser(usage=usage)
parser.add_option("-l", "--level", dest="level_num", type="int",
        help="specify the level number to play [1]", metavar="NUMBER", default=1)
parser.add_option("","--pddl-agent-verbose", action="store_true", dest="pddl_agent_verbose", 
        default=False, help="print extra log messages from the PDDL agent [false]")
parser.add_option("","--fast-downward-quiet", action="store_true",dest="fast_downward_quiet", 
        default=False, help="print Fast Downward status messages to a log instead of stdout [false]")
parser.add_option("","--fast-downward-log", dest="fast_downward_log", default="fd.log", metavar="FILE",
        help="specify log file where Fast Downward status messages should go instead of stdout [fd.log]")
(options, args) = parser.parse_args()
config.opts = options # Save to use in other modules
    
if len(args) > 0:
    level_set = args[0] 
else:
    print usage
    print "playing %s, the default level set, since no level set was specified" % DEFAULT_LEVEL_SET
    level_set = DEFAULT_LEVEL_SET

agent = pa.cacheing_pddl_agent()

class wrapper_agent:
    def __init__(self, get_move_func ):
        self.last_pos = None
        self.last_move = None
        self.skiped_moves = 0
        self.wrapped_get_move = get_move_func

    def get_move(self):
        '''A wrapper agent that has memory, to deal with fast ticks'''
	time.sleep( 1 / 20) # each tick is 1/20th of second
        try:
            if self.skiped_moves >= 4 or tworld.chips_pos() != self.last_pos:
                self.skiped_moves = 0
                if tworld.get_tile( *tworld.chips_pos() )[1] == tworld.Ice:
                    return tworld.WAIT
                self.last_pos= tworld.chips_pos()
                self.last_move=agent.get_move()
            else:
                self.skiped_moves += 1
            return self.last_move
        except Exception, e:
            print "EXCEPTION:"
            print e
            print "giving up and exiting, but you can try another level"
            sys.exit()

#wagent = wrapper_agent( pa.pddlagent )
wagent = wrapper_agent( agent.get_move )
tworld.set_agent( wagent.get_move )

tworld.load_level(level_set, options.level_num)
