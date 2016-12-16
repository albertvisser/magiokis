# -*- coding: UTF-8 -*-
import os
import shutil
import common
from xml.etree.ElementTree import ElementTree, Element, SubElement
from song import Song

class Songtekst(object):
    "bevat de gegevens van een songtekst plus methoden om die te lezen, wijzigen en schrijven"
    def __init__(self, id_):
        self._id = id_
        self._titel = ""
        self.regels = []
        self.aant_regels = 0
        self.found = False
        self._filenaam = ""
        sh = Song(id_)
        if sh.found:
            self._titel = sh.songtitel
            if sh.url != "n/a":
                if sh.url != "":
                    self._filenaam = sh.url
                else:
                    self._filenaam = self._titel + '.xml'
                self._filenaam = os.path.join(common.tekstpad, self._filenaam)

    def read(self):
        if self._filenaam:
            root = ElementTree(file=self._filenaam).getroot()
            self.regels = []
            titelgehad = False
            for x in list(root):
                if x.tag == 'titel':
                    self._titel = x.text
                    titelgehad = True
                elif not titelgehad:
                    continue
                elif x.tag == 'br':
                    self.regels.append("")
                elif x.tag == 'couplet':
                    self.regels.append('')
                    for y in list(x):
                        if y.tag == 'regel':
                            self.regels.append(y.text)
                        elif x.tag == 'br':
                            self.regels.append("")
            self.found = True

    @property
    def titel(self):
        ## if self._titel:
        return self._titel
        ## else:
            ## return "(untitled)"

    @titel.setter
    def titel(self, value):
        self._titel = value

    @property
    def file(self):
        return self._filenaam
        ## s = self._filenaam.split("\\")
        ## s = s[-1].split("/")
        ## return s[-1]

    @file.setter
    def file(self, value):
        ## s = value.split("\\")
        ## s = s[-1].split("/")
        self.oldfilenaam = self._filenaam
        ## self._filenaam = os.path.join(common.tekstpad, s[-1])
        self._filenaam = value

    def write(self):
        sh = Song(self._id)
        sh.read()
        old_url = sh.url
        sh.url = self._filenaam or 'n/a'
        if sh.url != old_url:
            sh.write()
        # songtekst terugschrijven
        root = Element('songtekst')
        t = SubElement(root,'titel')
        t.text = self._titel
        if self.regels[0] != '':
            c = SubElement(root,'couplet')
        for x in self.regels:
            if x == '':
                c = SubElement(root,'couplet')
            else:
                r = SubElement(c,'regel')
                r.text = x
        if self._filenaam == '':
            self._filenaam = os.path.join(common.tekstpad, self._titel.lower() + '.xml')
        tree = ElementTree(root)
        try:
            shutil.copyfile(self._filenaam, self._filenaam + '.old')
        except IOError:
            pass
        tree.write(self._filenaam)
