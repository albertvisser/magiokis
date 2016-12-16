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
    args = {"wat": "wijzigopname"}
    test = form.getfirst("song", '')
    if test:
        args["songid"] = test
    else:
        fout = "geensong"
    test = form.getfirst("opname", '')
    if test:
        args["opnid"] = test
    elif fout == "ok":
        fout = "geenopname"
    test =
    updateform = True if "update" in form else False
    args["edit"] = updateform
    if updateform:
        test = form.getfirst("Plaats", '')
        if test:
            args["plaatscode"] = test
        elif fout == "ok":
            fout = "geenplaats"
        test = form.getfirst("Datum", '')
        if test:
            args["datumcode"] = test
        elif fout == "ok":
            fout = "geendatum"
        args["bezetcode"] = form.getfirst("Bezet", '')
        args["instcodes"] = form.getfirst("Instcodes", '')
        args["urlregel"] = form.getfirst("Url", '')
        args["commentaar"] = form.getfirst("Opm", '')
    args["fout"] = fout
    print("Content-Type: text/html\n")     # HTML is following
    h = Songs(args)
    for x in h.regels:
        print(x)

if __name__ == '__main__':
	main()
