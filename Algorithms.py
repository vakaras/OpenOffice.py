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

        change = ( 
                (u' "',                 u' „'),
                (u'"',                  u'“'),
                (u',,',                 u'„'),
                (u'=',                  u'ž'),
                (u' r.',                u' rajono'),
                (u' m.',                u' miesto'),
                (u' pagr.',             u' pagrindinė'),
                (u' pagrindine',        u' pagrindinė'),
                (u' vid.',              u' vidurinė'),
                (u' vidurine',          u' vidurinė'),
                (u'Gimnazija',          u'gimnazija'),
                (u' G ',                u' gimnazija '),
                (u'g-ja',               u'gimnazija '),
                (u'm-kla',              u'mokykla'),
                (u'm-k',                u'mokykla'),
                (u'm - kla',            u'mokykla'),
                (u'm-la',               u'mokykla'),
                (u'mok.',               u'mokykla'),
                (u'mokykla',            u' mokykla '),
                (u'v.m.',               u' vidurinė mokykla '),
                (u'KTUG',         
                        u'Kauno technologijos universiteto gimnazija'),
                (u'KTU',         
                        u'Kauno technologijos universiteto '),
                (u'VDU',         
                        u' Vytauto Didžiojo universiteto '),
                (u'NMKČMM',
                        u'Nacionalinė Mikalojaus Konstantino '
                        u'Čiurlionio menų mokykla'),
                )
        ends = (
                (u'G',                   u' gimnazija '),
                )
        for k, v in change:
            title = title.replace(k, v)
        for k, v in ends:
            if title.endswith(k):
                title = title[:-len(k)] + v

        if u'Liubertien' in title:      # FIXME: Workaround mismach
            title = u'Viešoji įstaiga Vilniaus privati gimnazija'
        elif u'Kalniečių vidurinė' in title:
            title = u'Kauno Antano Smetonos vidurinė mokykla'
        if u'ktug' == title:
            title = u'Kauno technologijos universiteto gimnazija'

        self.title = title

    def simplifyTitle(self):
        """Simplifies title, to increase change to match it.
        """
        simple = self.title.lower()
        remove = [ 
                u' ',                   # FIXME: Hardcoded Lithuanian 
                u'„',                   # symbols.
                u'“',
                u'-',
                u'–',
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
                (u'ė', u'e'),
                (u'ų', u'u'),
                (u'ž', u'z'),

                ]
        for k, v in replace:
            simple = simple.replace(k, v)
        self.simple = simple
        self.words = set(simple.split())

    def clear(self):
        """Clears matching number.
        """
        self.matching = 0

    def inc(self):
        """Increases matching number. 
        """
        self.matching += 1

    def add(self, word):
        """Adds word match weight to matching number.
        """
        self.matching += 10
        if word in (u'mokykla', u'vidurine', u'pagrindine', u'gimnazija',):
            self.matching -= 1

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
                u' raj.':               u' rajonas ',
                u' raj ':               u' rajonas ',
                u' r.':                 u' rajonas ',
                u' r.sav':              u' rajonas ',
                u'rajonas.':            u' rajonas ',
                u' km.':                u' kaimas ',
                u' k.':                 u' kaimas ',
                u' km,':                u' kaimas, ',
                u' sav.':               u' savivaldybė ',
                u' mstl.':              u' miestelis ',
                u',':                   u' , ',
                u'.':                   u'. ',
                u';':                   u' , ',
                u'LT - ':               u'LT-',
                u'LT ':                 u'LT-',
                }
        
        for k, v in change.items():
            text = text.replace(k, v)

        if text.endswith(' raj'):
            text = text[:-3] + ' rajonas '
        elif text.endswith(' r'):
            text = text[:-1] + ' rajonas '

        self.town = None
        parts = text.split()

        for part in parts:
            if (part.isalpha() and part.isupper() and len(part) > 1) and \
                    (part not in (u'SB',)):
                raise ConversionError(u'Nepavyko atpažinti miesto! Did.')

        for i, part in enumerate(parts):
            if part == u'kaimas':
                if len(parts[i-1]) == 1:
                    self.town = u' '.join(parts[i-2:i+1])
                else:
                    self.town = u' '.join(parts[i-1:i+1])
                break
        if not self.town:
            for i, part in enumerate(parts):
                if part == u'miestelis':
                    self.town = u' '.join(parts[i-1:i+1])
                    break
        if not self.town:
            for i, part in enumerate(parts):
                if part == u'rajonas':
                    self.town = u' '.join(parts[i-1:i+1])
                    break
        if not self.town:
            for i, part in enumerate(parts):
                if part == u'savivaldybė':
                    self.town = u' '.join(parts[i-1:i+1])
                    break

        if not self.town:
            def notTown(part):
                if part in (u'g.', u'pr.', u'sen.', u'skg.', u'mstl.') or \
                        part.endswith(u'ų') or part.endswith(u'u') or \
                        part.endswith(u'io') or part.endswith(u'os') or \
                        part.endswith(u'o') or part.endswith(u'os') or \
                        part.endswith(u'ies') or \
                        part.endswith(u'ės'):
                    return True
                return False

            for part in reversed(parts):
                if notTown(part):
                    if parts[0].isalpha() and parts[0].istitle() and \
                            not notTown(parts[0]):
                        self.town = parts[0]
                    break
                if part.isalpha():
                    if part.endswith(u'e'):
                        raise ConversionError(u'Nepavyko atpažinti miesto!')

                    if part.istitle():
                        self.town = part
                    break
            if not self.town:
                raise ConversionError(u'Nepavyko atpažinti miesto!')

        if self.town == u'A':
            raise Exception(u'STOP!')

        for i in range(4):
            text = text.replace(u'  ', u' ').replace(u' ,', u',')
        self.value = text
