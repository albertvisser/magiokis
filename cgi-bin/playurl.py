#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""bijvoorbeeld: http://www.magiokis.nl/cgi-bin/playurl.py?type=MID&id=126"""
import cgi
import cgitb
cgitb.enable()
import progpad
from songs_main import Songs

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    args = {"wat": "afspelen"}
    print("Content-Type: text/html")     # HTML is following
    id_ = form.getfirst("id", '')
    if id_:
        args["id"] = id_
        args["type"] = form.getfirst("type", '').lower()
        args["titel"] = form.getfirst("titel", '')
        h = Songs(args)
        if len(h.regels) == 0:
            print() # blank line, end of headers
            print("<html><head></head><body>Er komt geen html terug</body></html>")
        else:
            for x in h.regels: # is eigenlijk maar 1 regel: de redirect
                print(x)
            print() # blank line, end of headers
    else:
        print() # blank line, end of headers
        print("<html><head></head><body>Geen song-id opgegeven</body></html>")

if __name__ == '__main__':
    main()
