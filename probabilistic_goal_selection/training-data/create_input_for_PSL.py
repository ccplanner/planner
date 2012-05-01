#!/usr/bin/python

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
while(True):
    try:
        locations = []
        for row in range(1,4):
            line = infile.readline().strip()
            cols = line.split(',')
            (c1, c2, c3) = map(lambda col: "_" if col=="" else col, cols)
            if v: print "%d: %s %s %s" % (row, c1, c2, c3)
            for c in cols:
                locations.append(c)
        (label,_,_) = infile.readline().strip().split(',')
        if v: print"label:%s" % label
        infile.readline()
        i = 1
        for loc in locations:
            if loc == 'p':
                pfile.write("%d\t%d\n" % (board,i))
            elif loc == 'e':
                efile.write("%d\t%d\n" % (board,i))
            elif loc == 'm':
                mfile.write("%d\t%d\n" % (board,i))
            i += 1

        board += 1
    except Exception as arg:
        print "got exception so stopping: %s" % arg
        break

infile.close()
pfile.close()
efile.close()
mfile.close()
