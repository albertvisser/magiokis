#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs, sys
writer = codecs.getwriter('utf8')(sys.stdout.buffer)
import progpad
from denk_main import Denk

def main():
    print("Content-Type: text/html\n")     # HTML is following
    d = Denk({"wat": "start"})
    for x in d.regels:
        print(x)

if __name__ == '__main__':
	main()

