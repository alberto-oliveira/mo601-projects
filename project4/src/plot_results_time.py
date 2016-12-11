#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import argparse
import glob

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load_exec_sz_table():

    getbasename = lambda(f): os.path.splitext(os.path.basename(f))[0]

    eszmap = {}

    with open('exec-dumplist.csv', 'r') as f:
        for line in f:
            ename, esz = line.strip("/").split(",")
            eszmap[getbasename(ename)] = int(esz)

    return eszmap

def create_final_table(basetable, eszmap):

    finaltable = []
    for row in basetable:

        if row['exec'] in eszmap:
            newrow = (row['exec'], eszmap[row['exec']], row['size'], row['inst'], row['time'])
            finaltable.append(newrow)

    dt = dict(names=('exec', 'esize', 'bsize', 'inst', 'time'),
                  formats=('S100', 'i32', 'i32', 'i32', 'f32'))

    return np.array(finaltable, dtype=dt)

def plot_results_time(csvfname, outfprefix):

    eszmap = load_exec_sz_table()

    dt = dict(names=('exec', 'size', 'inst', 'time'),
                  formats=('S100', 'i32', 'i32', 'f32'))

    auxtable = np.loadtxt(csvfname, dt, delimiter=',')
    table = create_final_table(auxtable, eszmap)

    table['esize'] = table['esize']/1000
    table['bsize'] = table['bsize']/1000

    outfname = "{0:s}--time-plot.pdf".format(outfprefix)

    #psize = np.polyfit(table['size'], table['time'], 1)
    #yfitsize_linear = table['size'] * psize[0] + psize[1]
    psize = np.polyfit(table['bsize'], table['time'], 2)
    yfitsize_quad = np.power(table['bsize'], [2]) * psize[0] + table['bsize'] * psize[1] + psize[2]

    #pinst = np.polyfit(table['inst'], table['time'], 1)
    #yfitinst_linear = table['inst'] * pinst[0] + pinst[1]
    pinst = np.polyfit(table['inst'], table['time'], 2)
    yfitinst_quad = np.power(table['inst'], [2]) * pinst[0] + table['inst'] * pinst[1] + pinst[2]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(12,7))

    ax1.scatter(table['esize'], table['time'], s=10, c='purple')
    #ax1.plot(table['size'], yfitsize_linear, c='red', linewidth=3)
    #ax2.plot(table['bsize'], yfitsize_quad, c='green', linewidth=3)
    #ax1.set_title('Executable Size(B) vs Time(s)')
    ax1.set_xlim(left=0)
    ax1.grid(True)
    ax1.set_xlabel('Executable Size(KB)')

    ax2.scatter(table['bsize'], table['time'], s=10)
    #ax1.plot(table['size'], yfitsize_linear, c='red', linewidth=3)
    ax2.plot(table['bsize'], yfitsize_quad, c='green', linewidth=3)
    #ax2.set_title('Dump Size(B) vs Time(s)')
    ax2.set_xlim(left=0)
    ax2.grid(True)
    ax2.set_xlabel('Dump Size(KB)')

    ax3.scatter(table['inst'], table['time'], s=10)
    #ax2.plot(table['inst'], yfitinst_linear, c='red', linewidth=3)
    ax3.plot(table['inst'], yfitinst_quad, c='green', linewidth=3)
    #ax3.set_title('Instruction # vs Time(s)')
    ax3.set_xlim(left=0)
    ax3.grid(True)
    ax3.set_xlabel('Instruction #')

    ax1.set_ylim(bottom=0)
    ax1.set_ylabel('Time (s)')

    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=-45)

    fig.tight_layout()
    fig.savefig(outfname)


    outfname = "{0:s}--execsize-plot.pdf".format(outfprefix)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12,7))

    ax1.scatter(table['esize'], table['bsize'], s=10, c='purple')
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0)
    ax1.grid(True)
    ax1.set_xlabel('Executable Size(KB)')
    ax1.set_ylabel('Dump Size(KB)')

    ax2.scatter(table['esize'], table['inst'], s=10, c='purple')
    ax2.set_xlim(left=0)
    ax2.set_ylim(bottom=0)
    ax2.grid(True)
    ax2.set_xlabel('Executable Size(KB)')
    ax2.set_ylabel('Instruction #')

    ax3.scatter(table['bsize'], table['inst'], s=10, c='blue')
    ax3.set_xlim(left=0)
    ax3.set_ylim(bottom=0)
    ax3.grid(True)
    ax3.set_xlabel('Dump Size(KB)')
    ax3.set_ylabel('Instruction #')

    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=-45)

    fig.tight_layout()
    fig.savefig(outfname)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("csvfname", help="Input Csv file.",
                        type=str)

    parser.add_argument("outfprefix", help="Prefix to output file.",
                        type=str)

    args = parser.parse_args()

    csvfname = args.csvfname
    outfprefix = args.outfprefix

    plot_results_time(csvfname, outfprefix)