#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# http://wiki.services.openoffice.org/wiki/Playing_with_Window_Toolkit_AWT
'''
from com.sun.star.awt import Rectangle
from com.sun.star.awt import WindowDescriptor
 
from com.sun.star.awt.WindowClass import MODALTOP
#import com.sun.star.awt.VclWindowPeerAttribute as AttrConst
from com.sun.star.awt.VclWindowPeerAttribute import OK, OK_CANCEL, \
        YES_NO, YES_NO_CANCEL, RETRY_CANCEL, DEF_OK, DEF_CANCEL, \
        DEF_RETRY, DEF_YES, DEF_NO

OK, OK_CANCEL, YES_NO, YES_NO_CANCEL, \
RETRY_CANCEL, DEF_OK, DEF_CANCEL, DEF_RETRY, DEF_YES, DEF_NO
'''
 
'''
def MessageBox(ParentWin, MsgText, MsgTitle, MsgType="messbox", 
        MsgButtons=AttrConst.OK):
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

def DocMessageBox(MsgText, MsgTitle, MsgType, MsgButtons=AttrConst.OK):
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
    a = 0
    #return DocMessageBox(MsgText, MsgTitle, 'errorbox')

def InfoBox(MsgText, MsgTitle=u'Informacija.'):
    """Shows info message.
    @param MsgText - message text.
    @param MsgTitle - message title.
    """
    return DocMessageBox(MsgText, MsgTitle, 'infobox')
    

def change(event):
    """Bla
    """
    return "labas"
'''
 
# Logger for debugging.
def add(str, clear=False):
    """Add debugging string to file "$HOME/tmp.txt".
    @param str - string to add;
    @param clear - clear file, before add?
    """
    home = os.getenv("HOME")
    if clear:
        os.system('echo "%s" > "%s/tmp.txt"'%(str, home))
    else:
        os.system('echo "%s" >> "%s/tmp.txt"'%(str, home))
