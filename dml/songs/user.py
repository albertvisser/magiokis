# -*- coding: UTF-8 -*-
import sqlite3
import common
from coderec import CodeRec

class User:
    "lees een bepaalde user en controleer of deze een bepaald password heeft"
    def __init__(self, userid, paswd): # user aanmaken
        self.userfound = False
        self.con = sqlite3.connect(common.data)
        self.userid = userid
        self.paswd = paswd
        self.read()
        if self.paswd != dh.password:
            self.paswdok = False
            raise common.DataError("Password mismatch")
        else:
            self.paswdok = True

    def read(self):
        cmd = "select * from users where id == '%s'" % self.userid
        try:
            c = self.con.execute(cmd)
        except sqlite3.OperationalError as mld:
            raise common.DataError(mld)
        except:
            ## print self.__dict__
            raise common.DataError("User niet gevonden")
        self.userfound = True

    def set_pass(self,value):
        "wijzigen van het wachtwoord"
        self.paswd = value

    def write(self):
        if self.found:
            cmd = 'update registraties set muziek = "%s",tekst = "%s"' \
                ',titel = "%s",datering = "%s",datumtekst = "%s",url = "%s"' \
                ',commentaar = "%s" where id == "%s"' % (self.muziek_id,
                self.tekst_id, self.songtitel, self.datering, self.datumtekst,
                self.url, self.commentaar, self.id)
        else:
            cmd = 'insert into registraties (id,muziek,tekst,titel,datering,' \
                'datumtekst,url,commentaar) values ("%s","%s","%s","%s","%s","%s"' \
                ',"%s","%s")' % (self.id, self.muziek_id, self.tekst_id,
                self.songtitel, self.datering, self.datumtekst, self.url,
                self.commentaar)
        c = self.con.execute(cmd)
        self.con.commit()
        if not self.found:
            self.userfound = True

