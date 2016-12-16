#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import cgi
import cgitb
cgitb.enable()
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
from debug_routines import showkeys
import progpad
from vertel_main import Detail

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    ## showkeys(form)
    ## return

    sel_item = form.getfirst("lbSelItem", '')
    sel_hs = form.getfirst("selHoofdstuk", '')
    chg_hs = form.getfirst("hselHs", '')
    titel = form.getfirst("hTitel", '')
    if sel_item:           # we komen vanuit selectie
        args = {"doe": "selTekst",
            "user": form.getfirst("hUser", ''),
            "van": form.getfirst("hVan", ''),    #-- t.b.v. terug naar selectie
            "selId": sel_item}
    elif sel_hs:        # we komen vanuit kies hoofdstuk
        args = {"doe": "selHs",
            "user": form.getfirst("hUserH", ''), # hier moet typesel doorgegeven zijn tbv. terugkeer naar selectie
            "selId": form.getfirst("hselIdH", ''),
            "selH": sel_hs}
    elif chg_hs:          # we komen vanuit wijzig hoofdstuk
        args = {"doe": "wijzigTxt",
            "user": form.getfirst("hUserT", ''),
            "selId": form.getfirst("hselIdT", ''),
            "selHs": int(chg_hs),
            "HsTitel": form.getfirst("titel2", ''),
            "HsTekst": form.getfirst("txtHoofdstuk", '')}
    elif titel:          # we komen vanuit updaten tekst
        args = {"doe": "wijzigVh",
            "user": form.getfirst("hUser", ''),
            "selId": form.getfirst("hId", ''),
            "selHs": int(form.getfirst("hHs", '-1')),
            "titel": titel,
            "selItem": form.getfirst("hselItem", ''),
            "selCat": form.getfirst("lbSelCat", '')}
    else:
        args = {"doe": "nieuw",
            "selId": '0',
            "user": form.getfirst("hUser", ''),
            "selCat": form.getfirst("hNwInCat", '')}
    print("Content-Type: text/html")    # HTML is following
    ## print
    ## for x, y in args.items():
        ## print('<p>{}: {}</p>'.format(x, y))
    ## return
    l = Detail(args)
    if len(l.regels) == 1:
        print(l.regels[0])
        print('')                               # blank line, end of headers
    else:
        print('')                               # blank line, end of headers
        ## sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
        for x in l.regels:
            print(x)

if __name__ == '__main__':
    main()
