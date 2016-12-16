# -*- coding: UTF-8 -*-
import os
import sqlite3
import common
from coderec import CodeRec
from regtype import RegType
from song import Song

class Muziekreg(object):
    "Bevat alle gegevens van een muziekregistratie plus methoden om die te lezen, wijzigen en schrijven"
    def __init__(self,id_):
        self.con = sqlite3.connect(common.data)
        self._id = id_
        self._type_id = self._song_id = 0
        self.regtype = self.url = self.pad = self.file = self.commentaar = ""
        self.found = False
        if id_ == 0:
            self.new()
        else:
            self.read()

    def new(self):
        dh = CodeRec("laatste", "registratie")
        self._id = str(int(dh.item_naam) + 1)

    def read(self):
        cmd = 'select * from registraties, songs, regtypes where songs.id == ' \
            'registraties.song and regtypes.id == registraties.type and ' \
            'registraties.id == "%s"' % self._id
        ## print cmd
        try:
            c = self.con.execute(cmd)
        except sqlite3.OperationalError as e:
            print(cmd)
            raise common.DataError("Ophalen mislukt: " + str(e))
        i = 0
        for x in c:
            self._type_id = x[1]
            self._song_id = x[2]
            self._file = x[3]
            self.commentaar = x[4]
            self.songtitel = x[8]
            self.regtype = x[14]
            ## self.player = x[17]
            ## self.editor = x[18]
            self.url = '/'.join((x[16], self._file))
            self.pad = os.path.join(x[15], self._file)
            i += 1
        if i > 0:
            self.found = True

    @property # (getter)
    def type(self):
        return self._type_id

    @type.setter
    def type(self, value):
        """als het regtype wijzigt moeten ook de naam ervan, de player, de editor
        en het filepad en de url aangepast worden (door het item op te halen)"""
        self._type_id = value
        data = RegType(value)
        self.regtype = data.typenaam
        ## self.player = data.playernaam
        ## self.editor = data.readernaam
        self.pad = os.path.join(data.padnaam, self._file)
        self.url = '/'.join((data.htmlpadnaam, self._file))

    @property # (getter)
    def song(self):
        return self._song_id

    @song.setter
    def song(self, value):
        """als het songid wijzigt moet ook de titel aangepast worden (door de song
        te raadplegen)"""
        self._song_id = value
        data = Song(value)
        self.songtitel = data.songtitel if data.found else ""

    @property # (getter)
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        """als de filenaam wijzigt moeten ook het filepad en de url aangepast
        worden"""
        self._file = value
        data = RegType(self._type_id)
        self.pad = os.path.join(os.path.abspath(data.padnaam), value)
        self.url = '/'.join((data.htmlpadnaam.split('/')[0], value))

    def write(self):
        if self.found:
            cmd = 'update registraties set type = "%s", song = "%s",' \
                'url = "%s", commentaar = "%s" where id == "%s"' % (self._type_id,
                self._song_id, self._file, self.commentaar, self._id)
        else:
            cmd = 'insert into registraties (id, type, song, url, commentaar) ' \
                'values ("%s","%s","%s","%s","%s")' % (self._id, self._type_id,
                self._song_id, self._file, self.commentaar)
        try:
            c = self.con.execute(cmd)
        except sqlite3.OperationalError as mld:
            print(cmd)
            raise common.DataError(mld)
        except:
            raise common.DataError("Bijwerken mislukt")
        self.con.commit()
        if not self.found:
            dh = CodeRec("laatste", "registratie")
            dh.item_naam = self._id
            dh.write()
            self.found = True
