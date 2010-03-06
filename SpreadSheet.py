#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Exceptions import ValidationError

class Column(list):
    """Object representing one table column.
    """
    caption = u''

    def __init__(self, caption, *args, **kwargs):
        """Constructor.
        """
        self.caption = caption
        super(Column, self).__init__(*args, **kwargs)

class Document(object):
    """Object representing spreadsheet document.
    """

    def __init__(self):
        """Constructor.
        """
        self.width = 0
        self.height = 0
        self.order = []         # Columns order.
        self.data = {}          # Data dictionary.

    def addColumn(self, caption, rows):
        """Adds column.
        @param caption - new column caption.
        @param rows - data.
        """

        if self.width:
            if self.height != len(rows):
                raise Exception(
                        u'Rows numbers mismatch: document has '+
                        u'%s and given column %s rows.'%(
                            self.height, len(rows)))
        
        if (caption in self.data.keys()):
            raise NameError(u'Column with caption "%s" already exists'%(
                caption))
        self.order.append(caption)
        self.data[caption] = Column(caption, rows)
        self.width += 1

    def addRow(self, row):
        """Adds row data to table. Rows elements are interpreted as defined
        in order attribute.
        @param row - iterable containing needed elements.
        """
        if self.width != len(row):
            raise Exception(
                    u'Row elements (%s) and document columns (%s) '%(
                    len(row), self.width) + u'number mismatch!')
        for key, value in zip(self.order, row):
            self.data[key].append(value)
        self.height += 1

    def getColumn(self, key):
        """Returns column with given key.
        @param key - can be one of these types:
            * int - the number of column, returns Column;
            * string - the caption of column, returns Column;
        """
        if type(key) == int:
            return self.data[self.order[key]]
        elif type(key) == str:
            return self.data[key]
        elif type(key) == unicode:
            return self.data[key]
        else:
            raise TypeError(
                    u'Key must be one of these types: '+
                    u'int, str, unicode')

    def __getitem__(self, key):
        """Returns item with given key.
        @param key - can be one of these types:
            * int - the number of column, returns Column;
            * string - the caption of column, returns Column;
            * tuple((int/string), int index) - returns element.
        """
        if type(key) == tuple:
            return self.getColumn(key[0])[key[1]]
        else:
            return self.getColumn(key)

class CSVDocument(Document):
    """Object representing CSV document.
    """
    
    def read(self, file, field_separator=';', text_separator='"'):
        """Reads document from CSV file.
        @param file - path to file;
        @param field_separator - 
        @param text_separator -
        """
        
        with open(file) as fp:
            for i, line in enumerate(fp):
                line = unicode(line.decode('utf-8'))
                try:
                    if i == 0:
                        for caption in line[:-1].split(field_separator):
                            self.addColumn(caption[1:-1], [])     
                            # FIXME: use text_separator
                    else:
                        row = []
                        for element in line[:-1].split(field_separator):
                            row.append(element[1:-1])
                        self.addRow(row)
                except Exception, e:
                    raise Exception(u'%s\nIn line %s'%(e, i))

    def generateLine(self, list, fs, ts):
        """Generates line.
        @param list - elements list;
        @param fs - field separator;
        @param ts - text separator;
        @returns unicode string representing result line.
        """
        se = [u'%s%s%s'%(ts, i, ts) for i in list]
        line = fs.join(se)
        return u'%s\n'%line

    def write(self, file, field_separator=';', text_separator='"'):
        """Writes document to CSV file.
        @param file - path to file;
        @param field_separator - 
        @param text_separator -
        """
        
        with open(file, "w") as fp:
            line = self.generateLine(self.order, field_separator, 
                    text_separator)
            fp.write(line.encode('utf-8'))
            for row in zip(*[self.data[i] for i in self.order]):
                line = self.generateLine(row, field_separator, 
                        text_separator)
                fp.write(line.encode('utf-8'))



if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("UTF-8")
    import doctest
    doctest.testmod()
