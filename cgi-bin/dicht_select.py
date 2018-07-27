#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
from debug_routines import showkeys
import progpad
from dicht_main import Dicht

def main():
    form = cgi.FieldStorage()
    ## showkeys(form)
    ## return

    action = ""
    args = {
        "wat": "select",
        "selItem": None
        }
    test = form.getfirst("rbselZoek", '')
    if test:
        args["selItem"] = test
    test = form.getfirst("txtNwTrefw", '')
    if test:
        args["selData"] = test
        args["selItem"] = "nwTrefw"
    test = form.getfirst("txtNwJaar", '')
    if test:
        args["selData"] = test
        args["selItem"] = "nwJaar"
    test = form.getfirst("lbSelTrefw", '')
    if test:
        args["selData"] = test
        args["selItem"] = "selTrefw"
    test = form.getfirst("lbSelJaar", '')
    if test:
        args["selData"] = test
        args["selItem"] = "selJaar"
    test = form.getfirst("txtZoek", '')
    if test:
        args["selData"] = test
        args["selItem"] = form.getfirst("rbselZoek", '')
    print("Content-Type: text/html")     # HTML is following
    d = Dicht(args)
    if len(d.regels) == 1:
        print(d.regels[0])
        print('')                              # blank line, end of headers
    else:
        print('')                               # blank line, end of headers
        for x in d.regels:
            try:
                print(x) #.encode('iso-8859-1')
            except UnicodeEncodeError:
                print(x.encode('iso-8859-1'))

if __name__ == '__main__':
	main()

