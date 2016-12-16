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
    form_ok = 0
    ## showkeys(form)
    ## return

    args = {}
    test = form.getfirst("lbSelItem", '')
    if test:           # we komen vanuit selectie
        args["selJaar"], args["selItem"] = test.split('_')
        args["wat"] = "detail"
    else:
        test = form.getfirst("hselItem", '')
        if test:          # we komen vanuit updaten tekst
            args["wat"] = "detail_wijzig"
            args["selItem"] = form.getfirst("hselItem", '')
            args["selJaar"] = form.getfirst("hSelJaar", '')
            test = form.getfirst("txtTitel", '')
            if test:
                args["titel"] = test
            test = form.getfirst("txtTekst", '')
            if test:
                args["tekst"] = test
            test = form.getfirst("txtGedicht", '')
            if test:
                args["gedicht"] = test
    print("Content-Type: text/html")     # HTML is following
    print('')                              # blank line, end of headers
    d = Dicht(args)
    for x in d.regels:
        try:
            print(x) #.encode('iso-8859-1')
        except UnicodeEncodeError:
            print(x.encode('iso-8859-1'))

if __name__ == '__main__':
	main()
