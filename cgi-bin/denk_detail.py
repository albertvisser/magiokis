#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# nog aanpassen: naast trefwoord(en) opvoeren bij tekst ook tekst(id) opvoeren bij trefwoord
import cgi
import cgitb
cgitb.enable()
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
from debug_routines import showkeys
import progpad
from denk_main import Denk

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    ## showkeys(form)
    ## return

    args = {}
    selitem = form.getfirst("lbSelItem", '')
    if selitem:           # we komen vanuit selectie
        args = {"wat": "detail", "selItem": selitem}
    else:
        selitem = form.getfirst("hselItem", '')
        if selitem:          # we komen vanuit updaten tekst
            args = {"wat": "detail_wijzig", "selItem": selitem,
                "titel": form.getfirst("txtTitel", ''),
                "tekst": form.getfirst("txtTekst", ''),
                "trefw": form.getfirst("txtTrefw", '')
                }
    print("Content-Type: text/html\n")     # HTML is following
    l = Denk(args)
    for x in l.regels:
        ## try:
        print(x)
        ## except UnicodeEncodeError:
            ## print(x.encode('utf-8').decode('utf-8'))

if __name__ == '__main__':
	main()
