'''
note.py

Max Gambee
Brady Pearson

Copyright 2018

Description: A class to model a musical note/pitch class abstraction.
'''

def pclass(pitch):
    ret = None
    if(isinstance(pitch, int)):
        ret = pitch % 12
    return ret
        

def register(pitch):
    ret = None
    if(isinstance(pitch, int)):
        if(pitch >= 0):
            ret = int(pitch / 12)
        else:
            ret = int((pitch - 11) / 12)
    return ret


class Note:
    def __init__(self, pitch):
        if(isinstance(pitch, int)):
            self.pitch = pitch
        #elif(isinstance(pitch, tuple

    def pclass(self):
        return self.pitch % 12

    def register(self):
        ret = None
        if(self.pitch >= 0):
            ret = self.pitch / 12


