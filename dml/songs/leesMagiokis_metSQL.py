# -*- coding: UTF-8 -*-
from datapad import *
FIELD_MIN_WIDTH = 5
FIELD_MAX_WIDTH = 20

class doit:

    def __init__(self):
        self.con = sqlite.connect("magiokis.dat")

    def listdb(self):
        ## c = self.con.execute("PRAGMA database_list")
        ## c = self.con.execute("PRAGMA foreign_key_list(table-name);")
        ## c = self.con.execute("PRAGMA index_info(index-name);")
        ## c = self.con.execute("PRAGMA index_list(table-name);")
        cur = self.con.cursor()
        cur.execute("SELECT * FROM sqlite_master")
        for row in cur:
            print row[0],row[1],":",
            c = self.con.execute("PRAGMA table_info(%s);" % row[1])
            for x in c.fetchall():
                print x[1],
            print

    def listtables(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM sqlite_master")
        for fieldDesc in cur.description:
            print fieldDesc[0].ljust(FIELD_MAX_WIDTH) ,
        print # Finish the header with a newline.
        for fieldDesc in cur.description:
            print '-' * FIELD_MAX_WIDTH,
        print # Finish the header with a newline.
        fieldIndices = range(len(cur.description))
        for row in cur:
            for fieldIndex in fieldIndices:
                fieldValue = str(row[fieldIndex])
                print fieldValue.ljust(FIELD_MAX_WIDTH) ,

            print # Finish the row with a newline.

    def listtabellen(self):
        c = self.con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        for x in c.fetchall():
            self.listtabel(x[0])

    def listtabel(self,tabel):
        cur = self.con.cursor()
        cmd = "select * from %s order by id" % tabel
        cur.execute(cmd)
        # Print a header.
        print cmd
        print "List of records in table",tabel
        for fieldDesc in cur.description:
            print fieldDesc[0].ljust(FIELD_MAX_WIDTH) ,
        print # Finish the header with a newline.
        for fieldDesc in cur.description:
            print '-' * FIELD_MAX_WIDTH,
        print # Finish the header with a newline.

        # For each row, print the value of each field left-justified within
        # the maximum possible width of that field.
        fieldIndices = range(len(cur.description))
        for row in cur:
            for fieldIndex in fieldIndices:
                fieldValue = str(row[fieldIndex].encode("utf-8"))
                print fieldValue.ljust(FIELD_MAX_WIDTH) ,

            print # Finish the row with a newline.

        print # finish the report with a newline

    def misc(self):
        cur = self.con.cursor()
        ## cmd = 'select opnameseries.opname,songs.titel from opnameseries,opnames,songs where opnameseries.id = "B 9A" and opnameseries.opname = opnames.id and opnames.song = songs.id'
        ## # opnameseries moet een extra veld bij: opgenomen
        ## cmd = 'select * from opnameseries where id = "B9_B" and opname = ""'
        ## cmd = "select * from opnames where id in ('10','20','30')"
        cmd = 'select songseries.song,songs.titel,opnames.id,opnames.url from songseries,songs,opnames where songseries.id = "Kramp" and songs.id = songseries.song and opnames.song = songseries.song'
        cur.execute(cmd)
        print cmd
        for fieldDesc in cur.description:
            print fieldDesc[0].ljust(FIELD_MAX_WIDTH) ,
        print # Finish the header with a newline.
        for fieldDesc in cur.description:
            print '-' * FIELD_MAX_WIDTH,
        print # Finish the header with a newline.

        # For each row, print the value of each field left-justified within
        # the maximum possible width of that field.
        i = 0
        fieldIndices = range(len(cur.description))
        for row in cur:
            i += 1
            print i,
            for fieldIndex in fieldIndices:
                fieldValue = str(row[fieldIndex])
                print fieldValue.ljust(FIELD_MAX_WIDTH) ,

            print # Finish the row with a newline.

        print # finish the report with a newline


if __name__ == "__main__":
    x = doit()
    ## x.listdb()
    ## x.listtables()
    ## x.listtabel("songseries")
    ## x.listtabellen()
    x.misc()