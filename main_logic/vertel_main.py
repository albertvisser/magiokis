# -*- coding: UTF-8 -*-
import os
import sys
import shared
sys.path.append(os.path.join(shared.dmlroot, "vertel"))
from vertellers import Cats, User, NoDataError
from vertel_item import vertellijst, catlijst, VertelItem, Verteller
from verhalen import hoofdstuklijst, Hoofdstuk, Verhaal

htmlroot = shared.htmlroot + "/vertel/"
httproot = shared.httproot
http_cgipad = shared.http_cgipad.replace('local', 'vertel')
fouttekst = """\
Argumenten fout, mogelijke oorzaak:<br/><br/>
usernaam {} bestaat niet of is niet ingevuld<br/><br/>
select optie {} is fout of niet ingevuld<br/>
&nbsp;(toegestane waarden zijn: selCat, selZoek, nweCat en nweRoot)<br/>
"""
scripttext = """\
<script type="text/javascript">
function btnText()
{
    i = document.getElementById("pbSubmit");
    i.value = "  Uitvoeren  ";
}
</script>
"""

class Select:
    def __init__(self, args):
        self.user = args.get("user", "")
        self.select = args.get("select", "")
        self.cat =  args.get("cat", "")
        self.zoek = args.get("zoek", "")
        self.meld = args.get("meld", "")
        self.regels = []
        if self.select == "start":
            self.toon_start()
            return
        # het eerste dat er moet gebeuren is controleren of de user (Verteller) bestaat
        # zo niet, dan ALTIJD terugsturen met de melding "bestaat niet, klik op uitvoeren om de user op te voeren"
        #   of de knoptekst aanpassen, en met een onchange op het userveld deze terug wijzigen
        if not self.user:
            self.select = "noUser"
            self.toon_start()
            return
        dh = Verteller(self.user)
        if dh.exists:
            if self.select == "nweUser":
                self.meld = 'User bestaat al'
                self.toon_start()
                return
        else:
            if self.select == "nweUser":
                h = User(self.user).new()
                if h == "OK":
                    h = ""
                    dh = Verteller(self.user)
                    try:
                        dh.nieuw()
                    except AttributeError as meld:
                        h = meld
                if h != "":
                    self.regels = ("<br/>", h)
                    return
                self.select = "chgRoot"
            else:
                self.select = "errUser"
                self.toon_start()
                return
        if self.select == "nweTekst":
            self.regels.append('Location: %svertel_detail.py?hUser=%s' % (
                http_cgipad, self.user))
            return
        with open(os.path.join(htmlroot, "vertel_select.html")) as f_in:
            for r in f_in:
                r = r.rstrip()
                if "Magiokis!" in r:
                    self.regels.append(r % self.user)
                elif r == "<!-- backtotop -->":
                    hgoto = ("document.location='vertel_start.py?user=%s'" %
                        self.user)
                    self.regels.append('<input type="button" value="Terug naar '
                        'startscherm" onclick="%s" />\n' % hgoto)
                elif r == "<!-- select -->":
                    self.fout = False
                    self.c = Cats(self.user)
                    if self.select == "selCat":
                        if len(self.c.categorieen) > 0:
                            self.maak_selcat()
                        else:
                            self.meld = ("nog geen categorieen aanwezig bij deze "
                                "verteller")
                            self.maak_chgroot()
                    elif self.select == "selZoek":
                        if self.zoek == "":
                            self.regels = []
                            self.meld = 'Geen zoektekst opgegeven'
                            self.toon_start()
                            return
                        self.maak_selzoek()
                    elif self.select == "nweCat":
                        self.maak_nwecat()
                    elif self.select == "chgRoot":
                        self.maak_chgroot()
                    else:
                        self.fout = True
                    if self.fout:
                        self.regels.append(fouttekst.format(self.user, self.select))
                elif "stylesheet" in r:
                    self.regels.append(r % httproot)
                else:
                    self.regels.append(r)

    def toon_start(self):
        with open(os.path.join(htmlroot, "vertel_start.html")) as f_in:
            for x in f_in:
                x = x.rstrip()
                if x == "<!-- backtotop -->":
                    # alleen als door Launch een cookie gezet is met het userid, moet nog gemaakt worden
                    #~ hquery = 'userid=woefdram'	# voor nu even
                    #~ # hgoto = "document.location='magiokis_begin.py?" + hquery + "'"
                    #~ hgoto = "document.location='" + httproot + "magiokis_launch.html'"
                    #~ print ('<input type="button" value="Terug naar startscherm" onclick="%s" />' % (hgoto))
                    pass
                elif "%s" in x:
                    if x.startswith("<link"):
                        self.regels.append(x % httproot)
                        if self.select == "errUser":
                            self.regels.append(scripttext)
                    elif x.startswith("<form"):
                        self.regels.append(x % http_cgipad)
                    elif "txtUser" in x:
                        h = ""
                        if self.select == "errUser":
                            h = ' onchange="btnText()"'
                        h = ('value="%s"%s' % (self.user,h))
                        self.regels.append(x % h)
                    elif "hDo" in x:
                        h = ""
                        if self.select == "errUser":
                            h = "nweUser"
                        self.regels.append(x % h)
                elif '"meld"' in x:
                    if self.select == "noUser":
                        self.meld = ("Geen usernaam opgegeven; "
                            "zonder usernaam kunnen we niet verder")
                    elif self.select == "errUser":
                        self.meld = ("User bestaat niet; "
                            "vul een andere naam in of voer hem eerst op")
                    if self.meld != "":
                        self.regels.append(x.replace('&nbsp;', self.meld))
                elif "  Uitvoeren  " in x and self.select == "errUser":
                    self.regels.append(x.replace("  Uitvoeren  ",
                        "Nieuwe user opvoeren"))
                else:
                    self.regels.append(x)

    def maak_selcat(self):
        if self.cat != "":
            try:
                lijst = catlijst(self.user, self.cat)[2]
            except AttributeError as err:
                self.regels = []
                self.meld = str(err) + ' bij user ' + self.user
                self.toon_start()
                return
            titels = False
            if len(lijst) > 0:
                titels = True
        with open(os.path.join(htmlroot, "vertel_selcat.html")) as f_in:
            for x in f_in:
                x = x.rstrip()
                if "body" in x:
                    continue
                elif x.startswith("<form"):
                    self.regels.append(x % http_cgipad)
                    if "frmlist" in x and self.cat == "":
                        break # de rest is alleen van toepassing bij een ingevulde categorie
                elif "hUser" in x:
                    self.regels.append(x % self.user)
                elif x.startswith("<select"):
                    if "lbSelCat" in x:
                        select, option, value, endvalue, endoption, endselect = \
                            x.split("%s")
                        self.regels.append(select)
                        for y in self.c.categorieen:
                            s = ""
                            if y[1] == self.cat:
                                s = ' selected="selected"'
                            self.regels.append("".join((option, s, value, y[1],
                                endvalue, y[1], endoption)))
                        self.regels.append(endselect)
                    elif "lbSelItem" in x:
                        select, option, midoption, endoption, endselect = \
                            x.split("%s")
                        if titels:
                            self.regels.append(select)
                            for y in lijst:
                                self.regels.append("".join((option, y[0],
                                    midoption, y[1], endoption)))
                            self.regels.append(endselect)
                elif "%seksten" in x:
                    if titels:
                        s1, s2 = "T", ": "
                    else:
                        s1, s2 = "Geen t", ""
                    self.regels.append(x % (s1, self.cat, s2))
                elif "hVan" in x:
                    s = "cat-%s" % self.cat if titels else ""
                    self.regels.append(x % s)
                elif "Toon tekst" in x:
                    s = 'disabled="disabled"' if titels else ''
                    self.regels.append(x % s)
                elif "hNwInCat" in x:
                    self.regels.append(x % self.cat)
                else:
                    self.regels.append(x)

    def maak_selzoek(self):
        lijst = vertellijst(self.user, self.zoek)[2]
        with open(os.path.join(htmlroot, "vertel_selzoek.html")) as f_in:
            for x in f_in:
                if "body" in x:
                    continue
                elif x.startswith("<form"):
                    self.regels.append(x % http_cgipad)
                elif "hUser" in x:
                    self.regels.append(x % self.user)
                elif x.startswith("<select"):
                    select, option, midoption, endoption, endselect = x.split("%s")
                    if "lbSelItem" in x:
                        if lijst:
                            self.regels.append(select)
                            for y in lijst:
                                self.regels.append("".join((option, y[0], midoption,
                                    y[1], endoption)))
                            self.regels.append(endselect)
                elif "%seksten" in x:
                    if lijst:
                        s1, s2 = "T", ": "
                    else:
                        s1, s2 = "Geen t", ""
                    self.regels.append(x % (s1, self.zoek, s2))
                elif "hVan" in x:
                    s = "zoek-%s" % self.zoek if lijst else ""
                    self.regels.append(x % s)
                elif "Toon tekst" in x:
                    s = 'disabled="disabled"' if lijst else ''
                    self.regels.append(x % s)
                else:
                    self.regels.append(x)

    def maak_nwecat(self):
        m = ""
        if self.cat != "":
            if self.c.new_cat(self.cat):
                self.regels = []
                self.meld = ('categorie "%s" opgevoerd' % self.cat)
                self.toon_start()
                return
            else:
                m = "<br /><br />De opgegeven categorie komt al voor"
        with open(os.path.join(htmlroot, "vertel_nwecat.html")) as f_in:
            for x in f_in:
                if "body" in x:
                    continue
                elif x.startswith("<form"):
                    self.regels.append(x % http_cgipad)
                elif "txtNweCat" in x:
                    self.regels.append(x % self.cat)
                elif "%s" in x:
                    self.regels.append(x % m)
                else:
                    self.regels.append(x)

    def maak_chgroot(self):
        dh = Cats(self.user)
        vh = Verteller(self.user)
        u = vh.urlbase or "http://..."
        p = vh.basepath or '/home/user/...'
        skip = False
        herhaal = False
        self.regels = []
        herhaalze = []
        with open(os.path.join(htmlroot, "vertel_user.html")) as f_in:
            for x in f_in:
                x = x.rstrip()
                if x == "<!-- backtotop -->":
                    hgoto = ("document.location='vertel_start.py?user=%s'" %
                        self.user)
                    self.regels.append('<input type="button" value="Terug naar '
                        'startscherm" onclick="%s" />\n' % hgoto)
                elif x == "<!--":
                    skip = True
                if skip:
                    if x == "-->":
                        skip = False
                    continue
                if herhaal:
                    herhaalze.append(x)
                    if "/form" in x:
                        herhaal = False
                        for c in dh.categorieen:
                            id = int(c[0])
                            naam = c[1]
                            for y in herhaalze:
                                if "<form" in y:
                                    self.regels.append(y % http_cgipad)
                                elif "hUser%03i" in y:
                                    self.regels.append(y % (id, id, self.user))
                                elif "txtCat%03i"  in y:
                                    self.regels.append(y % (id, naam))
                                else:
                                    self.regels.append(y)
                        id = len(dh.categorieen) + 1
                        naam = "(nieuwe, nog niet bestaande categorie)"
                        for y in herhaalze:
                            if "<form" in y:
                                self.regels.append(y % http_cgipad)
                            elif "hUser%03i" in y:
                                self.regels.append(y % (id, id, self.user))
                            elif "txtCat%03i" in y:
                                self.regels.append(y % (id, naam))
                            else:
                                self.regels.append(y)
                elif "Categorie" in x:
                    self.regels.append(x)
                    herhaal = True
                elif "<link" in x:
                    self.regels.append(x % httproot)
                elif "<form" in x:
                    self.regels.append(x % http_cgipad)
                elif "hUser" in x:
                    self.regels.append(x % (self.user, self.user))
                elif "txtUrl" in x:
                    self.regels.append(x % u)
                elif "txtPad" in x:
                    self.regels.append(x % p)
                elif "meld" in x:
                    self.regels.append(x % self.meld)
                else:
                    self.regels.append(x)

class Detail:
    def __init__(self,args):
        self.doe = args.get("doe", '') # actie
        self.sel_id = args.get("selId", '')  # verhaal id
        self.user = args.get("user", '')  # current user
        self.van = args.get("van", '')    # afkomstig van selectiescherm?
        self.sel_hoofdst = args.get("selH", '')  # selhoofdstuk vanuit kiezen hoofdstuk
        self.hoofdstuknummer = int(args.get("selHs", '-1')) # hoofdstuk nummer vanuit wijzig hoofdstuk
        self.hoofdstuktitel = args.get("HsTitel", '') # titel van het hoofdstuk
        self.hoofdstuktekst = args.get("HsTekst", '').split('\n') # tekst van het hoofdstuk
        self.verhaaltitel = args.get("titel", '')  # htitel bij updaten tekst (verhaaltitel?)
        self.sel_cat = args.get("selCat", '')  # geselecteerde categorie bij updaten tekst en opvoeren nieuwe
        self.sel_item = args.get("selItem", '') # filenaam
        if self.doe == '':
            self.breekaf("Geen actie ('doe') opgegeven")
            return
        if self.user == '':
            self.breekaf("Geen user opgegeven")
            return
        ## self.regels = []
        ## self.regels.append(args)
        ## self.regels.append(self.__dict__)
        ## self.regels.append(" ")
        ## return
        self.aantal_hoofdst = 0
        self.meld = ''
        self.hoofdstuktitels = []
        nieuw = False
        dh = Verteller(self.user)
        if not dh.exists:
            self.breekaf("Verteller bestaat niet")
            return
        self.laatste = dh.laatste
        self.basepath = dh.basepath
        self.cats = Cats(self.user).categorieen
        err = ''
        if self.doe == "nieuw":     # nieuweTekst = 1 - nieuweTekst, selCat
            if self.sel_id != '0':
                self.breekaf('Geen selid of fout verhaal geselecteerd')
                return
            nieuw = True
            for cat, name, text in self.cats:
                if name == self.sel_cat:
                    self.sel_cat = cat
            err = self.nieuw_verhaal()
        else:
            if self.sel_id == '':
                self.breekaf('Geen verhaal geselecteerd')
                return
            if self.doe == "selTekst":    # we komen vanuit selectie - alleen selId is gevuld
                self.hoofdstuknummer = 1
            elif self.doe == "selHs":     # we komen vanuit kies hoofdstuk - selId, selH
                if self.sel_hoofdst == '':
                    self.breekaf('Geen hoofdstuk geselecteerd')
                    return
                i = self.sel_hoofdst.find("nw")
                if i >= 0:
                    self.hoofdstuknummer = int(self.sel_hoofdst[:i])
                    ## self.nieuw_hoofdstuk = True
                else:
                    self.hoofdstuknummer = int(self.sel_hoofdst)
            elif self.doe == "wijzigTxt": # we komen vanuit wijzig hoofdstuk - selId, selHs, HsTitel, HsTekst
                if self.hoofdstuknummer == -1:
                    self.breekaf('Geen hoofdstuk geselecteerd')
                    return
                else:
                    err = self.wijzig_hoofdstuktekst()
            elif self.doe == "wijzigVh":  # we komen vanuit updaten tekst - selId, titel, selItem, selCat
                if self.sel_item == "" and self.hoofdstuknummer == 0:
                    self.breekaf('Geen bestandsnaam meegegeven')
                    return
                err = self.wijzig_verhaal()
            else:
                err = "Onbekende actie: '%s'" % self.doe
            if not err:
                err = self.bestaand_verhaal()
        self.regels = []
        if err:
            self.breekaf(err)
            return
        self.maakhtml(nieuw)

    def breekaf(self, melding):
        """bepaal vanuit welk scherm we komen en zet dat opnieuw klaar met melding"""
        try:
            sel, zoek = self.van.split('-')
        except ValueError:
            sel = ''
        args = {'user': self.user, 'meld': melding}
        if self.doe == 'Nieuw':
            if sel == 'cat':
                args['select'] = 'selCat'
                args['cat'] = zoek
            elif sel =='zoek':
                args['select'] = 'selZoek'
                args['zoek'] = zoek
            else:
                args['select'] = 'start'
        elif self.doe == "selTekst":
            if sel == 'cat':
                args['select'] = 'selCat'
                args['cat'] = zoek
            elif sel =='zoek':
                args['select'] = 'selZoek'
                args['zoek'] = zoek
            else:
                self.meld = melding
                self.maakhtml()
                return
        elif self.doe in ("selHs", "wijzigTxt", "wijzigVh"):
            self.meld = melding
            self.maakhtml()
            return
        else:
            args['select'] = 'start'
            args['meld'] = melding
        self.regels = Select(args).regels

    def maakhtml(self, nieuw=False):
        overslaan = False
        with open(os.path.join(htmlroot, "vertel_detail.html")) as f_in:
            for x in f_in:
                x = x.rstrip()
                if "Magiokis!" in x:
                    self.regels.append(x % self.user)
                elif x == "<!-- backtotop -->":
                    hgoto = ("document.location='vertel_start.py?user=%s'" %
                        self.user)
                    self.regels.append('<input type="button" value="Terug naar '
                        'startscherm" onclick="%s" />\n' % hgoto)
                    hgoto = ""
                    if self.van.startswith("cat-"): # th.zoekId(self.van[4:])
                        hgoto = ("document.location='vertel_select.py?hUser=%s"
                            "&lbSelCat=%s'" % (self.user, self.van[4:]))
                    elif self.van.startswith("zoek-"):
                        hgoto = ("document.location='vertel_select.py?hUser=%s"
                            "&txtZoek=%s'" % (self.user, self.van[5:]))
                    if hgoto != "":
                        self.regels.append('<input type="button" value="Terug '
                            'naar selectie" onclick="%s" />\n' % hgoto)
                elif "stylesheet" in x:
                    self.regels.append(x % httproot)
                elif "<form" in x:
                    h = (x % http_cgipad)
                    if "frmWijzigVerhaal" in h:
                        self.regels.append(h)
                    elif "frmKiesAlinea" in h:
                        if nieuw:
                            overslaan = True
                        else:
                            self.regels.append(h)
                    elif "frmWijzigAlinea" in h:
                        if nieuw:
                            overslaan = True
                        else:
                            self.regels.append(h)
                elif '"hUser"' in x:
                    self.regels.append(x % str(self.user))
                elif '"meld"' in x:
                    if self.meld != "":
                        self.regels.append(x % self.meld)
            #-- regels uit frmWijzigVerhaal
                elif "hTitel" in x:
                    self.regels.append(x % self.verhaaltitel)
                elif "hId" in x:
                    self.regels.append(x % self.sel_id)
                elif "hHs" in x:
                    self.regels.append(x % str(self.hoofdstuknummer))
                elif "hselItem" in x:
                    self.regels.append(x % self.sel_item)
                elif "lbSelCat" in x:
                    select, option, endselect = x.split("$s")
                    self.regels.append(select)
                    for cat, name, text in self.cats:
                        s = ""
                        if cat == self.sel_cat:
                            s = ' selected="selected"'
                        self.regels.append(option % (s, cat, name))
                    self.regels.append(endselect)
                elif "Verhaal%s" in x:
                    if nieuw:
                        s = ' (titel en evt. categorie) opvoeren'
                    else:
                        s = 'titel en/of categorie toekennen/wijzigen'
                    self.regels.append(x % s)
            #-- regels uit frmKiesAlinea
                elif "hUser" in x:
                    if not overslaan:
                        self.regels.append(x % str(self.user))
                elif "hselId" in x:
                    if not overslaan:
                        self.regels.append(x % self.sel_id)
                elif "selHoofdstuk" in x:
                    self.nieuw_hoofdstuk = False
                    if not overslaan:
                        select, option, endoption, endselect = x.split("$s")
                        self.regels.append(select)
                        if len(self.hoofdstuktitels) > 0:
                            for i, y in enumerate(self.hoofdstuktitels):
                                s = ""
                                if i + 1 == self.hoofdstuknummer:
                                    s = ' selected="selected" '
                                self.regels.append(option % (s, i + 1, y))
                        else:
                            self.nieuw_hoofdstuk = True
                        s = ""
                        if self.nieuw_hoofdstuk:
                            s = ' selected="selected" '
                        self.regels.append(endoption % (s,self.aantal_hoofdst + 1))
                        self.regels.append(endselect)
                elif "Toon hoofdstuk" in x:
                    if not overslaan:
                        self.regels.append(x)
            #-- regels uit frmWijzigAlinea
                elif "hselHs" in x:
                    if not overslaan:
                        self.regels.append(x % str(self.hoofdstuknummer))
                elif "titel2" in x:
                    if not overslaan:
                        h = '' if self.nieuw_hoofdstuk else self.hoofdstuktitel
                        self.regels.append(x % h)
                elif "txtHoofdstuk" in x:
                    if not overslaan:
                        if self.nieuw_hoofdstuk:
                            h = ''
                        else:
                            h = "\n".join(self.hoofdstuktekst)
                        self.regels.append(x % h)
                ## elif "Hoofdstuktitel of -tekst aanpassen" in x:
                    ## if not overslaan:
                        ## self.regels.append(x)
                else:
                    if not overslaan:
                        self.regels.append(x)
                if "</form>" in x:
                    overslaan = False

    def nieuw_verhaal(self):
        try:
            dh = VertelItem(self.user, self.sel_id)
            dh.read()
        except (ValueError, AttributeError) as err:
            return err
        if dh.found:
            return "Verhaal bestaat al"
        else:
            nieuw = int(self.laatste) + 1
            self.sel_item = os.path.join(self.basepath, "tekst%03i.xml" % nieuw)
            self.sel_id = str(nieuw)
            self.hoofdstuknummer = 0
            ## self.nieuw_hoofdstuk = True
            self.titel = ""
            self.aantal_hoofdst = 0

    def wijzig_hoofdstuktekst(self):
        try:
            dh = VertelItem(self.user, self.sel_id)
        except (ValueError, AttributeError) as err:
            return err
        try:
            dh.read()
        except AttributeError as err:
            return err
        if dh.found:
            vh = Hoofdstuk(os.path.join(dh.path, dh.url), hst=self.hoofdstuknummer)
            vh.read()
            #~ print vh.__dict__
            if vh.found or self.hoofdstuknummer == 0 or \
                    self.hoofdstuknummer == vh.aanthst + 1:
                vh.htitel = self.hoofdstuktitel
                vh.htekst = self.hoofdstuktekst
                vh.write()
            else:
                return "Hoofdstuk %i Bestaat Niet" % self.hoofdstuknummer
        else:
            return "Verteller Bestaat Niet"

    def wijzig_verhaal(self):
        try:
            dh = VertelItem(self.user, self.sel_id)
        except (ValueError, AttributeError) as err:
            return err
        try:
            dh.read()
        except AttributeError as err:
            return err
        schrijf = False
        if dh.found:
            if self.hoofdstuknummer == 0:
                return 'ID voor nieuw verhaal bestaat al'
            self.sel_item = os.path.join(dh.path, dh.url)
        else:
            dh.url = os.path.basename(self.sel_item)
            schrijf = True
        if self.verhaaltitel != dh.titel:
            dh.titel = self.verhaaltitel
            schrijf = True
        if self.sel_cat != "" and self.sel_cat != dh.cat:
            dh.wijzig_cat(self.sel_cat)
            schrijf = True
        if schrijf:
            dh.write()
        ## dh = Verteller(self.user)
        ## dh.laatste = self.sel_id
        ## dh.write()
        dh = Verhaal(self.sel_item)
        if dh.bestaat:
            dh.read()
        else:
            dh.write()
        if self.verhaaltitel != dh.titel:
            dh.titel = self.verhaaltitel
            schrijf = True
        if schrijf:
            dh.write()
        ## if self.hoofdstuknummer == 0:
            ## self.nieuw_hoofdstuk = True
        if self.sel_hoofdst == '0':
            self.sel_hoofdstuk = '1'
            self.nieuw_verhaal = True

    def bestaand_verhaal(self):
        try:
            dh = VertelItem(self.user, self.sel_id)
        except (ValueError, AttributeError) as err:
            return err
        try:
            dh.read()
        except AttributeError as err:
            return err
        if dh.found:
            self.sel_item = os.path.join(dh.path, dh.url) # fysieke locatie
            self.sel_cat = dh.cat # categorie (nog niet gevuld)
            self.sel_id = dh.id # het id
            self.verhaaltitel = dh.titel # de titel
            self.url = dh.urlbase + dh.url # webadres locatie
            try:
                lijst = hoofdstuklijst(self.sel_item)[1]
            except TypeError:
                pass
            if lijst:
                self.hoofdstuktitels = lijst
                self.aantal_hoofdst = len(lijst)
                vh = Hoofdstuk(self.sel_item, self.hoofdstuknummer)
                if self.aantal_hoofdst > 0 and \
                        self.hoofdstuknummer <= self.aantal_hoofdst:
                    vh.read()
                    self.hoofdstuktitel = vh.htitel
                    self.hoofdstuktekst = vh.htekst
                ## else:
                    ## self.nieuw_hoofdstuk = True
            ## elif self.nieuw_verhaal:
                ## self.nieuw_hoofdstuk = True
            else:
                return "Tekst %s Van %s Bestaat Echt Niet: %s" % (self.sel_id,
                    self.user, self.sel_item)
        else:
            return "Tekst %s Van %s Bestaat Niet" % (self.sel_id, self.user)

def process_user(args):
    cat_id = args.get("id", '')
    if cat_id:
        catnaam = args["naam"]
        dh = Cats(args["user"])
        try:
            huidigenaam = dh.zoek_naam(catnaam)
        except NoDataError:
            dh.new_cat(catnaam)
            self.meld = ("categorie '%s' toegevoegd" % catnaam)
            return
        if huidigenaam != catnaam:
            dh.wijzig_cat(huidigenaam, catnaam)
            meld = ("categorie '%s' gewijzigd in %s" %
                (huidigenaam, catnaam))
        else:
            meld = ("categorie '%s' is niet gewijzigd" % catnaam)
    else:
        wijzig = False
        dh = Verteller(args["user"])
        test = args.get("url", '')
        if test:
            dh.new_urlbase(test)
            wijzig = True
        test = args.get("pad", '')
        if test:
            dh.new_basepath(test)
            wijzig = True
        if wijzig:
            dh.write()
            self.meld = "Gegevens verteller gewijzigd"
        else:
            self.meld = "Gegevens verteller niet gewijzigd"
