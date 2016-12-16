# -*- coding: UTF-8 -*-
import os
from vertel_datapad import xmlpad
vertellerfile = os.path.join(xmlpad, 'verteller_{}.xml')
backupfile = '_old'.join(os.path.splitext(vertellerfile))
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from vertellers import Cats

class NoGoodError(Exception):
    pass

class FindItem(ContentHandler):
    "Bevat de gegevens van een bepaald verhaal: Titel, Id, Url, trefwoorden"
    def __init__(self, item, type='id'):
        self.search_item = item
        self.search_type = type
        self.in_urlbase = self.in_url = False
        self.in_path = self.in_trefw = False
        self.id_ = self.cat = self.titel = self.url = ""
        self.id_titels = []
        self.trefwoorden = []
        self.founditem = self.itemfound = False

    def startElement(self, name, attrs):
        if name == 'urlbase':
            self.in_urlbase = True
            self.urlbase = ''
        elif name == 'path':
            self.in_path = True
            self.basepath = ''
        elif name == 'verhaal':
            item = attrs.get('id', None)
            if self.search_type == 'id' and item == self.search_item:
                self.founditem = True
            item2 = attrs.get('titel', None)
            if self.search_type == 'titel' and item2.lower() == self.search_item.lower():
                self.founditem = True
            item3 = attrs.get('categorie', None)
            if self.founditem:
                self.id_ = item
                self.titel = item2
                self.cat = item3
        elif name == 'url':
            if self.founditem:
                self.in_url = True
                self.url = ""
        elif name == 'trefwoord':
            if self.founditem:
                self.in_trefw = True
                self.trefwoord = ''

    def characters(self, ch):
        if self.in_urlbase:
            self.urlbase += ch
        elif self.in_path:
            self.basepath += ch
        elif self.in_url:
            self.url += ch
        elif self.in_trefw:
            self.trefwoord += ch

    def endElement(self, name):
        if name == 'urlbase':
            if self.in_urlbase:
                self.in_urlbase = False
        elif name == 'path':
            if self.in_path:
                self.in_path = False
        elif name == 'verhaal':
            if self.founditem:
                if self.search_type == 'titel':
                    self.dit_item = (self.id_, self.titel, self.url)
                    self.id_titels.append(self.dit_item)
                self.itemfound = True
                self.founditem = False
        elif name == 'url':
            if self.in_url:
                self.in_url = False
        elif name == 'trefwoord':
            if self.in_trefw:
                self.in_trefw = False
                self.trefwoorden.append(self.trefwoord)

class FindList(ContentHandler):
    "Maakt een lijst met verhalen"
    "Zonder meegegeven item: alles"
    "Zonder meegegeven type: selectie op deel van de titel"
    "Anders bijvoorbeeld zoeken op categorie"
    def __init__(self, item=None, type=""):
        if item == None:
            self.geef_alles = True
        else:
            self.search_item = item
            self.geef_alles = False
        self.search_type = type
        self.in_titel = False
        self.titel = ""
        self.in_path = self.in_urlbase = self.in_url = False
        self.url = ""
        self.id_titels = []
        self.founditem = self.itemfound = False

    def startElement(self, name, attrs):
        if name == 'urlbase':
            self.in_urlbase = True
            self.urlbase = ''
        elif name == 'path':
            self.in_path = True
            self.path = ''
        elif name == 'verhaal':
            item = attrs.get('id', None)
            item2 = attrs.get('titel', None)
            item3 = attrs.get('categorie', None)
            if self.geef_alles:
                self.founditem = True
            else:
                if self.search_type == "cat":
                    if item3 == self.search_item:
                        self.founditem = True
                else:
                    if self.search_item.upper() in item2.upper():    # altijd ignore case search
                        self.founditem = True
            if self.founditem:
                self.dit_item = [item, item2]
        elif name == 'url':
            if self.founditem:
                self.in_url = True
                self.url = ""

    def characters(self, ch):
        if self.in_urlbase:
            self.urlbase = self.urlbase + ch
        elif self.in_path:
            self.path = self.path + ch
        elif self.in_url:
            self.url = self.url + ch

    def endElement(self, name):
        if name == 'urlbase':
            if self.in_urlbase:
                self.in_urlbase = False
        elif name == 'path':
            if self.in_path:
                self.in_path = False
        elif name == 'verhaal':
            if self.founditem:
                self.dit_item.append(self.url)
                self.id_titels.append(self.dit_item)
                self.founditem = False
        elif name == 'url':
            if self.in_url:
                self.in_url = False

class UpdateItem(XMLGenerator):
    "schrijf tekst weg in XML-document"
    def __init__(self, item):
        self.dh = item
        self.search_item = self.dh.id
        self.titel = self.dh.titel
        self.url = self.dh.url
        self.cat = str(self.dh.cat)
        self.trefwoorden = self.dh.trefwoorden
        self.fh = open(self.dh._fn, 'w')
        self.founditem = self.itemfound = False
        self.laatste = 0
        XMLGenerator.__init__(self, self.fh)

    def startElement(self, name, attrs):
        if name == 'verhaal':
            self.id = attrs.get('id', None)
            if self.id == str(self.search_item) and not self.itemfound:
                self.founditem = self.itemfound = True
            if int(self.id) > self.laatste:
                self.laatste = int(self.id)
        if not self.founditem:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if not self.founditem:
            XMLGenerator.characters(self, ch)

    def endElement(self, name):
        if name == "verhaal" and self.founditem:
            self.founditem = False
            self.itemfound = True
            self.startElement("verhaal", {"categorie": self.cat,
                "id": self.id, "titel": self.titel})
            self.startElement("url", {})
            self.characters(self.url)
            self.endElement("url")
            for x in self.trefwoorden:
                self.startElement("trefwoord", {})
                self.characters(x)
                self.endElement("trefwoord")
        if not self.founditem:
            if name == 'verhalen':
                if not self.itemfound:
                    self.laatste += 1
                    self.id = str(self.laatste)
                    self.founditem = True
                    self.endElement("verhaal")
            XMLGenerator.endElement(self, name)

    def endDocument(self):
        #~ XMLGenerator.endDocument(self)
        self.fh.close()

class FindRoot(ContentHandler):
    def __init__(self):
        self.urlbase = ''
        self.in_urlbase = False
        self.basepath = ''
        self.in_path = False
        self.laatste = 0

    def startElement(self, name, attrs):
        if name == 'verhaal':
            id_ = attrs.get('id', None)
            if int(id_) > self.laatste:
                self.laatste = int(id_)
        elif name == 'urlbase':
            self.in_urlbase = True
        elif name == 'path':
            self.in_path = True

    def characters(self, ch):
        if self.in_urlbase:
            self.urlbase = self.urlbase + ch
        elif self.in_path:
            self.basepath = self.basepath + ch

    def endElement(self, name):
        if name == 'urlbase':
            if self.in_urlbase:
                self.in_urlbase = False
        elif name == 'path':
            if self.in_path:
                self.in_path = False

class UpdateRoot(XMLGenerator):
    "schrijf tekst weg in XML-document"
    def __init__(self, item):
        self.dh = item
        self.fh = open(self.dh.fn, 'w')
        self.write = True
        self.urldone = self.pathdone = False
        XMLGenerator.__init__(self, self.fh)

    def startElement(self, name, attrs):
        XMLGenerator.startElement(self, name, attrs)
        if name == 'urlbase' or name == "path":
            self.write = False

    def characters(self, ch):
        if self.write:
            XMLGenerator.characters(self, ch)

    def endElement(self, name):
        if not self.write:
            self.write = True
            if name == 'urlbase':
                self.characters(self.dh.urlbase)
                self.urldone = True
            elif name == "path":
                self.characters(self.dh.basepath)
                self.pathdone = True
        elif name == "verhalen":
            if not self.urldone:
                self.startElement('urlbase', {})
                self.write = True
                self.characters(self.dh.urlbase)
                self.endElement('urlbase')
            if not self.pathdone:
                self.startElement("path", {})
                self.write = True
                self.characters(self.dh.basepath)
                self.endElement("path")
        XMLGenerator.endElement(self, name)

    def endDocument(self):
        #~ XMLGenerator.endDocument(self)
        self.fh.close()

class Verteller:
    def __init__(self, user):
        self.user = user
        self.fn = vertellerfile.format(self.user)
        self.fno = backupfile.format(self.user)
        self.laatste = 0
        self.urlbase = self.basepath = ""
        self.exists = os.path.exists(self.fn)
        if self.exists:
            self.laatste = 0
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = FindRoot()
            parser.setContentHandler(dh)
            parser.parse(self.fn)
            self.laatste = dh.laatste
            self.urlbase = dh.urlbase
            self.basepath = dh.basepath

    def nieuw(self):
        if self.exists:
            raise AttributeError("Verteller '%s' bestaat al" % self.user)
        else:
            fh = open(self.fn, 'w')
            fh.write('<?xml version="1.0" encoding="utf-8"?>\n')
            fh.write('</verhalen>\n')
            fh.write('  <urlbase>http://local.magiokis.nl/</urlbase>\n')
            fh.write('  <path>/home/albert/magiokis/data/vertel</path>\n')
            fh.write('</verhalen>\n')
            fh.close()
            self.exists = True

    def write(self):
        shutil.copyfile(self.fn, self.fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateRoot(self)
        parser.setContentHandler(dh)
        parser.parse(self.fno)

    def new_urlbase(self, data):
        if isinstance(data, str):
            self.urlbase = data
        else:
            raise ValueError("nieuwe UrlBase is geen string")

    def new_basepath(self,data):
        if isinstance(data, str):
            self.basepath = data
        else:
            raise ValueError("nieuwe BasePath is geen string")

def vertellijst(user, item=None):
    """lijst alle verhalen met een bepaalde zoektekst

    geeft AttributeError als de opgegeven user niet bestaat
    """
    fn = vertellerfile.format(user)
    if not os.path.exists(fn):
        raise AttributeError('Geen verhalen van deze verteller bekend')
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = FindList(item)
    parser.setContentHandler(dh)
    parser.parse(fn)
    urlbase = dh.urlbase
    path = dh.path
    lijst = [x for x in dh.id_titels]
    return urlbase, path, lijst

def catlijst(user, item=None):
    """lijst alle verhalen bij een bepaalde categorie

    geeft AttributeError als de opgegeven user niet bestaat
    """
    dh = Cats(user)
    search_id = dh.zoek_id_bij_naam(item)
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = FindList(search_id, "cat")
    parser.setContentHandler(dh)
    parser.parse(vertellerfile.format(user))
    urlbase = dh.urlbase
    path = dh.path
    lijst = [x for x in dh.id_titels]
    return urlbase, path, lijst

class VertelItem:
    "lijst alle gegevens van een bepaald 'vertel'-item"
    def __init__(self, user, ident, type='id'):
        self.id = self.titel = self.url = self.cat = ""
        self.user = user
        self._type = type
        if self._type in ("id", "titel"):
            self._ident = ident
        else:
            raise ValueError('Verkeerd type voor sleutel (moet "id" of "titel" zijn)')
        self._fn = vertellerfile.format(self.user)
        if not os.path.exists(self._fn):
            raise AttributeError('Geen verhalen van deze verteller bekend')
        self._fno = backupfile.format(self.user)
        self.trefwoorden = []
        self.found = False

    def read(self):
        """
        theoretisch kan bij zoeken op titel meer dan 1 item gevonden zijn.
        de list id_titels is dan gevuld. In dat geval een fout geven
        """
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindItem(str(self._ident), self._type)
        parser.setContentHandler(dh)
        parser.parse(self._fn)
        if dh.itemfound:
            if len(dh.id_titels) > 1:
                raise AttributeError('Meer dan 1 verhaal met deze titel gevonden')
            self.found = True
            self.id = dh.id_ #.encode('ISO-8859-1')
            self.titel = dh.titel #.encode('iso-8859-1')
            self.cat = dh.cat #.encode('iso-8859-1')
            self.urlbase = dh.urlbase #.encode('iso-8859-1')
            self.url = dh.url #.encode('iso-8859-1')
            self.path = dh.basepath #.encode('ISO-8859-1')
            if len(dh.trefwoorden) > 0:
                ## for x in dh.trefwoorden:
                    ## self.trefwoorden.append(x.encode('ISO-8859-1'))
                self.trefwoorden = [x for x in dh.trefwoorden]

    def write(self):
        shutil.copyfile(self._fn, self._fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateItem(self)
        parser.setContentHandler(dh)
        parser.parse(self._fno)

    def get_catnaam(self):
        ch = Cats(self.user)
        return ch.zoek_naam(self.cat)

    def wijzig_cat(self, item):
        th = Cats(self.user)
        try:
            test = int(item)
        except ValueError:
            test = 0
        if test:
            try:
                test = th.zoek_naam_bij_id(item)
            except AttributeError:
                raise AttributeError("Categorie %s bestaat niet bij user" % item)
            self.cat = item
        else:
            try:
                self.cat = th.zoek_id_bij_naam(item)
            except AttributeError:
                raise AttributeError("Categorie %s bestaat niet bij user" % item)

    def add_trefw(self, item):
        "voeg een trefwoord toe aan self.Trefwoorden"
        if item in self.trefwoorden:
            raise AttributeError("trefwoord %s komt al voor bij item" % item)
        self.trefwoorden.append(item)

    def rem_trefw(self, item):
        "haal een trefwoord weg uit self.Trefwoorden"
        if item not in self.trefwoorden:
            raise AttributeError("trefwoord %s komt niet voor bij item" % item)
        self.trefwoorden.remove(item)
