#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Magiokis_Begin.py: controleert aanloggegevens voor Magiokis database
"""
import os
import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)

from progpad import htmlroot, http_cgipad
#~ from Magiokis_User import User

def main():
    form = cgi.FieldStorage()
    form_ok = 0

    ok = "ok"
    user = ""
    #~ paswd = ""
    #~ if form.has_key("userid"):
        #~ user = form.getfirst("userid", '')
        #~ if form.has_key("passwd"):
            #~ paswd = form.getfirst("passwd", '')
            #~ dh = User(user, paswd)
            #~ if dh.found:
                #~ if ok == ok and dh.paswdok == 0:
                    #~ ok = "Wachtwoord foutief"
            #~ else:
                #~ ok = "Userid onbekend"
        #~ else:
            #~ paswd = ""
            #~ ok = "Geen wachtwoord opgegeven"
    #~ else:
        #~ ok = "Geen userid opgegeven"
    print("Content-type: text/html")
    sel = form.getfirst("rbsel", '')
    if sel:
        print('Location: http://%s.magiokis.nl/' % sel)
        print()
        return
    else:
        ok = "niks opgegeven om te doen"
        print()
        with open(os.path.join(htmlroot,'magiokis_launch.html')) as f_in:
            for x in f_in:
                y = x.rstrip()
                if 'id="userid"' in y:
                    if user != "":
                        y = y.replace('id="userid"',('value="%s" id="userid"' % user))
                elif 'id="meld"' in y:
                    y = y.replace('&nbsp;',ok)
                print(y)

if __name__ == '__main__':
	main()
