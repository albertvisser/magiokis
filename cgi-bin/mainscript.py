#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
if not sys.version < '3':
    from codecs import getwriter
    sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import debug_routines as dbu
import progpad
from magiokis_page import Pagina

def main():
    form = cgi.FieldStorage()
    ## dbu.showkeys(form)
    ## return
    mp = Pagina({
        "sectie": form.getfirst("section", "OW"),
        "subsectie": form.getfirst("subsection", "Home"),
        "selitem": form.getfirst("item", '1'),
        "selid": form.getfirst("id", '1'),
        "trefwoord": form.getfirst("trefwoord", 'init'),
        "tekstid": form.getfirst("tekstnr", '-1')
        })
    print("Content-Type: text/html")     # HTML is following
    if len(mp.regels) == 1:
        print(mp.regels[0]) # .encode('latin-1'))
        print('')
    else:
        print('')
        for x in mp.regels:
            print(x) # .encode('latin-1')

if __name__ == '__main__':
    main()

