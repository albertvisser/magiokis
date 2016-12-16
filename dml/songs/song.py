# -*- coding: UTF-8 -*-
import sqlite3
import common
from coderec import CodeRec

class Song(object):
    "bevat de gegevens van een song plus methoden om die te lezen, wijzigen en schrijven"
    def __init__(self,id_):
        self.con = sqlite3.connect(common.data)
        self._id = id_
        self._titel = self._auteur = self._maker = ""
        self.tekst_id = self.muziek_id = 0
        self.datering = self.datumtekst = self.url = self.commentaar = ""
        ## self.new_song = False
        self.found = False
        if self._id == 0:
            self.new()
        else:
            self.read()

    def new(self):
        dh = CodeRec("laatste", "song")
        self._id = str(int(dh.item_naam) + 1)

    def read(self):
        """songs(id,muziek,tekst,titel,datering,datumtekst,url,commentaar)"""
        try:
            c = self.con.execute('select * from songs '
                'left join auteurs on auteurs.id == songs.tekst '
                'left join makers on makers.id == songs.muziek '
                'where songs.id == ?', (str(self._id),))
        except sqlite3.OperationalError as mld:
            raise common.DataError("Ophalen mislukt")
        i = 0
        for x in c:
            self._muziek_id = x[1]
            self._tekst_id = x[2]
            self._titel = x[3]
            self.datering = x[4]
            self.datumtekst = x[5]
            self.url = x[6]
            if self.url == "" and self.songtitel != "":
                self.url = self.songtitel + ".xml"
            self.commentaar = x[7]
            self.tekst_van = x[9]
            self.muziek_van = x[11]
            i += 1
        if i > 0:
            self.found = True

    @property
    def song_id(self):
        return self._id

    @song_id.setter
    def song_id(self, value):
        self._id = value

    @property
    def songtitel(self):
        "titel van de song"
        if self._titel:
            return self._titel
        else:
            return "(untitled)"

    @songtitel.setter
    def songtitel(self, value):
        if value != "(untitled)":
            self._titel = value

    @property
    def auteur(self):
        "schrijver van de songtekst"
        return self._tekst_id

    @auteur.setter
    def auteur(self, value):
        self._tekst_id = value
        self.tekst_van = CodeRec('auteur', value).item_naam

    @property
    def maker(self):
        "schrijver van de muziek"
        return self._muziek_id

    @maker.setter
    def maker(self, value):
        self._muziek_id = value
        self.muziek_van = CodeRec('maker', value).item_naam

    def write(self):
        if self.url == self.songtitel + ".xml":
            self.url = ""
        if self.found:
            cmd = 'update songs set muziek = "%s",tekst = "%s",titel = "%s",' \
                'datering = "%s",datumtekst = "%s",url = "%s",commentaar = "%s" '\
                'where id == "%s"' % (self.muziek_id, self.tekst_id, self.songtitel,
                self.datering, self.datumtekst, self.url, self.commentaar, self._id)
        else:
            cmd = 'insert into songs (id, muziek, tekst, titel, datering, ' \
                'datumtekst, url, commentaar) values ("%s", "%s", "%s", "%s", ' \
                '"%s", "%s", "%s", "%s")' % (self._id, self.muziek_id, self.tekst_id,
                self.songtitel, self.datering, self.datumtekst, self.url,
                self.commentaar)
        try:
            c = self.con.execute(cmd)
        except sqlite3.OperationalError as mld:
            print(cmd)
            raise common.DataError(mld)
        except BaseException:
            raise common.DataError("Bijwerken mislukt")
        self.con.commit()
        if not self.found:
            dh = CodeRec("laatste", "song")
            dh.item_naam = self._id
            dh.write()
            self.found = True
