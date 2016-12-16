#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import cgi
import cgitb
cgitb.enable()
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
from debug_routines import showkeys
import progpad
from vertel_main import User, Select, process_user

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    ## showkeys(form)
    ## return

    data = {
        "user": form.getfirst("hUser", ''),
        "url":  form.getfirst("txtUrl", ''),
        "pad":  form.getfirst("txtPad", '')
        }
    #~ tzt ook txtWW1 en txtWW2
    s = ""
    for x in form.keys():
        if x.startwith("hId"):
            s = x[4:]
            data["id"] = int(s)
            data["user"] = form.getfirst("hUser{}".format(s), '')
            data["naam"] = form.getfirst("txtCat{}".format(s), '')
            break
    data["meld"] = process_user(data)
    data["select"] = "chgRoot"
    l = Select(data)

    if len(l.regels) == 1:
        print("Content-Type: text/html")     # HTML is following
        print(l.regels[0])
        print()                              # blank line, end of headers
    else:
        print("Content-Type: text/html\n")     # HTML is following
        if len(l.regels) == 0:
            print("Er is iets misgegaan...")
        else:
            for x in l.regels:
                print(x)

if __name__ == '__main__':
	main()





