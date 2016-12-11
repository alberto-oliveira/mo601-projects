#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, os
import argparse


def combine_imap(in_imap_files, outfile):

    outf = open(outfile, 'w')

    for infname in in_imap_files:

        if infname.endswith(".imap"):
            print "Transcribing: ", os.path.basename(infname)
            with open(infname, 'r') as infi:

                for line in infi:

                    outf.write(line)
        else:
            print "Not a valida .imap file: ", os.path.basename(infname)

    outf.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("input_imap_files",
                        help="Input .imap file list",
                        type=str, default=[], nargs='+')

    parser.add_argument("-o", "--outfile",
                        help="Combined .imap file name. Default is \'combined.imap\'",
                        type=str, default="combined.imap")

    args = parser.parse_args()

    in_imap_files = args.input_imap_files
    outfile = args.outfile

    combine_imap(in_imap_files, outfile)