import re
import yaml

fd_properties = {
        'title',
        'string_count',
        'fret_range',
        'fingerings'
        }

class FretDiagram:
    def __init__(self, yaml_dict={}, **kwargs):
        # load from the dictionary (with overrides, if provided)
        args = {}
        args.update(yaml_dict)
        args.update(kwargs)

        if 'title' in args:
            self.title = args['title']
        if 'string_count' in args:
            self.string_count = args['string_count']
        if 'fret_range' in args:
            self.fret_min = args['fret_range'][0]
            self.fret_max = args['fret_range'][1]
        if 'fingerings' in args:
            self.fingerings = args['fingerings']

        if(not set(args) <= fd_properties):
            t = "["
            for i in set(args) - fd_properties:
               t += "'" + i + "', "
            t = t[:-2] + "]"
            print("Uknown parameters: " + t)

    def __str__(self):

