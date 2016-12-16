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
    args = {"wat": "detail"}
    print("Content-Type: text/html\n")     # HTML is following
    songid = form.getfirst("song", '')
    if songid:
        args["songid"] = songid
        if "wijzigO" in form:
            args["wijzigO"] = True
        h = Songs(args)
        if len(h.regels) == 0:
            print("<html><head></head><body>Er komt geen html terug</body></html>")
        else:
            for x in h.regels:
                try:
                    print(x) # .encode('latin-1')
                except UnicodeEncodeError:
                    print(x.encode('latin-1'))
    else:
        print("<html><head></head><body>Geen song-id opgegeven</body></html>")

if __name__ == '__main__':
	main()


