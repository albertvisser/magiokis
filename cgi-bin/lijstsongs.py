#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import progpad
from songs_main import Songs

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    print("Content-Type: text/html")     # HTML is following
    h = Songs({"wat": "lijstsongs", "select": form.getfirst("select", ''),
        "soortsel": form.getfirst("soortsel", '')})
    if len(h.regels) == 1:
        print(h.regels[0])
        print()
    elif len(h.regels) > 0:
        print()                               # blank line, end of headers
        for x in h.regels:
            try:
                print(x) # .encode('latin-1')
            except UnicodeEncodeError:
                print(x.encode('latin-1'))

if __name__ == '__main__':
    main()


