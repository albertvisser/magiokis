Files in deze directory
=======================

cgi-bin/
--------
cgi response routines, roepen verwerkingsroutines aan

    denk_detail.py
        aansturing toon/wijzig details
    denk_select.py\
        aansturing toon/wijzig selectie
    denk_start.py
        aansturing startscherm
    dicht_detail.py
        opstarten detailscherm
    dicht_select.py
        opstarten selectiescherm
    dicht_start.py
        opstarten startscherm
    lijstopnames.py
        songs app: opbouwen lijst opnames o.b.v. selectie
        gebruikt: cgi
        importeert: progpad, songs
    lijstregs.py
        songs app: opbouwen registraties o.b.v. selectie
        gebruikt: cgi
        importeert: progpad, songs
    lijstsongs.py
        songs app: opbouwen lijst songs o.b.v. selectie
        gebruikt: cgi
        importeert: progpad, songs
    magiokis_begin.py
        main site: aansturen apps startscherm (magiokis launch)
    mainscript.py
        main site: aansturen verwerkingsprogramma magiokis site
    playurl.py
        songs app: afspelen volgens bepaalde url
        gebruikt: cgi
        importeert: progpad, songs
    progpad.py
        include tbv locatie verwerkingsroutines
    sendxml.py
        main site: uitsturen xml document
    showpic.py
        main site: uitsturen plaatje met desgewenst link naar volgende/vorige pagina
    showxml.py
        main site: uitsturen xml document voorzien van toepasselijk stylesheet
    songs_detail.py
        opbouwen detailscherm
        gebruikt: cgi
        importeert: progpad, songs
    songs_start.py
        opbouwen startscherm
        importeert: progpad, songs
    vertel_detail.py
        opbouwen detailscherm
        gebruikt cgi
        importeert progpad, vertel_main
    vertel_select.py
        opbouwen selectiescherm
        gebruikt cgi
        importeert progpad, vertel_main
    vertel_start.py
        opbouwen startscherm
        gebruikt cgi
        importeert progpad, vertel_main
    vertel_user.py
        opbouwen user scherm
        gebruikt cgi
        importeert progpad, vertel_main
    wijzigdetails.py
        songs app: opbouwen invulbaar detailscherm voor song
        gebruikt: cgi
        importeert: progpad, songs
    wijzigopname.py
        songs app: opbouwen invulbaar detailscherm voor opname
        gebruikt: cgi
        importeert: progpad, songs
    wijzigsongtekst.py
        songs app: opbouwen invulbaar detailscherm voor songtekst
        gebruikt: cgi
        importeert: progpad, songs
    wijzigtabel.py
        songs app: opbouwen invulbaar lijstscherm voor tabellen
        gebruikt: cgi
        importeert: progpad, songs

dml/
....
data manipulatie routines, aangeroepen door verwerkingsroutines

    magiokis_globals.py
        diverse paden o.a. waar de data staat
    magiokis_user.py
        data manipulatie gebruikers
    pagehandler.py
        datamanipulatie pagina gegevens
    zetom.py
        utility programma om xml (bv. een gedicht) om te zetten naar html
        module level code bevat aanroep om dit te doen voor tocs.xml
        het hoofdbestanddeel hiervan zit ook in pagehandler.py

dml/denk/
.........
    denk_globals.py
        include t.b.v. locatie applicatiedata  (xml bestanden)
    denk_item.py
        routines t.b.v. benadering/manipulatie teksten
    denk_trefw.py
        routines t.b.v. benadering/manipulatie trefwoorden

dml/dicht/
..........
    dicht_datapad.py
        locatie data (xml bestanden)
    dicht_item.py
        data manipulatie gedichten
    dicht_trefw.py
        data manipulatie trefwoorden/thema's

dml/songs/
..........
    coderec.py
        data manipulatie voor codetabellen
        importeert datapad
    createplaylists.py
        code voor opbouwen afspeellijsten
        wordt niet gebruikt in de sql versie, daarom werkt het afspelen niet?
        gebruikt xml.etree
        importeert datapad
    datapad.py
        include voor pad naar data
        importeert sqlite3, mystuff
    muziekreg.py
        datamanipulatie registratie
        importeert datapad, coderec, regtype, song
    objectlists.py
        datamanipulatie samenstellen lijstverzamelingen
        importeert datapad, coderec
    opname.py
        datamanipulatie opname
        importeert datapad, coderec, objectlists, song
    opname_join.py
        datamanipulatie opname
        ophalen met alle gerelateerde gegevens d.m.v. "join"
        importeert datapad, coderec, objectlists, song
    regtype.py
        data manipulatie registratie type
        importeert uit datapad, coderec
    song.py
        data manipulatie song
        importeert datapad, coderec
    Songtekst.py
        data manipulatie sogtekst (nog met xml)
        gebruikt xml.etree
        importeert datapad, song
    user.py (niet af)
        data manipulatue gebruiker
        importeert datapad, coderec

dml/vertel/
...........
    verhalen.py
        datamanipulatie verhalen
        gebruikt xml.sax
        importeert vertel_datapad
    vertellers.py
        datamanipulatie gebruikers (vertellers)
        gebruikt xml.sax
        importeert vertel_datapad
    vertel_datapad.py
        locatie data (xml bestanden)
    vertel_item.py
        bevat classes voor selectielijsten
        gebruikt xml.sax
        importeert vertel_datapad
        importeert uit vertellers

html/
-----
html sources e.d.

    favicon.ico
        site icon
    index.html
        startpagina magiokis site
    Magiokis.css
        styling
    magiokis_launch.html
        startpagina apps
    xspf_player_button.html
        html voor xspfplayer als button
    xspf_player_slim.html
        html voor xspf player als control met titel

html/denk/
..........
    denk.css
        styling info for XML - so unneeded here
        contains styling for elements denkerij gedenk titel trefwoord alinea
    detail.html
        detailscherm
    favicon.ico
        site icon
    index.html
        opstarten startscherm
    select_args.html
        opgeven trefwoord
    select_list.html
        selectiescherm titels
    start.html
        startscherm

html/dicht/
...........
    detail.html
        detailscherm
    dicht.css
        styling info for XML - elements gedichten gedicht titel couplet regel tekst
    favicon.ico
        site icon
    index.html
        opstarten startscherm
    select_args.html
        selecteren trefwoord/thema
    select_list.html
        selecteren gedicht
    start.html
        startscherm

html/songs/
...........
    favicon.ico
        site icon
    index.html
        opstarten startpagina
    opnlist.html
        lijst opnames
    reglist.html
        lijst registraties
    songdetail.html
        detailscherm
    songlist.html
        lijst songs
    start.html
        startpagina
    wijzigdetail.html
        scherm voor wijzigen song gegevens
    wijzigopname.html
        scherm voor wijzigen opnamegegevens
    wijzigregtypes.html
        scherm voor wijzigen registratiegegevens
    wijzigsongtekst.html
        scherm voor wijzigen songtekst
    wijzigtabel.html
        scherm voor wijzgen tabelgegevens

html/vertel/
............
    favicon.ico
        site icon
    index.html
        opstarten startpagina
    Vertel.css (not in manifest anymeore)
        styling info for XML - elements
    vertel_detail.html
        detailscherm
    vertel_nwecat.html
        opvoeren nieuwe categorie (bundel)
    vertel_selcat.html
        selecteren categorie (bundel) en tonen lijst
    vertel_select.html
        schermkop selectieschermen
    vertel_selzoek.html
        opgeven zoekargument en tonen lijst
    vertel_start.html
        startscherm
    vertel_user.html
        opgeven user (verteller)

main_logic/
-----------
verwerkingsroutines, aangeroepen vanuit cgi responses

deze vullen de html sources verder in aan de hand van de opgehaalde gegevens

    denk_main.py
        verwerkingsprogramma
    dicht_main.py
        verwerkingsprogramma
    magiokis_globals.py
        locatie data manipulatie routines en dergelijke
    magiokis_login.py
        opbouwen aanlog pagina
    magiokis_page.py
        opbouwen pagina
    shared.py
        shared code: paden e.d.
    songs.py
        samenstellen pagina's
        gebruikt: mystuff
        importeert: magiokis_globals, song, opname, muziekreg, songtekst,
        regtype, coderec, objectlists
    vertel_main.py
        verwerkingsprogramma
        importeert magiokis_globals
        importeert uit vertellers, vertel_item, verhalen
