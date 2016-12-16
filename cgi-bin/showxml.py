#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""SendXML.py
stuur het gekozen xml-document terug
"""
import sys
import os
import cgi
import cgitb
cgitb.enable()
from progpad import http_cgipad, http_datapad, httproot, html_datapad, htmlroot

def sendxml(srt, docnaam, f=sys.stdout):
    gotstyle = False
    cssdic = {"act":"toneelstuk.css",
        "zing":"songtekst.css",
        "dicht":"dicht.css",
        "vertel":"vertel.css"}
    styleregel = '<?xml-stylesheet href="{}style/{}" type="text/css" ?>'.format(
        httproot,cssdic[srt.lower()])
    for x in file(docnaam):
        if "?xml" in x:
            if "xml-stylesheet" in x:
                f.write(styleregel)
                gotstyle = True
            else:
                f.write(x)
        else:
            if not gotstyle:
                f.write(styleregel)
                gotstyle = True
            f.write(x)

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    form_ok = False
    section = form.getfirst("type", '')
    if section:
        docnaam = form.getfirst("url", '')
        if docnaam:
            form_ok = True
            with open(os.path.join(htmlroot,"tempfile.xml"),"w") as f:
                sendxml(section, docnaam, f)
        else:
            mld = "<H1>No Dice, Matey!</H1><p>You forgot to tell me which document to open.</p>"
    else:
        mld = "<H1>No Dice, Matey!</H1><p>You forgot to tell me what type of document to open.</p>"
    if form_ok:
        print("Content-Type: text/html")      # XML is following
        print("Location: {}tempfile.xml".format(httproot))
        print()                              # blank line, end of headers
    else:
        print("Content-Type: text/html")     # HTML is following
        print()                              # blank line, end of headers
        print("<html><head></head><body>{}</body></html>".format(mld))

if __name__ == '__main__':
    main()

