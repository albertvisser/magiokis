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
    args = {"wat": "wijzigtabel"}
    print("Content-Type: text/html\n")     # HTML is following
    tabel = form.getfirst("tabel", '')
    type_ = form.getfirst("hType", '')
    if tabel:
        args["tabnm"] = tabel
        args["edit"] = False
        h = Songs(args)
        for x in h.regels:
            print(x) # .encode('latin-1')
    elif type_:
        args["tabnm"] = type_
        args["edit"] = True
        args["code"] = form.getfirst("txtCode", '') or form.getfirst("hCode", '')
        args["naam"] = form.getfirst("txtNaam", '')
        if tabel == "datum":
            args["waarde"] = form.getfirst("txtWaarde", '')
        h = Songs(args)
        for x in h.regels:
            print(x) # .encode('latin-1')
    else:
        # fout melden
        print("<html><head></head><body>Geen tabel opgegeven</body></html>")

if __name__ == '__main__':
	main()
