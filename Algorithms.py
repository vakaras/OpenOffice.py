#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Exceptions import ConversionError

class School(object):
    """Object representing school data.
    """
    
    def __init__(self, title, id, lid):
        """Constructor.
        @param title - school title;
        @param id - school id;
        @param lid - location id.
        """

        self.title = title
        self.id = id
        self.lid = lid

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
                u' "':                  u' „',
                u'"':                   u'“',
                u' r.':                 u' rajono',
                u' m.':                 u' miesto',
                u' pagr.':              u' pagrindinė',
                u' vid.':               u' vidurinė',
                u'Gimnazija':           u'gimnazija',
                u'm-kla':               u'mokykla',
                u'KTUG':         
                        u'Kauno technologijos universiteto gimnazija',
                u'KTU':         
                        u'Kauno technologijos universiteto ',
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

class Address(object):
    """Object representing address.
    """
    
    def __init__(self, text, validate=False):
        """Constructor.
        @param text - unicode text representing address.
        """
        
        self.text = text

        if validate:
            self.validate()

    def validate(self):
        """Validates address, and extracts info such as town/region.
        """

        text = self.text

        change = {
                u' raj.':               u' rajonas',
                u' r.':                 u' rajonas',
                u' r.sav':              u' rajonas',
                u'rajonas.':            u'rajonas',
                u',':                   u' , ',
                }
        
        for k, v in change.items():
            text = text.replace(k, v)

        self.town = None
        parts = text.split()
        for i, part in enumerate(parts):
            if part == u'rajonas':
                self.town = u' '.join(parts[i-1:i+1])
                break

        if not self.town:
            for part in reversed(parts):
                if part in (u'g.', u'pr.', u'km.', u'sen.', u'skg.', 
                        u'mstl.'):
                    break
                if part[-1] == u'.':
                    part = part[:-1]
                if part.isalpha():
                    if part.istitle():
                        self.town = part
                    break
            if not self.town:
                raise ConversionError(u'Nepavyko atpažinti miesto!')

        self.value = text.replace(u' , ', u',')
