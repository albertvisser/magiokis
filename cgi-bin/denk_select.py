#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import cgi
import cgitb
cgitb.enable()
import codecs, sys
writer = codecs.getwriter('utf8')(sys.stdout.buffer)
from debug_routines import showkeys
import progpad
from denk_main import Denk

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    ## showkeys(form)
    ## return

    args = {"wat": "select", "selItem": "", "selData": ""}
    test = form.getfirst("rbselZoek", '')
    if test:
        args["selItem"] = test
    test = form.getfirst("txtNwTrefw", '')
    if test:
        args["selItem"] = "nwTrefw"
        args["selData"] = test
    test = form.getfirst("txtNweCat", '')
    if test:
        args["selItem"] = "nweCat"
        args["selData"] = test
    test = form.getfirst("lbSelTrefw", '')
    if test:
        args["selItem"] = "selTrefw"
        args["selData"] = test
    test = form.getfirst("txtZoek", '')
    if test:
        args["selData"] = test
        args["selItem"] = form.getfirst("rbselZoek", '')
    print("Content-Type: text/html")     # HTML is following
    h = Denk(args)
    if len(h.regels) == 1:
        print(h.regels[0])
        print()                               # blank line, end of headers
    else:
        print()                               # blank line, end of headers
        for x in h.regels:
            ## try:
            print(x)
            ## except UnicodeEncodeError:
                ## print(x.decode('utf-8'))

if __name__ == '__main__':
   main()
