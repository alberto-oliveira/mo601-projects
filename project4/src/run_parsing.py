#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import argparse
import numpy as np
import glob
from parse_res import parse_res

getfname = lambda(p): os.path.splitext(os.path.basename(p))[0]

def write_out_csv(outfile, restable):

    if not outfile.endswith(".csv"):
        outfile = getfname(outfile) + ".csv"

    with open(outfile, 'w') as outf:

        outf.write("Bin name, Total Inst., RTL Matched Inst., RTL Not matched Inst., MNE not Found, OPND Not Found, "
                   "Total Generalizations, Success (%)\n")

        for res in restable:

            outf.write("{0:s}, {1:d}, {2:d}, {3:d}, {4:d}, {5:d}, {6:d}, {7:0.2f}\n".format(
                        res[0], int(res[6]), int(res[1]), int(res[4]), int(res[2]), int(res[3]), int(res[5]), res[7]))

    return



def run_parsing(resdir, outfile):

    resflist = glob.glob(resdir + "*")

    restable = []

    for resfpath in resflist:

        try:
            res = parse_res(resfpath)
            resname = getfname(resfpath)
            print resname + " parsed!"

            res = [resname] + res
            restable.append(res)

        except Exception as e:
            print resname + " could not be parsed!"

    write_out_csv(outfile, restable)





if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("resdir", help="Directory containing result files", type=str)

    parser.add_argument("--outfile", "-o", help="Output file name. Default is results.csv", type=str,
                        default="results.out")

    args = parser.parse_args()

    resdir = args.resdir
    outfile = args.outfile

    if resdir[-1] != "/": resdir += "/"

    run_parsing(resdir, outfile)
