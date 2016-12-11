#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import subprocess
import argparse
import glob

from list_execs import list_execs_simple

used_inst = set()

disass_path = "/home/alberto/mo601/lisc/utils/disass.sh"

def fmt_size(sz):

    if sz >= 1000000: sz_name = "{0:0.2f}M".format(float(sz)/1000000)
    elif sz >= 1000: sz_name = "{0:0.2f}K".format(float(sz)/1000)
    else: sz_name = "{0:0.2f}B".format(float(sz))

    return sz_name

def run_disass(disass_path, outdir, execlist):

    for execpath in execlist:

        try:
            outfname = os.path.splitext(os.path.basename(execpath))[0]

            tmpf = open("{0:s}{1:s}.bin".format(outdir, outfname), 'w')
            print "disassembling: ", execpath, " ({0:s})".format(fmt_size(os.path.getsize(execpath)))
            subprocess.call([disass_path, execpath, "x86"], stdout=tmpf)
            tmpf.close()

        except Exception as e:
            print "could not disassemble ", execpath
        print "---\n"

    print "-- Done --"
    print "Number of unique programs: ", len(execlist)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("dpath", help="Disassembly script path (disass.sh)",
                        type=str)

    parser.add_argument("--outdir", "-o", help="Output directory. Default: empty",
                        type=str, default="")

    parser.add_argument("--execdir", "-e", help="Path with executables. If empty, gets all executables from the system. "
                                                "Default is empty",
                        type=str, default="")

    args = parser.parse_args()

    outdir = args.outdir
    execdir = args.execdir
    disass_path = args.dpath

    if execdir == "": execlist = list_execs_simple()
    else:
        if execdir[-1] != "/":
            execdir += "/"
        execlist = glob.glob(execdir + "*")

    if outdir != "" and outdir[-1] != "/":
        outdir += "/"

    run_disass(disass_path, outdir, execlist)