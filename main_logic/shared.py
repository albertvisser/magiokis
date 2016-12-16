# Magiokis globals, o.a. het pad voor de xml data
import sys
import os

root = os.path.dirname(os.path.dirname(__file__)) # was "/home/albert/www"
htmlroot = os.path.join(root, 'html') # was os.path.join(root,"magiokis")
cgipad = os.path.join(root,'cgi-bin') # was os.path.join(root,"cgi-bin/magiokis")

docroot = "/home/albert/magiokis/data" # blijft zo
htmlpad = os.path.join(docroot, "content")
dmlroot = os.path.join(root, 'dml') # pad naar de dml-programmatuur
sys.path.append(dmlroot)

httproot = "http://original.magiokis.nl/"
httppad = httproot
http_cgipad = httproot + "cgi-bin/"
http_picpad = httproot + "images/"

datapad = "http://data.magiokis.nl/"
xmlpad = datapad
tekstpad = datapad + 'zing/'
mp3pad = datapad + "mp3/"
artpad= datapad + "artwork/"
