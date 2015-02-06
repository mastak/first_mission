import os
import sys


GUARDED_MODULES_FOLDER = os.path.join(os.path.dirname(__file__), 'guarded_modules')

sys.path.append(GUARDED_MODULES_FOLDER)

ALLOWED_MODULES = [
    'array',
    'base64',
    'binascii',
    'bisect',
    'calendar',
    'collections',
    'copy',
    'datetime',
    'decimal',
    'exceptions',
    'fractions',
    'functools',
    'hashlib',
    'heapq',
    'itertools',
    'math',
    'numbers',
    'operator',
    'pprint',
    'random',
    're',
    'struct',
    'string',
    'StringIO',
    'textwrap',
    'time',
    'types',
    'unicodedata',
    'unittest',
    'weakref',
    '_strptime',
]


CLOSE_BUILDINS = [
    '__import__',
    'memoryview',
    'open',
    'buffer',
    'execfile',
    'raw_input',
    'input',
    'reload',
    'help'
]
