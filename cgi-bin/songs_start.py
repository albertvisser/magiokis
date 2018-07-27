#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import progpad

from songs_main import Songs

def main():
    print("Content-Type: text/html")     # HTML is following
    print('')
    d = Songs({"wat": "start"})
    for x in d.regels:
        print(x)

if __name__ == '__main__':
	main()

