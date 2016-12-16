# -*- coding: utf-8 -*-
import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from dicht_datapad import trefwoordenfile

class FindJaar(ContentHandler):
    def __init__(self, jaar=None):
        if jaar is None:
            self.maaklijst = True
            self.jaren = []
        else:
            self.maaklijst = False
            self.jaar = jaar

    def startElement(self, name, attrs):
        if name == 'jaar':
            t = attrs.get('id', None)
            if self.maaklijst:
                self.jaren.append(t)
            else:
                if t == self.jaar:
                    self.laatste = attrs.get('laatste', '0')

def jarenlijst(item=None):
    "lijst alle jaren"
    jaren = []
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = FindJaar()
    parser.setContentHandler(dh)
    parser.parse(trefwoordenfile)
    jaren = dh.jaren
    return jaren

class NwJaar(XMLGenerator):
    def __init__(self, jaar, fn):
        self.fh = open(fn,'w')
        self.jaar = jaar
        self.foundjaar = False
        XMLGenerator.__init__(self, self.fh)

    def startElement(self, name, attrs):
        if name == 'jaar':
            t = attrs.get('id', None)
            if t == self.jaar:
                self.foundjaar = True
        XMLGenerator.startElement(self, name, attrs)

    def endElement(self,name):
        if name == 'jaren':
            if not self.foundjaar:
                self._out.write("  <jaar id='%s' />\n  " % self.jaar)
        XMLGenerator.endElement(self, name)

    def endDocument(self):
        self.fh.close()

def add_jaar(jaar):
    "jaar toevoegen aan lijst alle jaren"
    fn = trefwoordenfile
    fno = '_old'.join(os.path.splitext(fn))
    shutil.copyfile(fn, fno)
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = NwJaar(jaar, fn)
    parser.setContentHandler(dh)
    parser.parse(fno)

class FindItem(ContentHandler):
    """item = None: maakt een lijst met alle trefwoorden
    item = None en zoek = value: idem voor een bepaalde song
    item = value: maakt een lijst met alle tekstrefs bij trefwoord
    """
    def __init__(self, item, zoek):
        self.search_item = item
        self.maaklijst = self.zoeklijst = False
        if self.search_item is None:
            self.maaklijst = True
            self.search_this = zoek
            if self.search_this is not None:
                self.zoeklijst = True
        else:
            self.search_item = item
        ## self.in_trefwoord = self.in_tekstref = False
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
        elif name == 'gedicht':
            if self.founditem or self.zoeklijst:
                jaar = attrs.get('jaar', None)
                id = attrs.get('id', None)
                self.tekstref = (jaar, id)

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
        elif name == 'gedicht':
            if self.founditem:
                self.tekstrefs.append(self.tekstref)
            if self.zoeklijst:
                if self.tekstref == self.search_this:
                    self.gevonden = True

def trefwoordenlijst(item=None):
    """lijst alle trefwoorden (eventueel bij opgegeven tekst"""
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = FindItem(None, item)
    parser.setContentHandler(dh)
    parser.parse(trefwoordenfile)
    if item is None:
        return dh.trefwoorden, []
    else:
        return dh.nietdezetekst, dh.dezetekst

class UpdateItem(XMLGenerator):
    "lijst met tekstrefs bij trefwoord updaten"
    def __init__(self, item):
        self.sh = item
        self.search_item = self.sh.id
        self.tekstrefs = self.sh.tekstrefs
        self.fh = open(self.sh.fn,'w')
        self.founditem = self.itemfound = False
        XMLGenerator.__init__(self, self.fh)

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
            XMLGenerator.characters(self,ch)

    def endElement(self, name):
        if not self.founditem:
            if name == 'trefwoorden':
                if not self.itemfound:
                    self._out.write("  ")
                    self.startElement("trefwoord",{"id": self.sh.id})
                    self._out.write("\n    ")
                    self.endElement("trefwoord")
                    self._out.write("\n")
            XMLGenerator.endElement(self, name)
        else:
            if name == 'trefwoord':
                for x in self.tekstrefs:
                    self._out.write('\n        ')
                     ## self._out.write('  <gedicht jaar="%s" id="%s" />\n' % x)
                    self.startElement("gedicht",{"jaar": x[0], "id": x[1]})
                    self.endElement("gedicht")
                XMLGenerator.endElement(self, name)
                self.founditem = False

    def endDocument(self):
        self.fh.close()

class Trefwoord(object):
    """lijst alle tekstrefs bij een bepaald trefwoord"""
    def __init__(self,id):
        self.id = id
        self.fn = trefwoordenfile
        self.fno = '_old'.join(os.path.splitext(self.fn))
        ## self.trefwoord = ""
        self.tekstrefs = []
        self.found = False

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindItem(str(self.id), None)
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            self.tekstrefs = dh.tekstrefs

    def write(self):
        shutil.copyfile(self.fn,self.fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateItem(self)
        parser.setContentHandler(dh)
        parser.parse(self.fno)

    def add_ref(self,item):
        "voeg een tekstref toe aan self.Tekstrefs"
        self.tekstrefs.append(item)

    def rem_ref(self,item):
        "haal een tekstref weg uit self.Tekstrefs"
        try:
            self.tekstrefs.remove(item)
        except ValueError:
            pass

