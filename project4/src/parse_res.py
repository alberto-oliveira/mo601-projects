#!/usr/bin/env python
#-*- coding: utf-8 -*-

def multi_split(sep_list, string):

    parts = [string]
    for sep in sep_list:

        aux = []
        for p in parts:
            aux.extend(p.split(sep))

        parts = aux

    return parts


def parse_res(resfilepath):

    res = []
    with open(resfilepath) as resf:

        resf.readline()
        resf.readline()

        val = resf.readline().strip(")% \n").split(":")[1]
        val = val.strip(" ").split(" ")[0]
        res.append(val)

        val = resf.readline().strip(")% \n").split(":")[1]
        val = val.strip(" ").split(" ")[0]
        res.append(val)

        val = resf.readline().strip(")% \n").split(":")[1]
        val = val.strip(" ").split(" ")[0]
        res.append(val)

        val = resf.readline().strip(")% \n").split(":")[1]
        val = val.strip(" ").split(" ")[0]
        res.append(val)

        val = resf.readline().strip(")% \n").split(":")[1]
        val = val.strip(" ").split(" ")[0]
        res.append(val)

        val = resf.readline().strip(")% \n").split(":")[1]
        val = val.strip(" ").split(" ")[0]
        res.append(val)

        val = resf.readline().strip(")% \n").split(":")[1]
        val = val.strip(" ").split(" ")[0]
        res.append(val)

        return [float(x) for x in res]

