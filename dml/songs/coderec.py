# -*- coding: UTF-8 -*-
import common
import sqlite3
stypes = ("auteur", "maker", "datum")
ntypes = ("plaats", "bezetting", "instrument")
valid_types = [x for x in stypes] + [x for x in ntypes]

class CodeRec(object):
    def __init__(self, type, id):
        self.con = sqlite3.connect(common.data)
        self.item_id = id
        self.found = False
        self.type = type
        self.item_naam = ""
        self.item_waarde = ""
        if type in stypes:
            self.tbnaam = type + "s"
        elif type in ntypes:
            self.tbnaam = type + "en"
        elif type == "laatste":
            self.tbnaam = type
        else:
            raise ValueError("Onbekend coderecord type")
        if self.item_id == 0 or self.item_id == '0':
            if type != "instrument":
                self.item_id = str(self._new(type))
            ## print "nieuw id:",self.ItemID
        else:
            self.read()

    def _new(self, type):
        dh = CodeRec("laatste", type)
        i = int(dh.item_naam) + 1
        return i

    def read(self):
        self.found = False
        cmd = "select * from %s where id == '%s'" % (self.tbnaam, self.item_id)
        c = self.con.execute(cmd)
        self.con.commit()
        i = 0
        for x in c:
            self.item_id = x[0]
            self.item_naam = x[1]
            if len(x) > 2:
                self.item_waarde = x[2]
            i += 1
        if i > 0:
            self.found = True

    def write(self):
        if self.found:
            if self.type == "datum":
                cmd = 'update {} set naam = ?, waarde = ?  where id == ?'.format(
                    self.tbnaam)
                c = self.con.execute(cmd, (self.item_naam, self.item_waarde,
                    self.item_id))
            else:
                cmd = 'update {} set naam = ? where id == ?'.format(self.tbnaam)
                c = self.con.execute(cmd, (self.item_naam, self.item_id))
        else:
            if self.type == "datum":
                cmd = 'insert into {} (id, naam, waarde) values (?, ?, ?)'.format(
                    self.tbnaam)
                c = self.con.execute(cmd, (self.item_id, self.item_naam,
                    self.item_waarde))
            else:
                cmd = 'insert into {} (id, naam) values (?, ?)'.format(self.tbnaam)
                c = self.con.execute(cmd, (self.item_id, self.item_naam))
        self.con.commit()
        if self.tbnaam != "laatste":
            dh = CodeRec("laatste", self.type)
            dh.naam = str(self.item_id)
            dh.write()
        if not self.found:
            self.found = True
