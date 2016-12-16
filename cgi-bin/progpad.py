# -*- coding: utf-8 -*-

import os
import sys
root = os.path.dirname(os.path.dirname(__file__))
## htmlroot = os.path.join(root, "main_logic") # was htmlroot = "/home/albert/magiokis"
## sys.path.append(htmlroot)
sys.path.append(os.path.join(root, "main_logic"))
html_datapad = os.path.join(root, 'data') # html_datapad = os.path.join(htmlroot, 'data')

httproot = "http://original.magiokis.nl/"
http_cgipad = httproot + 'cgi-bin/'
http_datapad = httproot + 'data/' # of moet dit data.magiokis.nl zijn?
dataroot = "http://data.magiokis.nl/"

# t.b.v. opruimen onnodige zaken
## Gezocht naar 'htmlroot' in opgegeven bestanden/directories
## Gezocht naar 'html_datapad' in opgegeven bestanden/directories
## Gezocht naar 'httproot' in opgegeven bestanden/directories
## Gezocht naar 'http_cgipad' in opgegeven bestanden/directories
## Gezocht naar 'http_datapad' in opgegeven bestanden/directories
## De bestanden staan allemaal in of onder de directory "/home/albert/projects/magiokis/cgi-bin/"

## magiokis_begin.py r. 14 from progpad import htmlroot, http_cgipad
## magiokis_begin.py r. 48         with open(os.path.join(htmlroot,'magiokis_launch.html')) as f_in:

## sendxml.py r. 11 from progpad import http_cgipad, httproot, htmlroot
## sendxml.py r. 29             open(os.path.join(htmlroot, "tempfile.xml"), "w") as f:
## sendxml.py r. 34                         ' type="text/css" ?>' % httproot)
## sendxml.py r. 41                         ' type="text/css" ?>' % httproot)
## sendxml.py r. 45     print("Location: {}tempfile.xml".format(httproot))

## showpic.py r. 23 from progpad import httproot, http_cgipad, dataroot
## showpic.py r. 52             ' type="text/css" /><title>Picture</title></head><body>' % httproot)

## showxml.py r. 12 from progpad import http_cgipad, http_datapad, httproot, html_datapad, htmlroot
## showxml.py r. 21         httproot,cssdic[srt.lower()])
## showxml.py r. 44             with open(os.path.join(htmlroot,"tempfile.xml"),"w") as f:
## showxml.py r. 52         print("Location: {}tempfile.xml".format(httproot))

## Het belangrijkste waar ik progpad.py voor gebruik is kennelijk om op 1 plek
## vast te leggen welk pad er aan sys.path moet worden toegevoegd
