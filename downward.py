#!/usr/bin/python2

import os
from time import time

var = "FAST_DOWNWARD_HOME"
if var not in os.environ:
    raise Exception("Please set the environment variable %s as the path to the directory containing Fast Downward." % var)
FAST_DOWNWARD_HOME = os.environ[var]

def run( pddl):
    t0 = time()
    translate( pddl )
    t1 = time()
    print "translate took: %f sec" % ( t1 - t0)
    preprocess()
    t2 = time()
    print "preprocess took: %f sec" % ( t2 - t1)
    search()
    t3 = time()
    print "translate took: %f sec" % ( t3 - t2)
    print "total took: %f sec" % ( t3 - t0)
    return get_moves()


def translate( pddl, domain = 'pddl/domain.pddl', down_home=FAST_DOWNWARD_HOME):
    ''' run fast downward translate, produces output'''
#    os.remove('output')
#    os.remove('output.sas')
#    os.remove('sas_plan')
    os.system("%s/src/translate/translate.py %s %s" % (down_home, domain, pddl) )

def preprocess(sas='output.sas', down_home=FAST_DOWNWARD_HOME):
    ''' do the preporcess stuff'''
    os.system("%s/src/preprocess/preprocess < %s" % (down_home, sas) )

def search(heurestic = "astar(blind())", problem='output', down_home=FAST_DOWNWARD_HOME):
    ''' do the search'''
    os.system("""%s/src/search/downward --search "%s" < %s""" % (down_home, heurestic, problem) )

def get_moves(plan='sas_plan'):
    f = open(plan, 'r')
    lines = f.readlines()
    f.close()
    return lines

# run('pddl/cc-agent1.pddl')

