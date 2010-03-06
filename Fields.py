#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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
                raise ValidationError(
                        u'Vardas turi būti sudarytas tik iš raidžių!')
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
        
        self.text = text

        if len(self.text) and self.text[0] == u'+':
            super(PhoneNumberField, self).__init__(text[1:])
            self.international = True
        else:
            super(PhoneNumberField, self).__init__(text)
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


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("UTF-8")
    import doctest
    doctest.testmod()
