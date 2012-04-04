#!/usr/bin/python2

import os
from time import time
import config as cfg

var = "FAST_DOWNWARD_HOME"
if var not in os.environ:
    raise Exception("Please set the environment variable %s as the path to the directory containing Fast Downward." % var)
FAST_DOWNWARD_HOME = os.environ[var]

def run( pddl):
    for fpath in ["output","output.sas","sas_plan","elapsed.time","plan_numbers_and_cost"]:
        if os.path.exists(fpath):
            os.remove(fpath)
    t0 = time()
    translate( pddl )
    t1 = time()
    print "FD translate took: %f sec" % ( t1 - t0)
    preprocess()
    t2 = time()
    print "FD preprocess took: %f sec" % ( t2 - t1)
    search()
    t3 = time()
    print "FD search took: %f sec" % ( t3 - t2)
    print "FD total took: %f sec" % ( t3 - t0)
    return get_moves()


def translate( pddl, domain = 'pddl/domain.pddl', down_home=FAST_DOWNWARD_HOME):
    ''' run fast downward translate, produces output'''
    code = os.system("%s/src/translate/translate.py %s %s" % (down_home, domain, pddl) 
            + (""">> %s""" % cfg.opts.fast_downward_log if cfg.opts.fast_downward_quiet else ""))
    if code != 0:
        raise Exception("FD translate did not terminate normally")

def preprocess(sas='output.sas', down_home=FAST_DOWNWARD_HOME):
    ''' do the preporcess stuff'''
    code = os.system("%s/src/preprocess/preprocess < %s" % (down_home, sas) 
            + (""">> %s""" % cfg.opts.fast_downward_log if cfg.opts.fast_downward_quiet else ""))
    if code != 0:
        raise Exception("FD preprocess did not terminate normally")

def search(heurestic = "astar(blind())", problem='output', down_home=FAST_DOWNWARD_HOME):
    ''' do the search'''
    code = os.system("""%s/src/search/downward --search "%s" < %s""" % (down_home, heurestic, problem) 
            + (""">> %s""" % cfg.opts.fast_downward_log if cfg.opts.fast_downward_quiet else ""))
    if code != 0:
        raise Exception("FD search did not terminate normally")

def get_moves(plan='sas_plan'):
    try:
        f = open(plan, 'r')
    except Exception, e:
        print e
        raise Exception("planner output file %s doesn't exist, which means the planner cannot solve this level" % plan)

    lines = f.readlines()
    f.close()
    return lines

