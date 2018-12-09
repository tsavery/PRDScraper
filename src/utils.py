# -*- coding: utf-8 -*-

import os
import errno

def remove_trailing_and_leading_spaces(value):
    while value.endswith(' '):
        value = value[:-1]
    while value.startswith(' '):
        value = value[1:]
    return value

def replace_unicode_characters(value):
    value = value.replace('\u2013', '-')
    value = value.replace('\u00d7','x')
    value = value.replace('\t', '')

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

def save_json(jsonstr, filename):
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
