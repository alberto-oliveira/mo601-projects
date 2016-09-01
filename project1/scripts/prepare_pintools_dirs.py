#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import argparse
import glob
import errno
import shutil

#pin_path = "/home/alberto/disciplinas/mo601/tools/pin-3.0-76991-gcc-linux/pin"

def safe_create_dir(dir):
    """ Safely creates dir, checking if it already exists.

    Creates any parent directory necessary. Raises exception
    if it fails to create dir for any reason other than the
    directory already existing.

    :param dir: of the directory to be created
    """


    try:
        os.makedirs(dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def gen_runfile_name():

    runlist = glob.glob("./*run_pintools_inscount_op*")
    runlist.sort()

    lastrf = os.path.basename(runlist[1])
    parts = lastrf.split(".")
    nr = int(parts[1])

    runfile_name = "run_pintools_inscount_op.{0:04d}.out".format(nr+1)

    return runfile_name


def prepare_pintools_dirs(pinpath, pintoolspath, benchsbasedir, outdir, pinopt, dset):

    #runf = open(gen_runfile_name(), 'w')

    benchlist = [b for b in os.listdir(benchsbasedir) if os.path.isdir(benchsbasedir + b)]

    for benchdir in benchlist:

        print "-- Preparing bench --", b

        pin_run_dir = "{0:s}{1:s}/".format(outdir, benchdir)
        pin_output_dir = pin_run_dir + "pin_output/"

        print "    -> pin run dir: ", pin_run_dir
        print "    -> pin output dir: ", pin_output_dir, "\n"

        safe_create_dir(pin_run_dir)
        safe_create_dir(pin_output_dir)

        toolname = os.path.splitext(os.path.basename(pintoolspath))[0]
        benchexec = glob.glob(benchsbasedir + benchdir + "/exe/*")[0]
        inputlist = glob.glob(benchsbasedir + benchdir + "/data/{0:s}/input/*".format(dset))
        inputnamelist = [os.path.basename(x) for x in inputlist]

        print "    -> toolname: ", toolname
        print "    -> benchexe: ", benchexec

        for inputpath in inputlist: shutil.copy2(inputpath, pin_run_dir)

        scriptname = pin_run_dir + "run_pin_on_bench_{0:s}.sh".format(benchdir)

        sfi = open(scriptname, 'w')

        sfi.write("#!/bin/bash\n")

        for inname in inputnamelist:
            sfi.write("{0:s} -t {1:s} -o {2:s} {3:s} -- {4:s} {5:s}\n".format(
                      pinpath,
                      pintoolspath,
                      pin_output_dir + "{2:s}.out".format(benchdir, inname, toolname),
                      pinopt,
                      benchexec,
                      os.path.splitext(inname)[0]))




if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("pinpath", help="Path to pin.", type=str)
    parser.add_argument("pintoolspath", help="Path to pintools script", type=str)
    parser.add_argument("benchsbasedir", help="Base directory containing SPEC benchmark run subdirectories.", type=str)
    parser.add_argument("outdir", help="Output directory for bechmarks count subdirectories.", type=str)
    parser.add_argument("-o", "--pinopt", help="String containing options to running pin. Default is empty",
                        type=str, default="")
    parser.add_argument("-s", "--dset", help="Dataset used for running. Can be \'train\', \'test\' or \'ref\'. Default is"
                                            "\'ref\'",
                        type=str,
                        choices=["train", "test", "ref"],
                        default="ref")

    args = parser.parse_args()

    pinpath = args.pinpath
    pintoolspath = args.pintoolspath
    benchsbasedir = args.benchsbasedir
    outdir = args.outdir
    pinopt = args.pinopt
    dset = args.dset

    if benchsbasedir[-1] != "/": benchsbasedir += "/"
    if outdir[-1] != "/": outdir += "/"

    prepare_pintools_dirs(pinpath, pintoolspath, benchsbasedir, outdir, pinopt, dset)