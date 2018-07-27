# -*- coding: utf-8 -*-

import os
import sys
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "main_logic"))
htmlroot = os.path.join(root, "html") # was htmlroot = "/home/albert/magiokis"
html_datapad = os.path.join(root, 'data') # html_datapad = os.path.join(htmlroot, 'data')

httproot = "http://original.magiokis.nl/"
http_cgipad = httproot + 'cgi-bin/'
http_datapad = httproot + 'data/' # of moet dit data.magiokis.nl zijn?
dataroot = "http://data.magiokis.nl/"

