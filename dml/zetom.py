import xml.etree.ElementTree as ET
import sys,os

def zetom(bron,doel):
    if bron.text is not None:
        doel.text = bron.text
    for x in list(bron):
        y = ET.SubElement(doel,'span')
        y.set("class",x.tag)
        zetom(x,y)

def main(fnaam):
    print "start"
    tree = ET.ElementTree(file=fnaam)
    root = tree.getroot()
    onaam = os.path.splitext(fnaam)[0] + '.html'

    newroot = ET.Element('span')
    newroot.set("class",root.tag)
    zetom(root,newroot)
    out = ET.ElementTree(newroot)
    out.write(file=sys.stdout)
    print "einde"

if __name__ == "__main__":
    main('tocs.xml')