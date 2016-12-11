#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, os
import argparse
import glob
import numpy as np

if __name__ == "__main__":

    bindir = sys.argv[1]
    outfile = sys.argv[2]

    completedir = lambda(d): d+"/" if d[-1] != "/" else d
    checkifnop = lambda(t): True if (t.split(" ", 1)[1] == ";" or t.split(" ", 1)[1] == "nop;") else False
    getbasename = lambda(x): os.path.splitext(os.path.basename(x))[0]

    bindir = completedir(bindir)
    binlist = glob.glob(bindir + "*.bin")
    binlist.sort()

    fnames = []
    nopcs = []
    uniquecs = []
    totalcs = []

    with open(outfile, 'w') as of:

        for binfname in binlist:
            nopcount = 0
            total_inst = 0
            unique_inst = set([])
            binfbasename = getbasename(binfname)

            with open(binfname, 'r') as bf:

                for line in bf:
                    total_inst += 1
                    unique_inst.add(line.strip("\n").split(" ", 1)[1])
                    if checkifnop(line.strip("\n")): nopcount += 1

            fnames.append(binfbasename)
            nopcs.append(nopcount)
            uniquecs.append(len(unique_inst))
            totalcs.append(total_inst)

    aux = zip(fnames, totalcs, uniquecs, nopcs)
    dt = dict(names=('exec', 'total', 'unique', 'nops'),
                  formats=('S100', 'i32', 'i32', 'i32'))

    nopcsarray = np.array(aux, dtype=dt)
    nopcsarray.sort(order=('nops', 'unique', 'total', 'exec'))
    nopcsarray = nopcsarray[::-1]

    np.savetxt(outfile, nopcsarray, fmt="%s,%d,%d,%d", header="exec,total inst.,unique inst., nops")
