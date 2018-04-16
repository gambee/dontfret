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

from note import *

class String:
    def __init__(self, lowest_note, fret_limit=16):
       self.limit = fret_limit
       self.lowest = Pitch(lowest_note)

       
    def __contains__(self, pitch):
        p = Pitch(pitch)
        a = self.lowest <= Pitch(pitch)
        b = Pitch(pitch) <= (self.lowest + self.limit)
        return (a and b)

