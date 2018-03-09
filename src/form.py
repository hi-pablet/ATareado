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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 661,551 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( -1, -1)

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		bSizer6.SetMinSize( wx.Size( 300,-1 ) )
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, u"solapas" )
		self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"Commands" )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_button5 = wx.Button( self.m_panel1, wx.ID_ANY, u"Device Info", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button5, 0, wx.ALL, 5 )

		self.m_button6 = wx.Button( self.m_panel1, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button6, 0, wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Run script", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer4.Add( self.m_staticText3, 0, wx.ALL, 5 )

		m_comboBox3Choices = []
		self.m_comboBox3 = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"Select script...", wx.DefaultPosition, wx.DefaultSize, m_comboBox3Choices, 0 )
		self.m_comboBox3.SetMinSize( wx.Size( 160,-1 ) )

		bSizer4.Add( self.m_comboBox3, 0, wx.ALL, 5 )

		self.run_script_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.run_script_button, 0, wx.ALL, 5 )


		self.m_panel1.SetSizer( bSizer4 )
		self.m_panel1.Layout()
		bSizer4.Fit( self.m_panel1 )
		self.m_notebook1.AddPage( self.m_panel1, u"General", False )
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText4 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Direct commands", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer5.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_textCtrl4 = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl4.SetMinSize( wx.Size( 160,-1 ) )

		bSizer5.Add( self.m_textCtrl4, 0, wx.ALL, 5 )

		self.send_cmd_button = wx.Button( self.m_panel2, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.send_cmd_button, 0, wx.ALL, 5 )


		self.m_panel2.SetSizer( bSizer5 )
		self.m_panel2.Layout()
		bSizer5.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"TCP/UDP", True )

		bSizer6.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


		fgSizer3.Add( bSizer6, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.log_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,400 ), wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer7.Add( self.log_text, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT, 5 )

		self.clear_button = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.clear_button, 0, wx.ALL, 5 )


		fgSizer3.Add( bSizer7, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )


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
		self.m_textCtrl3.SetMinSize( wx.Size( 120,-1 ) )

		fgSizer4.Add( self.m_textCtrl3, 0, wx.ALL, 5 )


		bSizer1.Add( fgSizer4, 0, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.conn_button.Bind( wx.EVT_BUTTON, self.conn_button_onclick )
		self.m_button5.Bind( wx.EVT_BUTTON, self.info_button_onclick )
		self.m_button6.Bind( wx.EVT_BUTTON, self.status_button_onclick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def conn_button_onclick( self, event ):
		event.Skip()

	def info_button_onclick( self, event ):
		event.Skip()

	def status_button_onclick( self, event ):
		event.Skip()
