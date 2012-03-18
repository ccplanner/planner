#!/usr/bin/python2
# For running planner

import pddlagent as pa
import tworld
tworld.set_agent( pa.pddl_agent )
tworld.load_level('classical.dac',1)
