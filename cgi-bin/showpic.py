#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" ShowPicture.py: toon plaatje in standaard formaat in html pagina
in plaats van linken naar url van plaatje zelf

eerste argument is een of meer urls gescheiden door ; (picture)
tweede argument is paginavolgummer (seq)
kijken of de picture-variabele meer urls bevat
zo nee, gewoon doorgaan
zo ja, kijken naar waarde voor paginavolgnummer en de zoveelste url eruit halen
    dan bovendien buttons toevoegen
        waarmee gebladerd kan worden naar eerste, vorige, volgende, laatste

bijvoorbeeld:
http://www.magiokis.nl/cgi-bin/showpic.py?
    picture=blz09.jpg:blz10.jpg:blz11.jpg:blz12.jpg&
    pad=/home/albert/magiokis/data/mmap

"""
import cgi
import cgitb
cgitb.enable()
from progpad import httproot, http_cgipad, dataroot

def main():
    #   initialisatie
    form = cgi.FieldStorage()
    form_ok = 0
    ok = "ok"
    pic = form.getfirst("picture", '')
    if not pic:
        ok = "nopic"
    pad = form.getfirst("pad", '')
    if not pad and ok == 'ok':
        ok = "nopath"
    volgnr = int(form.getfirst("seq", '0'))
    if not volgnr:
        volgnr = 1
    print("Content-Type: text/html\n")     # HTML is following
    if ok == "ok":
        if ':' in pic:
            pics = pic.split(':')
            picc = pics[volgnr - 1]
            multipage = True
            aantal = len(pics)
        else:
            aantal = 1
            multipage = False
            picc = pic
        print('<html><head><meta http-equiv="Content-Type" content="text/html"'
            ' charset="utf-8" /><link rel="stylesheet" href="%smagiokis.css"'
            ' type="text/css" /><title>Picture</title></head><body>' % httproot)
##        print multipage, volgnr, aantal
        if multipage:
            if volgnr > 1:
                print('<a href="showpic.py?picture=%s&pad=%s&seq=1" class="back">'
                    'eerste blad</a>&nbsp;' % (pics[0], pad))
                h = volgnr - 1
                print('<a href="showpic.py?picture=%s&pad=%s&seq=%s" class="back">'
                    'vorige blad</a>&nbsp;' % (pics[h-1], pad, str(h)))
            else:
                print('<span class="back">dit is het eerste blad</span>&nbsp;')
                print('<span class="back">geen vorig blad</span>&nbsp;')
            if volgnr < aantal:
                h = volgnr + 1
                print('<a href="showpic.py?picture=%s&pad=%s&seq=%s" class="back">'
                    'volgende blad</a>&nbsp;' % (pics[h-1], pad, str(h)))
                print('<a href="showpic.py?picture=%s&pad=%s&seq=%s" class="back">'
                    'laatste blad</a>&nbsp;' % (pics[aantal-1], pad, str(aantal)))
            else:
                print('<span class="back">geen volgend blad</span>&nbsp;')
                print('<span class="back">dit is het laatste blad</span>&nbsp;')
        print('<img src="%s/%s" border="0" width="800" height="1072" alt="%s" />'
            '</body></html>' % (pad, picc, picc))
    else:
        print("<html><head></head><body>{}</body></html>".format(ok))

if __name__ == '__main__':
    main()
