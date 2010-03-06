#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
'''


class ValidationError(Exception):
    """It doesn't validate!
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def __unicode__(self):
        return unicode(self.value)

class ConversionError(Exception):
    """It cannot be converted!
    
    >>> ConversionError('veikia!')
    ConversionError()
    >>> raise ConversionError('veikia!')
    Traceback (most recent call last):
    ...
    ConversionError: 'veikia!'
    >>> try:
    ...   raise ConversionError('veikia!')
    ... except ConversionError, e:
    ...   print "%s"%e
    ... 
    'veikia!'
    >>> try:
    ...   raise ConversionError(u'Ačiū!')
    ... except ConversionError, e:
    ...   x = u'%s'%e
    ...   #print u'%s'%e
    ... 
    >>> x == u'Ačiū!'
    True
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def __unicode__(self):
        return unicode(self.value)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
