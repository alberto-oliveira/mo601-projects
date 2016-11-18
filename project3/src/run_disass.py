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

def run_disass(disass_path, outfile, execlist):

    parseinst = lambda(x) : x.split(" ", 1)[1]

    icounter = 0
    with open(outfile, 'w') as outf:
        for execpath in execlist:

            try:
                tmpf = open("tmp.bin", 'w')
                print "disassembling: ", execpath, " ({0:s})".format(fmt_size(os.path.getsize(execpath)))
                subprocess.call([disass_path, execpath, "x86"], stdout=tmpf)
                tmpf.close()

                print "parsing: ", execpath
                with open("tmp.bin") as inpf:

                    for line in inpf:

                        icounter += 1
                        inst = parseinst(line)

                        if inst not in used_inst:

                            outf.write(line)
                            used_inst.add(inst)

                print "deleting tmp.bin"
                os.unlink("tmp.bin")
            except Exception as e:
                print "could not disassemble ", execpath
            print "---\n"

    print "-- Done --"
    print "Number of unique programs: ", len(execlist)
    print "Total number of instruction: ", icounter
    print "Number of unique instructions: ", len(used_inst)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("dpath", help="Disassembly script path (disass.sh)",
                        type=str)

    parser.add_argument("--outfile", "-o", help="Output file name. Default: outfile.bin",
                        type=str, default="outfile.bin")

    parser.add_argument("--execdir", "-e", help="Path with executables. If empty, gets all executables from the system. "
                                                "Default is empty",
                        type=str, default="")

    args = parser.parse_args()

    outfile = args.outfile
    execdir = args.execdir
    disass_path = args.dpath

    if execdir == "": execlist = list_execs_simple()
    else:
        if execdir[-1] != "/":
            execdir += "/"

        execlist = glob.glob(execdir + "*")

    run_disass(disass_path, outfile, execlist)