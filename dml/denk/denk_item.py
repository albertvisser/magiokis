# -*- coding: utf-8 -*-

import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from denk_globals import denkerijfile
from denk_trefw import trefwoordenlijst, Trefwoord

class DataFout(Exception):
    pass

class FindItem(ContentHandler):
    "Bevat de gegevens van een bepaald gedenk: Titel, Tekst, gedenk"
    def __init__(self, item):
        self.search_item = item
        self.in_titel = self.in_trefwoord = self.in_alinea = False
        self.id_titels = []
        self.trefwoorden = []
        self.alineas = []
        self.founditem = self.itemfound = False

    def startElement(self, name, attrs):
        if name == 'gedenk':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = True
        elif name == 'titel':
            if self.founditem:
                self.in_titel = True
                self.titel = ""
        elif name == 'trefwoord':
            if self.founditem:
                self.in_trefwoord = True
                self.trefwoord = ""
        elif name == 'alinea':
            if self.founditem:
                self.in_alinea = True
                self.alinea = ""

    def characters(self, ch):
        if self.in_titel:
            self.titel = self.titel + ch
        elif self.in_trefwoord:
            self.trefwoord = self.trefwoord + ch
        elif self.in_alinea:
            self.alinea = self.alinea + ch

    def endElement(self, name):
        if name == 'gedenk':
            if self.founditem:
                self.itemfound = True
                self.founditem = False
        elif name == 'titel':
            if self.in_titel:
                self.in_titel = False
        elif name == 'trefwoord':
            if self.in_trefwoord:
                self.in_trefwoord = False
                self.trefwoorden.append(self.trefwoord)
        elif name == 'alinea':
            if self.in_alinea:
                self.in_alinea = False
                ## if self.alinea != "" and self.alinea[0] == "\n":
                    ## self.alinea = self.alinea[1:]
                ## self.alinea = self.alinea.rstrip()
                ## if self.alinea != "" and self.alinea[-1] == "\n":
                    ## self.alinea = self.alinea[:-1]
                ## self.alineas.append(self.alinea)
                self.alineas.append(self.alinea.strip())

class FindList(ContentHandler):
    "Bevat alle gedenken of alleen de gedenken met een zoektekst"
    def __init__(self, item=None, sel_titel=False, sel_text=False):
        if item is None:
            self.geef_alles = True
        else:
            self.search_item = item
            self.sel_titel = sel_titel
            self.sel_tekst = sel_text
            self.geef_alles = False
        self.in_titel = self.in_tekst = False
        self.in_trefwoord = self.in_alinea = False
        self.id_titels = []
        self.founditem = self.itemfound = False

    def startElement(self, name, attrs):
        if name == 'gedenk':
            item = attrs.get('id', None)
            self.itemsbijdeze = [ item ]
            self.got_titel = False
            self.trefwoorden = []
            self.alineas = []
        elif name == 'titel':
            self.in_titel = True
            self.titel = ""
            self.got_titel = True
        elif name == 'trefwoord':
            self.in_trefwoord = True
            self.trefwoord = ""
        elif name == 'alinea':
            ## if not self.got_titel:
            self.in_alinea = True
            self.alinea = ""

    def characters(self, ch):
        if self.in_titel:
            self.titel = self.titel + ch
        elif self.in_trefwoord:
            self.trefwoord = self.trefwoord + ch
        elif self.in_alinea:
            self.alinea = self.alinea + ch

    def endElement(self, name):
        if name == 'gedenk':
            oktoappend = False
            if self.geef_alles:
                self.itemsbijdeze.append(self.titel)
                self.id_titels.append(self.itemsbijdeze)
            else:
                if self.sel_titel:
                    if self.search_item.upper() in self.titel.upper():
                        oktoappend = True
                if self.sel_tekst:
                    ## print('sel_tekst: kijk of {}'.format(self.search_item.upper()))
                    for alinea in self.alineas:
                        ## print('  voorkomt in {}'.format(alinea.encode('latin-1').upper()))
                        if self.search_item.upper() in alinea.upper():
                            ## print('  ja dus')
                            oktoappend = True
                            break
                if oktoappend:
                    ## print('toevoegen maar')
                    self.itemsbijdeze.append(self.titel)
                    self.id_titels.append(self.itemsbijdeze)
        elif name == 'titel':
            if self.in_titel:
                self.in_titel = False
        elif name == 'tekst':
            if self.in_tekst:
                self.in_tekst = False
        elif name == 'trefwoord':
            if self.in_trefwoord:
                self.in_trefwoord = False
                self.trefwoorden.append(self.trefwoord)
        elif name == 'alinea':
            if self.in_alinea:
                self.in_alinea = False
                self.alineas.append(self.alinea)

class UpdateItem(XMLGenerator):
    """denktekst updaten"

    aan het eind zit een element genaamd laatste.
    Als het id van de tekst hoger is dan deze, dan laatste aanpassen.
    schrijf tekst weg in XML-document"""
    def __init__(self, item):
        self.dh = item
        self.search_item = self.dh.itemid
        self.fh = open(self.dh._fn, 'w')
        self.founditem = self.itemfound = False
        XMLGenerator.__init__(self, self.fh, encoding='utf-8')

    def startElement(self, name, attrs):
        if name == 'gedenk':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.itemfound = True
        if not self.itemfound:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if not self.itemfound:
            XMLGenerator.characters(self,ch)

    def endElement(self, name):
        if name == 'denkerij' and not self.founditem:
            self.itemfound = True
            self.endElement("gedenk")
            XMLGenerator.endElement(self, name)
        elif name == "gedenk" and self.itemfound:
            self.itemfound = False
            XMLGenerator.startElement(self, name,{"id": self.dh.itemid})
            self.startElement("titel", {})
            self.characters(self.dh.titel)
            self.endElement("titel")
            for x in self.dh.tekst:
                self.startElement("alinea", {})
                self.characters(x)
                self.endElement("alinea")
            for x in self.dh.trefwoorden:
                self.startElement("trefwoord", {})
                self.characters(x)
                self.endElement("trefwoord")
            XMLGenerator.endElement(self,name)
            self.founditem = True
        elif not self.itemfound:
            XMLGenerator.endElement(self, name)

    def endDocument(self):
        self.fh.close()

class FindLaatste(ContentHandler):
    def __init__(self):
        self.laatste = 0

    def startElement(self, name, attrs):
        if name == 'gedenk':
            item = int(attrs.get('id', -1))
            if item > self.laatste:
                self.laatste = item

def denk_laatste():
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = FindLaatste()
    parser.setContentHandler(dh)
    parser.parse(denkerijfile)
    return dh.laatste

def denk_lijst(item=None, type=None):
    "lijst alle gedenken van een bepaald jaar of met een bepaalde zoektekst"
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    if item is None:
        dh = FindList()
    elif type == "selTitel":
        dh = FindList(item, sel_titel=True)
    elif type == "selTekst":
        dh = FindList(item, sel_text=True)
    elif type == "selBeide":
        dh = FindList(item, sel_titel=True, sel_text=True)
    parser.setContentHandler(dh)
    parser.parse(denkerijfile)
    return dh.id_titels

class DenkItem(object):
    "lijst alle gegevens van een bepaald 'gedenk'-item"
    def __init__(self, id_):
        self.itemid = id_
        self._fn =  denkerijfile
        self._fno = '_old'.join(os.path.splitext(denkerijfile))
        self._fnn = '_new'.join(os.path.splitext(denkerijfile))
        self.titel = ""
        self.trefwoorden = []
        self.tekst = []
        self.found = False
        self._tl, _ = trefwoordenlijst()

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindItem(str(self.itemid))
        parser.setContentHandler(dh)
        parser.parse(self._fn)
        self.found = dh.itemfound
        if self.found:
            self.titel = dh.titel
            self.trefwoorden = [x for x in dh.trefwoorden]
            self.tekst = [x for x in dh.alineas]

    def write(self):
        shutil.copyfile(self._fn,self._fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateItem(self)
        parser.setContentHandler(dh)
        parser.parse(self._fno)

    def add_trefw(self, item):
        "voeg een trefwoord toe aan self.trefwoorden"
        if item not in self._tl:
            raise DataFout("trefwoord %s bestaat niet" % item)
        else:
            if item in self.trefwoorden:
                raise DataFout("trefwoord %s is al aanwezig" % item)
            else:
                self.trefwoorden.append(item)
                ti = Trefwoord(item)
                ti.read()
                ti.add_ref(self.itemid)
                ti.write()

    def rem_trefw(self,item):
        "haal een trefwoord weg uit self.trefwoorden"
        if item in self.trefwoorden:
            self.trefwoorden.remove(item)
            ti = Trefwoord(item)
            ti.read()
            ti.rem_ref(self.itemid)
            ti.write()
        else:
            raise DataFout("trefwoord %s is niet aanwezig" % item)

    def wijzig_trefw(self, data):
        "vervang self.trefwoorden"
        self.trefwoorden = []
        for x in data:
            if x not in self._tl:
                raise DataFout("trefwoord %s bestaat niet" % x)
            else:
                self.trefwoorden.append(x)

    def add_tekst(self, item):
        "voeg een alinea toe aan self.tekst"
        self.tekst.append(item)

    def rem_tekst(self, item):
        "haal een alinea weg uit self.tekst"
        try:
            self.tekst.remove(item)
        except ValueError:
            raise dataFout("Opgegeven alinea bestaat niet")

    def wijzig_tekst(self, data):
        "vervang self.tekst"
        self.tekst = [x for x in data]

