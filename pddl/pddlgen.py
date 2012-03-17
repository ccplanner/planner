#!/usr/bin/python2

def proc_text( text ):
	return map( proc_line, map( list, text.splitlines() ))

def proc_line( line):
	'''process a line recursivelly'''
	if len( line) >= 2:
		return [line[:2]] + proc_line(line[2:] )
	if len( line) == 1:
		return [[line[0], ' ']]
	if len( line) == 0:
		return []

def produce_problem( board, chips ):
	print """(define (problem p01-cc)
	  (:domain chips-challenge)
	  """
	produce_objects( board, chips )
	produce_init( board, chips)
	produce_goal( board)
	print ")"

def produce_objects( board, chips ):
	print """(:objects
	dir-down - direction
	dir-left - direction
	dir-right - direction
	dir-up - direction
	player-01 - player"""
	produce_numbers( chips )
	produce_locations( board )
	print ")"

def produce_numbers( num ):
	for n in range( num + 1):
		print "n%d - number" % n

def produce_init( board, chips ):
	print """(:init"""
	print "(chips-left n%d)" % chips
	produce_succesors( chips) 
	produce_predicates(board )
	print ")"

def produce_succesors( num ):
	for n in range( num ):
		print "(successor n%d n%d)" % (n, n+1)

def produce_locations( board ):
	''' product locations'''
	for i in range( len(board) ):
		for j in range( len(board[i] ) ):
			print "pos-%d-%d - location" % (i,j )

def produce_predicates( board ):
	''' product locations'''
	for i in range( len(board) ):
		for j in range( len(board[i] ) ):
			top, bot = board[i][j]
			if top == ' ' or top =='E' or top== '?':
				print "(floor pos-%d-%d)" % (i,j)
			elif top == 'H':
				print "(socket pos-%d-%d)" % (i,j)
			elif top == '@':
				print "(floor pos-%d-%d)" % (i,j)
				print "(at player-01 pos-%d-%d)" % (i,j)
			elif top == '$':
				print "(chip pos-%d-%d)" % (i,j)
			elif top == '#':
				print "(wall pos-%d-%d)" % (i,j)
			elif top == ',':
				print "(water pos-%d-%d)" % (i,j)
			elif top == '&':
				print "(fire pos-%d-%d)" % (i,j)
			elif top == 'A':
				print "(blue-key pos-%d-%d)" % (i,j)
			elif top == 'B':
				print "(red-key pos-%d-%d)" % (i,j)
			elif top == 'C':
				print "(yellow-key pos-%d-%d)" % (i,j)
			elif top == 'D':
				print "(blue-door pos-%d-%d)" % (i,j)
			elif top == 'F':
				print "(red-door pos-%d-%d)" % (i,j)
			elif top == 'G':
				print "(green-door pos-%d-%d)" % (i,j)
			elif top == 'I':
				print "(yellow-door pos-%d-%d)" % (i,j)
			elif top == 'J':
				print "(green-key pos-%d-%d)" % (i,j)
			if i != 0:
				print "(MOVE-DIR pos-%d-%d pos-%d-%d dir-down)" % (i-1,j, i,j)
				print "(MOVE-DIR pos-%d-%d pos-%d-%d dir-up)" % (i,j, i-1,j)
			if j != 0:
				print "(MOVE-DIR pos-%d-%d pos-%d-%d dir-right)" % (i,j-1, i,j)
				print "(MOVE-DIR pos-%d-%d pos-%d-%d dir-left)" % (i,j, i,j-1)

def produce_goal( board ):
	''' product locations'''
	print "(:goal "
	for i in range( len(board) ):
		for j in range( len(board[i] ) ):
			top, bot = board[i][j]
			if top =='E' :
				print "(at player-01 pos-%d-%d)" % (i,j)
	print ")"

easy = """# # # # # # # # #
# @ #   # E H   #
#   #   # # #   #
#   #   #       #
#         #     #
# # # #   #   # #
#         #     #
#   # #       # #
# # # # # # # # #
"""

chips_x = """# # # # # # # # #
# E # $ #   $   #
# H #   #   #   #
# @             #
#   # # # #     #
#   # $         #
#   # # # #     #
#               #
# # # # # # # # #
"""

pie="""# # # # # # # # #
# @       $ # $ #
#   # # # # # # #
#   #   H E     #
#   #   # # #   #
#   #           #
# $     #   # # #
# $     # $ # $ #
# # # # # # # # #
"""

chips = """# # # # # # # # #
# E # $ #   $   #
# H #   #   #   #
# @             #
#   # # # #     #
#   # $         #
#   # # # #     #
#               #
# # # # # # # # #
"""

hazard="""# # # # # # # # #
# @         , $ #
#   , , ,       #
#   & E H   ,   #
#   & & &   ,   #
#               #
#   &   & & &   #
# $ &     $ & $ #
# # # # # # # # #
"""

hints="""# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # @ # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # ? # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # $ # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # H # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # E # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""

#A	blue key
#B	red key
#C	yellow key
#D	blue door
#F	red door
#G	green door
#I	yellow door
#J	green key

keys="""# # # # # # # # #
# # $ # $ # A $ #
# # B # C #     #
# # D # F #     #
# @             #
# # G # I # G # #
# #   # J #   H #
# # $ # $ # H E #
# # # # # # # # #
"""

#produce_problem( proc_text(easy), 0 )
#produce_problem( proc_text(chips), 3 )
#produce_problem( proc_text(pie), 5 )
produce_problem( proc_text(hazard), 4 )
#produce_problem( proc_text(hints), 0 )
#produce_problem( proc_text(keys), 5 )

