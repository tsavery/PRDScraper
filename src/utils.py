# -*- coding: utf-8 -*-

import os
import errno
import json

def remove_trailing_and_leading_spaces(value):
    while value.endswith(' '):
        value = value[:-1]
    while value.startswith(' '):
        value = value[1:]
    return value

def replace_unicode_characters(value):
    value.encode('utf-8')
    value = value.replace('\\u2013', u'-')
    value = value.replace('\\u2014', u'-')
    value = value.replace('\\u00d7', u'x')
    value = value.replace('\\t', u'')

    return value

def obj_dict(obj):
    return del_empty(obj._attrs.copy())

def del_empty(d):
    for key, value in list(d.items()):
        if (not isinstance(value, int) and len(value) is 0) or (isinstance(value, int) and value == 0):
            del d[key]
        elif isinstance(value, dict):
            del_empty(value)
    return d

def save_json(val, filename):
    jsonstr = json.dumps(val, default=obj_dict, sort_keys=False, indent=4)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    f = open(filename, "w")
    jsonstr = replace_unicode_characters(jsonstr)
    f.write(jsonstr)
    f.close()
