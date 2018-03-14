#!/usr/bin/python
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import form
import serialconnection
import atcmds
from atcmds import ATcommand
from serial.tools.list_ports import comports
import scriptsreader

SCRIPTS_PATH = './scripts/'


class ATareado(form.MainFrame):


    def __init__(self, parent):
        form.MainFrame.__init__(self, parent)
        self.__serialPort = serialconnection.SerialConnection()
        self.__serialPort.receivedData = self.rxDataCallback
        self.__serialPort.receivedAnswer = self.rxAnswerCallback
        self.__cmdSent = None
        pub.subscribe(self.AppendLogText, "AppendLogText")
        pub.subscribe(self.SetStatusText, "SetStatusText")
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def initialize(self):
        serialPorts = serialconnection.getPortsList()
        self.port_combo.Clear()
        self.port_combo.AppendItems(serialPorts)
        self.setConnectionStatus(False)
        scripts = scriptsreader.loadAllScripts(SCRIPTS_PATH)
        self.m_comboBox3.Clear()
        self.m_comboBox3.AppendItems(scripts)

    def OnClose(self, event):
        self.__serialPort.stop()
        self.Destroy()

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
            self.log_text.AppendText("\nModem Info:")
            cmd = ATcommand(atcmds.ATI_CMD_ID, True, None)
            self.__serialPort.sendCommand(cmd)
        else:
            self.log_text.AppendText("\nSerial connection closed")

    def status_button_onclick(self, event):
        if self.__serialPort.status:
            self.log_text.AppendText("\nSignal Quality:")

            cmd = ATcommand(atcmds.CPIN_CMD_ID, False, None)
            self.__serialPort.sendCommand(cmd)
            cmd = ATcommand(atcmds.CSQ_CMD_ID, False, None)
            self.__serialPort.sendCommand(cmd)
            #cmd = ATcommand(atcmds.CGATT_CMD_ID, False, None)
            #self.__serialPort.sendCommand(cmd)
        else:
            self.log_text.AppendText("\nSerial connection closed")

    def script_button_onclick(self, event):
        print self.m_comboBox3.GetValue()
        self.runScript(self.m_comboBox3.GetValue())

    def runScript(self, name):
        if name in scriptsreader.scriptsList:
            script = scriptsreader.scriptsList[name]
            for cmd in script:
                self.__serialPort.sendCommand(cmd)


    def rxDataCallback(self, data):
        self.log_text.AppendText('\n')
        try:
            self.log_text.AppendText(data)
        except Exception as e:
            print >> sys.stdout, "Exception writing to log_text %s" % e

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
    atareado.initialize()
    atareado.Show()

    app.MainLoop()
