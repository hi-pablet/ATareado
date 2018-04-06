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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ATareado", pos = wx.DefaultPosition, size = wx.Size( 661,564 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints(  wx.Size( 731,564 ), wx.DefaultSize )
		#self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		bSizer6.SetMinSize( wx.Size( 300,-1 ) )
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, u"solapas" )
		self.m_notebook1.SetMinSize( wx.Size( 350,-1 ) )
		
		self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"Commands" )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.info_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Device Info", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.info_button, 0, wx.ALL, 5 )
		
		self.status_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.status_button, 0, wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Run script", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer4.Add( self.m_staticText3, 0, wx.ALL, 5 )

		m_comboBox3Choices = []
		self.m_comboBox3 = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"Select script...", wx.DefaultPosition, wx.DefaultSize, m_comboBox3Choices, 0 )
		self.m_comboBox3.SetMinSize( wx.Size( 160,-1 ) )

		bSizer4.Add( self.m_comboBox3, 0, wx.ALL, 5 )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.run_script_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.run_script_button, 0, wx.ALL, 5 )
		
		self.stop_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.stop_button, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		self.m_staticline3 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Direct command", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer4.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.direct_cmd_text = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.direct_cmd_text.SetMinSize( wx.Size( 230,-1 ) )
		
		bSizer4.Add( self.direct_cmd_text, 0, wx.ALL, 5 )
		
		self.send_direct_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.send_direct_button, 0, wx.ALL, 5 )
		
		
		self.m_panel1.SetSizer( bSizer4 )
		self.m_panel1.Layout()
		bSizer4.Fit( self.m_panel1 )
		self.m_notebook1.AddPage( self.m_panel1, u"Serial commands", False )
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText9 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"TCP/UDP bridge", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		fgSizer5.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		
		fgSizer5.AddSpacer( 0 )
		
		self.m_staticText10 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		fgSizer5.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		conntype_comboChoices = [ u"TCP", u"UDP" ]
		self.conntype_combo = wx.ComboBox( self.m_panel2, wx.ID_ANY, u"Select...", wx.DefaultPosition, wx.DefaultSize, conntype_comboChoices, 0 )
		self.conntype_combo.SetSelection( 0 )
		fgSizer5.Add( self.conntype_combo, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Local port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer5.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.localport_text = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"5001", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.localport_text, 0, wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Local UDP down port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		fgSizer5.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.local_down_port_text = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"5002", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.local_down_port_text, 0, wx.ALL, 5 )
		
		self.m_staticText71 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Remote port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		fgSizer5.Add( self.m_staticText71, 0, wx.ALL, 5 )
		
		self.remoteport_text = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"5001", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.remoteport_text, 0, wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Remote Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		fgSizer5.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.remoteaddress_text = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"18.220.184.30", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.remoteaddress_text, 0, wx.ALL, 5 )
		
		self.connect_remote_button = wx.Button( self.m_panel2, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.connect_remote_button, 0, wx.ALL, 5 )
		
		self.close_remote_conn_button = wx.Button( self.m_panel2, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.close_remote_conn_button, 0, wx.ALL, 5 )
		
		
		self.m_panel2.SetSizer( fgSizer5 )
		self.m_panel2.Layout()
		fgSizer5.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"Socket bridge", False )
		self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer41 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer41.SetFlexibleDirection( wx.BOTH )
		fgSizer41.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText12 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Throughput", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		fgSizer41.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.serialdata_txt = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer41.Add( self.serialdata_txt, 0, wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Duration", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		fgSizer41.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.serialdelay_txt = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer41.Add( self.serialdelay_txt, 0, wx.ALL, 5 )
		
		self.serialstart_btn = wx.Button( self.m_panel4, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer41.Add( self.serialstart_btn, 0, wx.ALL, 5 )
		
		self.serialstop_btn = wx.Button( self.m_panel4, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer41.Add( self.serialstop_btn, 0, wx.ALL, 5 )
		
		
		self.m_panel4.SetSizer( fgSizer41 )
		self.m_panel4.Layout()
		fgSizer41.Fit( self.m_panel4 )
		self.m_notebook1.AddPage( self.m_panel4, u"Serial tx", False )
		
		bSizer6.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		gSizer2.Add( bSizer6, 0, 0, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText411 = wx.StaticText( self, wx.ID_ANY, u"AT commands", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText411.Wrap( -1 )
		bSizer7.Add( self.m_staticText411, 0, wx.ALL, 5 )
		
		self.atcmd_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE|wx.TE_READONLY )
		self.atcmd_text.SetMinSize( wx.Size( 300,180 ) )
		
		bSizer7.Add( self.atcmd_text, 1, wx.EXPAND|wx.ALL, 5 )
		
		self.clear_button = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.clear_button, 0, wx.ALL, 5 )
		
		
		gSizer2.Add( bSizer7, 1, wx.EXPAND|wx.ALL, 5 )
		
		
		bSizer1.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"Log", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		bSizer5.Add( self.m_staticText41, 0, wx.ALL, 5 )
		
		self.log_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE|wx.TE_READONLY )
		self.log_text.SetMinSize( wx.Size( 610,80 ) )
		
		bSizer5.Add( self.log_text, 1, wx.ALL|wx.BOTTOM|wx.EXPAND|wx.RIGHT, 5 )
		
		
		bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 5, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		#fgSizer4.SetMinSize( wx.Size( -1,-1 ) )
		fgSizer4.AddSpacer(30)
		m_comboBox2Choices = [ u"4000000", u"3686400",u"3200000", u"921600", u"460800", u"230400", u"115200", u"57600", u"38400", u"19200", u"14400", u"9600" ]
		self.m_comboBox2 = wx.ComboBox( self, wx.ID_ANY, u"Baudrate", wx.DefaultPosition, wx.Size( 120,-1 ), m_comboBox2Choices, 0 )
		self.m_comboBox2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		fgSizer4.Add( self.m_comboBox2, 0, wx.ALL, 5 )

		port_comboChoices = [ u"COM1", u"COM2", u"COM3", u"COM4", u"COM5", u"COM6", u"COM7", u"COM8", u"COM9", u"COM10", u"COM11", u"COM12", u"COM13", u"COM14", u"COM15", u"COM16", u"COM17", u"COM18", u"COM19", u"COM20" ]
		self.port_combo = wx.ComboBox( self, wx.ID_ANY, u"Select port", wx.DefaultPosition, wx.Size( 120,-1 ), port_comboChoices, 0 )

		fgSizer4.Add( self.port_combo, 0, wx.ALL, 5 )

		self.conn_button = wx.Button( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.conn_button, 0, wx.ALL, 5 )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Disconnected", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer4.Add( self.m_staticText1, 0, wx.ALL, 10 )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer4.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer1.Add( fgSizer4, 0, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.info_button.Bind( wx.EVT_BUTTON, self.info_buttonOnButtonClick )
		self.status_button.Bind( wx.EVT_BUTTON, self.status_buttonOnButtonClick )
		self.run_script_button.Bind( wx.EVT_BUTTON, self.run_script_buttonOnButtonClick )
		self.stop_button.Bind( wx.EVT_BUTTON, self.stop_buttonOnButtonClick )
		self.direct_cmd_text.Bind( wx.EVT_TEXT_ENTER, self.direct_cmd_textOnTextEnter )
		self.send_direct_button.Bind( wx.EVT_BUTTON, self.send_direct_buttonOnButtonClick )
		self.connect_remote_button.Bind( wx.EVT_BUTTON, self.connect_remote_buttonOnButtonClick )
		self.close_remote_conn_button.Bind( wx.EVT_BUTTON, self.close_remote_conn_buttonOnButtonClick )
		self.serialstart_btn.Bind( wx.EVT_BUTTON, self.serialstart_btnOnButtonClick )
		self.serialstop_btn.Bind( wx.EVT_BUTTON, self.serialstop_btnOnButtonClick )
		self.clear_button.Bind( wx.EVT_BUTTON, self.clear_buttonOnButtonClick )
		self.conn_button.Bind( wx.EVT_BUTTON, self.conn_button_onclick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def info_buttonOnButtonClick( self, event ):
		event.Skip()
	
	def status_buttonOnButtonClick( self, event ):
		event.Skip()
	
	def run_script_buttonOnButtonClick( self, event ):
		event.Skip()
	
	def stop_buttonOnButtonClick( self, event ):
		event.Skip()
	
	def direct_cmd_textOnTextEnter( self, event ):
		event.Skip()
	
	def send_direct_buttonOnButtonClick( self, event ):
		event.Skip()
	
	def connect_remote_buttonOnButtonClick( self, event ):
		event.Skip()
	
	def close_remote_conn_buttonOnButtonClick( self, event ):
		event.Skip()
	
	def serialstart_btnOnButtonClick( self, event ):
		event.Skip()
	
	def serialstop_btnOnButtonClick( self, event ):
		event.Skip()
	
	def clear_buttonOnButtonClick( self, event ):
		event.Skip()
	
	def conn_button_onclick( self, event ):
		event.Skip()
	

