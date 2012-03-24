#!/usr/bin/python2

import os

var = "FAST_DOWNWARD_HOME"
if var not in os.environ:
    raise Exception("Please set the environment variable %s as the path to the directory containing Fast Downward." % var)
FAST_DOWNWARD_HOME = os.environ[var]

def run( pddl):
    translate( pddl )
    preprocess()
    search()
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

