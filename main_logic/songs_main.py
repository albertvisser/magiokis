# -*- coding: UTF-8 -*-
import sys
import os
import shutil
import shared
sys.path.append(os.path.join(shared.dmlroot, "songs"))
from common import DataError
from song import Song
from opname import Opname
from muziekreg import Muziekreg
from songtekst import Songtekst
from regtype import RegType
from coderec import CodeRec
from objectlists import ItemList, SongList, OwnerList, MemberList, Selection

songsroot = "http://songs.magiokis.nl/"
songspad = shared.xmlpad + "songs/" # geen filepad maar webadres
htmlpad = os.path.join(shared.htmlroot, "songs")
httproot = shared.httproot
http_cgipad = shared.http_cgipad.replace('local', 'songs')
HTML = "<html><head></head><body>{}</body></html>"

class Songs:
    def __init__(self, args):
        self.regels = []
        self.fout = ""
        ## self.regels = ["{}".format(args)]
        ## return
        wat = args.get("wat",'')
        ## self.regels.append('<p>{}</p>'.format(wat))
        self.select = args.get('select', '')
        if not wat:
            self.regels.append("Geen actie ('wat') opgegeven")
            return
        if wat == "start":
            self.start()
        elif wat == "lijstopnames":
            self.lijstopnames()
        elif wat == "lijstregs":
            self.lijstregs()
        elif wat == "lijstsongs":
            self.soortsel = args.get("soortsel", "")
            self.lijstsongs()
        elif wat == "detail":
            self.songid = args["songid"]
            self.wijzigO = args.get("wijzigO", False)
            self.songdetail()
        elif wat == "wijzigdetails":
            self.songid = args.get("songid", '')
            if self.songid == "":
                self.fout = "geensong"
            self.edit = args.get("edit", '')
            if self.edit:
                self.songtitel = args.get("songtitel", '')
                if self.songtitel == "":
                    self.fout = "geentitel"
                self.datering = args.get("datering", '')
                if self.datering == "":
                    self.fout = "geendatum"
                self.auteurval = args["auteurval"]
                self.makerval = args["makerval"]
                self.commentaar = args["commentaar"]
            self.wijzigdetails()
        elif wat == "wijzigsongtekst":
            self.songid = args.get("songid", '')
            if self.songid == "":
                self.fout = "geensong"
            self.fnaam = args.get("fnaam", '')
            if self.fnaam == "":
                self.fout = "geenfile"
            self.edit = args.get("edit", '')
            if self.edit:
                self.songtitel = args.get("songtitel", '')
                if self.songtitel == "":
                    self.fout = "geentitel"
                self.filenm = args["filenm"]
                self.tekst = args["tekst"]
            self.wijzigsongtekst()
        elif wat == "wijzigopname":
            self.songid = args.get("songid", '')
            if self.songid == "":
                self.fout = "geensong"
            self.opnid = args.get("opnid", '')
            if self.opnid == "":
                self.fout = "geenopname"
            self.edit = args.get("edit", '')
            if self.edit != '':
                self.plaatscode = args.get("plaatscode", '')
                if self.plaatscode == "":
                    self.fout = "geenplaats"
                self.datumcode = args.get("datumcode", '')
                if self.datumcode == "":
                    self.fout = "geendatum"
                self.bezetcode = args.get("bezetcode", 0)
                self.instcodes = args.get("instcodes", '')
                self.urlregel = args.get("urlregel", '')
                self.commentaar = args.get("commentaar", '')
            self.wijzigopname()
        elif wat == "wijzigtabel":
            self.tabnm = args["tabnm"]
            self.edit = args.get("edit", '')
            if self.edit:
                self.code = args["code"]
                self.naam = args["naam"]
                self.waarde = args.get("waarde", '')
            self.wijzigtabel()
        elif wat == "afspelen":
            self.type = args.get("type", '')
            self.id = args.get("id", "")
            self.titel = args.get("titel", '')
            if self.titel:
                self.file = self.id
                self.afspelen_xspf()
            else:
                self.titel = "(untitled)"
                self.afspelen()
        else:
            self.regels.append("onbekende actie (wat) opgegeven: '%s'" % wat)

    def start(self):
        with open(os.path.join(htmlpad, "start.html")) as f_in:
            for x in f_in:
                self.regels.append(x.rstrip())

    def lijstopnames(self):
        try:
            lh = OwnerList('opnameseries')
        except DataError as meld:
            self.fout, = meld
            series = []
        else:
            series = lh.lijst
        if self.select != "":    #-- songkeys array opbouwen: bevat de ids van alle te tonen songs
            opnameid = titel = url = []
            datum = []
            comment = []
            ## titel = [ ]
            ## mp3url = []
            try:
                lh = MemberList(self.select, 'opnameseries')
            except DataError as meld:
                self.fout = str(meld) + ' (opnameseries voor {})'.format(self.select)
            else:
                opnameid = lh.lijst
                titel = lh.titels
                url = lh.urls
            for x in opnameid:
                oh = Opname(x)
                oh.read()
                if oh.found:
                    pd = oh.plaats
                    if pd != "":
                        pd = pd.split(' - ')[0] + ", "
                    pd = pd + oh.datum
                    datum.append(pd)
                    comment.append(oh.commentaar)
                    ## mp3url.append(oh.url)
                    ## h = "(untitled)"
                    ## songid = oh.SongID
                    ## if songid != "" and songid != None:
                        ## sh = Song(songid)
                        ## sh.read()
                        ## if sh.found:
                            ## h = sh.Songtitel
                        ## else:
                            ## h = "(unknown)"
                    ## titel.append(h)
                else:
                    datum.append("")
                    comment.append("")
                    ## mp3url.append("")
                    #~ songid.append("")
                    ## titel.append("")
        inselect = False
        with open(os.path.join(htmlpad,"opnlist.html")) as template:
            for x in template:
                x = x.rstrip()
                if self.select != "":
                    if x == '<!-- select -->':
                        inselect = True
                        selrgl = []
                    if x == '<!-- endselect -->':
                        for r in selrgl:
                            if 'Lijst met opnames' in r:
                                self.regels.append(r % self.select)
                            elif '<tr><td' in r:
                                for ix, y in enumerate(opnameid):
                                    # deze voor afspelen via winamp (zie playurl.py -> self.afspelen vs. self.afspelen_xspf alhier)
                                    ## self.regels.append(r % (http_cgipad,y[1],titel[y[0]],titel[y[0]],datum[y[0]],comment[y[0]])) # .encode("iso-8859-1"
                                    # deze voor afspelen met xspf player
                                    if titel[ix] is None:
                                        titel[ix] = "(untitled)"
                                    self.regels.append(r % (http_cgipad,
                                        url[ix].lower() + '.mp3', titel[ix], titel[ix],
                                        datum[ix], comment[ix])) # .encode("iso-8859-1"
                            else:
                                self.regels.append(r)
                        if self.fout:
                            self.regels.append('<p>{}</p>'.format(self.fout))
                        inselect = False
                if inselect:
                    selrgl.append(x)
                elif "%s" in x:
                    if '<link rel="stylesheet"' in x:
                        self.regels.append(x % httproot)
                    elif 'Terug naar hoofdmenu' in x:
                        self.regels.append(x % http_cgipad)
                    elif 'lijstopnames' in x:
                        for y in series:
                            self.regels.append((x % (http_cgipad, y, y)))
                else:
                    self.regels.append(x)

    def lijstregs(self):
        self.select = self.select.lower()
        if self.select == "med":
            select = "1"
        elif self.select == "mod":
            select = "2"
        elif self.select == "xm":
            select = "3"
        elif self.select == "mid":
            select = "4"
        elif self.select == "cb":
            select = "6"
        elif self.select == "mm":
            select = "5"
        else:
            self.regels = [HTML.format("Geen of foute selectie opgegeven")]
            return
        lijst = []   #-- uit muziek.xml de registraties van een bepaald type selecteren
        if select != "":
            try:
                lh = Selection('muziek', 'type', select)
            except DataError as meld:
                naam = ''
                self.fout = meld
            else:
                l = [(lh.items[y]["Titel"], y, lh.items[y]) for y in lh.items.keys()]
                l.sort()
                lijst = [(y[1], y[2]) for y in l]    # y[0] was alleen voor het sorteren
                rh = RegType(select)
                rh.read()
                naam = rh.typenaam
                pad = rh.padnaam
                regpad = rh.htmlpadnaam

        inselect = False
        with open(os.path.join(htmlpad,"reglist.html")) as template:
            for x in template:
                x = x.rstrip()
                if select != "":
                    if x == '<!-- select -->':
                        inselect = True
                        selrgl = []
                    if x == '<!-- endselect -->':
                        for r in selrgl:
                            if 'Lijst registraties' in r:
                                self.regels.append(r % naam)
                            elif 'Klik op een titel' in r:
                                if select == "5":
                                    s = 'de muzieknotatie te bekijken'
                                else:
                                    s = 'de opname te beluisteren'
                                self.regels.append(r % s)
                            elif '<tr><td' in r:
                                for y in lijst:
                                    ## print y
                                    titel = y[1]["Titel"]
                                    ## mp3url = y[1]["Urltekst"]
                                    mp3url = y[1]["File"].lower()
                                    comment = y[1].get("Commentaar",'')
                                    if mp3url == "":
                                        urltekst = titel
                                    else:
                                        if select == "5":
                                            urldeel = ('%sshowpic.py?picture=%s'
                                                '&pad=%smmap' % (http_cgipad,
                                                mp3url, shared.datapad))
                                        else:
                                            urldeel = ('%splayurl.py?type=%s'
                                                '&id=%s' % (http_cgipad,
                                                self.select, y[0])) # mp3url
                                        urltekst = ('<a target="_blank" href="%s">'
                                            '%s</a></td>' % (urldeel, titel))
                                    self.regels.append(r % (urltekst,comment))
                            else:
                                self.regels.append(r)
                        inselect = False
                if inselect:
                    selrgl.append(x)
                elif "%s" in x:
                    if '<link rel="stylesheet"' in x:
                        self.regels.append(x % httproot)
                    elif 'Terug naar hoofdmenu' in x:
                        self.regels.append(x % http_cgipad)
                else:
                    self.regels.append(x)

    def lijstsongs(self):
        try:
            lh = OwnerList('letterseries')
        except DataError as meld:
            self.fout = meld
            letters = []
        else:
            letters = lh.lijst
        try:
            lh = OwnerList('jaarseries')
        except DataError as meld:
            self.fout = meld
            jaren = []
        else:
            jaren = lh.lijst
        ## print self.soortsel,self.select
        if self.soortsel == "titel":
        #-- zorgen dat 1-letter- of -cijferige titelselecties behandeld worden als letterselecties
            if len(self.select) == 1:
                for y in ["0","1","2","3","4","5","6","7","8","9"]:
                    if self.select == y:
                        self.select = "0"
                        break
                for y in letters:
                    if self.select == y:
                        self.soortsel = "letter"
                        break
        elif self.soortsel == "":
        #-- kijken of afgeleid kan worden wat voor soort selectie er gemaakt moet worden
            if self.select != "":
                for y in letters:
                    if self.select == y:
                        self.soortsel = "letter"
                        break
                if self.soortsel == "":
                    for y in jaren:
                        if self.select == y:
                            self.soortsel = "jaar"
                            break
    #--
    #-- songkeys array opbouwen: bevat de ids van alle te tonen songs
    #--
        songid = []
        if self.select != "":
            if self.soortsel == "titel":
                try:
                    lh = SongList()
                except DataError as meld:
                    self.fout = meld
                else:
                    for x in lh.items.keys():
                        if self.select.upper() in lh.items[x].upper():
                            songid.append(x)
            else:
                if self.soortsel == "letter":
                    h = 'letterseries'
                elif self.soortsel == "jaar":
                    h = 'jaarseries'
                try:
                    lh = MemberList(self.select, h)
                except DataError as meld:
                    self.fout = meld
                    songid = []
                else:
                    songid = lh.lijst
            if len(songid) > 0: #--  bouw een tabel op met titels, dateringen, beschrijvingen en song-ids
                titel = []
                datum = []
                comment = []
                for x in songid:
                    sh = Song(x)
                    sh.read()
                    if sh.found:
                        #~ print sh.__dict__
                        titel.append(sh.songtitel)
                        datum.append(sh.datering)
                        comment.append(sh.commentaar)

        #~ print songid
        #~ print titel
        #~ print datum
        #~ print comment
        if self.select != "" and len(songid) == 1:
            self.regels.append('Location: {}songs_detail.py?song={}'.format(
                http_cgipad, songid[0]))
            return

        op = ""
        inselect = False
        with open(os.path.join(htmlpad,"songlist.html")) as template:
            for x in template:
                x = x.rstrip()
                if '<table' in x:
                    selrgl = []
                    inselect = True
                if x == '<!-- endselect -->': # and inselect:
                    schrijfdoor = True
                    for r in selrgl:
                        if '<table' in r:
                            if len(songid) == 0:
                                schrijfdoor = False
                            else:
                                self.regels.append(r)
                        elif '<tr><td' in r:
                            if schrijfdoor:
                                for h in range(len(songid)):
                                    self.regels.append(r % (http_cgipad,
                                        str(songid[h]), titel[h], datum[h],
                                        comment[h]))
                        elif '</table' in r:
                            if len(songid) == 0:
                                schrijfdoor = True
                            else:
                                self.regels.append(r)
                        elif '<h3>' in r:
                            h = ''
                            if len(songid) == 0:
                                if self.select != "" and self.soortsel != "":
                                    h = 'Geen gegevens gevonden'
                            elif len(songid) == 1:
                                h = 'Even geduld, detailscherm komt eraan'
                            self.regels.append(r % h)
                        elif schrijfdoor:
                            self.regels.append(r)
                        else:
                            if selrgl == '</table>':
                                if len(songid) == 1:
                                    self.regels.append("Even geduld, detailscherm komt eraan".join(selrgl[-1]))
                    inselect = False
                if "alfabet:" in x:
                    op = "alfabet"
                elif "jaar:" in x:
                    op = "jaar"
                if inselect:
                    selrgl.append(x)
                elif "%s" in x:
                    if '<link rel="stylesheet"' in x:
                        self.regels.append(x % httproot)
                    elif 'Terug naar hoofdmenu' in x:
                        self.regels.append(x % http_cgipad)
                    elif 'lijstsongs' in x:
                        if op == "alfabet":
                            for y in letters:
                                h = "0-9" if y == 0 else y
                                self.regels.append(x % (http_cgipad, y, h))
                        elif op == "jaar":
                            for y in jaren:
                                self.regels.append(x % (http_cgipad, y, y))
                        else:
                            self.regels.append(x % http_cgipad)
                    elif 'lijst met' in x:
                        if self.select != "":
                            if self.soortsel == "letter":
                                h = ('songtitels beginnend met "%s"' % self.select)
                            elif self.soortsel == "jaar":
                                #~ if select == "1985":
                                    #~ select = "1985-1989"
                                if self.select == "1993":
                                    self.select = "1993 en later"
                                h = ("songs uit %s" % self.select)
                            elif self.soortsel == "titel":
                                h = ('songtitels met "%s" erin' % self.select)
                            self.regels.append(x % h)
                else:
                    self.regels.append(x)


    def songdetail(self):
        #   lees de gegevens van de opgegeven song
        sh = Song(self.songid)
        sh.read()
        if sh.found:
            songtitel = sh.songtitel
            auteur = sh.tekst_van
            maker = sh.muziek_van
            datering = sh.datumtekst or sh.datering
            fnaam = sh.url
            if fnaam == "":
                fnaam = songtitel + ".xml"
            fnaam = fnaam.lower()
            commentaar = sh.commentaar
        else:
            self.regels = [HTML.format("Song-gegevens niet aanwezig")]
            return
        #   lijstje met opnames maken
        try:
            lh = MemberList(self.songid, 'songopnames')
        except DataError as meld:
            self.fout = meld
            opnameids = []
        else:
            opnameids = lh.lijst
        #   lees de gegevens van de opgegeven opnames
        datumplaats, bezet, opnids, urls, commentaar2 = [], [], [], [], []
        for z in opnameids:                                # opnames langs
            oh = Opname(z)
            oh.read()
            if oh.found:
                plaatstekst = oh.plaats
                if plaatstekst != "" and oh.datum != '':
                    plaatstekst += ", "
                plaatstekst += oh.datum
                datumplaats.append(plaatstekst)
                bezettingtekst = oh.bezetting or ''
                hlp = oh.instrumenten or ''
                if bezettingtekst != "" and hlp != '':
                    bezettingtekst += ", "
                bezettingtekst += hlp
                bezet.append(bezettingtekst)
                opnids.append(oh.opname_id)
                urls.append(oh.url)
                commentaar2.append(oh.commentaar)
        #   lijstje met muziekregistraties maken
        try:
            lh = MemberList(self.songid, 'songregistraties')
        except DataError as meld:
            self.fout = meld
            regids = []
        else:
            regids = lh.lijst
        #   lees de gegevens van de opgegeven registraties
        regs = []
        for z in regids:                                   # registraties langs
            rh = Muziekreg(z)
            rh.read()
            if rh.found:
                regs.append((rh.regtype, rh.url, rh.commentaar, rh.type))

        #   tekst
        songtekstregels = []
        ds = Songtekst(self.songid)
        ds.read()
        if ds.found:
            songtekstregels = ds.regels

        listopn = False
        listreg = False
        listtxt = False
        with open(os.path.join(htmlpad,"songdetail.html")) as template:
            for x in template:
                x = x.rstrip()
                if "<!-- opnames -->" in x:
                    listopn = True
                elif "<!-- endopnames -->" in x:
                    listopn = False
                elif "<!-- registraties -->" in x:
                    listreg = True
                elif "<!-- endregistraties -->" in x:
                    listreg = False
                elif "<!-- tekst -->" in x:
                    listtxt = True
                elif "<!-- endtekst -->" in x:
                    listtxt = False
                elif "%s" in x:
                    if "stylesheet" in x:
                        self.regels.append(x % httproot)
                    elif "Terug naar hoofdmenu" in x:
                        self.regels.append(x % http_cgipad)
                    elif "Titel:" in x:
                        self.regels.append(x % songtitel)
                    elif "Tekst van:" in x:
                        self.regels.append(x % auteur)
                    elif "Muziek van:" in x:
                        self.regels.append(x % maker)
                    elif "Datering:" in x:
                        self.regels.append(x % datering)
                    elif "Opmerkingen:" in x:
                        self.regels.append(x % commentaar)
                    elif "Wijzig details" in x:
                        self.regels.append(x % (http_cgipad,
                            str(self.songid)))
                    elif "Terug naar lijst" in x:
                        self.regels.append(x % http_cgipad)
                    elif '%sOpnames' in x:
                        if len(datumplaats) > 0:
                            self.regels.append(x % ("on", '<a href="#opnames">',
                                '</a>'))
                        else:
                            self.regels.append(x % ("no", '', ''))
                    elif '%sMuziekregistraties' in x:
                        if len(regids) > 0:
                            self.regels.append(x % ("on", '<a href="#muziek">',
                                '</a>'))
                        else:
                            self.regels.append(x % ("no", '', ''))
                    elif '%sTekst' in x:
                        if len(songtekstregels) > 0:
                            self.regels.append(x % ("on", '<a href="#tekst">',
                                '</a>'))
                        else:
                            self.regels.append(x % ("no", '', ''))
                    elif 'name="opnames"' in x:
                        title, table, row, endtable = x.split("$$")
                        if listopn and len(datumplaats) > 0:
                            self.regels.append(title % "Opnames:")
                            self.regels.append(table)
                            for ix, data in enumerate(datumplaats):
                                if self.wijzigO:
                                    link = ('%swijzigopname.py?song=%s'
                                        '&opname=%s' % (http_cgipad,
                                        str(self.songid), opnameids[ix]))
                                else:
                                    link = '%splayurl.py?id=%s&type=mp3' % (
                                        http_cgipad, opnids[ix])
                                self.regels.append(row % (link, data, bezet[ix],
                                    commentaar2[ix]))
                            self.regels.append(endtable)
                        else:
                            self.regels.append(title % "Geen opnames aanwezig")
                            self.regels.append("<br/>")
                    elif 'name="muziek"' in x:
                        title, table, row, endtable = x.split("$$")
                        if listreg and len(regids) > 0:
                            self.regels.append(title % "Registraties:")
                            if listreg and len(regids) > 0:
                                self.regels.append(table)
                                for ix, data in enumerate(regids):
                                    if regs[ix][3] == '5':
                                        urldeel = ('%sshowpic.py?picture=%s'
                                            '&pad=%smmap' % (http_cgipad,
                                            os.path.basename(regs[ix][1]).lower(),
                                            shared.datapad))
                                    else:
                                        urldeel = regs[ix][1].lower()
                                    self.regels.append(row % (urldeel,
                                        regs[ix][0], regs[ix][2]))
                            self.regels.append(endtable)
                        else:
                            self.regels.append(title % "Geen registraties aanwezig")
                            self.regels.append("<br/>")
                    elif 'name="tekst"' in x:
                        if listtxt and len(songtekstregels) > 0:
                            self.regels.append(x % "Songtekst:")
                        else:
                            self.regels.append(x % "Geen songtekst aanwezig")
                    elif '%sSongtekst' in x:
                        if len(songtekstregels) > 0:
                            link = ('<a href="%swijzigsongtekst.py?song=%s&fnaam=%s'
                                '">' % (http_cgipad, str(self.songid), fnaam))
                            self.regels.append(x % (link,' wijzigen</a>'))
                        else:
                            self.regels.append(x % ("",' opvoeren'))
                elif 'id="teksttab"' in x and listtxt and len(songtekstregels) > 0:
                    self.regels.append(x)
                    for y in songtekstregels:
                        self.regels.append("%s<br />" % y)
                else:
                    self.regels.append(x)

    def wijzigdetails(self):
        if self.edit and self.fout == "":
    #------ song wijzigen in songs.xml
            sh = Song(self.songid)
            sh.songtitel = self.songtitel
            sh.auteur = self.auteurval
            sh.maker = self.makerval
            sh.datering = self.datering
            if self.commentaar != "":
                sh.commentaar = self.commentaar
            sh.write()
        fnaam = songtitel = auteurval = auteur = makerval = maker = ""
        datering = commentaar = ""
        auteurkey, auteurnaam, makerkey, makernaam = [], {}, [], {}
        #   tabellen inlezen t.b.v. selectievakjes
        try:
            lh = ItemList('tekst')
        except DataError as meld:
            self.fout, = meld
        else:
            auteurkey = list(lh.lijst.keys())
            auteurkey.sort()
            auteurnaam = lh.lijst
        try:
            lh = ItemList('muziek')
        except DataError as meld:
            self.fout, = meld
        else:
            makerkey = list(lh.lijst.keys())
            makerkey.sort()
            makernaam = lh.lijst
        #   lees de gegevens van de opgegeven song
        sh = Song(self.songid)
        sh.read()
        if sh.found:
            songtitel = sh.songtitel
            auteurval = str(sh.auteur)
            auteur = str(sh.tekst_van)
            makerval = str(sh.maker)
            maker = str(sh.muziek_van)
            datering = sh.datering
            fnaam = sh.url
            commentaar = sh.commentaar
        with open(os.path.join(htmlpad,"wijzigdetail.html")) as f_in:
            for x in f_in:
                x = x.rstrip()
                if 'Tekst van:' in x:
                    typesel = "tekst"
                elif 'Muziek van:' in x:
                    typesel = "muziek"
                if "%s" in x:
                    if "stylesheet" in x:
                        self.regels.append(x % httproot)
                    elif "Terug naar hoofdmenu" in x:
                        self.regels.append(x % http_cgipad)
                    elif "Terug naar overzicht" in x:
                        self.regels.append(x % (http_cgipad, str(self.songid)))
                    elif "Terug naar lijst" in x or "form action" in x:
                        self.regels.append(x % http_cgipad)
                    elif 'Details van song:' in x:
                        self.regels.append(x % str(self.songid))
                    elif "option %s" in x:
                        if typesel == "tekst":
                            for i in auteurkey:
                                h = ""
                                if i == auteurval:
                                    h = 'selected="selected" '
                                self.regels.append(x % (h,i,auteurnaam[i][0]))
                        elif typesel == "muziek":
                            for i in makerkey:
                                h = ""
                                if i == makerval:
                                    h = 'selected="selected" '
                                self.regels.append(x % (h,i,makernaam[i][0]))
                    elif "Titel:" in x:
                        self.regels.append(x % songtitel)
                    elif "Datering:" in x:
                        self.regels.append(x % datering)
                    elif "Opmerkingen :" in x:
                        self.regels.append(x % commentaar)
                    elif "<h4>" in x:
                        if self.fout == "geensong":
                            self.regels.append(x % "Geen song-id opgegeven")
                        elif self.fout == "geentitel":
                            self.regels.append(x % "Wijzigen niet mogelijk: geen songtitel opgegeven")
                        elif self.fout == "geendatum":
                            self.regels.append(x % "Wijzigen niet mogelijk: geen datering opgegeven")
                        elif self.fout != "":
                            self.regels.append(x %  self.fout)
                else:
                    self.regels.append(x)

    def wijzigsongtekst(self):
        if self.edit and self.fout == "":
            songtekstregels = self.tekst.split("\n")
            sh = Songtekst(self.songid)
            sh.titel = self.songtitel
            if self.filenm != "":
                sh.file = self.filenm
            else:
                sh.file = self.fnaam
            sh.tekst = songtekstregels
            sh.write()
        songtitel = ""
        songtekstregels = []
        ds = Songtekst(self.songid)
        ds.read()
        songtitel = ds.titel if ds.found else ''
        filenaam = ds.file if ds.found else ''
        songtekstregels = ds.regels if ds.found else ''
        #~ print ds.__dict__
        with open(os.path.join(htmlpad, "wijzigsongtekst.html")) as template:
            for x in template:
                x = x.rstrip()
                if "%s" in x:
                    rrh = x.split("%s")
                    if "stylesheet" in x:
                        self.regels.append(x % httproot)
                    elif "Terug naar hoofdmenu" in x:
                        self.regels.append(x % httproot)
                    elif "Terug naar overzicht" in x:
                        self.regels.append(x % (http_cgipad, str(self.songid)))
                    elif "Terug naar lijst" in x or "form action" in x:
                        self.regels.append(x % http_cgipad)
                    elif "titel" in x:
                        self.regels.append(x % songtitel)
                    elif '"song"' in x:
                        self.regels.append(x % str(self.songid))
                    elif "tekst" in x:
                        starttext, endtext = x.split("%s")
                        for ix, regel in enumerate(songtekstregels):
                            s = [""]
                            if ix == 0:
                                s.append(starttext)
                            s.append(regel)
                            if ix == len(songtekstregels) - 1:
                                s.append(endtext)
                            self.regels.append("".join(s))
                    elif "fnaam" in x:
                        self.regels.append(x % self.fnaam)
                    elif "filenm" in x:
                        self.regels.append(x % filenaam)
                    elif "<h4>" in x:
                        if self.fout == "geensong":
                            self.regels.append(x % "Geen song-id opgegeven")
                        elif self.fout == "geenfile":
                            self.regels.append(x % "Geen filenaam opgegeven")
                        elif self.fout == "geentitel":
                            self.regels.append(x % "Wijzigen niet mogelijk: "
                                "geen songtitel opgegeven")
                        elif self.fout != "":
                            self.regels.append(x % self.fout)
                else:
                    self.regels.append(x)

    def wijzigopname(self):
    #------ opname wijzigen in opnames.xml
        if self.edit and self.fout == "":
            oh = Opname(self.opnid)
            oh.song = self.songid
            oh.plaats_id = self.plaatscode
            oh.datum_id = self.datumcode
            if self.bezetcode != 0:
                oh.bezet_id = self.bezetcode
            if self.instcodes != "":
                oh.instlist = self.instcodes
            if self.urlregel != "":
                oh.url = self.urlregel
            if self.commentaar != "":
                oh.commentaar = self.commentaar
            oh.write()
        plaatskey = datumkey = bezettingkey = instkey = ""
        urltekst = commentaartekst = instkeytekst = ""
        plaatskeys, plaatsitems, datumkeys, datumitems = [], {}, [], {}
        bezetkeys, bezetitems, instkeys, institems = [], {}, [], {}
        #   tabellen inlezen t.b.v. selectievakjes
        try:
            lh = ItemList('plaats')
        except DataError as meld:
            self.fout, = meld
        else:
            plaatskeys = list(lh.lijst.keys())
            plaatskeys.sort()
            plaatsitems = lh.lijst
        try:
            lh = ItemList('datum')
        except DataError as meld:
            self.fout, = meld
        else:
            datumkeys = list(lh.lijst.keys())
            datumkeys.sort()
            datumitems = lh.lijst
        try:
            lh = ItemList('bezetting')
        except DataError as meld:
            self.fout, = meld
        else:
            bezetkeys = list(lh.lijst.keys())
            bezetkeys.sort()
            bezetitems = lh.lijst
        try:
            lh = ItemList('instrument')
        except DataError as meld:
            self.fout, = meld
        else:
            instkeys = list(lh.lijst.keys())
            instkeys.sort()
            institems = lh.lijst
    #   lees de gegevens van de opgegeven opname
        oh = Opname(self.opnid)
        oh.read()
        if oh.found:
            plaatskey, datumkey = oh.plaats_id, oh.datum_id
            bezettingkey, instkey = oh.bezet_id, oh.instlist
            urltekst, commentaartekst = oh.url, oh.commentaar
        with open(os.path.join(htmlpad, "wijzigopname.html")) as template:
            for x in template:
                x = x.rstrip()
                if "%s" in x:
                    if "stylesheet" in x:
                        self.regels.append(x % httproot)
                    elif "Terug naar hoofdmenu" in x:
                        self.regels.append(x % httproot)
                    elif "Terug naar overzicht" in x:
                        self.regels.append(x % (http_cgipad, str(self.songid)))
                    elif "Terug naar lijst" in x or "form action" in x:
                        self.regels.append(x % http_cgipad)
                    elif "Details van opname" in x:
                        self.regels.append(x % (str(self.songid), str(self.opnid)))
                    elif 'name="Plaats"' in x:
                        select, option, endselect = x.split("$s")
                        self.regels.append(select)
                        for i in plaatskeys:
                            h = ' selected="selected"' if i == plaatskey else ''
                            self.regels.append(option % (h, i, plaatsitems[i][0]))
                        self.regels.append(endselect)
                    elif 'name="Datum"' in x:
                        select, option, endselect = x.split("$s")
                        self.regels.append(select)
                        for i in datumkeys:
                            h = ' selected="selected"' if i == datumkey else ''
                            self.regels.append(option % (h, i, datumitems[i][0]))
                        self.regels.append(endselect)
                    elif 'name="Bezet"' in x:
                        select, option, endoption, endselect = x.split("$s")
                        self.regels.append(select)
                        h = ' selected="selected"' if bezettingkey == "" else ''
                        self.regels.append(option % h)
                        for i in bezetkeys:
                            h = ' selected="selected"' if i == bezettingkey else ''
                            self.regels.append(endoption % (h, i, bezetitems[i][0]))
                        self.regels.append(endselect)
                    elif 'name="Inst"' in x:
                        select, option, endselect = x.split("$s")
                        self.regels.append(select)
                        for i in instkeys:
                            h = ""
                            if i in instkey:
                                self.regels.append(option % (h, i, institems[i][0]))
                        self.regels.append(endselect)
                    elif 'name="InstList"' in x:
                        select, option, endselect = x.split("$s")
                        self.regels.append(select)
                        for i in instkeys:
                            h = ""
                            if i not in instkey:
                                self.regels.append(option % (h, i, institems[i][0]))
                        self.regels.append(endselect)
                    elif "Filenaam:" in x:
                        self.regels.append(x % urltekst)
                    elif "Opmerkingen:" in x:
                        self.regels.append(x % commentaartekst)
                    elif "instcodes" in x:
                        self.regels.append(x % instkeytekst)
                    elif "<h4>" in x:
                        if self.fout == "geensong":
                            f = "Geen song-id opgegeven"
                        elif self.fout == "geenopname":
                            self.regels.append(x % "Geen opname-id opgegeven")
                        elif self.fout == "geenplaats":
                            self.regels.append(x % "Wijzigen niet mogelijk: "
                                "geen opnameplaats opgegeven")
                        elif self.fout == "geendatum":
                            self.regels.append(x % "Wijzigen niet mogelijk: "
                                "geen opnamedatum opgegeven")
                        elif self.fout != "":
                            self.regels.append(x % self.fout)
                else:
                    self.regels.append(x)

    def wijzigtabel(self):
        tabcls = ("wi40pct","51","wi50pct")
        if self.tabnm == "Auteur":
            fn = "tekst"
        elif self.tabnm == "Maker":
            fn = 'muziek'
        elif self.tabnm == "Plaats":
            fn = 'plaats'
        elif self.tabnm == "Datum":
            fn = 'datum'
            tabcls = ("wi30pct", "37", "wi50pct")
        elif self.tabnm == "Bezetting":
            fn = 'bezetting'
            tabcls = ("wi65pct", "85", "wi25pct")
        elif self.tabnm == "Instrument":
            fn = 'instrument'
            tabcls = ("wi50pct", "64", "wi40pct")
        else:
            fn = self.tabnm

        if self.edit and self.fout == "":
            try:
                dh = CodeRec(fn, self.code)
            except DataError as mld:
                self.fout = mld
            else:
                dh.item_id = self.code
                dh.item_naam = self.naam
                dh.item_waarde = self.waarde
                dh.write()

        # tabel lezen
        try:
            lh = ItemList(fn)
        except DataError as meld:
            self.fout = meld
            sleutel = []
        else:
            waarde = lh.lijst
            sleutel = list(lh.lijst.keys())
            if self.tabnm not in ('Instrument'):
                sleutel = ['%05i' % int(x) for x in sleutel]
            sleutel.sort()
            if self.tabnm not in ('Instrument'):
                sleutel = [x.lstrip('0') for x in sleutel]
        inform = False
        with open(os.path.join(htmlpad, "wijzigtabel.html")) as template:
            for x in template:
                x = x.rstrip()
                if "<form" in x:
                    inform = True
                    fregels = [x]
                elif inform:
                    fregels.append(x)
                    if "</form>" in x:
                        inform = False
                        for y in sleutel:
                            self.regels.append(fregels[0] % http_cgipad)
                            self.regels.append(fregels[1] % y)
                            if self.tabnm == "Datum":
                                self.regels.append(fregels[2] % (tabcls[0],
                                    tabcls[1], waarde[y][0], y))
                                self.regels.append(fregels[3] % (waarde[y][1], y))
                                wi = "wi5pct"
                            else:
                                self.regels.append(fregels[2] % (tabcls[0],
                                    tabcls[1], waarde[y][0], y))
                                wi = "wi15pct"
                            ## self.regels.append(fregels[4] % (tabcls[2], y, fn))
                            self.regels.append(fregels[4] % (tabcls[2], y))
                            self.regels.append(fregels[5] % (self.tabnm, y))
                            self.regels.append(fregels[6] % y)
                            self.regels.append(fregels[7])
                elif "%s" in x:
                    if "stylesheet" in x:
                        self.regels.append(x % httproot)
                    elif "tabel</title>" in x:
                        self.regels.append(x % self.tabnm)
                    elif "col1" in x:
                        self.regels.append(x % tabcls[0])
                    elif "col3" in x and self.tabnm == "Datum":
                        self.regels.append(x % "Sortkey")
                    elif "col4" in x:
                        self.regels.append(x % tabcls[2])
                    elif "Terug naar hoofdmenu" in x:
                        self.regels.append(x % http_cgipad)
                    elif "Tabellenbeheer" in x:
                        if self.tabnm == "Auteur":
                            self.regels.append(x % "tekstauteurs")
                        elif self.tabnm == "Maker":
                            self.regels.append(x % 'muziek-auteurs')
                        elif self.tabnm == "Plaats":
                            self.regels.append(x % 'opnameplaatsen')
                        elif self.tabnm == "Datum":
                            self.regels.append(x % 'opnamedata')
                        elif self.tabnm == "Bezetting":
                            self.regels.append(x % 'bezettingen')
                        elif self.tabnm == "Instrument":
                            self.regels.append(x % 'instrumenten')
                elif "<h4>" in x:
                    self.regels.append(x % self.fout)
                else:
                    self.regels.append(x)

    def afspelen(self):
        if self.type == "mp3":
            h = Opname(self.id)
            # uitzoeken welke filenaam er bij hoort; het file kopieren naar een standaardnaam en dat doorgeven als redirect
            h.read()
            ## fn, _ = os.path.splitext(h.url.upper())
            fn = h.url
        else:
            h = Muziekreg(self.id)
            # uitzoeken welke filenaam er bij hoort; het file kopieren naar een standaardnaam en dat doorgeven als redirect
            h.read()
            fn = h.pad.lower() # huh? niet overal aanwezig?
        fn_to = os.path.join(htmlpad, "tempfile" + os.path.splitext(fn)[1])
        shutil.copyfile(fn, fn_to)
        self.regels.append("Location: " + songsroot + os.path.split(fn_to)[1])

    def afspelen_xspf(self):
        with open(os.path.join(htmlpad, 'xspf_player_slim.html')) as f_in, \
                open(os.path.join(htmlpad, 'tempfile.html'), 'w') as f_out:
            for x in f_in:
                if '<object' in x or '<param' in x:
                    f_out.write(x % (httproot, shared.datapad, self.type,
                        self.file, self.titel))
                else:
                    f_out.write(x)
        self.regels.append("Location: " + songsroot + 'tempfile.html')
