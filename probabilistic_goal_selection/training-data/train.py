#!/usr/bin/python

# This is incomplete, but could be developed further to convert the CSV file
# into training data for the PSL program

from optparse import OptionParser
import sys

usage = "usage: python %s [options] <input training data file> <output player file> <output exit file> <output monster file>" % sys.argv[0]
parser = OptionParser(usage=usage)
parser.add_option("-q", "--quiet", dest="q", action="store_true", default=False, help="Quiet logging output [false]")
(opt, args) = parser.parse_args()

if len(args) < 4:
    print usage
    sys.exit(-1)

v = not opt.q

infile = open(args[0],'r')
pfile = open(args[1],'w')
efile = open(args[2],'w')
mfile = open(args[3],'w')

board = 100
entity = 1
while(True):
    try:
        for row in range(1,4):
            line = infile.readline().strip()
            #print line
            cols = line.split(',')
            (c1, c2, c3) = map(lambda col: "_" if col=="" else col, cols)
            if v: print "%d: %s %s %s" % (row, c1, c2, c3)
            pfile.write("%d\t%d%d\n" % (entity, row, 1))
            entity += 1
            pfile.write("%d\t%d,%d\n" % (entity, row, 2))
            entity += 1
            pfile.write("%d\t%d,%d\n" % (entity, row, 3))
            entity += 1

        (label,_,_) = infile.readline().strip().split(',')
        if v: print"label:%s\n" % label
        infile.readline()
        board += 1
    except Exception as arg:
        print arg
        break

infile.close()
pfile.close()
efile.close()
