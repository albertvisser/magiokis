# -*- coding: utf-8 -*-
import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from dicht_trefw import add_jaar, trefwoordenlijst, jarenlijst
from dicht_datapad import xmlpad
nieuwjaarxml = """\
<?xml version='1.0' encoding='iso-8859-1' ?>
<?xml-stylesheet href='http://dicht.magiokis.nl/dicht.css' type='text/css' ?>
<gedichten>
  <laatste id='0' />
</gedichten>
"""

class FindList(ContentHandler):
    "Bevat alle gedichten van een bepaald jaar (item == None)"
    "of alle gedichten met een zoektekst"
    "als er geen titel is moeten we de eerste regel hiervoor gebruiken"
    def __init__(self, item=None, seltitel=False, seltext=False):
        if item is None:
            self.geef_alles = True
        else:
            self.search_item = item
            self.sel_titel = seltitel
            self.sel_tekst = seltext
            self.geef_alles = False
        # Initialize the flags to false
        self.id_titels = []
        self.titel = self.tekst = ""
        self.in_titel = self.in_tekst = False
        self.in_trefwoord = self.in_regel = False
        self.founditem = self.itemfound = False

    def startElement(self, name, attrs):
        if name == 'gedicht':
            item = attrs.get('id', None)
            self.deze_item = [ item ]
            self.titel = self.tekst = ""
            self.in_titel = self.in_tekst = False
            self.in_trefwoord = self.in_regel = False
            self.got_titel = False
##            self.trefwoorden = []
##            self.alineas = []
        elif name == 'titel':
            self.in_titel = True
            self.got_titel = True
        elif name == 'tekst':
            self.in_tekst = True
##        elif name == 'trefwoord':
##            self.in_trefwoord = 1
##            self.trefwoord = ""
        elif name == 'regel':
            self.in_regel = True
            self.regel = ""
            if not self.got_titel:
                self.got_titel = True

    def characters(self, ch):
        if self.in_titel:
            self.titel += ch
        if self.in_tekst:
            self.tekst += ch
##        elif self.in_trefwoord:
##            self.trefwoord += ch
        elif self.in_regel:
            self.regel += ch

    def endElement(self, name):
        if name == 'gedicht':
            if self.geef_alles:
                self.deze_item.append(self.titel)
                self.id_titels.append(self.deze_item)
            else:
                oktoappend = False
                if self.sel_titel:
                    if self.titel != "":
                        if self.search_item.upper() in self.titel.upper():
                            oktoappend = True
                if self.sel_tekst:
                    if self.tekst != "":
                        if self.search_item.upper() in self.tekst.upper():
                            oktoappend = True
                if oktoappend:
                    self.deze_item.append(self.titel)
                    self.id_titels.append(self.deze_item)
        elif name == 'titel':
            if self.in_titel:
                self.in_titel = False
        elif name == 'tekst':
            if self.in_tekst:
                self.in_tekst = False
##        elif name == 'trefwoord':
##            if self.in_trefwoord:
##                self.in_trefwoord = False
##                self.trefwoorden.append(self.trefwoord)
        elif name == 'regel':
            if self.in_regel:
                self.in_regel = False
                if not self.got_titel:
                    self.titel = "(" + self.regel + ")"

class DichtLijst(object):
    """lijst alle gedichten van een bepaald jaar of met een bepaalde zoektekst
    lijst alle gedicht's: id en titel
    object DichtZoek: zoek de gedichts met een bepaalde string in de titel
    object DichtZoekT: zoek de gedichts met een bepaalde string in de tekst"""
    def __init__(self, jaar=None, item=None, type=None):
        id_titels = []
        self.search_item = item
        self.search_type = type
        if jaar is not None:  # item and type should be None
            if item is None and type is None:
                self.fn = os.path.join(xmlpad, 'Dicht_{}.xml'.format(jaar))
                self.parse()
                for y in self.item_list.id_titels:
                    y.insert(0, jaar)
                    id_titels.append(y)
        else:
            dh = jarenlijst()
            if len(dh) > 0:
                for x in dh:
                    self.fn = os.path.join(xmlpad, 'Dicht_{}.xml'.format(x))
                    self.parse()
                    for y in self.item_list.id_titels:
                        y.insert(0, x)
                        id_titels.append(y)
        self.id_titels = []
        for x in id_titels:
            e = []
            for y in x:
                e.append(y) # .encode('ISO-8859-1'))
            self.id_titels.append(e)

    def parse(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        if self.search_item == None:
            dh = FindList()
        elif self.search_type == "selTitel":
            dh = FindList(self.search_item, seltitel=True)
        elif self.search_type == "selTekst":
            dh = FindList(self.search_item, seltext=True)
        elif self.search_type == "selBeide":
            dh = FindList(self.search_item, seltitel=True, seltext=True)
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.item_list = dh

class FindItem(ContentHandler):
    "Bevat de gegevens van een bepaald gedicht: Titel, Tekst, gedicht"
    def __init__(self, item):
        self.search_item = item
        # Initialize the flags to false
        self.in_titel = self.in_tekst = self.in_regel = False
        self.titel = self.tekst = ""
        self.id_titels = []
        ## self.trefwoorden = []
        self.gedicht = []
        self.founditem = self.itemfound = False

    def startElement(self, name, attrs):
        if name == 'gedicht':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = True
        elif name == 'titel':
            if self.founditem:
                self.in_titel = True
                self.titel = ""
        elif name == 'tekst':
            if self.founditem:
                self.in_tekst = True
                self.tekst = ""
        elif name == 'couplet':
            if self.founditem:
                if len(self.gedicht) > 0:
                    self.gedicht.append('')
        elif name == 'regel':
            if self.founditem:
                self.in_regel = True
                self.regel = ""

    def characters(self, ch):
        if self.in_titel:
            self.titel +=  ch
        elif self.in_tekst:
            if ch[:1] == " ":
                self.tekst += "" + ch.strip()
            else:
                self.tekst += ch
##        elif self.inTrefwoordContent:
##            self.Trefwoord = self.Trefwoord + ch
        elif self.in_regel:
            self.regel += ch

    def endElement(self, name):
        if name == 'gedicht':
            if self.founditem:
                self.itemfound = True
                self.founditem = False
        elif name == 'titel':
            if self.in_titel:
                self.in_titel = False
        elif name == 'tekst':
            if self.in_tekst:
                self.in_tekst = False
                if self.tekst[0] == "\n":
                    self.tekst = self.tekst[1:]
                self.tekst = self.tekst.strip()
#                self.Tekst = self.Tekst.rstrip()
                if self.tekst[-1] == "\n":
                    self.tekst = self.tekst[:-1]
        ## elif name == 'trefwoord':
            ## if self.in_trefwoord:
                ## self.in_trefwoord = 0
                ## self.trefwoorden.append(self.trefwoord)
        elif name == 'regel':
            if self.in_regel:
                self.in_regel = 0
                self.gedicht.append(self.regel)

class UpdateItem(XMLGenerator):
    "denktekst updaten"
    # aan het eind zit een element genaamd laatste. Als het id van de tekst hoger is dan deze, dan laatste aanpassen.
    "schrijf tekst weg in XML-document"
    def __init__(self, item):
        self.dh = item
        self.search_item = self.dh.id
        self.fh = open(self.dh.fn,'w')
        self.founditem = self.itemfound = False
        self.dontwrite = False
        XMLGenerator.__init__(self,self.fh)

    def startElement(self, name, attrs):
    #-- kijk of we met de te wijzigen tekst bezig zijn
        if name == 'gedicht':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = self.itemfound = True
        elif name == 'laatste':
            self.laatste = attrs.get('id', None)
        #-- xml element (door)schrijven
        if not self.founditem:
            if name != 'laatste':
                XMLGenerator.startElement(self, name, attrs)
        else:
            if name == 'gedicht':
                XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if not self.founditem:
            if not self.dontwrite:
                XMLGenerator.characters(self,ch)

    def endElement(self, name):
        if name == 'laatste':
            dontwrite = False
        elif name == 'gedichten':
            if not self.itemfound:
                self.startElement("gedicht", {"id": self.dh.id})
                self.endElement("gedicht")
                self._out.write("\n  ")
                self.laatste = self.dh.id
            self._out.write('  <laatste id="%s" />\n' % self.laatste)
            self._out.write('</gedichten>\n')
        elif name == 'gedicht':
            if not self.founditem:
                self._out.write('</gedicht>')
            else:
                self._out.write("\n")
                if self.dh.titel != "":
                    self._out.write('    <titel>%s</titel>\n' % self.dh.titel)
                if self.dh.tekst != "":
                    self._out.write('    <tekst>\n%s\n    </tekst>\n' % self.dh.tekst)
                if len(self.dh.gedicht) > 0:
                    self._out.write('    <couplet>\n')
                    for x in self.dh.gedicht:
                        if x == "":
                            self._out.write('    </couplet>\n')
                            self._out.write('    <couplet>\n')
                        else:
                            self._out.write('      <regel>%s</regel>\n' % x)
                    self._out.write('    </couplet>\n')
                ## for x in self.dh.trefwoorden:
                    ## self._out.write('    <trefwoord>%s</trefwoord>\n' % x)
                self._out.write('  </gedicht>')
                self.founditem = False
        elif not self.founditem:
            XMLGenerator.endElement(self, name)

    def endDocument(self):
        self.fh.close()

class FindLaatste(ContentHandler):
    def __init__(self):
        self.laatste = 0

    def startElement(self, name, attrs):
        if name == 'laatste':
            t = attrs.get('id', None)
            self.laatste = t

class DichtItem(object):
    """lijst alle gegevens van een bepaald 'gedicht'-item

    zoek een gedicht met een bepaald id en maak een lijst
    van alle trefwoorden en alinea's"""
    def __init__(self, jaar, id_="0"):
        self.fn = os.path.join(xmlpad, 'Dicht_{}.xml'.format(jaar))
        self.jaar = jaar
        self.id = id_
        if id_ == "0":
            self.new()
        self.fno = '_old'.join(os.path.splitext(self.fn))
        self.fnn = '_new'.join(os.path.splitext(self.fn))
        self.titel = ""
        self.trefwoorden = []
        self.tekst = ""
        self.gedicht = []
        self.found = 0

    def new(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindLaatste()
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.id = str(int(dh.laatste) + 1)

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindItem(str(self.id))
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            self.titel = dh.titel # .encode('ISO-8859-1')
            self.tekst = dh.tekst # .encode('ISO-8859-1')
            for x in dh.gedicht:
                self.gedicht.append(x) # .encode('ISO-8859-1'))
            # trefwoorden worden niet  bij het gedicht opgeslagen maar bij het trefwoord.
            # hiervoor moeten we een trefwoodenlijst ophalen
            for x in trefwoordenlijst((self.jaar, self.id))[1]:
                self.trefwoorden.append(x) # .encode('ISO-8859-1'))

    def write(self):
        shutil.copyfile(self.fn, self.fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateItem(self)
        parser.setContentHandler(dh)
        parser.parse(self.fno)

    def add_trefw(self, item):
        "voeg een trefwoord toe aan self.Trefwoorden"
        self.trefwoorden.append(item)

    def rem_trefw(self, item):
        "haal een trefwoord weg uit self.Trefwoorden"
        try:
            self.trefwoorden.remove(item)
        except ValueError:
            pass

    ## def wijzig_gedicht(self, item):
        ## self.gedicht = []
        ## for x in item:
            ## self.gedicht.append(x)

def nieuw_jaar(jaar):
    fn = os.path.join(xmlpad, 'Dicht_{}.xml'.format(jaar))
    if not os.path.exists(fn):
        with open(fn, 'w') as f:
            f.write(nieuwjaarxml)
    add_jaar(jaar)
