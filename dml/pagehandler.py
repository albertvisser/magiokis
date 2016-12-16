# -*- coding: utf-8 -*-
import sys
import os
import xml.etree.ElementTree as ET
## from xml.sax import make_parser
## from xml.sax.handler import feature_namespaces
## from xml.sax import saxutils
## from xml.sax import ContentHandler
## from xml.sax.saxutils import XMLGenerator
## from xml.sax.saxutils import escape
HERE = os.path.dirname(__file__)
import magiokis_globals as mg
sys.path.append(os.path.join(HERE, "songs"))
from opname import Opname
from songtekst import Songtekst
from song import Song
from objectlists import OwnerList, MemberList
import common
sys.path.append(os.path.join(HERE, "vertel"))
from vertellers import Cats
from vertel_item import catlijst
dichtpad = os.path.join(HERE, "dicht")
sys.path.append(dichtpad)
from dicht_trefw import jarenlijst

## cssregel = '<?xml-stylesheet href="%ssongs/songtekst.css" type="text/css" ?>'
## def toontekst(dirnaam, docnaam):
    ## gotstyle = False
    ## for x in file("/".join((dirnaam, docnaam))):
        ## if x.find("?xml") > 0:
            ## if x.find("xml-stylesheet") > 0:
                ## print (cssregel % mg.httproot)
                ## gotstyle = True
            ## else:
                ## print x
        ## else:
            ## if not gotstyle:
                ## print (cssregel % mg.httproot)
                ## gotstyle = True
            ## print x

def zetom(bron, doel):
    if bron.text is not None:
        doel.text = bron.text
    for x in list(bron):
        y = ET.SubElement(doel, 'div')
        y.set("class", x.tag)
        zetom(x, y)

playlist_code = "".join((
    '<object type="application/x-shockwave-flash" data="{0}xspf_player/xspf_player',
    '.swf?playlist_url={0}pl/{2}.xspf&amp;autoload=false" width="400" height="152">',
    '<param name="movie" value="{0}xspf_player/xspf_player',
    '.swf?playlist_url={0}pl/{2}.xspf&amp;autoload=false">',
    '{2}',
    '</object>',
    ))
playlist_autoload_code = "".join((
    '<object type="application/x-shockwave-flash" data="{0}xspf_player/xspf_player',
    '.swf?playlist_url={0}pl/{2}.xspf&amp;player_title={1}&amp;autoload=true" ',
    'width="600" height="152">',
    '<param name="movie" value="{0}xspf_player/xspf_player',
    '.swf?playlist_url={0}pl/{2}.xspf&amp;player_title={1}&amp;autoload=true">',
    '{2}',
    '</object>',
    ))
playsong_code = "".join((
    '<object type="application/x-shockwave-flash" data="{0}xspf_player/xspf_player',
    '_slim.swf?song_url={1}&amp;song_title={2}" width="400" height="15">',
    '<param name="movie" value="{0}xspf_player/xspf_player_slim',
    '.swf?song_url={1}&amp;song_title={2}">',
    '{1}',
    '</object>',
    ))
playsong_autoplay_code = "".join((
    '<object type="application/x-shockwave-flash" data="{0}xspf_player/xspf_player',
    '_slim.swf?song_url={1}&amp;song_title={2}&amp;autoplay=true" width="400"',
    ' height="15"> <param name="movie" value="{0}xspf_player/xspf_player_slim',
    '.swf?song_url={1}&amp;song_title={2}&amp;autoplay=true">',
    '{2}',
    '</object>',
    ))
def make_xspf_objects(fl):
    y = []
    with open(fl, encoding='latin-1') as f:
        for x in f:
            s = x[:-1].split()
            if s[:2] == ['<!--','xspf']:
                if s[2] == 'playlist': #
                    y.append(playlist_code.format(mg.httproot, mg.dataroot, s[3]))
                if s[2] == 'song':
                    y.append(playsong_code.format(mg.httproot, do.wwwurl, titel))
            else:
                y.append(x)
    return y

def make_xspf_opn_page(it):
    r = []
    if isinstance(it, str):
        it = it.upper()
    do = Opname(it)
    ## print it,do.__dict__
    titel = do.songtitel
    r.append(playsong_code.format(mg.httproot, do.wwwurl, titel))
    if do.song:
        ds = Songtekst(do.song)
        ds.read()
        ## print ds.__dict__
        if ds.found:
            r.extend(make_tekst_page(ds.file))
    if not do.song:
        r.append("<p/><p>instrumental: {}</p>".format(do.commentaar))
    return r

def make_xspf_pl_page(it):
    pl_head = ('<?xml version="1.0" encoding="UTF-8" ?><playlist version="0" '
        'xmlns="http://xspf.org/ns/0/"><title>%s</title><trackList>')
    pl_entry = '<track><location>%s</location><title>%s</title></track>'
    pl_tail = '</trackList></playlist>'
    r = []
    do = Song(it)
    titel = do.songtitel
    try:
        dl = MemberList(it, 'songopnames')
    except common.DataError:
        dl = None
    l = []
    if dl:
        for x in dl.lijst:
            do = Opname(x)
            l.append((do.wwwurl, ' '.join((do.plaats, do.datum))))
    if len(l) == 0:
        r.append('(No recordings found for this song)\n'.format(it))
    elif len(l) == 1:
        x = l[0]
        r.append(playsong_autoplay_code.format(mg.httproot, x[0], x[1]))
    else:
        name = titel.replace(' ', '_').replace('?', '')
        with open(os.path.join(mg.xmlpad, 'pl', name + '.xspf'),'w') as f:
            f.write(pl_head % titel)
            for x in l:
                f.write(pl_entry % (x[0], x[1]))
            f.write(pl_tail)
        r.append(playlist_autoload_code.format(mg.httproot, titel, name))
    if do.song:
        ds = Songtekst(do.song)
        ds.read()
        ## print ds.__dict__
        r.extend(make_tekst_page(ds.file))
    return r

def make_tekst_page(it):
    r = []
    tree = ET.ElementTree(file=it)
    root = tree.getroot()
    onaam = "tempfile.html"
    newroot = ET.Element('div')
    if root:
        newroot.set("class", root.tag)
        zetom(root, newroot)
    else:
        newroot.text = '(no lyrics available)'
    ## out = ET.ElementTree(newroot)
    ## out.write(onaam)
    ## for x in file(onaam):
        ## r.append(x)
    ## return r
    ## of:
    return ET.tostringlist(newroot, encoding='unicode')

class DataError(Exception):
    pass

class PageHandler:
    def __init__(self):
        self.fn = os.path.join(mg.xmlpad, 'tocs.xml')
        self.found = False
        if not os.path.exists(self.fn):
            raise DataError("XML bestand niet gevonden")
            return
        tree = ET.ElementTree(file=self.fn)
        self.root = tree.getroot()

    def write(self, id):
        raise DataError("Updaten nog niet mogelijk")

subsectionpagetext = '%%cgipad%%cgiprog?section=%s&amp;subsection=%s'
areatext = ' <area shape="rect" coords="%i,1,%i,39" href="{}" alt="%s" />'.format(
    subsectionpagetext)
class ListTocs(PageHandler):
    """bouw de tekst voor de imagemaps op

    dit is in magiokis_page.py anders geïmplementeerd in Pagina.topbalk_out"""
    def __init__(self):
        PageHandler.__init__(self)
        self.items = []
        self.lines = []
        mapc = 0
        for x in list(self.root):
            y = x.get('id')
            self.items.append(y)
            mapx = mapc + 3
            mapc = mapx + int(x.get('width'))
            self.lines.append(areatext % (mapx, mapc, y, x.get('start'), y))

class ListPages(PageHandler):
    def __init__(self):
        PageHandler.__init__(self)
        self.items = []
        for x in list(self.root):
            ## self.item = (x.get('id'),x.get('start'),x.get('width'))
            for y in x.getiterator("page"):
                ## self.items.append((self.item,y.get('id')))
                if y.get('id') is not None:
                    self.items.append((x.get('id'), y.get('id')))

link_tpl = '<a href="{}">'
listitem_tpl = '<li class="nobul">{}</li>'

subsectionpagelink = '<a href="{}"'.format(subsectionpagetext)
itempagetext = subsectionpagetext + '&amp;item=%s'
itempagelink = link_tpl.format(itempagetext)
listitemtext = listitem_tpl.format(subsectionpagelink + '">%s</a>') # '<li class="nobul">{}>%s</a></li>'.format(subsectionpagelink)
class Toc(PageHandler):
    def __init__(self, id):
        PageHandler.__init__(self)
        self.lines = []
        for x in list(self.root): # y.tag is altijd "toc" attributes: start, width
            if x.get("id") == id:
                self.found = True
                break
        if not self.found:
            return
        self.id = id
        self.start = x.get("start")
        self.width = x.get("width")
        for y in list(x): # y.tag kan zijn: page, regel, level, link (en theoretisch ook list)
            self.print_tocdeel(y)

    def print_tocdeel(self, y, level=0):
        if y.tag == "page":  # page.id of page.url
            i = y.get("id")
            u = y.get("url") # directe link off-site
            s = y.get("src") # geeft aan waar de page source staat
            t = y.text
            if t is None or t == '':
                if self.id == 'Art':
                    return
                t = "&nbsp;"
            a1, a2 = '', ''
            if i is not None and t != '&nbsp;':
                s = ""
                if y.get("extra") is not None:
                    s = "&amp;%s" + y.get("extra")
                linktext = link_tpl.format(subsectionpagetext + '%s')
                a1, a2 = linktext % (self.id, i, s), '</a>'
            elif u is not None:
                a1, a2 = link_tpl.format(u), '</a>'
            t = ''.join((a1, t, a2))
            if level > 0:
                t = listitem_tpl.format(t)
            else:
                t += '<br/>'
            self.lines.append(t)
        elif y.tag == "regel":
            c = y.get("class")
            t = y.text
            if t is None or t == '':
                t = "&nbsp;"
            if t[0] == "[":
                t = t.replace("[","<").replace("]",">")
            h = ''
            if c is not None:
                h = c.join((' class="','"'))
            t = "<span{}>{}</span>".format(h, t)
            if level > 0:
                t = listitem_tpl.format(t)
            else:
                t += '<br/>'
            self.lines.append(t)
        elif y.tag == "level":
            level += 1
            self.lines.append('<ul>')
            for x in list(y):
                self.print_tocdeel(x,level)
            self.lines.append('</ul>')
            level -= 1
        elif y.tag == "list":
            if self.id == "Zing":
                try:
                    m = OwnerList('jaarseries')
                except DataError as meld:
                    print(meld)
                else:
                    for y in m.lijst:
                        linktext = link_tpl.format(subsectionpagetext) + '%s</a>'
                        thislistitemtext = listitem_tpl.format(linktext)
                        self.lines.append(thislistitemtext % (self.id, y, y))
            elif self.id == "Vertel":
                dh = Cats("papa")
                for y in dh.categorieen:
                    if y[2] != "":
                        self.lines.append(listitemtext % (self.id, y[1], y[2]))
                    ## else:
                        ## self.lines.append('<li class="nobul"><a href="%%cgipad%%cgiprog?section=%s&amp;subsection=%s">%s</a></li>' % (self.id,y[1],y[1]))
            elif self.id == "Dicht":
                for y in jarenlijst():
                    self.lines.append(listitemtext % (self.id, y, y))
            elif self.id == "OW":
                for x in list(y):            # <page id="OW1" serie="B9_A">The Old Whores</page>
                    self.lines.append(listitemtext % (self.id, x.get("id"), x.text))
        elif y.tag == "link":
            a1,a2 = "",""
            if y.get("show") is not None: #
                linktext = link_tpl.format(itempagetext[:-2] + '%%datapadacteer/%s')
                a1,a2 = linktext % (self.id, y.text, y.get("show")), '</a>'
            u = y.text.join((a1,a2))
            if level > 0:
                u = listitem_tpl.format(u)
            else:
                u += '<br/>'
            self.lines.append(u)

twoitemtext = '<td width="50%%">{}%s</a></td>'.format(itempagelink)
sub_onbekend = "<div>subsection %s niet bekend bij section '%s'</div>"
onaf_melding = "<h3>hee, typisch, deze zijn geen van alle afgemaakt...</h3>"
class Page(PageHandler):
    def __init__(self, s, u, it="", id=""):
        PageHandler.__init__(self)
        self.adres = ""
        self.regels = []
        for x in list(self.root): # y.tag is altijd "toc" attributes: start, width
            if x.get("id") == s:
                for z in x.getiterator('page'):
                    if z.get("id") == u:
                        self.found = True
                        break
            if self.found:
                break
        if self.found:
            if z.get("src") is not None:
                self.adres = z.get("src")
        ## print "zo zie je me nog"
        ## print "en nu nog steeds"
        if s == "OW":
            if u in ('Home','Bio'):
                pass
            elif it != "" and it != "1":
                r = make_xspf_opn_page(it)
                self.regels += r
            else:
                zoek = z.get("serie")
                t = z.text # boeit niet echt, want wordt uit de memberlist gehaald
                x = MemberList(zoek.replace("9_"," 9"),"opnameseries")
                self.regels.append('<p align="left">%s<br />Recorded: %s</p>' % (
                    x.titel, x.tekst))
                self.regels.append('<table align="center" cellspacing="0" border="0'
                    '" cellpadding="4" width="90%">')
                h = int(len(x.lijst) / 2)
                if h * 2 < len(x.lijst):
                    h = h + 1
                for y in range(h):
                    lines = ['<tr>', twoitemtext % (s, u, x.lijst[y], x.titels[y])]
                    z = y + h
                    if z < len(x.lijst):
                        lines.append(twoitemtext % (s, u, x.lijst[z], x.titels[z]))
                    lines.append('</tr>')
                    self.regels.extend(lines)
                self.regels.append('</table>')
        elif s == "SpeelMee":
            if "Opnames" in u:
                self.found = False
                fl = os.path.join(mg.xmlpad, self.adres)
                r = make_xspf_objects(fl)
                self.regels += r
            elif "Songs" not in u:
                pass
            elif it != "" and it != "1":
                self.found = False
                r = make_xspf_opn_page(it)
                self.regels += r
            else:
                self.found = False
                fl = os.path.join(mg.xmlpad, self.adres)
                f = open(fl, encoding='latin-1') if sys.version > '3' else open(fl)
                with f:
                    for x in f:
                        if '<a href' in x:
                            y = x.split('"')
                            y[1] = itempagetext % (s, u,  y[1])
                            self.regels.append('"'.join(y))
                        else:
                            self.regels.append(x)
        elif s == "Speel":
            if u in ('Begin','Fase1','Fase2','Fase3'):
                self.found = False
                fl = os.path.join(mg.xmlpad, self.adres)
                r = make_xspf_objects(fl)
                self.regels += r
            elif u != "Bestof":
                pass
            elif it != "" and it != "1":
                self.found = False
                r = make_xspf_opn_page(it)
                self.regels += r
            else:
                self.found = False
                with open(os.path.join(mg.xmlpad, self.adres)) as fl:
                    for x in fl:
                        if '<a href' in x:
                            y = x.split('"')
                            y[1] = itempagetext % (s, u, y[1])
                            self.regels.append('"'.join(y))
                        else:
                            self.regels.append(x)
        elif s == "Vertel":
            if u in ("Start","About"):
                pass
            elif it != "" and it != "1":
                self.found = False
                r = make_tekst_page(it)
                self.regels += r
            else:
                dh = Cats("papa")
                ok = False
                for y in dh.categorieen:
                    if u == y[1]:
                        ok = True
                        break
                if not ok:
                    self.regels.append(sub_onbekend % (u, s))
                    return
                _, path, id_titels = catlijst("papa",u)
                # catlijst roept cats aan en die kan nog geen pad en urlbase doorgeven, zit nog niet in vertellers.xml
                if u == "Langere":
                    self.regels.append(onaf_melding)
                else:
                    self.regels.append("<br />")
                self.regels.append('<div style="padding-left: 20%">')
                for x in id_titels:
                    linktext = link_tpl.format(itempagetext + '/%s') + '%s</a><br />'
                    self.regels.append(linktext % (s, u, path, x[2], x[1]))
                self.regels.append('</div>')
        elif s == "Zing":
            if u in ("Intro","Contents"):
                pass
            elif it != "" and it != "1":
                self.found = False
                r = make_xspf_pl_page(it)
                self.regels += r
            else:
                # overige toegestane subsections bepalen
                try:
                    m = OwnerList('jaarseries')
                except DataError as meld:
                    self.regels.append("<div>%s</div>" % meld)
                    return
                if u not in m.lijst:
                    self.regels.append(sub_onbekend % (u, s))
                    return
                try:
                    m = MemberList(u,"jaarseries")
                except DataError as meld:
                    self.regels.append("<div>%s</div>" % meld)
                    return
                self.regels.append("<div>%s</div>" % m.tekst)
                for x in m.lijst: #
                    ds = Song(x)
                    if ds.found:
                        ## h = (s, u, x, ds.songtitel, ds.datering, ds.commentaar)
                        ## print h
                        text = link_tpl.format(itempagetext) + '%s</a> (%s) %s<br />'
                        self.regels.append(text % (s, u, x, ds.songtitel,
                            ds.datering, ds.commentaar))
                        ## if s.tekstpad != "":
                            ## tp = s.tekstpad
                        ## doc = '/'.join((tp[:-1],s.url))
                        ## self.regels.append('<a href="%sshowxml.py?type=Zing&amp;url=%s">%s</a> (%s) %s<br />'
                        ## % (http_cgipad,doc,s.Songtitel,s.datering,s.commentaar))
        elif s == "Dicht":
            ## print self.adres
            if u in ("Start","Cover","Inhoud"):
                if it != "" and it != "1":
                    self.found = False
                    ## print it
                    r = make_tekst_page(it)
                    self.regels += r
            else:
                if u not in jarenlijst():
                    self.regels.append(sub_onbekend % (u, s))
                    return
                tree = ET.ElementTree(file=os.path.join(dichtpad,
                    'Dicht_{}.xml'.format(u)))
                root = tree.getroot()
                onaam = os.path.join(dichtpad, "tempfile.html")
                newroot = ET.Element('span')
                newroot.set("class",root.tag)
                zetom(root,newroot)
                out = ET.ElementTree(newroot)
                out.write(onaam)
                with open(onaam) as f:
                    for x in f:
                        self.regels.append(x)
        elif s == 'Art':
            pass
            # als ART dan de pagina uit de content directory lezen
            #                       plaatje kopieren naar standaard naam
            #                       img veranderen naar standaard naam en standaard grootte + link eromheen naar ware grootte
        elif s == "Act":
            if u == 'Contents':
                pass
            elif it != "" and it != "1":
                self.found = False
                ## print it
                r = make_tekst_page(it)
                self.regels += r
        else:
            return
