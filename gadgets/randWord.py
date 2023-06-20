#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:39:10 2023

@author: ubuntu
"""
'''
wget https://gist.githubusercontent.com/hugsy/8910dc78d208e40de42deb29e62df913/raw/eec99c5597a73f6a9240cab26965a8609fa0f6ea/english-nouns.txt
wget https://gist.githubusercontent.com/hugsy/8910dc78d208e40de42deb29e62df913/raw/eec99c5597a73f6a9240cab26965a8609fa0f6ea/english-adjectives.txt
'''
from pathlib import Path
from os import chdir, environ
chdir(environ['HOME'] + '/LAB/gadgets_cloud') #this line is for Spyder IDE only
root = Path(".")
from numpy.random import choice
with open(str(root / 'english-nouns.txt'), 'r') as file:
    # Read the file line by line
    nouns = file.readlines()
    
with open(str(root / 'english-adjectives.txt'), 'r') as file:
    # Read the file line by line
    adjectives = file.readlines()


print(choice(adjectives).strip() + '_' + choice(nouns).strip())

