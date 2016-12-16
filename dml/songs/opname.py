# -*- coding: UTF-8 -*-
import os
import sqlite3
import common
from coderec import CodeRec
from objectlists import ItemList
from song import Song

class Opname(object):
    "Bevat alle gegevens van een opname plus methoden om die te lezen, wijzigen en schrijven"
    def __init__(self, id_):
        self.con = sqlite3.connect(common.data)
        self._id = id_
        self._plaatsid = self._datumid = self._songid = self._bezetid = 0
        self.plaats = self.datum = self.songtitel = self.bezetting = ""
        self.instlist = self.url = self.wwwurl = self.commentaar = ""
        self.found = False
        if id_ == 0:
            self.new()
        else:
            self.read()

    def new(self):
        dh = CodeRec("laatste", "opname")
        self._id = str(int(dh.naam) + 1)

    def read(self):
        by_id = by_url = False
        cmd = 'select * from opnames, plaatsen, datums ' \
            'left join songs on songs.id == opnames.song ' \
            'left join bezettingen on bezettingen.id == opnames.bezetting ' \
            'where plaatsen.id == opnames.plaats and datums.id == opnames.datum '
        try:
            int(self._id)
            by_id = True
        except ValueError:
            by_url = True
        if by_id:
            cmd += 'and opnames.id == "%s"' % self._id
        elif by_url:
            cmd += 'and opnames.url == "%s"' % self._id
        i = 0
        cur = self.con.execute(cmd)
        for x in cur:
            y = x
            i += 1
        ## if i == 0:
            ## # tweede poging: zoeken via url(deel)
            ## cmd = 'select * from opnames where url == "%s"' % self.id
            ## c = self.con.execute(cmd)
            ## for x in c:
                ## y = x
                ## i += 1
        if i > 1:
            raise ValueError('Query `%s` returned more than one row from table' %
                cmd)
        elif i > 0:
            self.found = True
            self._id = x[0]
            self._plaatsid = 7 # x[1]
            self._datumid = x[2]
            self._songid = x[3]
            self._bezetid = x[4]
            self.instlist = x[5]
            url = x[6].lower().replace('#', '_')
            self.url = os.path.join(common.mp3pad, url) + '.mp3'
            self.wwwurl = url.join((common.mp3root, '.mp3'))
            self.commentaar = x[7]
            self.plaats = x[9]
            self.datum = x[11]
            self.bezetting = x[22]
            self.songtitel = x[16]

    @property
    def opname_id(self):
        return self._id

    @opname_id.setter
    def opname_id(self, value):
        self._id = value

    @property
    def plaats_id(self):
        return self._plaatsid

    @plaats_id.setter
    def plaats_id(self, value):
        """als de plaats gewijzigd wordt moet ook de naam bijgewerkt worden"""
        self._plaatsid = value
        self.plaats = CodeRec("plaats", value).item_naam

    @property
    def datum_id(self):
        return self._datumid

    @datum_id.setter
    def datum_id(self, value):
        """als de datum gewijzigd wordt moet ook de naam bijgewerkt worden"""
        self._datum_id = value
        self.datum = CodeRec("datum", value).item_naam

    @property
    def song(self):
        return self._songid

    @song.setter
    def song(self, value):
        """als de song gewijzigd wordt moet ook de titel bijgewerkt worden"""
        self._songid = value
        data = Song(value)
        self.songtitel = data.songtitel if data.found else ""

    @property
    def bezet_id(self):
        return self._bezetid

    @bezet_id.setter
    def bezet_id(self, value):
        """als de bezetting gewijzigd wordt moet ook de naam bijgewerkt worden"""
        self._bezetid = value
        data = CodeRec("bezetting", value)
        self.bezetting = data.item_naam if data.found else ""

    @property
    def instrumenten(self):
        return ', '.join([CodeRec("instrument", l).item_naam for l in self.instlist])

    def write(self):
        if self.found:
            cmd = 'update opnames set plaats = "%s", datum = "%s", somg = "%s"' \
            ', bezetting = "%s",instrumenten = "%s", url = "%s", commentaar = "%s" ' \
            'where id == "%s"' % (self._plaatsid, self._datumid, self._songid,
            self._bezetid, self.url, self.commentaar, self._id)
        else:
            cmd = 'insert into opnames (id, plaats, datum, song, bezetting, ' \
            'instrumenten, url, commentaar) values ("%s", "%s", "%s", "%s", "%s", ' \
            '"%s","%s","%s")' % (self._id, self._plaatsid, self._datumid,
            self._songid, self._bezetid, self.url, self.commentaar)
        try:
            c = self.con.execute(cmd)
        except sqlite3.OperationalError as mld:
            print(cmd)
            raise common.DataError(mld)
        except:
            raise common.DataError("Bijwerken mislukt")
        self.con.commit()
        if not self.found:
            dh = CodeRec("laatste", "opname")
            dh.setAttr("naam", self._id)
            dh.write()
            self.found = True
