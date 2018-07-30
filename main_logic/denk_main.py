# -*- coding: utf-8 -*-
import sys, os
import shared
sys.path.append(os.path.join(shared.dmlroot, "denk"))
from denk_trefw import trefwoordenlijst, Trefwoord
from denk_item import denk_lijst, denk_laatste, DenkItem

htmlroot = os.path.join(shared.htmlroot, "denk")
httproot = shared.httproot
http_cgipad = shared.http_cgipad.replace('local', 'denk')
input_text = '<input type="{}" name="{}" value="{}"{}>'
size_text =  'size="{}" maxlength="{}"'
select_text = '<select name="{}" size="{}">$s<option value="%s">%s</option>$s</select>'
checked_text = ' checked="checked"'

class Denk:
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
        if "titel" in args:
            self.titel = args["titel"]
        if "tekst" in args:
            self.tekst = args["tekst"]
        if "trefw" in args:
            self.trefw = args["trefw"].split("$#$")
        self.form_ok = True
        if wat == "start":
            self.start()
        elif wat == "select":
            if self.sel_item == "nwTrefw":
                if self.sel_data != "":
                    self.nieuw_trefw()
                size_t = size_text.format("40", "40")
                self.select_args('Nieuw trefwoord:' + input_text.format("text",
                    "txtNwTrefw", "%s", size_t))
            # elif self.sel_item == "nweCat":
                # if self.sel_data != "":
                    # self.nweCat()
                # self.sel_args('Nieuw jaar:<input type="text" name="txtNwJaar" value="%s" size="40" maxlength="40">')
            elif self.sel_item == "nweTekst":
                self.regels.append('Location: %sdenk_detail.py?lbSelItem=0' %
                    http_cgipad)
            elif self.sel_item == "selAll":
                self.select()
            elif self.sel_item == "selTrefw":
                if self.sel_data == "":
                    self.select_trefw()
                    self.select_args('Kies een trefwoord:' + select_text.format(
                        "lbSelTrefw", "1"))
                else:
                    self.select()
            elif self.sel_item in ["selZoek", "selTitel","selTekst","selBeide"]:
                # is selZoek met selData gevuld niet onzin?
                # en een van de andere drie zonder selData ook? Nee, dat kan submitten zonder zoektekst ingevuld zijn
                if self.sel_data == "":
                    self.select_zoek()
                    if self.sel_item != "selZoek":
                        self.meld = "geen zoektekst opgegeven"
                    size_t = size_text.format("40", "80")
                    h = ['Zoek naar:' + input_text.format("text", "txtZoek", "",
                        size_t) + '<br /><br />']
                    s = ""
                    if self.sel_item in ("selZoek","selTitel"):
                        s = checked_text
                    h.append(input_text.format("radio", "rbselZoek", "selTitel",
                        s) + 'Zoek in titel<br>')
                    s = ""
                    if self.sel_item == "selTekst":
                        s = ' checked="checked"'
                    h.append(input_text.format("radio", "rbselZoek", "selTekst",
                        s) + 'Zoek in tekst<br>')
                    s = ""
                    if self.sel_item == "selBeide":
                        s = ' checked="checked"'
                    h.append(input_text.format("radio", "rbselZoek", "selBeide",
                        s) + 'Zoek in beide<br><br /><br />')
                    self.select_args(h)
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
        with open(os.path.join(htmlroot, "start.html")) as template:
            for x in template:
                self.regels.append(x.rstrip())

    def nieuw_trefw(self):
        if self.sel_data in trefwoordenlijst()[0]:
            dh = Trefwoord(self.sel_data)
            dh.write()
            self.meld = "trefwoord opgevoerd"
        else:
            self.form_ok = False
            self.meld = "Het opgegeven trefwoord komt al voor"

    def nieuwe_cat(self):
        pass # we doen niet aan categorieen

    def select_cat(self):
        pass # we doen niet aan categorieen

    def select_trefw(self):
        self.lijst, _ = trefwoordenlijst()

    def select_zoek(self):
        pass

    def select_args(self,data):
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
                    if self.sel_item in ("nwTrefw", "nweCat"):
                        self.regels.append(data % self.sel_data)
                    elif self.sel_item in ("selTrefw", "selCat"):
                        select, option, endselect = data.split("$s")
                        self.regels.append(select)
                        for y in self.lijst:
                            self.regels.append(option % (y, y))
                        self.regels.append(endselect)
                    else:
                        self.regels += data
                ## elif "Terug" in x:
                    ## self.regels.append(x % http_cgipad)
                elif "submit" in x:
                    if self.sel_item in ("nwTrefw", "nweCat"):
                        self.regels.append(x % "Opvoeren")
                    elif self.sel_item in ("selTrefw", "selCat"):
                        self.regels.append(x % "Selectie uitvoeren")
                    else:
                        self.regels.append(x % "Zoek")
                elif 'meld' in x:
                    self.regels.append(x % self.meld)
                else:
                    self.regels.append(x)

    def select(self):
        if self.sel_item == "selTrefw":
            titel = "Denk: zoek op trefwoord"
            th = Trefwoord(self.sel_data)
            th.read()
            self.lijst = th.tekstrefs
            self.gezocht = ('bij trefwoord %s' % self.sel_data)
        # elif self.sel_item == "selCat":
            # titel= "Denk: zoek op categorie"
            # th = CatLijst(self.sel_data)
            # self.lijst = th.IdTitels
            # self.gezocht = ('bij categorie %s' % self.sel_data)
        elif self.sel_item == "selAll":
            titel = "Denk: toon alles"
            self.lijst = denk_lijst()
            self.gezocht = ('in de database')
        elif self.sel_item in ["selTitel","selTekst","selBeide"]:
            titel = "Denk: zoek op tekst"
            if self.sel_item == "selTitel":
                seltekst = "in de titel"
            elif self.sel_item == "selTekst":
                seltekst = "in de tekst"
            elif self.sel_item == "selBeide":
                seltekst = "in titel of tekst"
            self.lijst = denk_lijst(self.sel_data, self.sel_item)
            self.gezocht = ('met "%s" %s' % (self.sel_data, seltekst))
        with open(os.path.join(htmlroot, "select_list.html")) as f_in:
            for x in f_in:
                if '<title>' in x:
                    self.regels.append(x[:-1] % self.sel_item)
                elif 'link rel="stylesheet"' in x:
                    self.regels.append(x[:-1] % httproot)
                elif 'form action' in x:
                    self.regels.append(x[:-1] % http_cgipad)
                elif "meld" in x:
                    if len(self.lijst) == 0:
                        self.regels.append(x[:-1] % ("Geen d",self.gezocht))
                    else:
                        self.regels.append(x[:-1] % ("D",self.gezocht))
                elif "select" in x:
                    if len(self.lijst) > 0:
                        self.regels.append(x[:-1])
                elif "option" in x:
                    if len(self.lijst) > 0:
                        for y in self.lijst:
                            if self.sel_item == "selTrefw":
                                dh = DenkItem(y)
                                dh.read()
                                hh = dh.titel
                                h = y
                            else:
                                h = y[0]
                                hh = y[1]
                            self.regels.append(x[:-1] % (h,hh))
                elif "Nieuwe gedachte opvoeren" in x:
                    s = "?lbSelItem=0"
                    # if self.sel_item == "selCat":
                        # s = ("?lbSelItem=%s_0" % self.sel_data)
                    self.regels.append(x[:-1] % (http_cgipad,s))
                #~ elif "Nieuw gedicht opvoeren" in x:
                    #~ self.regels.append(x[:-1] % http_cgipad)
                ## elif "Terug" in x:
                    ## self.regels.append(x[:-1] % http_cgipad)
                else:
                    self.regels.append(x[:-1])

    def detail(self):
        # self.sel_item levert het volgnummer binnen het jaar, self.selJaar levert het jaar
        # als self.sel_item 0 is pagina opbouwen voor een nieuwe
        submit_tekst = 'wijzigen'
        if self.wat == "detail_wijzig":
            if self.sel_item == "0":
                self.sel_item = str(denk_laatste() + 1)
                submit_tekst = 'opvoeren'
            dh = DenkItem(self.sel_item)
            dh.read()
            gewijzigd = False
            if self.titel != dh.titel:
                dh.titel = self.titel
                gewijzigd = True
            h = []
            if len(self.trefw) > 0:
                h = self.trefw
            if h != dh.trefwoorden:
                y = dh.trefwoorden[:] # kopie van trefwoorden om bij te houden welke er uit gehaald zijn
                for x in h:
                    if x in y:
                        y.remove(x)
                    else:
                        dh.add_trefw(x)
                for x in y:
                    dh.rem_trefw(x)
                dh.wijzig_trefw(h)
                gewijzigd = True
            h = []
            if self.tekst != "":
                h = self.tekst.split("\n")
            if h != dh.tekst:
                dh.wijzig_tekst(h)
                gewijzigd = True
            if gewijzigd:
                dh.write()
        dh = DenkItem(self.sel_item)
        dh.read()
        trefwoorden, teksttrefw = trefwoordenlijst(self.sel_item)
        with open(os.path.join(htmlroot, "detail.html" )) as _in:
            for x in _in:
                x = x.rstrip()
                if 'link rel="stylesheet"'in x:
                    self.regels.append(x % httproot)
                elif 'form action' in x:
                    self.regels.append(x % http_cgipad)
                elif "txtTitel" in x:
                    self.regels.append(x % dh.titel)
                elif "hselItem" in x:
                    self.regels.append(x % self.sel_item)
                elif "txtTrefw" in x and "<input" in x:
                    h = "$#$".join(teksttrefw) if teksttrefw else ""
                    self.regels.append(x % h)
                elif "txtTekst" in x:
                    self.regels.append(x % "\n".join(dh.tekst))
                elif "lbselList" in x and "<select" in x:
                    select, option, endselect = x.split("$s")
                    self.regels.append(select)
                    for y in trefwoorden:
                        self.regels.append(option % (y,y))
                    self.regels.append(endselect)
                elif "lbselTrefw" in x and "<select" in x:
                    select, option, endselect = x.split("$s")
                    self.regels.append(select)
                    for y in teksttrefw:
                        ## if type(y) is str or unicode:
                        self.regels.append(option % (y,y))
                    self.regels.append(endselect)
                ## elif "Terug" in x:
                    ## self.regels.append(x % http_cgipad)
                elif "submit" in x:
                    self.regels.append(x % submit_tekst)
                else:
                    self.regels.append(x)

