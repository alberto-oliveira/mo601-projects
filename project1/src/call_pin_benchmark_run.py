#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import argparse
import subprocess

bm_list = ["400.perlbench",
           "401.bzip2",
           "403.gcc",
           "410.bwaves",
           "416.gamess",
           "429.mcf",
           "433.milc",
           "434.zeusmp",
           "435.gromacs",
           "436.cactusADM",
           "437.leslie3d",
           "444.namd",
           "445.gobmk",
           "447.dealII",
           "450.soplex",
           "453.povray",
           "454.calculix",
           "456.hmmer",
           "458.sjeng",
           "459.GemsFDTD",
           "462.libquantum",
           "464.h264ref",
           "465.tonto",
           "470.lbm",
           "471.omnetpp",
           "473.astar",
           "481.wrf",
           "482.sphinx3",
           "483.xalancbmk"]


def print_benchmarks():

    print "### Benchmark Numbers ###"
    for i, bmn in enumerate(bm_list):

        print "{0:02d} -> {1:s}".format(i, bmn)
    print "    ###      "

def call_pin_benchmark_run(snum, enum, configpath, stdoutdir):

    runspec_list = ["runspec", "--config", configpath, "--size", "ref", "--iterations",
                    "1", "--noreportable", "--verbose", "35"]

    for i in range(snum, enum):

        bmname = bm_list[i]
        stdoutname = "{0:s}output_{1:s}.out".format(stdoutdir, bmname)
        stdoutf = open(stdoutname, 'w')
        #print runspec_list + [bmname]
        #print stdoutname

        call_list = runspec_list + [bmname]

        print "##### Starting {0:s} bench #####".format(bmname)

        print call_list

        print stdoutname

        subprocess.call(call_list, stdout=stdoutf)

        print "\n"


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("snum", type=int, help="Starting BM number",
                        choices=range(0, 29))

    parser.add_argument("enum", type=int, help="Ending BM number",
                        choices=range(1, 30))

    parser.add_argument("configpath", type=str, help="Path to the SPEC config file")

    parser.add_argument("stdoutdir", type=str, help="Directory to store stdout files of benchmark runs")

    parser.add_argument("-p", "--printbm", help="Print benchmark list",
                        action='store_true', default=False)

    args = parser.parse_args()

    snum = args.snum
    enum = args.enum
    configpath = args.configpath
    stdoutdir = args.stdoutdir
    printbm = args.printbm

    if stdoutdir[-1] != "/": stdoutdir += "/"

    if printbm:
        print_benchmarks()
        sys.exit(0)
    else:
        if snum >= enum:
            enum = snum + 1

        call_pin_benchmark_run(snum, enum, configpath, stdoutdir)