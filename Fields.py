#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime

from Exceptions import ValidationError

LETTERS_LT_SMALL = u'ąčęėįšųūqwertyuiopasdfghjklzxcvbnm'
LETTERS_LT_BIG   = u'ĄČĘĖĮŠŲŪQWERTYUIOPASDFGHJKLZXCVBNM'
SPACE = u' '

class NumberField(object):
    """Text field, were all elements are numbers.
    """
    
    def __init__(self, text, minlen=0, maxlen=0, validate=False):
        """Constructor.
        @param text - input text;
        @param minlen - minum length of number in digits, 0 - means any;
        @param maxlen - maximum length of number in digits, 0 - means any;
        @param validate - if validate in constructor.
        """

        self.text = text
        self.minlen = minlen
        self.maxlen = maxlen

        if validate:
            self.validate()
    
    def validate(self):
        """Validates if text is correct number.
        """

        try:
            self.value = [int(i) for i in self.text]
        except ValueError, e:
            raise ValidationError(u'Turi būti vien skaitmenys!')

        if (len(self.value) < self.minlen):
            raise ValidationError(
                    u'Turi būti ne mažiau nei %s '%(self.minlen) +
                    u'skaitmenys! (Yra %s.)'%(len(self.value)))

        if (self.maxlen != 0):
            if (len(self.value) > self.maxlen):
                raise ValidationError(
                        u'Turi būti ne daugiau nei %s '%(self.minlen) +
                        u'skaitmenys! (Yra %s.)'%(len(self.value)))

class IntegerField(object):
    r"""Text field, representing integer.

    >>> #import interlude
    >>> #interlude.interact(locals())

    >>> n = IntegerField('a', validate=True)
    Traceback (most recent call last):
    ...
    ValidationError: u'Turi b\u016bti sveikasis skai\u010dius!'
    >>> n = IntegerField('-1000000000', validate=True)
    >>> n.value
    -1000000000
    >>> n = IntegerField('30000000', validate=True)
    >>> n.value
    30000000
    >>> n = IntegerField('30000000e3', validate=True)
    Traceback (most recent call last):
    ...
    ValidationError: u'Turi b\u016bti sveikasis skai\u010dius!'
    >>> n = IntegerField('3.14', validate=True)
    Traceback (most recent call last):
    ...
    ValidationError: u'Turi b\u016bti sveikasis skai\u010dius!'
    >>> n = IntegerField('0', min=6, max=12, 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Skai\u010dius turi b\u016bti ne ma\u017eesnis nei 6!
    (Yra 0.)'
    >>> n = IntegerField('6', min=6, max=12, validate=True)
    >>> n.value
    6
    >>> n = IntegerField('12', min=6, max=12, validate=True)
    >>> n.value
    12
    >>> n = IntegerField('13', min=6, max=12, 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Skai\u010dius turi b\u016bti ne didesnis nei 12! 
    (Yra 13.)'
    >>> 

    """
    
    def __init__(self, text, min=None, max=None, validate=False):
        """Constructor.
        @param text - input text;
        @param minlen - minum length of number in digits, 0 - means any;
        @param maxlen - maximum length of number in digits, 0 - means any;
        @param validate - if validate in constructor.
        """

        self.text = text
        self.min = min
        self.max = max

        if validate:
            self.validate()
    
    def validate(self):
        """Validates if text is correct number.
        """

        try:
            self.value = int(self.text)
        except ValueError, e:
            raise ValidationError(u'Turi būti sveikasis skaičius!')

        if self.min != None:
            if self.value < self.min:
                raise ValidationError( 
                        u'Skaičius turi būti ne mažesnis nei '+
                        u'%s! (Yra %s.)'%(self.min, self.value))

        if self.max != None:
            if self.value > self.max:
                raise ValidationError(
                        u'Skaičius turi būti ne didesnis nei '+
                        u'%s! (Yra %s.)'%(self.max, self.value))

class NamesField(object):
    r"""Text field, which contains one or more names. (Words, whose first
    letter is capital and rest are small, separated by one spaces.)

    >>> n = NamesField(u'vytautas', validate=True)
    >>> n.value
    u'Vytautas'
    >>> n = NamesField(u' vytautas  ', validate=True)
    >>> n.value
    u'Vytautas'
    >>> n = NamesField(u' vytautas \t\n', validate=True)
    >>> n.value
    u'Vytautas'
    >>> n = NamesField(u' vyTaUtas \t\n', validate=True)
    >>> n.value
    u'Vytautas'
    >>> n = NamesField(u' vytautas \ta', 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Turi b\u016bti ne daugiau nei 1 vardai. 
    (Yra \u2013 2.)'
    >>> n = NamesField(u' vyTaU3tas \t\n', 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Vardas turi b\u016bti sudarytas tik i\u0161 
    raid\u017ei\u0173!'
    >>> n = NamesField(u'', 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Turi b\u016bti ne ma\u017eiau nei 
    1 vardai. (Yra \u2013 0.)'
    >>> n = NamesField(u'vytautas', minnum=1, maxnum=2, validate=True)
    >>> n.value
    u'Vytautas'
    >>> n = NamesField(u'vytautas dainius', minnum=1, maxnum=2,\
    ... validate=True)
    >>> n.value
    u'Vytautas Dainius'
    >>> n = NamesField(u'vytautas\t\ndainius', minnum=1, maxnum=2,\
    ... validate=True)
    >>> n.value
    u'Vytautas Dainius'
    >>> n = NamesField(u'vytautas\t\nk\u0118stutis', minnum=1, maxnum=2,\
    ... validate=True)
    >>> n.value
    u'Vytautas K\u0119stutis'
    """
    
    def __init__(self, text, minnum=1, maxnum=1, validate=False):
        """Constructor.
        @param text - input text;
        @param number - number of names;
        @param validate - if validate in constructor;
        """

        self.text = text
        self.minnum = minnum
        self.maxnum = maxnum

        if validate:
            self.validate()

    def validate(self):
        """Validates if field text is correct.
        """

        words = self.text.split()
        if len(words) < self.minnum:
            raise ValidationError(
                    u'Turi būti ne mažiau nei %s vardai. '%(self.minnum) +
                    u'(Yra – %s.)'%(len(words)))
        if len(words) > self.maxnum:
            raise ValidationError(
                    u'Turi būti ne daugiau nei %s vardai. '%(self.maxnum) +
                    u'(Yra – %s.)'%(len(words)))

        cwords = []
        for word in words:
            if not word.isalpha():
                for i in word.split(u'-'):
                    if not i.isalpha():
                        raise ValidationError( 
                                u'Vardas turi būti sudarytas tik '\
                                        u'iš raidžių!')
            cwords.append(word.title())

        self.value = u' '.join(cwords)

class EmailField(object):
    r"""Text field, for valid email.
    
    >>> e = EmailField('vakaras.l@gmail.com', True)
    >>> e = EmailField('vakaras.l@yahoo.co.uk', True)
    >>> e = EmailField('vakaras.l@nmakademija.lt', True)
    >>> e = EmailField('vakaras.l@port_nmakademija.lt',
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Neteisingas elektroninio 
    pa\u0161to adresas!'
    >>> e = EmailField('vakaras.l_grybas@po32rt.nmakademija.lt', True)
    >>> e = EmailField('vakaras.l_gryb.as@po32rt.nmakademija.lt', True)
    >>> e = EmailField('vakaras.l_gryb.!as@po32rt.nmakademija.lt', 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Neteisingas elektroninio 
    pa\u0161to adresas!'
    >>> e = EmailField(' vakaras.l_gryb.as@po32rt.nmakademija.lt', 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Neteisingas elektroninio 
    pa\u0161to adresas!'
    >>> e = EmailField('vakaras.l_gryb.as@po32rt.nmakademija.lt ', 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Neteisingas elektroninio 
    pa\u0161to adresas!'
    >>> e = EmailField('vakaras.l_gryb.as^po32rt.nmakademija.lt',
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Neteisingas elektroninio 
    pa\u0161to adresas!'

    """

    def __init__(self, text, validate=False):
        """Construcotr.
        @param text - input text;
        @param validate - if validate in constructor.
        """

        self.text = text

        if validate:
            self.validate()
    
    def validate(self):
        """Validates if text is correct email address.
        """

        email_regex = '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'
        
        if not re.match(email_regex, self.text, re.IGNORECASE):
            raise ValidationError(
                    u'Neteisingas elektroninio pašto adresas!')
        else:
            self.value = self.text

class PhoneNumberField(NumberField):
    r"""Text field for valid phone number.

    >>> from Fields import PhoneNumberField
    >>> p = PhoneNumberField('+37062340866', True)
    >>> p.value
    u'+37062340866'
    >>> p = PhoneNumberField('+370623408', 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Mobiliojo telefono numeris turi 
    tur\u0117ti 11 skaitmen\u0173!'
    >>> p = PhoneNumberField('37062340866', True)
    >>> p.value
    u'37062340866'
    >>> p = PhoneNumberField('862340866', True)
    >>> p.value
    u'+37062340866'
 
    """
    
    
    def __init__(self, text, validate=False):
        """Constructor.
        @param text - input text;
        @param validate - if validate in constructor.
        """
        
        for i in u' *()-~':
            text = text.replace(i, u'')
        self.text = text

        if len(self.text) and self.text[0] == u'+':
            super(PhoneNumberField, self).__init__(self.text[1:])
            self.international = True
        else:
            super(PhoneNumberField, self).__init__(self.text)
            self.international = False

        if validate:
            self.validate()

    def validate(self):
        """Validates if text is correct phone number.
        """

        super(PhoneNumberField, self).validate()

        if self.international:
            if len(self.value) != 11:
                raise ValidationError(
                        u'Mobiliojo telefono numeris turi turėti ' +
                        u'11 skaitmenų!')
            else:
                self.value = u'+' + u''.join(
                        [unicode(i) for i in self.value])
        else:
            if len(self.value) == 9 and self.value[0] == 8:    
                # Mobile phone number.
                self.value = u'+370' + u''.join(
                        [unicode(i) for i in self.value[1:]])
            else:
                self.value = u''.join(
                        [unicode(i) for i in self.value])

class DateField(object):
    r"""Text field for valid date.

    FIXME: Update doctest!

    >>> #import interlude
    >>> #interlude.interact(locals())

    >>> a = DateField(u'2010-02-03', u'1990-01-01', u'2000-01-01', 
    ... validate=False)
    >>> a.min
    datetime.datetime(1990, 1, 1, 0, 0)
    >>> a.max
    datetime.datetime(2000, 1, 1, 0, 0)
    >>> a.text
    u'2010-02-03'
    >>> a.format
    u'%Y-%m-%d'
    >>> a.validate()    #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Per\u017eengti r\u0117\u017eiai! Data 2010-02-03 
    n\u0117ra tarp [1990-01-01;2000-01-01].'
    >>> a = DateField(u'2010-02-03', u'1990-01-01', u'2000-01-01', 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Per\u017eengti r\u0117\u017eiai! Data 2010-02-03 
    n\u0117ra tarp [1990-01-01;2000-01-01].'
    >>> a = DateField(u'1996-02-3', u'1990-01-01', u'2000-01-01', 
    ... validate=True)
    >>> a.value
    '1996-02-03'
    >>> a = DateField(u'1996-02-03', u'1990-01-01', u'2000-01-01', 
    ... validate=True)
    >>> a.value
    '1996-02-03'

    """
    
    def __init__(self, text, min=None, max=None, 
            formats=(u'%Y-%m-%d',),
            validate=False):
        """Constructor.
        @param text - input text;
        @param min - minimum possible date (unicode or datetime);
        @param max - maximum possible date (unicode or datetime);
        @param formats - possible formats (in tryed order) in which date
            could be written;
        @param validate - if validate in constructor.
        """

        self.text = text
        self.formats = formats
        if type(min) == unicode or type(min) == str:
            #self.min = datetime.datetime.strptime(min, self.format)
            self.min = self.convert(min)
        else:
            self.min = min
        if type(max) == unicode or type(max) == str:
            #self.max = datetime.datetime.strptime(max, self.format)
            self.max = self.convert(max)
        else:
            self.max = max

        if validate:
            self.validate()

    def convert(self, text):
        """Converts text to datetime. If fails, raises ValidationError.
        @param text - input text;
        @returns datetime object.
        """

        date = None

        for format in self.formats:
            try:
                date = datetime.datetime.strptime(text, format)
            except ValueError, e:
                pass
            else:
                break

        if not date:
            raise ValidationError(u'Data neatitiko nei vieno iš formatų!')
        else:
            return date
    
    def validate(self):
        """Validates if text is correct date.
        """

        self.date = self.convert(self.text)

        if not self.min is None:
            if self.date < self.min:
                raise ValidationError(
                        u'Peržengti rėžiai! Data %s nėra tarp [%s;%s].'%(
                            self.date.strftime(self.formats[0]),
                            self.min.strftime(self.formats[0]),
                            self.max.strftime(self.formats[0])))
        if not self.max is None:
            if self.max < self.date:
                raise ValidationError(
                        u'Peržengti rėžiai! Data %s nėra tarp [%s;%s].'%(
                            self.date.strftime(self.formats[0]),
                            self.min.strftime(self.formats[0]),
                            self.max.strftime(self.formats[0])))
        self.value = self.date.strftime(self.formats[0])

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("UTF-8")
    import doctest
    doctest.testmod()
