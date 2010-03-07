#!/usr/bin/env python
# -*- coding: utf-8 -*-

class School(object):
    """Object representing school data.
    """
    
    def __init__(self, title, id):
        """Constructor.
        @param title - school title;
        @param id - school id;
        """

        self.title = title
        self.id = id

        self.correctTitle()
        self.simplifyTitle()

        self.matching = 0

    def correctTitle(self):
        """Corrects most common mistakes in title.
        """
        title = self.title
        if title[0] == u'"' or title[0] == u'\'':
            title = u'„' + title[1:]
        if title[-1] == u'"' or title[0] == u'\'':
            title = title[:-1] + u'“'

        change = { 
                u' "':              u' „',
                u'"':               u'“',
                u' r.':             u' rajono',
                u' m.':             u' miesto',
                u' pagr.':          u' pagrindinė',
                u' vid.':           u' vidurinė',
                u'Gimnazija':       u'gimnazija',
                }
        for k, v in change.items():
            title = title.replace(k, v)

        if u'Liubertien' in title:      # FIXME: Workaround mismach
            title = u'Viešoji įstaiga Vilniaus privati gimnazija'

        self.title = title

    def simplifyTitle(self):
        """Simplifies title, to increase change to match it.
        """
        simple = self.title.lower()
        remove = [ 
                u' ',           # FIXME Hardcoded Lithuanian symbols.
                u'„',
                u'“',
                u'-',
                u',',
                u'.',
                #u'gimnazija',
                #u'pagrindinė',
                #u'pagrindine',
                #u'vidurinė',
                #u'vidurine',
                #u'pradinė',
                #u'pradine',
                u'mokykla',
                ]
        for i in remove:
            simple = simple.replace(i, u' ')
        replace = [
                (u'ė', u'e')
                ]
        for k, v in replace:
            simple = simple.replace(k, v)
        self.simple = simple
        self.words = simple.split()

    def clear(self):
        """Clears matching number.
        """
        self.matching = 0

    def inc(self):
        """Increases matching number.
        """
        self.matching += 1

    def get(self):
        """Returns matching number.
        """
        return self.matching
