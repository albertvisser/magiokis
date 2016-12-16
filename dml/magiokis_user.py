from globals import xmlpad
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from string import index

class FindUser(ContentHandler):
    "bevat de gegevens van een bepaalde user"
##<!DOCTYPE users [
##  <!ELEMENT users (user+)>
##  <!ELEMENT user (PCDATA)>
##  <!ATTLIST user id CDATA #REQUIRED>
##  <!ATTLIST user paswd CDATA #REQUIRED>
##]>
    def __init__(self, username):
        self.search_username = username
        # Initialize the flags to false
        self.userfound = 0
        self.founduser = 0

    def startElement(self, name, attrs):
        if name == 'user':
            user = attrs.get('id', None)
            if user == self.search_username:
                self.founduser = 1
                self.username = user
            passwd = attrs.get('paswd', None)
            if self.founduser:
                self.password = passwd

    def endElement(self, name):
        if name == 'user':
            if self.founduser:
                self.userfound = 1
                self.founduser = 0

class UpdateUser(XMLGenerator):
    "schrijf nieuwe songgegevens weg in XML-document"
    def __init__(self, user):
        self.uh = user
        self.search_item = self.sh.userid
        self.fh = open(self.sh.fn,'w')
        self.founditem = 0
        self.itemfound = 0
##        self.sh = song
##        self.fh = open('C:\\Program Files\\Xitami\\Webpages\\Magiokis\\xmldata\\Users_new.xml','w')
##        XMLGenerator.__init__(self,self.fh)
##

    def startElement(self, name, attrs):
    #-- kijk of we met de te wijzigen song bezig zijn
        if name == 'user':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = 1
                self.itemfound = 1
    #-- xml element (door)schrijven
        if self.founditem != 1:
            XMLGenerator.startElement(self, name, attrs)
        else:
            if name == 'user':
                self._out.write('<' + name)
                self.username = user
                self.password = passwd
                for (name,value) in attrs.items():
                    h = value
                    if name == 'id':
                        if value != self.username:
                            h = self.username
                    if name == 'paswd':
                        if value != self.password:
                            h = self.password
                    self._out.write(' %s="%s"' % (name,escape(h)))

    def characters(self,content):
##        newcontent = content.encode("iso-8859-1")
##        XMLGenerator.characters(self,newcontent)
        pass


    def endElement(self, name):
        if self.founditem != 1:
            XMLGenerator.endElement(self, name)
        else:
            if name == 'song':
                self.founditem = 0
                self._out.write('  </%s>' % name)

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()

class User:
    "lees een bepaalde user en controleer of deze een bepaald password heeft"
    def __init__(self,userid,paswd): # user aanmaken
        self.fn = xmlpad + '\\users.xml'
        self.fno = xmlpad + '\\users_oud.xml'
        print self.fn
        self.userid = userid
        self.paswd = paswd
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = FindUser(str(self.userid))
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        self.found = dh.userfound
        if self.found:
            if self.paswd == dh.password:
                self.paswdok = 1
            else:
                self.paswdok = 0

    def setattr(self,value):
        "wijzigen van het wachtwoord"
        self.paswd = value

    def write(self):
        from shutil import copyfile
        from os import remove
        copyfile(self.fn,self.fno)
        remove(self.fn)
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = UpdateUser(self)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fno)

def test():
    dh = User('CB00139', '')
    if dh.found:
        if dh.paswdok == 1:
            print "found user, password ok"
        else:
            print "found user, password wrong"
    else:
        print "user not found"

if __name__ == '__main__':
	test()
