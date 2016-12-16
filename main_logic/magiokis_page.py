# -*- coding: UTF-8 -*-
"""aan de hand van meegegeven argumenten een webpagina opbouwen
 +-----------------------------+
 |  bovenbalk                  |
 +------+----------------------+
 | zij  |        main          |
 | balk |       content        |
 +------+----------------------+
 in de "bovenbalk" zit een "sectienavigatie" m.b.v. een imagemap
 in de "linkerzijbalk" zit een subsectienavigatie m.b.v. links
 in het rechterzijgedeelte zit de eigenlijke inhoud
 minimaal dus twee argumenten nodig: sectie en subsectie
 basis is een tabel opgebouwd ala:
    - sectienaam
    - subsectienaam
    - inhoud voor bovenbalk
    - inhoud voor linkerkant
    - inhoud voor rechterkant
 of twee tabellen:
    - sectienaam
    - inhoud voor bovenbalk
    en
    - sectienaam
    - subsectienaam
    - inhoud voor linkerkant
    - inhoud voor rechterkant
 logica: lees de betreffende inhoud regel voor regel in een list
         schrijf de regels uit de list op de juiste plaats in het template
"""
import sys
import os
import shared
import io

dmlpad = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dml')
sys.path.append(dmlpad) # pad naar de dml-programmatuur
from pagehandler import ListTocs, Toc, Page

sys.path.append(os.path.join(dmlpad, "denk"))
from denk_trefw import trefwoordenlijst, Trefwoord
from denk_item import denk_lijst, DenkItem

option_tpl = '<option%s value="%s">%s</option>'

def denkbank(trefwoord="", tekstnr=0):
    "samenstellen paginadeel (form)"
    regels = []
    with open(os.path.join(shared.htmlpad, 'Denk', 'select.html')) as template:
        for line in template:
            line = line.rstrip()
            if '<trefwoordenlijst>' in line:            #   selector voor trefwoorden opbouwen
                for x in trefwoordenlijst()[0]:                    # trefwoord selecteren in trefwoorden-selector
                    s = ''
                    if x == trefwoord:
                        s = ' selected'
                    regels.append('    ' + option_tpl % (s, x, x))
            elif '<titellijst>' in line:                   #   selector voor titels opbouwen (niet bij eerste keer)
                if trefwoord != 'init':
                    th = Trefwoord(trefwoord)
                    th.read()
                    if len(th.tekstrefs) != 0:
                        for x in th.tekstrefs:                # zoek in denkerij.xml de <gedenk> elementen met deze waarden als id
                            dh = DenkItem(x)
                            dh.read()
                            s = ""
                            if int(x) == tekstnr:
                                s = ' selected'
                            regels.append('    ' + option_tpl % (s,x, dh.titel))
            elif '<gekozentekst>' in line:                #   gevraagde tekst toevoegen in textarea
                if trefwoord != 'init' and tekstnr != -1:
                    dh = DenkItem(tekstnr)
                    dh.read()
                    #~ titel = dh.Titel
                    for x in dh.tekst:
                        regels.append(x)
            else:
                regels.append(line)
    return regels

class Pagina:
    "Argumenten omrekenen naar indices en terug te sturen pagina opbouwen"
    def __init__(self, data):
        self.regels = []
        self.sectie = data["sectie"] if "sectie" in data else ''
        self.subsectie = data["subsectie"] if "subsectie" in data else ''
        self.selitem = data["selitem"] if "selitem" in data else ''
        self.toc = Toc(self.sectie)
        if not self.toc.found:
            self.regel_erbij("Geen sectienaam opgegeven of deze bestaat niet: %s" %
                self.sectie)
            return
        self.page = Page(self.sectie, self.subsectie, self.selitem)
        if not self.page.found and len(self.page.regels) == 0:    # was:  if self.subsectie not in self.toc.items:
            self.regel_erbij("Geen subsectie opgegeven of deze bestaat niet: %s" %
                self.subsectie)
            return
        self.titel = self.sectie + '_' + self.subsectie
        self.selid = data["selid"] if "selid" in data else ''
        self.trefwoord = data["trefwoord"] if "trefwoord" in data else ''
        self.tekstid = data["tekstid"] if "tekstid" in data else ''
        try:
            self.tekstnr = int(self.tekstid)
        except ValueError:
            self.tekstnr = -1
        ## self.regels = [str(self.__dict__)]
        ## return
        with open(os.path.join(shared.htmlpad,'page.html')) as template:
            for y in template:
                x = y.rstrip()
                h = x.split()
                if h[0] != '<!--':
                    ## self.regels.append('\nnot a comment\n')
                    if 'magiokis.css' in x:
                        self.regel_erbij(x % shared.httproot)
                        if self.sectie == 'Dicht':
                            self.regel_erbij(x.replace('magiokis',
                                'style/dicht_html') % shared.httproot)
                        elif self.sectie in ('OW','SpeelMee',"Speel","Zing"):
                            self.regel_erbij(x.replace('magiokis',
                                'style/songtekst_html') % shared.httproot)
                        elif self.sectie == 'Vertel':
                            self.regel_erbij(x.replace('magiokis',
                                'style/vertel_html') % shared.httproot)
                        elif self.sectie == 'Act':
                            self.regel_erbij(x.replace('magiokis',
                                'style/toneelstuk_html') % shared.httproot)
                    else:
                        self.regel_erbij(x)
                elif x == '<!-- titel <title>%s</title> -->':
                    ## self.regels.append('\ntitle\n')
                    self.regel_erbij(" <title>%s</title>" % self.titel)
                elif x == "<!-- js goes here -->":
                    ## self.regels.append('\njs\n')
                    if self.titel == 'Denk_Select':
                        self.denkbankjs_out()
                elif x == '<!-- topbalk -->':
                    ## self.regels.append('\ntopbalk\n')
                    self.topbalk_out()
                elif x == "<!-- toc -->":
                    ## self.regels.append('\ntoc\n')
                    self.toc_out()
                elif x == "<!-- inhoud -->":
                    ## self.regels.append('\ninhoud\n')
                    if self.titel == 'Denk_Select':
                        for y in denkbank(self.trefwoord, self.tekstnr):
                            self.regel_erbij(y)
                    else:
                        self.inhoud_out()

    def denkbankjs_out(self):
        "JavaScript t.b.v. de DenkBank in header invoegen"
        #~ self.denkbankjs_data = os.path.join(htmlpad,'Denk/Functions.js')
        #~ foud = open(self.denkbankjs_data, 'r')
        #~ regels = foud.readlines()
        #~ foud.close()
        with open(os.path.join(shared.htmlpad, 'Denk', 'functions.js')) as f_in:
            for x in f_in:
                self.regel_erbij(x.rstrip())

    def topbalk_out(self):
        "Schrijf HTML-code voor de selectiebalk bovenin"
        with open(os.path.join(shared.htmlpad, 'Topbar.html')) as f_in:
            for x in f_in:
                x = x.rstrip()
                if '@@@@' in x:
                    self.regel_erbij(x.replace('@@@@', self.sectie))
                elif ('section=%s&' % self.sectie) in x:
                    self.regel_erbij('<!-- {} -->'.format(x))
                else:
                    self.regel_erbij(x)

    def toc_out(self):
        "Schrijf HTML-code voor de inhoudsopgave aan de linkerkant"
        regels = []
        ## print self.selitem.join(('.','.'))
        for h in self.toc.lines:
            z = 'section=%s&amp;subsection=%s"' % (self.sectie, self.subsectie)
            if self.sectie == 'Act':
                z = z[:-1]
            if z in h:
                spc = ' '
                zz = ('<a href="%%cgipad%%cgiprog?%s>' % z)
                if self.selitem == "" or self.selitem == "1":
                    x1 = h.replace(zz, spc)
                    x2 = x1.replace('</a>',spc)
                else:
                    x2 = h
                ## print x2
                if '<p' in x2:
                    x3 = x2.replace('<p', '<p class="back"')
                elif '<div' in x2:
                    x3 = x2.replace('<div', '<div class="back"')
                elif '<span' in x2:
                    x3 = x2.replace('<span', '<span class="back"')
                elif '<li class="nobul">' in x2:
                    if self.selitem == "" or self.selitem == "1":
                        x3 = x2.replace('<li class="nobul">',
                            '<li class="nobul"><span class="backnb">')
                        x3 = x3.replace('</li>','</span></li>')
                    else:
                        x3 = x2.replace('<li class="nobul">',
                            '<li class="nobul"><span class="back2nb">')
                        x3 = x3.replace('</li>','</span></li>')
                elif x2 != " &nbsp; <br/>":
                    x3 = x2.join(('<span class="back">','</span>'))
                else:
                    x3 = x2
                if self.sectie == 'Act':
                    x3 = '<span class="back2nb">%s<br/></span>' % self.subsectie
                self.regel_erbij(x3)
            else:
                self.regel_erbij(h)

    def inhoud_out(self):
        "Schrijf HTML-code voor de kern van de pagina"
        # alternatieve afhandeling m.b.v. xml-databases
        r = []
        if self.page.found:
            #~ self.regel_erbij('<p>&nbsp;</p>')
            if self.page.adres != "":
                fullpath = os.path.join(shared.docroot, self.page.adres)
                if sys.version < '3':
                    fl = open(fullpath) # io.TextIOWrapper(open(fullpath), encoding='utf-8')
                else:
                    fl = open(fullpath, encoding='latin-1')
                with fl:
                    for x in fl:
                        self.regel_erbij(x) # .decode('latin-1'))
        if len(self.page.regels) > 0:
            for x in self.page.regels:
                self.regel_erbij(x)

    def regel_erbij(self, x):
        x = str(x).replace('%cgipad', shared.http_cgipad)
        x = x.replace('%cgiprog', 'mainscript.py')
        x = x.replace('%imagepad', shared.http_picpad)
        x = x.replace('%datapad', shared.docroot + os.path.sep) # '/')
        x = x.replace('%dichtpad', os.path.join(shared.docroot, 'dicht') + os.path.sep)
        x = x.replace('%xmldatapad', shared.xmlpad)
        x = x.replace('%mp3pad', shared.mp3pad)
        x = x.replace('%artpad', shared.artpad)
        self.regels.append(x)

