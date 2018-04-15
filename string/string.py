'''
string.py

Max Gambee
Brady Pearson

Copyright 2018

Description: Models a single 'string' of a fretted string instrument, in the
    sense that one can query a pitch class (or a set of pitch classes) and 
    the string class will return a set of fret numbers on which those pitch
    classes lie.
'''

class String:
    def __init__(self, open_note, fret_count):
        
