# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Mar  3 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 647,547 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( -1,-1)
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6.SetMinSize( wx.Size( 300,-1 ) ) 
		self.devInfo_button = wx.Button( self, wx.ID_ANY, u"Device Info", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.devInfo_button, 0, wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button7, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.log_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,400 ), 0 )
		bSizer7.Add( self.log_text, 0, wx.ALL, 5 )
		
		self.clear_button = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.clear_button, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( fgSizer3, 1, wx.ALIGN_TOP|wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 5, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer4.SetMinSize( wx.Size( -1,60 ) ) 
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Connection", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer4.Add( self.m_staticText1, 0, wx.ALL, 10 )
		
		m_comboBox2Choices = [ u"115200", u"57600", u"38400", u"19200", u"14400", u"9600" ]
		self.m_comboBox2 = wx.ComboBox( self, wx.ID_ANY, u"Baudrate", wx.DefaultPosition, wx.Size( 120,-1 ), m_comboBox2Choices, 0 )
		fgSizer4.Add( self.m_comboBox2, 0, wx.ALL, 5 )
		
		port_comboChoices = [ u"COM1", u"COM2", u"COM3", u"COM4", u"COM5", u"COM6", u"COM7", u"COM8", u"COM9", u"COM10", u"COM11", u"COM12", u"COM13", u"COM14", u"COM15", u"COM16", u"COM17", u"COM18", u"COM19", u"COM20" ]
		self.port_combo = wx.ComboBox( self, wx.ID_ANY, u"Select port", wx.DefaultPosition, wx.DefaultSize, port_comboChoices, 0 )
		fgSizer4.Add( self.port_combo, 0, wx.ALL, 5 )
		
		self.conn_button = wx.Button( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.conn_button, 0, wx.ALL, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_textCtrl3, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( fgSizer4, 0, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.conn_button.Bind( wx.EVT_BUTTON, self.conn_button_onclick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def conn_button_onclick( self, event ):
		event.Skip()
	

