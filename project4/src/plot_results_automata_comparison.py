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


color_name_list = ['blue', 'green', 'red', 'purple', 'cyan', 'magenta', 'yellow']
getbasename = lambda(f): os.path.splitext(os.path.basename(f))[0]

def plot_results_automata_comparison(csvfiles, outfprefix):


    dt = dict(names=('exec', 'size', 'inst', 'time'),
                  formats=('S100', 'i32', 'i32', 'f32'))

    outfname = "{0:s}-plot.pdf".format(outfprefix)


    fig, ax = plt.subplots(1, 1, figsize=(14,7))

    for i, csvfname in enumerate(csvfiles):

        table = np.loadtxt(csvfname, dt, delimiter=',')
        clr = color_name_list[i]

        pinst = np.polyfit(table['inst'], table['time'], 2)
        yfitinst_quad = np.power(table['inst'], [2]) * pinst[0] + table['inst'] * pinst[1] + pinst[2]

        ax.plot(table['inst'], yfitinst_quad, c=clr, linewidth=3)

    leg_names = [getbasename(x).split('-', 1)[0] for x in csvfiles ]

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    ax.legend(leg_names, loc='upper center', bbox_to_anchor=(0.5, -0.09),
          fancybox=True, shadow=True, ncol=3, fontsize='small')
    #ax.set_title('Automata used impact on lifting time')
    ax.set_xlabel('Instruction #')
    ax.set_ylabel('Time (s)')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True)

    fig.savefig(outfname)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("csvfiles",
                        help="Input csv file list",
                        type=str, default=[], nargs='+')

    parser.add_argument("-p", "--outprefix", help="Prefix to output file. Default is output.pdf",
                        type=str, default="output")

    args = parser.parse_args()

    csvfiles = args.csvfiles
    outprefix = args.outprefix

    plot_results_automata_comparison(csvfiles, outprefix)