#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import cgi
import cgitb
cgitb.enable()
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
from debug_routines import showkeys
import progpad
from vertel_main import Select

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    ## showkeys(form)
    ## return

    data = {}
    select = form.getfirst("rbsel", '')
    test = form.getfirst("hDo", '')
    if test and not select:
        select = test
    test = form.getfirst("lbSelCat", '')
    if test:
        data["cat"] = test
        if not select:
            select = "selCat"
    test = form.getfirst("txtZoek", '')
    if test:
        data["zoek"] = test
        if not select:
            select = "selZoek"
    test = form.getfirst("txtNweCat", '')
    if test:
        data["cat"] = test
        if not select:
            select == "nweCat"
    data["select"] = select
    l = None
    test = form.getfirst("txtUser", '')
    if test:
        data["user"] = test
    test = form.getfirst("hUser", '')
    if test:
        data["user"] = test
    l = Select(data)

    print("Content-Type: text/html")     # HTML is following
    if l == None:
        print('\n<h1>Fout in aanroep:<br/></h1>U heeft geen usernaam opgegeven<br/>'
            '<input type="button" value="Terug" onclick="history.go(-1)"/>')
    elif len(l.regels) == 1:
        print(l.regels[0])
        print()                             # blank line, end of headers
    else:
        print()                             # blank line, end of headers
        if len(l.regels) == 0:
            print("Er is iets misgegaan...")
        else:
            for x in l.regels:
                print(x)

if __name__ == '__main__':
	main()





