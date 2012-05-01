#!/usr/bin/python

from optparse import OptionParser
import sys

usage = "usage: python %s [options] <input cells list file> <output spreadsheet file>" % sys.argv[0]
parser = OptionParser(usage=usage)
parser.add_option("-q", "--quiet", dest="q", action="store_true", default=False, help="Quiet logging output [false]")
(opt, args) = parser.parse_args()

if len(args) < 2:
    print usage
    sys.exit(-1)

v = not opt.q

infile = open(args[0],'r')
ofile = open(args[1],'w')


#cells = [None]*9
cells = [""]*9
#cells = []
board = 100
for line in infile:
    cols = line.strip().split(',')
    if cols[0] != board:
        board = cols[0]
        #print cells
        #print "%s,%s,%s" % cells[0:3]
        #print "%s,%s,%s" % (cells[3:6])
        #print "%s,%s,%s" % (cells[6:9])
        print "%s,%s,%s" % (cells[0], cells[1], cells[2])
        print "%s,%s,%s" % (cells[3], cells[4], cells[5])
        print "%s,%s,%s" % (cells[6], cells[7], cells[8])
        cells = [""]*9
        print ",,"

    #print cols
    cnum = int(cols[1])
    #print cnum
    if cols[2] == "g":
        #cells[cnum-1] = cells[cnum-1] + "," + cols[3]
        cells[cnum-1] = "/".join([cells[cnum-1] ,cols[3]])
    else:
        cells[cnum-1] = cols[2]

sys.exit()

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
                ofile.write("%d\t%d\n" % (board,i))
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
ofile.close()
