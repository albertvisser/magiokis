import shared
from magiokis_user import User

class Logon:
    def __init__(self,user,passw):
        self.user = user
        self.paswd = passw
        self.fout = ""
        if self.user == "":
            self.fout = "nouser"
        elif self.paswd == "":
            self.fout = "nopasw"
        else:
            dh = User(self.user, self.paswd)
            if dh.found:
                if dh.paswdok == 0:
                    self.fout = "nok"
            else:
                self.fout = "notfound"
        if self.fout == "":
            self.ok = True
        else:
            self.ok = False
            self.meldfout()

    def meldfout(self):
        self.regels = []
        fnaam = htmlroot + '/magiokis_launch.html'
        foud = open(fnaam, 'r')
        for x in foud.readlines():
            y = x[:-1]
            if x.find('<td><input type="text" name="userid" size="20" maxlength="20">') >= 0 and ok != 'nouser':
                    self.regels.append(y.replace('></td>',' value="%s"></td>' % user))
            elif x.find('<h3>&nbsp;</h3>') >= 0:
                if self.fout == 'nouser':
                    self.regels.append(y.replace('<h3>&nbsp;</h3>','<h3>Geen userid opgegeven</h3>'))
                elif self.fout == 'nopasw':
                    self.regels.append(y.replace('<h3>&nbsp;</h3>','<h3>Geen wachtwoord opgegeven</h3>'))
                elif self.fout == 'notfound':
                    self.regels.append(y.replace('<h3>&nbsp;</h3>','<h3>Userid onbekend</h3>'))
                elif self.fout == 'nok':
                    self.regels.append(y.replace('<h3>&nbsp;</h3>','<h3>Wachtwoord foutief</h3>'))
            else:
                self.regels.append(y)
        foud.close()

