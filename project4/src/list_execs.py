#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import numpy as np

def fmt_size(sizelist):

    sizenamelist = []

    for sz in sizelist:

        if sz >= 1000000: sz_name = "{0:10.2}M".format(float(sz)/1000000)
        elif sz >= 1000: sz_name = "{0:10.2}K".format(float(sz)/1000)
        else: sz_name = "{0:10.2}B".format(float(sz))

        sizenamelist.append(sz_name)

    return sizenamelist

def list_execs_full(outfile):

    paths = os.environ["PATH"].split(":")

    listdir = lambda(p) : os.listdir(p) if os.path.isdir(p) else [ ]

    isfile = lambda(x) : True if os.path.isfile(os.path.join(x[0],x[1])) else False

    isexe = lambda(x) : True if os.access(os.path.join(x[0],x[1]), os.X_OK) else False

    execlist = [ os.path.join(p,f) for p in paths for f in listdir(p) if isfile((p,f)) and isexe((p,f)) ]
    sizelist = [ os.path.getsize(x) for x in execlist]

    aux = zip(execlist, sizelist)
    dt = dict(names=('exec', 'size'),
                  formats=('S100', 'i32'))

    execs = np.array(aux, dtype=dt)
    execs.sort(order=('size', 'exec'))
    execs = execs[::-1]


    sizenamelist = fmt_size(execs['size'])
    aux = zip(execs['exec'], sizenamelist)
    dt = dict(names=('exec', 'sname'),
                  formats=('S100', 'S30'))
    execsname = np.array(aux, dtype=dt)

    np.savetxt(outfile, execsname, fmt="%-50s %15s")

    return execs

def list_execs_simple():

    paths = os.environ["PATH"].split(":")

    listdir = lambda(p) : os.listdir(p) if os.path.isdir(p) else [ ]

    isfile = lambda(x) : True if os.path.isfile(os.path.join(x[0],x[1])) else False

    isexe = lambda(x) : True if os.access(os.path.join(x[0],x[1]), os.X_OK) else False

    execlist = [ os.path.join(p,f) for p in paths for f in listdir(p) if isfile((p,f)) and isexe((p,f)) ]

    return execlist