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
    print()                               # blank line, end of headers
    h = Songs({"wat": "lijstregs", "select": form.getfirst("select", '')})
    for x in h.regels:
        print(x) # .encode('latin-1')

if __name__ == '__main__':
    main()



