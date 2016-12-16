# -*- coding: UTF-8 -*-
import sqlite3
import common
from coderec import CodeRec

class RegType(object):
    def __init__(self, type):
        self.con = sqlite3.connect(common.data)
        self.found = False
        self.type = type
        self.typenaam = self.padnaam = self.htmlpadnaam = ''
        self.playernaam = self.readernaam = ''
        if type == '':
            self.new()
        else:
            self.read()

    def new(self):
        dh = CodeRec("laatste", "regtype")
        self.type = str(int(dh.item_naam) + 1)

    def read(self):
        cmd = 'select * from regtypes where id == "%s"' % self.type
        try:
            c = self.con.execute(cmd)
        except:
            print(cmd)
            raise common.DataError("Ophalen mislukt")
        i = 0
        for x in c:
            ## self.Type = x[0]
            _, self.typenaam, self.padnaam, self.htmlpadnaam, self.playernaam, \
                self.readernaam = x
            i += 1
        if i > 0:
            self.found = True

    def write(self):
        if self.found:
            cmd = 'update regtypes set naam = "%s", pad = "%s", htmlpad = "%s",'\
                'player = "%s", editor = "%s" where id == "%s"' % (self.typenaam,
                self.padnaam, self.htmlpadnaam, self.playernaam, self.readernaam,
                self.type)
        else:
            cmd = 'insert into regtypes (id, naam, pad, htmlpad, player, editor) '\
                'values ("%s", "%s", "%s", "%s", "%s", "%s")' % (self.type,
                self.typenaam, self.padnaam, self.htmlpadnaam, self.playernaam,
                self.readernaam)
        c = self.con.execute(cmd)
        self.con.commit()
        if not self.found:
            dh = CodeRec("laatste", "regtype")
            dh.item_naam = self.type
            self.found = True


