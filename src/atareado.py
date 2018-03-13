#!/usr/bin/python

import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import atframe
import serialconnection
from serial.tools.list_ports import comports
import form

class ATareado(form.MainFrame):


    def __init__(self, parent):
        form.MainFrame.__init__(self, parent)
        self.__serialPort = serialconnection.SerialConnection()
        self.__serialPort.receivedData = self.rxDataCallback
        self.__serialPort.receivedAnswer = self.rxAnswerCallback
        self.__cmdSent = None
        pub.subscribe(self.AppendLogText, "AppendLogText")
        pub.subscribe(self.SetStatusText, "SetStatusText")

    def start(self):
        serialPorts = serialconnection.getPortsList()
        self.port_combo.Clear()
        self.port_combo.AppendItems(serialPorts)
        self.setConnectionStatus(False)

    def setConnectionStatus(self, status):
        if status:
            wx.CallAfter(pub.sendMessage, "SetStatusText", text="Connected")
        else:
            wx.CallAfter(pub.sendMessage, "SetStatusText", text="Disconnected")

    def conn_button_onclick(self, event):
        #self.log_text.AppendText('Conn %s %s '% (self.port_combo.GetValue(), self.m_comboBox2.GetValue()))
        status = self.__serialPort.start(self.port_combo.GetValue(), self.m_comboBox2.GetValue())
        self.setConnectionStatus(status)

    def info_button_onclick(self, event):
        if self.__serialPort.status:
            self.log_text.AppendText("Modem Info: \n")
            cmd = serialconnection.ATcommand(serialconnection.ATI_CMD_ID, True, None)
            self.__serialPort.sendCommand(cmd)
        else:
            self.log_text.AppendText("Serial connection closed\n")

    def status_button_onclick(self, event):
        if self.__serialPort.status:
            self.log_text.AppendText("Modem Status:")
        else:
            self.log_text.AppendText("Serial connection closed\n")

    def rxDataCallback(self, data):
        self.log_text.AppendText('\n')
        self.log_text.AppendText(data)

    def rxAnswerCallback(self, answer):

        if answer[0]:
            text = "Answer:"
            for t in answer[1]:
                text += t
        else:
            text = "Error:"+answer[1]

        wx.CallAfter(pub.sendMessage, "AppendLogText", text=text)

    def AppendLogText(self, text):
        self.log_text.AppendText(text)

    def SetStatusText(self, text):
        self.m_staticText1.SetLabel(text)


if __name__ == "__main__":
    app = wx.App(False)

    atareado = ATareado(None)
    atareado.start()
    atareado.Show()

    app.MainLoop()
