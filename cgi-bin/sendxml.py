#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SendXML.py: stuur het gekozen xml-document terug
"""

import cgi
import cgitb
cgitb.enable()
from progpad import http_cgipad, httproot, htmlroot

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    dirnaam = form.getfirst("location", '')
    docnaam = form.getfirst("titel", '')
    if not docnaam:
        print("Content-Type: text/html")     # HTML is following
        print()                              # blank line, end of headers
        print("<H1>No Dice, Matey!</H1>")
        print("<p>You forgot to tell me which document to open.</p>")
        return
    if docnaam == 'Kies een verhaal:':
        return
    ## docnaam = docnaam.replace("%20"," ")
    gotstyle = False
    with open(os.path.join(dirnaam,docnaam)) as f_in,
            open(os.path.join(htmlroot, "tempfile.xml"), "w") as f:
        for x in f_in:
            if "?xml"in x:
                if "xml-stylesheet"in x:
                    f.write('<?xml-stylesheet href="%sstyle/songtekst.css"'
                        ' type="text/css" ?>' % httproot)
                    gotstyle = True
                else:
                    f.write(x)
            else:
                if not gotstyle:
                    f.write('<?xml-stylesheet href="%sstyle/songtekst.css"'
                        ' type="text/css" ?>' % httproot)
                    gotstyle = True
                f.write(x)
    print("Content-Type: text/html")      # XML is following
    print("Location: {}tempfile.xml".format(httproot))
    print                               # blank line, end of headers

if __name__ == '__main__':
    main()

