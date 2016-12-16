import os
root = "/home/albert/magiokis/data"
xmlpad = os.path.join(root, "songs")
mp3pad = os.path.join(root, "mp3")
tekstpad = os.path.join(root, "zing")
data = os.path.join(xmlpad, 'magiokis.sdb')
mp3root = "http://data.magiokis.nl/mp3/"

class DataError(Exception):
    pass
