# -*- coding: utf-8 -*-

import cgi

def showkeys(form):
    print("Content-Type: text/html")     # HTML is following
    print('')
    print("<html><head></head><body>")
    keys = form.keys()
    keys.sort()
    print("<H3>Form Contents:</H3>")
    if not keys:
        print("<P>No form fields.")
    else:
        print("<DL>")
        for key in keys:
            print("<DT>{}:".format(cgi.escape(key), end=","))
            value = form[key]
            print("<i>{}</i>{}<DD>".format(cgi.escape(str(type(value))),
                cgi.escape(str(value))))
        print("</DL>")
    print("</body></html>")

def showargs(args):
    print('<html><head></head><body>')
    keys = args.keys()
    keys.sort()
    for key in keys:
        print('{}: {}<br/>'.format(key, args[key]))
    print('</body></html>')
