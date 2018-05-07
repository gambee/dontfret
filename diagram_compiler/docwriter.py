import re

class Property:
    def __init__(self, name, value=""):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + '="' + self.value + '"'

def tobool(s):
    if(isinstance(s, str)):
        if(bool(re.match('(t(rue)?|y(es)?)', s, re.IGNORECASE))):
            return True
        elif(bool(re.match('(f(alse)?|n(o)?)', s, re.IGNORECASE))):
            return False
        else:
            raise Exception('tobool: unknown format string')
    else:
        return bool(s)


class DocElement:
    def __init__(self, initargs={}):
        if('header' in initargs):
            self.header = initargs['header']
        else:
            self.header = ""

        if('footer' in initargs):
            self.footer = initargs['footer']
        else:
            self.footer = ""

        if('contents' in initargs):
            self.contents = initargs['contents']
        else:
            self.contents = []

    def __str__(self):
        return self._str_(0)

    def _str_(self, depth):
        indent = ""
        for i in range(depth):
            indent += "  "
        s = indent + self.header + '\n'
        for element in self.contents:
            if(isinstance(element, DocElement)):
                s += element._str_(depth + 1) + '\n'
            else:
                s += str(element) + '\n'
        s += indent + self.footer
        return s

html_header = '''<!DOCTYPE html>
<html>
<head>
<title>HtmlElement</title>
</head>
<body>'''

class HtmlDocument(DocElement):
    def __init__(self, initargs=[]):
        args = {
            'header': html_header,
            'footer': '</body>\n</html>',
            'contents': initargs
            }


        super().__init__(args)

class XMLTag(DocElement):
    def __init__(self, initargs={}):
        if('tagname' in initargs):
            self.tagname = initargs['tagname']
        else:
            self.tagname = '?unkown?'

        if('properties' in initargs):
            self.properties = initargs['properties']
        else:
            self.properties = []
        
        if('contents' in initargs):
            self.contents = initargs['contents']
        else:
            self.contents = []

        if('closed' in initargs):
            self.closed = tobool(initargs['closed'])
        else:
            self.closed = False

    def __getitem__(self, key):
        props = []
        for p in self.properties:
            props += [(p.name, p.value)]
        props = dict(props)
        if(key in props):
            return props[key]
        else:
            return None

    def __setitem__(self, key, value):
        for p in self.properties:
            if(key == p.name):
                p.value = value
                return
        self.properties += [Property(key, value)]

    def __delitem__(self, key):
        tmp = []
        for p in self.properties:
            if(p.name != key):
                tmp += [p]
        self.properties = tmp

    def _str_(self, depth):
        self.header = '<' + self.tagname
        for p in self.properties:
            self.header += ' ' + str(p)
        if(self.closed):
            self.header += '/>'
            self.footer = ''
        else:
            self.header += '>'
            self.footer = '</' + self.tagname + '>'
        return super()._str_(depth)
