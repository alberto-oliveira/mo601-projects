#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import argparse
import glob
import subprocess
import errno
import time

import numpy as np

prev_prog = 1
def print_progress(done, total):

    global prev_prog

    pct = float(done)/float(total)
    pct = int(pct*100)
    prg = int(pct/10)

    if done == 0:
        sys.stdout.write("                     ---- Progress ----\n")
        sys.stdout.write("010%")
        for i in range(2, 11):
            sys.stdout.write("   {0:03d}%".format(i*10))
        sys.stdout.write("\n")
    if prg >= prev_prog:
        prev_prog += 1
        sys.stdout.write(" *     ")

    if done == total:
        sys.stdout.write("\n")

    sys.stdout.flush()

    return

def get_inst_num(instfname):

    i = -1
    with open(instfname, 'r') as f:
        for i, l in enumerate(f):
            pass

    return i+1


def order_bins(execdumplist):

    execdumpszlist = [os.path.getsize(x) for x in execdumplist]

    aux = zip(execdumplist, execdumpszlist)
    dt = dict(names=('exec', 'size'),
                  formats=('S100', 'i32'))

    execdumplistsorted = np.array(aux, dtype=dt)
    execdumplistsorted.sort(order=('size', 'exec'))

    return execdumplistsorted




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


def run_lisc(liscdir, automata, execdumpdir, outroot, logfname, csvfname):

    # Logging Stuff
    logf = []
    logopen = lambda(f): open(f, 'w') if f != "" else []
    logwrite = lambda(s): logf.write(s) if logf else []
    logflush = lambda: logf.flush() if logf else []
    logclose = lambda: logf.close() if logf else []
    # ----

    # Time vs size stuf
    csvf = []
    csvopen = lambda(f): open(f, 'w') if f != "" else []
    csvwrite = lambda(s): csvf.write(s) if logf else []
    csvflush = lambda: csvf.flush() if csvf else []
    csvclose = lambda: csvf.close() if csvf else []

    # Utilities
    getbasename = lambda(x): os.path.splitext(os.path.basename(x))[0]
    # ----

    # Timming Stuff
    tic = lambda: time.time()
    toc = lambda(t): time.time() - t
    # ----

    lisc = liscdir + "learnopt"

    execdumplist = glob.glob(execdumpdir + "/*")
    execdumplistsorted = order_bins(execdumplist)

    safe_create_dir(outroot + "res")
    safe_create_dir(outroot + "log")

    total = len(execdumplistsorted['exec'])
    done = 0
    correct = 0

    ts_all = tic()
    logf = logopen(logfname)
    csvf = csvopen(csvfname)
    print_progress(done, total)
    for pair in execdumplistsorted:

        execdumppath = pair[0]
        execsize = pair[1]

        inum = get_inst_num(execdumppath)

        execname = getbasename(execdumppath)
        logwrite("---\nRunning for: {0:s} ({1:d}B)\n".format(execname, execsize))
        logflush()

        outresname = "{0:s}/{1:s}.res".format(outroot+"res", execname)
        outlogname = "{0:s}/{1:s}.log".format(outroot+"log", execname)

        outresf = open(outresname, 'w')
        outlogf = open(outlogname, 'w')

        try:
            ts = tic()
            subprocess.call([lisc, "-la", automata, "-lf", execdumppath], stdout=outresf, stderr=outlogf)
            correct += 1
            te = toc(ts)

            logwrite("Time elapsed: {0:0.2f}s\n---\n\n".format(te))
            logflush()

            csvwrite("{3:s},{0:d},{1:d},{2:0.2f}\n".format(execsize, inum, te, execname))
            csvflush()


        except Exception as e:
            logwrite("Error!\n---\n\n")
            logflush()

        outresf.close()
        outlogf.close()

        done += 1
        print_progress(done, total)

    logclose()
    csvclose()

    sys.stdout.write("\nTime elapsed: {0:0.2f}s\n".format(toc(ts_all)))
    print "Total: ", total
    print "Correctly done: ", correct



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("liscdir", help="directory containing lisc",
                        type=str)

    parser.add_argument("automata", help="Automata path",
                        type=str)

    parser.add_argument("execdumpdir", help="Path with executable dumps.", type=str)


    parser.add_argument("--outroot", "-o", help="Output root directory. Two folders will be created in the root: "
                                                "log and res. Default is ./",
                        type=str, default="./")

    parser.add_argument("--log", "-l", help="Run lisc log file. If empty, no log is created. Default is empty",
                        type=str, default="")

    parser.add_argument("--csv", "-c", help="Run lisc csv file. Logs program size vs time to lift If empty, no csv "
                                            "is created. Default is empty",
                        type=str, default="")

    args = parser.parse_args()

    liscdir = args.liscdir
    automata = args.automata
    execdumpdir = args.execdumpdir
    outroot = args.outroot
    logfname = args.log
    csvfname = args.csv

    if liscdir[-1] != "/": liscdir += "/"
    if execdumpdir[-1] != "/": execdumpdir += "/"
    if outroot[-1] != "/": outroot += "/"

    run_lisc(liscdir, automata, execdumpdir, outroot, logfname, csvfname)