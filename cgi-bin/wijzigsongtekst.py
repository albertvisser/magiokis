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
    fout = "ok"
    args = {"wat": "wijzigsongtekst"}
    test = form.getfirst("song", '')
    if test:
        args["songid"] = test
    else:
        fout = "geensong"
    args["fnaam"] = form.getfirst("fnaam", '')
    args["edit"] = True if "update" in form else False
    if args["edit"]:
        test = form.getfirst("titel", '')
        if test:
            args["songtitel"] = test
        elif fout == "ok":
            fout = "geentitel"
        args["filenm"] = form.getfirst("filenm", '')
        args["tekst"] = form.getfirst("tekst", '')
    args["fout"] = fout

    print("Content-Type: text/html\n")     # HTML is following
    h = Songs(args)
    for x in h.regels:
        print(x)

if __name__ == '__main__':
	main()
