#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ln -s "`pwd`/DBForms.py" "$HOME/.openoffice.org/3/user/Scripts/python/"

from com.sun.star.awt import Rectangle
from com.sun.star.awt import WindowDescriptor

from com.sun.star.awt.WindowClass import MODALTOP
from com.sun.star.awt.VclWindowPeerAttribute import OK, OK_CANCEL, \
        YES_NO, YES_NO_CANCEL, RETRY_CANCEL, DEF_OK, DEF_CANCEL, \
        DEF_RETRY, DEF_YES, DEF_NO

def MessageBox(ParentWin, MsgText, MsgTitle, MsgType="messbox", 
        MsgButtons=OK):
    """Shows message box.
    @param ParentWin 
    @param MsgText
    @param MsgTitle
    @param MsgType
    @param MsgButtons
    @returns message box response
    """
 
    MsgType = MsgType.lower()
    
    #available msg types
    MsgTypes = ("messbox", "infobox", "errorbox", "warningbox", "querybox")
    
    if MsgType not in MsgTypes:
        MsgType = "messbox"

    
    #describe window properties.
    aDescriptor = WindowDescriptor()
    aDescriptor.Type = MODALTOP
    aDescriptor.WindowServiceName = MsgType
    aDescriptor.ParentIndex = -1
    aDescriptor.Parent = ParentWin
    #aDescriptor.Bounds = Rectangle()
    aDescriptor.WindowAttributes = MsgButtons
    
    tk = ParentWin.getToolkit()
    msgbox = tk.createWindow(aDescriptor)
    
    msgbox.setMessageText(MsgText)
    if MsgTitle :
        msgbox.setCaptionText(MsgTitle)
    
    return msgbox.execute()

def DocMessageBox(MsgText, MsgTitle, MsgType, MsgButtons=OK):
    """Shows message box for current document. Params same as for 
    MessageBox.
    """
    doc = XSCRIPTCONTEXT.getDocument()
    parentwin = doc.CurrentController.Frame.ContainerWindow
    return MessageBox(parentwin, MsgText, MsgTitle, MsgType, MsgButtons)

def ErrorBox(MsgText, MsgTitle=u'Klaida!'):
    """Shows error message.
    @param MsgText - message text.
    @param MsgTitle - message title.
    """
    return DocMessageBox(MsgText, MsgTitle, 'errorbox')

def InfoBox(MsgText, MsgTitle=u'Informacija.'):
    """Shows info message.
    @param MsgText - message text.
    @param MsgTitle - message title.
    """
    return DocMessageBox(MsgText, MsgTitle, 'infobox')

from Notify import add#, ErrorBox, InfoBox
#from Notify import change
from Fields import NamesField, PhoneNumberField, EmailField
from Data import IdentityCode
from Exceptions import ValidationError

import sys
import os
sys.path.append(os.getenv("PWD"))

def dealWithEnteredException(field, exception, type="text"):
    """Deals with exception which occurred on reacting to "Entered" type
    event.
    @param field - field, to which event belongs;
    @param exception - exception, which occurred;
    @param type - field type.
    """

    if type == "text":

        if field.getSelectedText() == field.Text:
            return

        ErrorBox(u'%s'%exception)

        selection = field.getSelection()
        selection.Min = 0
        selection.Max = len(field.Text)
        field.setSelection(selection)
        field.setFocus()
    else:
        raise Exception('Not implemented type: %s !'%(type))

def nameEntered(event):
    """
    """
    name_field = event.Source
    try:
        name = NamesField(name_field.Text, minnum=1, maxnum=2, 
                validate=True)
        #raise ValidationError('veikia?')
    except ValidationError, e:
        dealWithEnteredException(name_field, e, 'text')
        return
    if name_field.Text != name.value:
        name_field.Text = name.value

def surnameEntered(event):
    """
    """
    name_field = event.Source
    try:
        name = NamesField(name_field.Text, minnum=1, maxnum=1, 
                validate=True)
    except ValidationError, e:
        dealWithEnteredException(name_field, e, 'text')
        return
    if name_field.Text != name.value:
        name_field.Text = name.value

def identityCodeEntered(event):
    """
    """
    code = event.Source
    try:
        ic = IdentityCode(code.Text, True)
        #raise ValidationError('veikia?')
    except ValidationError, e:
        dealWithEnteredException(code, e, 'text')
        return

    form = event.Source.Model.Parent

    date = form.getByName("datgim_data")
    date.Text = "1900-01-01"    # FIXME: Kodėl be šito neveikia?
    date.Text = ic.birth_date

    gender = form.getByName("txtlytis")
    for i, value in enumerate(gender.ListSource):
        if value == ic.gender:
            gender.SelectedItems = (i, )
            break

def emailEntered(event):
    """
    """
    field = event.Source
    try:
        email = EmailField(field.Text, validate=True)
    except ValidationError, e:
        dealWithEnteredException(field, e, 'text')
        return
    if field.Text != email.value:
        field.Text = email.value

def phoneNumberEntered(event):
    """
    """
    field = event.Source
    try:
        number = PhoneNumberField(field.Text, validate=True)
        #raise ValidationError('veikia?')
    except ValidationError, e:
        dealWithEnteredException(field, e, 'text')
        return
    if field.Text != number.value:
        field.Text = number.value
