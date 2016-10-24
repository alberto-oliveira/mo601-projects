#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import argparse
import numpy as np
import glob

bm_input_names = {"400.perlbench":["checkspam.pl", "diffmail.pl", "splitmail.pl"],
                  "401.bzip2":["input.source", "chicken.jpg", "liberty.jpg", "input.program", "text.html", "input.combined"],
                  "403.gcc":["166.in", "200.in", "c-typeck.in", "cp-decl.in", "expr.in", "expr2.in", "g23.in", "s04.in", "scilab.in"],
                  "410.bwaves":["bwaves.in"],
                  "416.gamess":["cytosine.2", "h2ocu2+.gradient", "triazolium"],
                  "429.mcf":["inp.in"],
                  "433.milc":["su3imp.in"],
                  "434.zeusmp":["zmp_inp"],
                  "435.gromacs":["gromacs.tpr"],
                  "436.cactusADM":["benchADM.par"],
                  "437.leslie3d":["leslie3d.in"],
                  "444.namd":["namd.input"],
                  "445.gobmk":["13x13.tst", "nngs.tst", "score2.tst", "trevorc.tst", "trevord.tst"],
                  "447.dealII":["DummyData"],
                  "450.soplex":["pds-50.mps", "ref.mps"],
                  "453.povray":["SPEC-benchmark-ref.pov"],
                  "454.calculix":["hyperviscoplastic.inp"],
                  "456.hmmer":["nph3.hmm", "retro.hmm"],
                  "458.sjeng":["ref.txt"],
                  "459.GemsFDTD":["ref.in"],
                  "462.libquantum":["control"],
                  "464.h264ref":["foreman_ref_encoder_baseline.cfg", "foreman_ref_encoder_main.cfg", "sss_encoder_main.cfg"],
                  "465.tonto":["stdin"],
                  "470.lbm":["lbm.in"],
                  "471.omnetpp":["omnetpp.ini"],
                  "473.astar":["BigLakes2048.cfg", "rivers.cfg"],
                  "481.wrf":["namelist.input"],
                  "482.sphinx3":["args.an4"],
                  "483.xalancbmk":["xalanc.xsl"],
                  "501.toy-bm-1":["---"],
                  "502.toy-bm-2":["---"]}

def read_csv_file(csvfpath):

    f = open(csvfpath)
    line = f.readline()
    parts = line.split(",")

    bm_name, nin = parts[0].split("_")

    row = []

    row.append(bm_name)
    row.append(bm_input_names[bm_name][int(nin)])

    row.extend([int(x) for x in parts[1:]])

    return row


def write_out_file(outfpath, results, bm_order):

    outf = open(outfpath, 'w')

    outf.write(",,total instruction memory accesses,,instruction TLB misses,,total instruction page table accesses")
    outf.write(",,total data memory accesses,,data TLB misses,,total data page table accesses\n")

    outf.write("BM name, input, 4 kiloB pages, 4 MegaB pages, 4 kiloB pages, 4 MegaB pages, 4 kiloB pages, 4 MegaB pages")
    outf.write(", 4 kiloB pages, 4 MegaB pages, 4 kiloB pages, 4 MegaB pages, 4 kiloB pages, 4 MegaB pages\n")

    for bm in bm_order:

        row = results[bm]

        aux = bm.split("_", 2)
        bm_name, bm_input = aux[0], aux[1]

        kilo_ins_mem_access = row[0]
        kilo_itlb_misses = row[1]
        kilo_ins_ptbl_access = row[2]
        kilo_data_mem_access = row[3]
        kilo_dtlb_misses = row[4]
        kilo_data_ptbl_access = row[5]

        mega_ins_mem_access = row[6]
        mega_itlb_misses = row[7]
        mega_ins_ptbl_access = row[8]
        mega_data_mem_access = row[9]
        mega_dtlb_misses = row[10]
        mega_data_ptbl_access = row[11]


        outf.write("{0:s}, {1:s}".format(bm_name, bm_input))

        outf.write(",{0:d}".format(kilo_ins_mem_access))
        outf.write(",{0:d}".format(mega_ins_mem_access))

        outf.write(",{0:d}".format(kilo_itlb_misses))
        outf.write(",{0:d}".format(mega_itlb_misses))

        outf.write(",{0:d}".format(kilo_ins_ptbl_access))
        outf.write(",{0:d}".format(mega_ins_ptbl_access))

        outf.write(",{0:d}".format(kilo_data_mem_access))
        outf.write(",{0:d}".format(mega_data_mem_access))

        outf.write(",{0:d}".format(kilo_dtlb_misses))
        outf.write(",{0:d}".format(mega_dtlb_misses))

        outf.write(",{0:d}".format(kilo_data_ptbl_access))
        outf.write(",{0:d}".format(mega_data_ptbl_access))

        outf.write("\n")

    outf.close()





def make_results(kilo_csv_dir, mega_csv_dir, outfile):

    results = {}
    bm_order = []

    kilo_flist = glob.glob(kilo_csv_dir + "*.csv")
    mega_flist = glob.glob(mega_csv_dir + "*.csv")

    assert(len(kilo_flist) == len(mega_flist))

    kilo_flist.sort()
    mega_flist.sort()

    for fpath in kilo_flist:

        row = read_csv_file(fpath)

        bm_order.append(row[0] + "_" + row[1])
        results[row[0] + "_" + row[1]] = row[2:]

    for fpath in mega_flist:

        row = read_csv_file(fpath)
        results[row[0] + "_" + row[1]].extend(row[2:])


    write_out_file(outfile, results, bm_order)

    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("kilo_csv_dir", help="Directory containing 4kB page csv files", type=str)
    parser.add_argument("mega_csv_dir", help="Directory containing 4MB page csv files", type=str)
    parser.add_argument("outfile", help="Output file", type=str)

    args = parser.parse_args()

    kilo_csv_dir = args.kilo_csv_dir
    mega_csv_dir = args.mega_csv_dir
    outfile = args.outfile

    if kilo_csv_dir[-1] != "/": kilo_csv_dir += "/"
    if mega_csv_dir[-1] != "/": mega_csv_dir += "/"
    if not outfile.endswith(".csv"): outfile += ".csv"

    make_results(kilo_csv_dir, mega_csv_dir, outfile)


