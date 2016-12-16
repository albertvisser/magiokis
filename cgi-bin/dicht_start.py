#! /usr/bin/env python3
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
import progpad
from dicht_main import Dicht

def main():
    print("Content-Type: text/html")     # HTML is following
    print('')                              # blank line, end of headers
    d = Dicht({"wat": "start"})
    for x in d.regels:
        print(x)

if __name__ == '__main__':
	main()

