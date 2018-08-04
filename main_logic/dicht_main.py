# -*- coding: utf-8 -*-
import sys
import os
import shared
sys.path.append(os.path.join(shared.dmlroot, "dicht"))
from dicht_trefw import jarenlijst, add_jaar, trefwoordenlijst, Trefwoord
from dicht_item import DichtLijst, DichtItem

htmlroot = os.path.join(shared.htmlroot, "dicht")
httproot = shared.httproot
http_cgipad = shared.http_cgipad.replace('original', 'dicht')

class Dicht:
    def __init__(self,args):
        self.regels = []
        self.meld = ""
        if "wat" in args:
            wat = args["wat"]
        else:
            self.regels.append(" ")
            self.regels.append("argument 'wat' ontbreekt")
            return
        if "selItem" in args:
            self.sel_item = args["selItem"]
        if "selData" in args:
            self.sel_data = args["selData"]
        else:
            self.sel_data = ""
        if "selJaar" in args:
            self.sel_jaar = args["selJaar"]
        if "titel" in args:
            self.titel = args["titel"]
        if "tekst" in args:
            self.tekst = args["tekst"]
        if "gedicht" in args:
            self.gedicht = args["gedicht"]
        self.form_ok = True
        if wat == "start":
            self.start()
        elif wat == "select":
            if self.sel_item == "nwTrefw":
                if self.sel_data != "":
                    self.nieuw_trefw()
                self.sel_args('Nieuw trefwoord:<input type="text" name="txtNwTrefw"'
                    ' value="%s" size="40" maxlength="40">')
            elif self.sel_item == "nwJaar":
                if self.sel_data != "":
                    self.nieuw_jaar()
                self.sel_args('Nieuw jaar:<input type="text" name="txtNwJaar"'
                    ' value="%s" size="40" maxlength="40">')
            elif self.sel_item == "nweTekst":
                self.regels.append('Location: %sdicht_detail.py?lbSelItem=_0' %
                    http_cgipad)
            elif self.sel_item == "selJaar":
                if self.sel_data == "":
                    self.lijst = jarenlijst()
                    self.sel_args('Kies een jaar:<select name="lbSelJaar" size="1">'
                        '$s<option value="%s">%s</option>$s</select>')
                else:
                    self.select()
            elif self.sel_item == "selTrefw":
                if self.sel_data == "":
                    self.lijst = trefwoordenlijst()[0]
                    self.sel_args('Kies een trefwoord:<select name="lbSelTrefw"'
                        ' size="1">$s<option value="%s">%s</option>$s</select>')
                else:
                    self.select()
            elif self.sel_item in ["selZoek", "selTitel","selTekst","selBeide"]:
                # is selZoek met selData gevuld niet onzin?
                # en een van de andere drie zonder selData ook? Nee, dat kan submitten zonder zoektekst ingevuld zijn
                if self.sel_data == "":
                    ## self.lijst = ...
                    if self.sel_item != "selZoek":
                        self.meld = "geen zoektekst opgegeven"
                    h = ['Zoek naar: <input type="text" name="txtZoek" value=""'
                            ' size="40" maxlength="80"><br /><br />']
                    s = ' checked="checked"' if self.sel_item in ("selZoek",
                            "selTitel") else ''
                    h.append('<input type="radio" name="rbselZoek" value="selTitel"'
                                '%s>Zoek in titel<br>' % s)
                    s = ' checked="checked"' if self.sel_item == "selTekst" else ''
                    h.append('<input type="radio" name="rbselZoek" value="selTekst"'
                                '%s>Zoek in tekst<br>' % s)
                    s = ' checked="checked"' if self.sel_item == "selBeide" else ''
                    h.append('<input type="radio" name="rbselZoek" value="selBeide"'
                                '%s>Zoek in beide<br><br /><br />' % s)
                    self.sel_args(h)
                elif self.sel_item == 'selZoek':
                    self.regels.append(" ")
                    self.regels.append("selZoek met data is onzin!?")
                    return
                else:
                    self.select()
            else:
                self.regels.append(" ")
                h = self.sel_item
                if h == "":
                    h = "(niks opgegeven)"
                self.regels.append("onbekend 'selItem' bij select: %s" % h)
        elif wat == "detail" or wat == "detail_wijzig":
            self.wat = wat
            self.detail()
        else:
            self.regels.append(" ")
            self.regels.append("onbekende actie ('wat') %s" % wat)
            return

    def start(self):
        with open(os.path.join(htmlroot, "start.html")) as f_in:
            for x in f_in:
                self.regels.append(x.rstrip())

    def nieuw_trefw(self):
        for x in trefwoordenlijst()[0]:
            if x == self.sel_data:
                self.form_ok = False
                break
        if self.form_ok:
            dh = Trefwoord(self.sel_data)
            dh.write()
            self.meld = "trefwoord opgevoerd"
        else:
            self.meld = "Het opgegeven trefwoord komt al voor"

    def nieuw_jaar(self):
        for x in jarenlijst():
            if x == self.sel_data:
                self.form_ok = False
                break
        if self.form_ok:
            dh = add_jaar(self.sel_data)
            self.meld = "jaar opgevoerd"
        else:
            self.meld = "Het opgegeven jaar komt al voor"

    def sel_args(self, data):
        with open(os.path.join(htmlroot, "select_args.html")) as f_in:
            for x in f_in:
                x = x.rstrip()
                if '<title>' in x:
                    self.regels.append(x % self.sel_item)
                elif 'link rel="stylesheet"' in x:
                    self.regels.append(x % httproot)
                elif 'form action' in x:
                    self.regels.append(x % http_cgipad)
                elif x == '<!-- data -->':
                    if self.sel_item in ("nwTrefw", "nwJaar"):
                        self.regels.append(data % self.sel_data)
                    elif self.sel_item in ("selTrefw", "selJaar"):
                        select, option, endselect = data.split("$s")
                        self.regels.append(select)
                        for x in self.lijst:
                            self.regels.append(option % (x, x))
                        self.regels.append(endselect)
                    else:
                        self.regels += data
                ## elif "Terug" in x:
                    ## self.regels.append(x % http_cgipad)
                elif "submit" in x:
                    if self.sel_item in ("nwTrefw", "nwJaar"):
                        self.regels.append(x % "Opvoeren")
                    elif self.sel_item in ("selTrefw", "selJaar"):
                        self.regels.append(x % "Selectie uitvoeren")
                    else:
                        self.regels.append(x % "Zoek")
                elif 'meld' in x:
                    self.regels.append(x % self.meld)
                else:
                    self.regels.append(x)

    def select(self):
        if self.sel_item == "selTrefw":
            titel = "Dicht: zoek op trefwoord"
            th = Trefwoord(self.sel_data)
            th.read()
            self.lijst = th.tekstrefs
            self.gezocht = ('bij trefwoord %s' % self.sel_data)
            terug = 'selTrefw'
        elif self.sel_item == "selJaar":
            titel= "Dicht: zoek op trefwoord"
            th = DichtLijst(jaar=self.sel_data)
            self.lijst = th.id_titels
            self.gezocht = ('uit jaar %s' % self.sel_data)
            terug = 'selJaar'
        elif self.sel_item in ["selTitel","selTekst","selBeide"]:
            titel = "Dicht: zoek op tekst"
            if self.sel_item == "selTitel":
                seltekst = "in de titel"
            elif self.sel_item == "selTekst":
                seltekst = "in de tekst"
            elif self.sel_item == "selBeide":
                seltekst = "in titel of tekst"
            dh = DichtLijst(item=self.sel_data, type=self.sel_item)
            self.lijst = dh.id_titels
            self.gezocht = ('met "%s" %s' % (self.sel_data, seltekst))
            terug = 'selZoek'
        with open(os.path.join(htmlroot, "select_list.html")) as f_in:
            for x in f_in:
                x = x.rstrip()
                if '<title>' in x:
                    self.regels.append(x % self.sel_item)
                elif 'link rel="stylesheet"' in x:
                    self.regels.append(x % httproot)
                elif 'form action' in x:
                    self.regels.append(x % http_cgipad)
                elif "meld" in x:
                    if len(self.lijst) == 0:
                        self.regels.append(x % ("Geen g", self.gezocht))
                    else:
                        self.regels.append(x % ("G", self.gezocht))
                elif "selectiescherm" in x:
                    self.regels.append(x % (http_cgipad, terug))
                elif "select" in x:
                    if len(self.lijst) > 0:
                        self.regels.append(x)
                elif "option" in x:
                    if len(self.lijst) > 0:
                        for y in self.lijst:
                            if self.sel_item == "selTrefw":
                                dh = DichtItem(y[0], y[1])
                                dh.read()
                                hh = dh.titel or '(untitled)'
                            else:
                                hh = y[2] or '(untitled)'
                            h = '%s_%s' % (y[0], y[1])
                            self.regels.append(x % (h, hh))
                elif "Nieuw gedicht opvoeren" in x:
                    s = "?lbSelItem=_0"
                    if self.sel_item == "selJaar":
                        s = ("?lbSelItem=%s_0" % self.sel_data)
                    self.regels.append(x % (http_cgipad,s))
                elif "Nieuw gedicht opvoeren" in x:
                    self.regels.append(x % http_cgipad)
                ## elif "Terug" in x:
                    ## self.regels.append(x % http_cgipad)
                else:
                    self.regels.append(x)

    def detail(self):
        # self.sel_item levert het volgnummer binnen het jaar, self.sel_jaar levert het jaar
        # als self.sel_item 0 is pagina opbouwen voor een nieuwe
        allTrefw = ""
        if self.wat == "detail_wijzig":
            dh = DichtItem(self.sel_jaar, self.sel_item)
            dh.read()
            gewijzigd = False
            if self.titel != dh.titel:
                dh.titel = self.titel
                gewijzigd = True
            if self.tekst != dh.tekst:
                dh.tekst = self.tekst
                gewijzigd = True
            if self.gedicht != "":
                h = self.gedicht.split("\n")
                if h != dh.gedicht:
                    dh.gedicht = h
                    gewijzigd = True
            if gewijzigd:
                dh.write()
        elif self.sel_item == "0":
            self.titel = ""
            self.tekst = ""
            self.gedicht = ""
        else:
            dh = DichtItem(self.sel_jaar, self.sel_item)
            dh.read()
            self.titel = dh.titel
            self.tekst = dh.tekst
            self.gedicht = "\n".join(dh.gedicht)
        with open(os.path.join(htmlroot, "detail.html")) as f_in:
            for x in f_in:
                x = x.rstrip()
                if 'link rel="stylesheet"'in x:
                    self.regels.append(x % httproot)
                elif 'form action' in x:
                    self.regels.append(x % http_cgipad)
                elif 'hSelJaar' in x:
                    select, option, endselect = x.split("$s")
                    self.regels.append(select)
                    for y in jarenlijst():
                        deze = "selected" if y == self.sel_jaar else ''
                        self.regels.append(option % (deze, y, y))
                    self.regels.append(endselect)
                elif "txtTitel" in x:
                    self.regels.append(x % self.titel)
                elif "hselItem" in x:
                    self.regels.append(x % self.sel_item)
                elif "txtTekst" in x:
                    self.regels.append(x % self.tekst)
                elif "txtGedicht" in x:
                    self.regels.append(x % self.gedicht)
                elif "submit" in x:
                    if self.sel_item == "0":
                        self.regels.append(x % 'opvoeren')
                    else:
                        self.regels.append(x % 'wijzigen')
                else:
                    self.regels.append(x)

