# -*- coding: UTF-8 -*-
import sqlite3
import common
from coderec import CodeRec

class Lijst:
    """base class voor de diverse lijsten"""
    def __init__(self,file=""):
        self.types_codes = ('tekst', 'muziek', 'plaats', 'datum', 'bezetting',
            'instrument', 'laatste')
        self.types_omlists = ('songregistraties', 'songopnames', 'opnameseries',
            'series', 'letterseries', 'jaarseries')
        self.tbnamen = {'tekst': 'auteurs', 'muziek': 'makers',
            'plaats': 'plaatsen', 'datum': 'datums',
            'bezetting': 'bezettingen', 'instrument': 'instrumenten',
            'songregistraties': 'registraties',
            'songopnames': 'opnames', 'opnameseries': 'opnameseries',
            'series': 'songseries', 'letterseries': 'letters',
            'jaarseries': "jaren", 'laatste': 'laatste'}
        self.file_attr = {
            'songs': {
                'attr': ("tekst", "muziek"),
                'selfrom': "songs, auteurs, makers",
                'cols': "songs.id, titel, auteurs.naam, makers.naam",
                'join': "tekst = auteurs.id and muziek = makers.id",
                },
            "opnames": {
                'attr': ("song", "plaats", "datum", "bezetting"),
                'selfrom': "opnames, songs, plaatsen, datums",
                'cols': "opnames.id, songs.titel, plaatsen.naam, datums.naam, "
                    "bezetting, instrumenten, opnames.commentaar",
                'join': "song = songs.id and plaats = plaatsen.id and "
                    "datum = datums.id",
                },
            "muziek": {
                'attr': ("song", "type"),
                'selfrom': "registraties,songs,regtypes",
                'cols': "registraties.id, songs.titel, registraties.url, "
                    "regtypes.naam, registraties.commentaar",
                'join': "song = songs.id and type = regtypes.id",
                },
            }
        self.con = sqlite3.connect(common.data)

class ItemList(Lijst):
    """Bouw een lijst op van coderecords

    de lijst staat in self.lijst en is een dictionary met ids als key"""
    def __init__(self, file):
        Lijst.__init__(self,file)
        if file not in self.types_codes:
            raise common.DataError("Codetabel naam onbekend")
        cur = self.con.cursor()
        c = cur.execute("select * from %s" % self.tbnamen[file])
        data = c.fetchall()
        if data:
            self.lijst = {}
            for x in data:
                self.lijst[x[0]] = x[1:]
        else:
            raise common.DataError("Codetabel bevat geen gegevens")

class OwnerList(Lijst):
    """Zoek alle owners die members hebben
    B.v. als ik wil weten welke series er allemaal zijn

    self.lijst is hier een list met ids"""
    def __init__(self, file):
        Lijst.__init__(self,file)
        if file not in self.types_omlists:
            raise common.DataError("Onbekend type Ownerlist")
        cur = self.con.cursor()
        c = cur.execute("select distinct id from %s" % self.tbnamen[file])
        data = c.fetchall()
        if data:
            self.lijst = [x[0] for x in data]
        else:
            raise common.DataError("Geen gegevens voor deze Ownerlist")

class MemberList(Lijst):
    """Zoek alle members van een bepaalde owner

    self.list is hier een lijst met ids"""
    def __init__(self, item, file):
        Lijst.__init__(self,file)
        if file not in self.types_omlists:
            raise common.DataError("Onbekend type Memberlist")
        if file in self.types_omlists[:2]:
            cmd = 'select id from %s where song == "%s"' % (self.tbnamen[file], item)
        elif file == self.types_omlists[2]:
            cmd = ('select {0}.opname,songs.titel,songs.id,opnames.url from '
                "{0}, opnames left outer join songs on opnames.song = songs.id"
                ' where {0}.id = "{1}" and {0}.opname = opnames.id order by'
                ' {0}.rowid'.format(self.tbnamen[file], item))
        elif file in self.types_omlists[3:]:
            cmd = 'select song from %s where id = "%s"' % (self.tbnamen[file], item)
        cur = self.con.cursor()
        ## print cmd
        c = cur.execute(cmd)
        data = c.fetchall()
        if data:
            self.lijst = [x[0] for x in data if x[0] != ""]
            if file == self.types_omlists[2]:
                self.songs = [x[2] for x in data if x[0] != ""]
                self.titels = [x[1] for x in data if x[0] != ""]
                self.urls = [x[3] for x in data if x[0] != ""]
            if len(self.lijst) == 0:
                raise common.DataError("Geen members bij owner")
            self.tekst = ""
            if file == self.types_omlists[2]:
                c = cur.execute('select titel, opgenomen from %s where id = "%s"'
                    ' and opname = ""' % (self.tbnamen[file], item))
                for x in c:
                    self.titel, self.tekst = x[0], x[1]
            elif file in self.types_omlists[4:]:
                c = cur.execute('select tekst from %s where id = "%s" and'
                    ' song = ""' % (self.tbnamen[file], item))
                for x in c:
                    self.tekst = x[0]
        else:
            raise common.DataError("Geen gegevens voor deze Memberlist")


class TypeList(Lijst):
    """maak een lijst van alle regtypes in self.lijst

    de lijst staat in self.lijst en is een dictionary met ids als key"""
    def __init__(self):
        Lijst.__init__(self)
        self.items = {}
        cur = self.con.cursor()
        c = cur.execute("select * from regtypes")
        data = c.fetchall()
        if data:
            tt = [x[0] for x in cur.description]
            for x in data:
                td = {}
                for i in range(1,len(tt)):
                    td[tt[i]] = x[i]
                self.items[x[0]] = td
        else:
            raise common.DataError("Geen regtypes gevonden")

class SongList(Lijst):
    """maak een lijst van songs

    de lijst staat in self.lijst en is een dictionary met ids als key"""
    def __init__(self):
        Lijst.__init__(self)
        self.items = {}
        cur = self.con.cursor()
        c = cur.execute("select id, titel from songs")
        data = c.fetchall()
        if data:
            for x in data:
                self.items[x[0]] = x[1]
        else:
            raise common.DataError("Geen songs gevonden")

class Selection(Lijst):
    """zoek alle objecten die een bepaalde waarde hebben van een bepaald attribuut

    de lijst staat in self.lijst en is een dictionary met ids als key"""
    def __init__(self, file, attrib, value):
        self.search_attr = attrib
        self.search_val = value
        bezet = ItemList('bezetting').lijst
        m = ItemList("instrument")
        ins = m.lijst
        ins['-'] = ('',)
        Lijst.__init__(self)
        if file not in self.file_attr:
            raise common.DataError("Foutief selectietype opgegeven")
        if attrib not in self.file_attr[file]['attr']:
                raise common.DataError("Foutief attribuut opgegeven")
        selfrom = self.file_attr[file]['selfrom']
        cols = self.file_attr[file]['cols']
        join = self.file_attr[file]['join']
        cur = self.con.cursor()
        sel = '{} and {} = "{}"'.format(join, attrib, value)
        cmd = 'select %s from %s where %s' % (cols, selfrom, sel)
        ## print cmd
        c = cur.execute(cmd)
        data = c.fetchall()
        self.items = {}
        if data:
            for x in data:
                if file == "songs":
                    y = {"Titel": x[1], "Tekst_van": x[2], "Muziek_van": x[3]}
                elif file == "opnames":
                    y = {"Titel": x[1], "Plaats": x[2], "Datum": x[3]}
                    if x[4] != '':
                        y["Bezetting"] = bezet[x[4]][0]
                    if x[5] != '':
                        y["Instrumenten"] = ", ".join([ins[z][0] for z in x[5]])
                    y["Commentaar"] = x[6]
                elif file == "muziek":
                    y = {"Titel": x[1], "File": x[2], "Type": x[3],
                        "Commentaar": x[4]}
                self.items[x[0]] = y
        else:
            raise common.DataError("Geen gegevens gevonden")
