import re
import yaml
from docwriter import *

fd_required = {
        'string_count',
        'fret_range'
        }

fd_optional = {
        'title',
        'fingerings',
        'base_width',
        'ratio',
        'offset'
        }

fd_properties = fd_required.union(fd_optional)

class FretDiagram:
    def __init__(self, yaml_dict={}, **kwargs):
        # load from the dictionary (with overrides, if provided)
        args = {}
        args.update(yaml_dict)
        args.update(kwargs)

        if(not set(args) <= fd_properties):
            t = "["
            for i in set(args) - fd_properties:
               t += "'" + i + "', "
            t = t[:-2] + "]"
            print("Uknown parameters: " + t)
            raise Exception('Uknown parameters')

        if(not set(args) <= fd_properties):
            t = "["
            for i in set(args) - fd_properties:
               t += "'" + i + "', "
            t = t[:-2] + "]"
            print("Missing required parameters: " + t)
            raise Exception('Missing required parameters')

        # Required Parameters
        self.string_count = args['string_count']
        self.fret_min = args['fret_range'][0]
        self.fret_max = args['fret_range'][1]
        for i in {self.string_count, self.fret_min, self.fret_max}:
            if(not isinstance(i, int)):
                raise Exception('Type oops!!')

        # Optional Parameters
        if 'fingerings' in args:
            self.fingerings = args['fingerings']
        else:
            self.fingerings = []

        if 'title' in args:
            self.title = args['title']
        else:
            self.title = ""

        if 'base_width' in args:
            self.base_width = args['base_width']
        else:
            self.base_width = 100

        if 'ratio' in args:
            self.ratio = args['ratio']
        else:
            self.ratio = 1.5

        if 'offset' in args:
            self.offset = args['offset']
        else:
            self.offset = 100

        if 'label_size' in args:
            self.label_size = args['label_size']
        else:
            self.label_size = 45

    def __str__(self):
        # establish geometry
        width = self.offset * 2 + (self.string_count - 1) * self.base_width
        height = self.offset * 2 + (self.fret_max - self.fret_min) * \
                    self.ratio * self.base_width
        vbox = [-self.offset,
                -self.offset,
                width + self.offset,
                height + self.offset]

        circle = XMLTag({
           'tagname': 'circle',
           'properties': [
               Property('cx', '25'),
               Property('cy', '25'),
               Property('r', '25')
               ],
           'closed': 'True'
           })

        symbol = XMLTag({
           'tagname': 'symbol',
           'properties': [
               Property('id', 'circ')
               ],
           'contents': [circle]
           })

        g = XMLTag({
           'tagname': 'g',
           'contents': [symbol]
           })

        defs = XMLTag({
           'tagname': 'defs',
           'contents': [g]
           })

        label = XMLTag({
            'tagname': 'text',
            'properties': [
                Property('x', '-10'),
                Property('y', str(self.label_size / 3)),
                Property('text-anchor', 'end'),
                Property('font-size', str(self.label_size))
                ],
            'contents': [ 'Nut' if self.fret_min == 0 else str(self.fret_min) ]
            })

        strings = []
        for i in range(self.string_count):
           strings += [
               XMLTag({
                   'tagname': 'line',
                   'closed': 'True',
                   'properties': [
                       Property('x1', str(self.base_width * i)),
                       Property('y1', str(0)),
                       Property('x2', str(self.base_width * i)),
                       Property('y2', str((self.fret_max - self.fret_min) * self.ratio * \
                               self.base_width)),
                       Property('stroke', 'black'),
                       Property('stroke-width', '2')
                       ]
                   })
               ]

        frets = []
        for i in range(self.fret_max - self.fret_min + 1):
           frets += [
                XMLTag({
                    'tagname': 'line',
                    'closed': 'True',
                    'properties': [
                       Property('x1', str(0)),
                       Property('y1', str(self.ratio * self.base_width * i)),
                       Property('x2', str(self.base_width * (self.string_count - 1))),
                       Property('y2', str(self.ratio * self.base_width * i)),
                       Property('stroke', 'black'),
                       Property('stroke-width', '2')
                       ]
                    })
                ]

        # Check if nut is to be rendered
        if(self.fret_min == 0):
            frets[0]['stroke-width'] = '10'
            frets[0]['stroke-linecap'] = 'square'

        fingerings = []
        for fngr in self.fingerings:
            fingerings += [
                XMLTag({
                    'tagname': 'use',
                    'closed': 'True',
                    'properties': [
                        Property('x', str(fngr[0] * self.base_width)),
                        Property('y', str((fngr[1] - 0.5) * self.base_width * self.ratio)),
                        Property('xlink:href', '#circ'),
                        Property('transform', 'translate(-25, -25)')
                        ]
                    })
                ]

        svg = XMLTag({
            'tagname': 'svg',
            'properties': [
                Property('width', str(width)),
                Property('height', str(height)),
                Property(
                    'viewBox',
                    str(vbox[0]) + ' ' + str(vbox[1]) + ' ' 
                        + str(vbox[2]) + ' ' + str(vbox[3]))
                    ],
            'contents': [defs, label] + frets + strings + fingerings
                })

        html = HtmlDocument([svg])
        
        return str(html)

d = yaml.load(open('example.yaml').read())
fd = FretDiagram(d)
with open('out.html', 'w') as f:
    f.write(str(fd))
