#!/usr/bin/python

import wx
import atframe
import serialconnection
from serial.tools.list_ports import comports
import form

class ATareado(form.MainFrame):


    def __init__(self, parent):
        form.MainFrame.__init__(self, parent)
        self.__serialconn = serialconnection.SerialConnection()
        self.__serialconn.receivedData = rxDataCallback
        self.__cmdSent = None

    def start(self):
        serialPorts = serialconnection.getPortsList()
        self.port_combo.Clear()
        self.port_combo.AppendItems(serialPorts)


    def setConnectionStatus(self, status):
        if status:
            self.m_staticText1.SetLabel("Connected")
        else:
            self.m_staticText1.SetLabel("Disconnected")

    def conn_button_onclick(self, event):
        self.log_text.AppendText('Conn %s %s '% (self.port_combo.GetValue(), self.m_comboBox2.GetValue()))
        status = self.__serialconn.start(self.port_combo.GetValue(), self.m_comboBox2.GetValue())
        self.setConnectionStatus(status)

    def info_button_onclick(self, event):
        self.log_text.AppendText("Modem Info:")

    def status_button_onclick(self, event):
        self.log_text.AppendText("Modem Status:")
        pass

    def rxDataCallback(self, data):



if __name__ == "__main__":
    app = wx.App(False)

    atareado = ATareado(None)
    atareado.start()
    atareado.Show()

    app.MainLoop()
