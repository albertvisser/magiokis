import os
from xml.etree.ElementTree import Element, SubElement, ElementTree
import common
## from datapad import *  # xmlpad en de exceptions DataError en FoundItem

def write_pl(track, titel=""):
    if titel == "": titel = "(untitled)"
    x1 = Element("playlist", version="0", xmlns="http://xspf.org/ns/0/")
    x2 = SubElement(x1, "title")
    x2.text = titel
    x3 = SubElement(x1, "trackList")
    x4 = SubElement(x3, "track")
    x5 = SubElement(x4, "location")
    x5.text = os.path.join(common.mp3pad, track + '.mp3')
    x6 = SubElement(x4, "title")
    x6.text = titel
    h = ElementTree(x1)
    h.write("pl/play_%s.xspf" % track, "UTF-8")

def main():
    con = sqlite.connect(os.path.join(xmlpad, "magiokis.dat"))
    cur = con.cursor()
    c = cur.execute('select opnames.url,songs.titel from opnames,songs '
        'where opnames.song = ?', songs.id)
    data = c.fetchall()
    for x in data:
        write_pl(x[0], x[1])

def more():
    for x in os.listdir(common.mp3pad):
        print('now adding {}...',format(x), end = ' ')
        y = os.path.join(common.root, 'pl', x)
        if os.path.exists(y):
            print('skipping, already exists')
            continue
        y = os.path.splitext(x)[0]
        print('ok')
        write_pl(y)

if __name__ == '__main__':
    ## write_pl('b1_a1','')
    ## main()
    more()
