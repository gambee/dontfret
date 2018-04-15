'''
note.py

Max Gambee
Brady Pearson

Copyright 2018

Description: A class to model a musical note/pitch class abstraction.

Notes on Abstractions & Representations:
    There are a number of reasonable ways to represent a pitch, and many of
    them will be useful to us. Our goal should be to allow the use of any of
    the following representations, to be used as inputs to any of the functions
    and any of the class methods/constructors that take a pitch as an input.
    This ensures maximum compatibility and convenience.

    Representations:
        - An integer:
            0 = c0,
            1 = b0,
            12 = c1,
            -12 = c-1
        - A tuple of the form (<register>, <pitch class>):
            (0, 0) = c0,
            (0, 1) = b0,
            (1, 0) = c1,
            (-1, 0) = c-1
        - A class of type 'Pitch'
        <to be continued>
        ...

The notion of register will always (almost) be tied to simply the integer
designation of the octave containing that pitch. The '(almost)' is mentioned
due to some grey area around the string repesentation of pitches involved with
parsing strings involving the edge cases:
    'Cb1' is enharmonic to 'B#0', but their register will be 0.
'''

import re

pitch_regex = '([A-G])(b{0,2}|#{0,2})(-?[0-9]{1,2})'
pclass_regex = '([A-G])(b{0,2}|#{0,2})-?[0-9]{0,2}'

npclass_to_i= dict(zip(['C', 'D', 'E', 'F', 'G', 'A', 'B'], range(12)))
accid_to_i = dict(zip(['#', '##', 'b', 'bb'], [1, 2, -1, -2]))


def pitch_class(pitch):
    # Given a pitch, determine the pitch class (c, d, e, etc.)
    # where pitch can be an integer, or an object of type Note (planned)

    ret = None  # If not a known type, return None

    # Integer Representation
    if(isinstance(pitch, int)):
        ret = pitch % 12  # Note: the python mod implementation is not like C's

    # List / Tuple Representation
    if(isinstance(pitch, tuple) or isinstance(pitch, list)):
        ret = pitch[1]

    return ret


def register(pitch):
    ret = None
    if(isinstance(pitch, int)):
        if(pitch >= 0):
            ret = int(pitch / 12)
        else:
            ret = int((pitch - 11) / 12)
    return ret


class PitchClass:
    def __init__(self, pclass):
        self.pclass = None
        if(isinstance(pclass, int)):
            self.pclass = pclass
        elif(isinstance(pclass, tuple) or isinstance(pclass, list)):
            self.pclass = pclass[1]
        elif(isinstance(pclass, str)):
            mtch = re.fullmatch(pclass_regex, pclass)
            if(bool(mtch)):
                args = mtch.groups()
                tmp = npclass_to_i[args[0]] + accid_to_i[args[1]]
                if(tmp < 0):
                    tmp += 12
                if(tmp > 11):
                    tmp -= 12
                self.pclass = tmp
            else:
                raise Exception('PitchClass: ',
                                'Constructor: ',
                                'Format String Error: ',
                                pclass)


class Pitch:
    def __init__(self, pitch):
        if(isinstance(pitch, int)):
            self.pitch = pitch
        elif(isinstance(pitch, tuple) or isinstance(pitch, list)):
            self.pitch = pitch.pitch

    def pclass(self):
        return self.pitch % 12

    def register(self):
        ret = None
        if(self.pitch >= 0):
            ret = self.pitch / 12
