#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
from debug_routines import showkeys
import progpad
from vertel_main import Select

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    ## showkeys(form)
    ## return

    l = Select({"select": "start",
        "user": form.getfirst("user", ''),
        "meld": form.getfirst("meld", '')
        })
    print("Content-Type: text/html\n")     # HTML is following
    if len(l.regels) == 0:
        print("Er is iets misgegaan...")
    else:
        for x in l.regels:
            print(x)

if __name__ == '__main__':
    main()



