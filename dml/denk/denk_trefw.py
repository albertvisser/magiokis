# -*- coding: utf-8 -*-

import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from denk_globals import trefwoordenfile

## ELEMENT trefwoorden (trefwoord+)
## ELEMENT trefwoord (tekstref*)
## ATTLIST trefwoord id #REQUIRED
## ELEMENT tekstref #PCDATA
## object TrefwoordenLijst: lijst alle trefwoorden
## object Trefwoord: lijst alle tekstrefs bij een bepaald trefwoord
# maak een class die de trefwoorden tabel uitleest en de items waar de tekst aan hangt in de ene, en die waar
# de tekst niet aan hangt in de andere tabel zet

class FindItem(ContentHandler):
    """
    input = None: maakt een lijst met alle trefwoorden
    input = value: maakt een lijst met alle tekstrefs bij trefwoord"""
    def __init__(self, item, tekst):
        self.search_item = item
        self.maaklijst = False
        self.zoeklijst = False
        if self.search_item is None:
            self.maaklijst = True
            self.search_text = tekst
            if self.search_text is not None:
                self.zoeklijst = True
        else:
            self.search_item = item
        # Initialize the flags to false
        self.in_trefwoord = self.in_tekstref = False
        self.trefwoorden = []
        self.tekstrefs = []
        self.dezetekst = []
        self.nietdezetekst = []
        self.founditem = self.itemfound = False

    def startElement(self, name, attrs):
        if name == 'trefwoord':
            self.item = attrs.get('id', None)
            if self.maaklijst:
                self.trefwoorden.append(self.item)
                if self.zoeklijst:
                    self.gevonden = False
            else:
                if self.item == self.search_item:
                    self.founditem = True
        elif name == 'tekstref':
            if self.founditem or self.zoeklijst:
                self.in_tekstref = True
                self.tekstref = ""

    def characters(self, ch):
        if self.in_tekstref:
            self.tekstref = self.tekstref + ch

    def endElement(self, name):
        if name == 'trefwoord':
            if self.founditem:
                self.itemfound = True
                self.founditem = False
            if self.zoeklijst:
                if self.gevonden:
                    self.dezetekst.append(self.item)
                else:
                    self.nietdezetekst.append(self.item)

        elif name == 'tekstref':
            if self.founditem:
                if self.in_tekstref:
                    self.in_tekstref = False
                    self.tekstrefs.append(self.tekstref)
            if self.zoeklijst:
                if self.tekstref == self.search_text:
                    self.gevonden = True

class UpdateItem(XMLGenerator):
    "lijst met tekstrefs bij trefwoord updaten"
    def __init__(self, item):
        self.sh = item
        self.search_item = self.sh.id
        self.tekstrefs = self.sh.tekstrefs
        self.fh = open(self.sh._fn,'w')
        self.founditem = self.itemfound = False
        XMLGenerator.__init__(self, self.fh, encoding='utf-8')

    def startElement(self, name, attrs):
    #-- kijk of we met de te wijzigen song bezig zijn
        if name == 'trefwoord':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = self.itemfound = True
    #-- xml element (door)schrijven
            XMLGenerator.startElement(self, name, attrs)
        else:
            if not self.founditem:
                XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if not self.founditem:
            XMLGenerator.characters(self, ch)

    def endElement(self, name):
        if not self.founditem:
            if name == 'trefwoorden':
                if not self.itemfound:
                    self._out.write(" ")
                    self.startElement("trefwoord", {"id": self.sh.id})
                    self._out.write("\n ")
                    self.endElement("trefwoord")
                    self._out.write("\n")
            XMLGenerator.endElement(self, name)
        else:
            if name == 'trefwoord':
                self._out.write('\n')
                for x in self.tekstrefs:
                     self._out.write('  <tekstref>%s</tekstref>\n' % x)
                self._out.write('  ')
                XMLGenerator.endElement(self, name)
                self.founditem = False

    def endDocument(self):
        self.fh.close()
        pass

def trefwoordenlijst(item=None):
    "lijst alle tekstrefs bij een bepaald trefwoord"
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = FindItem(None, item)
    parser.setContentHandler(dh)
    parser.parse(trefwoordenfile)
    if item is None:
        return dh.trefwoorden, []
    else:
        return dh.nietdezetekst, dh.dezetekst

class Trefwoord(object):
    "lijst alle tekstrefs bij een bepaald trefwoord"
    def __init__(self,id):
        self.id = id
        self._fn = trefwoordenfile
        self._fno = '_old'.join(os.path.splitext(trefwoordenfile))
        self.trefwoord = self.id
        self.tekstrefs = []
        self.found = False

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindItem(str(self.id), None)
        parser.setContentHandler(dh)
        parser.parse(self._fn)
        self.found = dh.itemfound
        if self.found:
            self.tekstrefs = [x for x in dh.tekstrefs]


    def write(self):
        shutil.copyfile(self._fn,self._fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateItem(self)
        parser.setContentHandler(dh)
        parser.parse(self._fno)

    def add_ref(self, item):
        "voeg een tekstref toe aan self.Tekstrefs"
        self.tekstrefs.append(item)

    def rem_ref(self, item):
        "haal een tekstref weg uit self.Tekstrefs"
        try:
            self.tekstrefs.remove(item)
        except ValueError:
            pass

