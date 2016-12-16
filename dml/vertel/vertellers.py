# -*- coding: UTF-8 -*-
import os
from vertel_datapad import xmlpad
vertellersfile = os.path.join(xmlpad, 'vertellers.xml')
backupfile = '_old'.join(os.path.splitext(vertellersfile))
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape

class Found(Exception):
    pass

class OptionError(Exception):
    pass

class NoDataError(Exception):
    pass

class FindUser(ContentHandler):
    """find a user.

    usage: FindUser(username)
    raise Found() exception when found.
    return/build a user object
    self.passwd contains the associated password
    """
    def __init__(self, naam):
        self.zoek_naam = naam

    def startElement(self, name, attrs):
        if name == "user":
            nm = attrs.get('naam', None)
            if nm == self.zoek_naam:
                self.passwd = attrs.get('wachtwoord', "")
                raise Found("Gevonden")

class WriteUser(XMLGenerator):
    """add, delete or modify a user.

    usage: WriteUser(option, user_object)
    option "add" adds another user element
    option "chg" rewrites user using a different password attribute
    option "del" effectively doesn't (re)write the user
    raise OptionError() when instantiated using another option
    """
    def __init__(self, doe, dh):
        self.zoek_naam = dh.naam
        if doe not in ("add", "del", "chg"):
            raise OptionError(doe)
        self.doe = doe
        self.data = dh.pw
        self.fh = open(dh.fn, 'w')
        self.itemfound = False
        XMLGenerator.__init__(self, self.fh)

    def startElement(self, name, attrs):
        if name == "user":
            nm = attrs.get('naam', None)
            if nm == self.zoek_naam:
                self.itemfound = True
                if self.doe == "chg":
                    attrs["wachtwoord"] = data
        if self.doe == "del" and self.itemfound:
            pass
        else:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if self.doe == "del" and self.itemfound:
            pass
        else:
            XMLGenerator.characters(self,ch)

    def endElement(self, name):
        if self.doe == "del" and self.itemfound:
            pass
        else:
            if name == "users" and self.doe == "add":
                self.startElement("user", {"naam": self.zoek_naam,
                    "wachtwoord": self.data})
                self.endElement("user")
            XMLGenerator.endElement(self, name)
        if name == 'user' and self.itemfound:
            self.itemfound = False

    def endDocument(self):
        #~ XMLGenerator.endDocument(self)
        self.fh.close()

class FindCats(ContentHandler):
    """find categories associated with a user

    usage: FindCats(story_name)
    return/build an object with the following attribute:
    categorieen - list of tuples consisting of id, name and description
    """
    def __init__(self, naam):
        self.zoek_naam = naam
        self.found = False
        self.categorieen = []
        self.in_categorie = False

    def startElement(self, name, attrs):
        if name == "user":
            nm = attrs.get('naam', None)
            if nm == self.zoek_naam:
                self.found = True
        elif name == 'categorie' and self.found:
            self.cat_id = attrs.get('id', None)
            self.cat_naam = attrs.get('naam', None)
            self.in_categorie = True
            self.cat_text = ""

    def characters(self,ch):
        if self.in_categorie:
            self.cat_text = self.cat_text + ch

    def endElement(self,name):
        if name == "user" and self.found:
            raise Found("klaar")
        elif name == 'categorie' and self.in_categorie:
            self.in_categorie = False
            self.item = [self.cat_id, self.cat_naam, self.cat_text]
            self.categorieen.append(self.item)

class WriteCats(XMLGenerator):
    """write back the user's category list
    """
    def __init__(self, dh):
        self.search_user = dh.user
        #~ self.search_id = id
        #~ self.search_item = naam
        self.fh = open(dh.fn, 'w')
        self.founditem = False
        self.in_cat = False
        self.cats = dh.categorieen
        XMLGenerator.__init__(self, self.fh)

    def startElement(self, name, attrs):
        if name == 'user':
            naam = attrs.get('naam', None)
            if naam == self.search_user:
                self.founditem = True
                self.user_attrs = attrs
        if not self.founditem:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if not self.founditem:
            XMLGenerator.characters(self,ch)

    def endElement(self, name):
        if self.founditem:
            if name == "user":
                self.founditem = False
                XMLGenerator.startElement(self, 'user', self.user_attrs)
                for id_, naam, tekst in self.cats:
                    XMLGenerator.startElement(self, "categorie", {"id": str(id_),
                        "naam": naam})
                    XMLGenerator.characters(self, tekst)
                    XMLGenerator.endElement(self, "categorie")
                XMLGenerator.endElement(self, 'user')
        else:
            XMLGenerator.endElement(self, name)

    def endDocument(self):
        #~ XMLGenerator.endDocument(self)
        self.fh.close()

class User:
    def __init__(self, naam):
        self.naam = naam
        self.pw = ""
        self.exists = False
        self.fn = vertellersfile
        if not os.path.exists(self.fn):
            return
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindUser(naam)
        parser.setContentHandler(dh)
        try:
            parser.parse(vertellersfile)
        except Found:
            self.exists = True
            self.pw = dh.passwd
        else:
            return

    def new(self, waarde=""):
        if self.exists:
            return "FOUT: usernaam bestaat al"
        if waarde != "":
            self.pw = waarde
        return self._write("add")

    def remove(self):
        if not self.exists:
            return "FOUT: onbekende user"
        return self._write("del")

    def _write(self, doe):
        shutil.copyfile(vertellersfile, backupfile)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        try:
            dh = WriteUser(doe, self)
        except OptionError as doe:
            return "FOUT: onbekend argument voor write ('%(doe)s')"
        parser.setContentHandler(dh)
        parser.parse(backupfile)
        return "OK"

class Cats:
    "lijst alle Categorieen bij een user"
    def __init__(self, user):
        if not os.path.exists(vertellersfile):
            return
        self.user = user
        self.categorieen = []
        self.fn = vertellersfile
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindCats(user)
        parser.setContentHandler(dh)
        try:
            parser.parse(self.fn)
        except Found:
            pass
        else:
            return
        ## for x in dh.categorieen:
            ## tekst = x[2].encode('iso-8859-1')
            ## naam = x[1].encode('iso-8859-1')
            ## id_ = x[0].encode('iso-8859-1')
            ## self.categorieen.append((id_, naam, tekst))
        self.categorieen = [x for x in dh.categorieen]

    def zoek_id_bij_naam(self, name):
        for cat_id, catnaam, tekst in self.categorieen:
            if catnaam == name:
                return cat_id
        raise AttributeError("Categorie %s niet gevonden" % name)

    def zoek_naam_bij_id(self, id_):
        for cat_id, catnaam, tekst in self.categorieen:
            if cat_id == id_:
                return catnaam
        raise AttributeError("Categorie %s niet gevonden" % id_)

    def new_cat(self, name):
        for cat_id, catnaam, tekst in self.categorieen:
            if catnaam == name:
                return False
        y = len(self.categorieen) + 1
        z = (y, name, '')
        self.categorieen.append(z)
        self._write()
        return True

    def wijzig_cat(self, name, newname):
        found = exists = False
        for ix, cat in enumerate(self.categorieen):
            cat_id, cat_name, cat_text = cat
            if cat_name == name:
                self.categorieen[ix] = cat_id, newname, cat_text
                found = True
            elif cat_name == newname:
                exists = True
        if not found:
            raise AttributeError('Category "{}" doesn`t exist'.format(name))
        if exists:
            raise AttributeError('Category "{}" already exists'.format(newname))
        self._write()

    def wijzig_cattext(self, name, text):
        found = False
        for ix, cat in enumerate(self.categorieen):
            cat_id, cat_name, cat_text = cat
            if cat_name == name:
                self.categorieen[ix] = cat_id, cat_name, text
                found = True
                break
        if found:
            self._write()
        return found

    def _write(self):
        shutil.copyfile(vertellersfile, backupfile)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = WriteCats(self)
        parser.setContentHandler(dh)
        parser.parse(backupfile)
