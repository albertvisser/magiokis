# -*- coding: UTF-8 -*-
import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from vertel_datapad import xmlpad

class HstFound (Exception):
    pass

class FindItem(ContentHandler):
    "Bevat de gegevens van een bepaald verhaal"
    def __init__(self, hst="", hslist=False):
        self.zoek_hst = self.tel_hst = False
        self.hslist = hslist
        self.aanthst = 0
        if hst != "":
            if isinstance(hst, int):
                self.tel_hst = True
            else:
                self.zoek_hst = True
            self.sel_hst = hst
        self.titel = ""
        self.titel2 = ""
        self.alinea = ""
        self.in_titel = self.in_titel2 = self.in_alinea = False
        self.hoofdstukken = []
        self.founditem = self.itemfound = False

    def startElement(self, name, attrs):
        if name == 'titel':
            self.in_titel = True
            self.titel = ""
        elif name == 'hoofdstuk':
            self.hoofdstuk = []
            self.aanthst += 1
            self.titel2 = ""
        elif name == 'titel2':
            self.in_titel2 = True
        elif name == 'alinea' and not self.hslist:
            self.in_alinea = True
            self.alinea = ""

    def characters(self, ch):
        if self.in_titel:
            self.titel = self.titel + ch
        elif self.in_titel2:
            self.titel2 = self.titel2 + ch
        elif self.in_alinea:
            self.alinea = self.alinea + ch

    def endElement(self, name):
        if name == 'titel':
            if self.in_titel:
                self.in_titel = False
        elif name == 'hoofdstuk':
            if self.zoek_hst:
                if self.titel2 == self.sel_hst:
                    self.hoofdstukken = (self.titel2, self.hoofdstuk)
                    self.itemfound = True
                    # raise HstFound("Genoemd hoofdstuk gevonden")
            elif self.tel_hst:
                if self.aanthst == self.sel_hst:
                    self.hoofdstukken = (self.titel2, self.hoofdstuk)
                    self.itemfound = True
                    # raise HstFound("Hoofdstuknummer gevonden")
            else:
                h = (self.titel2, self.hoofdstuk)
                self.hoofdstukken.append(h)
        elif name == 'titel2':
            if self.in_titel2:
                self.in_titel2 = False
        elif name == 'alinea' and not self.hslist:
            if self.in_alinea:
                self.in_alinea = False
                self.hoofdstuk.append(self.alinea)

class UpdateItem(XMLGenerator):
    "denktekst updaten"
    "schrijf tekst weg in XML-document"
    def __init__(self, item):
        self.dh = item
        self.fh = open(self.dh.fn, 'w')
        self.schrijf = True
        XMLGenerator.__init__(self,self.fh)

    def startDocument(self):
        XMLGenerator.startDocument(self)
        #~ self._out.write('<!DOCTYPE vertel SYSTEM "vertel.dtd">\n')

    def startElement(self, name, attrs):
        if self.schrijf:
            XMLGenerator.startElement(self, name, attrs)
        if name == 'vertel':
            self.schrijf = False

    def characters(self, ch):
        if self.schrijf:
            XMLGenerator.characters(self, ch)

    def endElement(self, name):
        if name == 'vertel':
            self.schrijf = True
            self.startElement("titel", {})
            self.characters(self.dh.titel)
            self.endElement("titel")
            for x in self.dh.tekst:
                self.startElement("hoofdstuk", {})
                if x[0] != "":
                    self.startElement("titel2", {})
                    self.characters(x[0])
                    self.endElement("titel2")
                for y in x[1]:
                    self.startElement("alinea", {})
                    self.characters(y)
                    self.endElement("alinea")
                self.endElement("hoofdstuk")
        if self.schrijf:
            XMLGenerator.endElement(self, name)

    def endDocument(self):
        self.fh.close()

class UpdateItemDeel(XMLGenerator):
    def __init__(self, item):
        self.dh = item
        self.zoek_hst = self.dh.hst
        self.vlgnrhst = 0
        self.fh = open(self.dh.fn, 'w')
        self.founditem = self.itemfound = False
        XMLGenerator.__init__(self,self.fh)

    def startDocument(self):
        XMLGenerator.startDocument(self)

    def startElement(self, name, attrs):
        if name == "hoofdstuk":
            self.vlgnrhst += 1
            if not self.itemfound:
                if self.vlgnrhst == int(self.zoek_hst):
                    self.founditem = True
        if not self.founditem:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if not self.founditem:
            XMLGenerator.characters(self, ch)

    def endElement(self, name):
        if name == "hoofdstuk":
            if self.founditem:
                self.itemfound = True
                self.founditem = False
                self.startElement("hoofdstuk", {})
                self.startElement("titel2", {})
                self.characters(self.dh.htitel)
                self.endElement("titel2")
                for x in self.dh.htekst:
                    self.startElement("alinea", {})
                    self.characters(x)
                    self.endElement("alinea")
                # XMLGenerator.endElement(self, "hoofdstuk")
        elif name == 'vertel':
            if not self.itemfound:
                self.founditem = True
                self.endElement("hoofdstuk")
        if not self.founditem:
            XMLGenerator.endElement(self, name)

    def endDocument(self):
        self.fh.close()

def hoofdstuklijst(fnaam):
        titel = ""
        htitel = []
        if os.path.exists(fnaam):
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = FindItem(hslist=True)
            parser.setContentHandler(dh)
            parser.parse(fnaam)
            titel = dh.titel
            htitel = [x[0] for x in dh.hoofdstukken]
            return titel, htitel

class Hoofdstuk:
    def __init__(self, url, hst):
        self.fn = url
        self.hst = hst
        self.fno = '_old'.join(os.path.splitext(url))
        self.titel = ""
        self.htitel = ""
        self.htekst = []
        self.aanthst = 0
        self.found = False
        self.bestaat = os.path.exists(self.fn)

    def read(self):
        if not self.bestaat:
            return
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindItem(self.hst)
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        # try:
            # parser.parse(self.fn)
        # except HstFound:
            # self.found = True
        # else:
            # return
        self.found = dh.itemfound
        self.titel = dh.titel
        self.aanthst = dh.aanthst
        if self.found:
            self.htitel = dh.hoofdstukken[0]
            self.htekst = [x for x in dh.hoofdstukken[1]]

    def write(self):
        if not self.bestaat:
            return
        shutil.copyfile(self.fn, self.fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateItemDeel(self)
        parser.setContentHandler(dh)
        parser.parse(self.fno)

class Verhaal:
    """
    objectrepresentatie dat een compleet verhaal

    attributen:
    .bestaat: boolean indicatie of het xml bestand aanwezig is
    .titel: titel van het verhaal
    .tekst: list met hoofdstukken als tuples
        eerste element is de hoofdstuktitel
        tweede element is een list met alinea's (elke alinea is een string)
    pas na aanroepen van read() zijn titel en tekst gevuld
    """
    def __init__(self, url):
        self.fn = url
        self.fno = '_old'.join(os.path.splitext(url))
        self.titel = ""
        self.tekst = []
        self.found = False
        self.bestaat = os.path.exists(self.fn)

    def read(self):
        if not self.bestaat:
            return
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindItem()
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.titel = dh.titel
        self.tekst = []
        if len(dh.hoofdstukken) > 0:
            for x in dh.hoofdstukken:
                titel = x[0]
                ht = [] if len(x) == 1 else [y for y in x[1]]
                hs = (titel,ht)
                self.tekst.append(hs)

    def write(self):
        if not self.bestaat:
            fh = open(self.fn,'w')
            fh.write('<?xml version="1.0" encoding="utf-8"?>\n')
            fh.write('<?xml-stylesheet href="http://data.magiokis.nl/vertel/vertel.css" type="text/css" ?>\n')
            fh.write('<vertel></vertel>\n')
            fh.close()
            self.bestaat = True
        else:
            shutil.copyfile(self.fn, self.fno)
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = UpdateItem(self)
            parser.setContentHandler(dh)
            parser.parse(self.fno)

    def add_hoofdstuk(self, titel, tekst=None):
        """nieuw hoofdstuk opvoeren

        argumenten: hoofdstuktitel, hoofdstuktekst (list met strings)
        """
        if tekst is None:
            tekst = []
        self.tekst.append((titel, tekst))

    def add_alinea(self, tel, tekst):
        """nieuwe alinea toevoegen aan het aangegeven hoofdstuk

        argumenten: volgnummer van het te wijzigen hoofdstuk, tekst
        de tekst moet een enkele string zijn

        retourneert een boolean die aangeeft of het toevoegen gelukt is c.q.
        of het opgegeven hoofdstuknummer bestaat
        """
        if tel < len(self.tekst):
            titel, hoofdstuk = self.tekst[tel]
            hoofdstuk.append(tekst)
            self.tekst[tel] = (titel, hoofdstuk)
            return True
        else:
            return False

    def wijzig_hoofdstuktitel(self, tel, titel):
        """titel van een aangegeven hoofdstuk wijzigen

        argumenten: volgnummer van het te wijzigen hoofdstuk, nieuwe titel

        retourneert een boolean die aangeeft of het wijzigen gelukt is c.q.
        of het opgegeven hoofdstuknummer bestaat
        """
        if tel < len(self.tekst):
            _, hoofdstuk = self.tekst[tel]
            self.tekst[tel] = (titel, hoofdstuk)
            return True
        else:
            return False

    def wijzig_hoofdstuktekst(self, tel, tekst):
        """tekst van een aangegeven hoofdstuk wijzigen

        argumenten: volgnummer van het te wijzigen hoofdstuk, nieuwe tekst
        de tekst moet een list of tuple van strings zijn

        retourneert een boolean die aangeeft of het wijzigen gelukt is c.q.
        of het opgegeven hoofdstuknummer bestaat
        """
        if tel < len(self.tekst):
            titel, _ = self.tekst[tel]
            self.tekst[tel] = (titel, tekst)
            return True
        else:
            return False
