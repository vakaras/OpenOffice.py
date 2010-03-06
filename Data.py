#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Exceptions import ValidationError
from Fields import NumberField

class IdentityCode(NumberField):
    r"""Class for manipulation with identity code.
    @member value
    @member gender
    @member year
    @member month
    @member day
    @member birth_date

    >>> ic = IdentityCode("1", 
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Turi b\u016bti ne ma\u017eiau nei 11 
    skaitmenys! (Yra 1.)'

    >>> ic = IdentityCode("1a", True)
    Traceback (most recent call last):
    ...
    ValidationError: u'Turi b\u016bti vien skaitmenys!'

    >>> ic = IdentityCode("39007281132",
    ... validate=True)  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValidationError: u'Neteisingas asmens kodas!\nKontrolinis 
    skaitmuo yra 2, buvo apskai\u010diuotas 1 pagal 1 atvej\u012f.'

    >>> ic = IdentityCode("79007281135", True)
    Traceback (most recent call last):
    ...
    ValidationError: u'Ne\u017einoma lytis: 7'

    >>> ic = IdentityCode("49007281132", True)
    >>> ic.value
    [4, 9, 0, 0, 7, 2, 8, 1, 1, 3, 2]
    >>> ic.gender
    u'Moteris'
    >>> ic.year
    '1990'
    >>> ic.month
    '07'
    >>> ic.day
    '28'
    >>> ic.birth_date
    '1990-07-28'

    """
    
    def __init__(self, code, validate=False):
        """Constructor.
        @param code - string representing identity code;
        @param validate - if validate in constructor.
        """
        
        super(IdentityCode, self).__init__(code, 11, 11)
        #NumberField.__init__(code, 11, 11)

        if validate:
            self.validate()
        '''
        try:
            self.numbers = [int(i) for i in code]
        except ValueError, e:
            raise ValidationError(
                    u'Asmens kodas turi būti vien iš skaitmenų!')

        if (len(numbers) != 11):
            raise ValidationError(
                    u'Asmens kodas privalo turėti 11 skaitmenų!')
        '''

    def validate(self):
        """Validates if code is correct identity code.
        """
        super(IdentityCode, self).validate()

        g, y1, y2, m1, m2, d1, d2, x1, x2, x3, k = self.value

        sum1 = (g*1+y1*2+y2*3+m1*4+m2*5+d1*6+d2*7+x1*8+x2*9+x3*1)%11
        sum2 = (g*3+y1*4+y2*5+m1*6+m2*7+d1*8+d2*9+x1*1+x2*2+x3*3)%11
        sum3 = 0
        if sum1 != 10:
            sum = [sum1, 1]
        elif sum2 != 10:
            sum = [sum2, 2]
        else:
            sum = [sum3, 3]

        if k != sum[0]:
            raise ValidationError(
                    u'Neteisingas asmens kodas!\n' + 
                    u'Kontrolinis skaitmuo yra %s, buvo apskaičiuotas '%k +
                    u'%s pagal %s atvejį.'%(sum[0], sum[1]))

        if g in (1, 3, 5):
            self.gender = u'Vyras'
        elif g in (2, 4, 6):
            self.gender = u'Moteris'
        else:
            raise ValidationError(u'Nežinoma lytis: %s'%(g))

        if g in (1, 2):
            self.year = '18'
        elif g in (3, 4):
            self.year = '19'
        else:
            self.year = '20'
        self.year = '%s%s%s'%(self.year, y1, y2)
        self.month = '%s%s'%(m1, m2)
        self.day = '%s%s'%(d1, d2)
        self.birth_date = '%s-%s-%s'%(self.year, self.month, self.day)


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("UTF-8")
    import doctest
    doctest.testmod()
