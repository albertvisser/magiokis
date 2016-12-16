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
    args = {"wat": "wijzigdetails"}
    songid = form.getfirst("song", '')
    if not songid:
        fout = "geensong"
    args['songid'] = songid
    args["edit"] = True if "update" in form else False
    if args["edit"]:
        test = form.getfirst("Titel", '')
        if test:
            args["songtitel"] = test
        elif fout == "ok":
            fout = "geentitel"
        test = form.getfirst("Datering", '')
        if test:
            args["datering"] = test
        elif fout == "ok":
            fout = "geendatum"
        args["auteurval"] = form.getfirst("Tekst", '')
        args["makerval"] = form.getfirst("Muziek", '')
        args["commentaar"] = form.getfirst("Opmerkingen", '')
    args["fout"] = fout
    print("Content-Type: text/html\n")     # HTML is following
    f = Songs(args)
    for x in f.regels:
        print(x)

if __name__ == '__main__':
	main()
