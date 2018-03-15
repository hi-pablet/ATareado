#!/usr/bin/python
import sys
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import form
import serialconnection
import atcmds
from atcmds import ATcommand
from serial.tools.list_ports import comports
from localsocket import LocalSocket
import scriptsreader

SCRIPTS_PATH = './scripts/'
LOCAL_PORT = 5001


class ATareado(form.MainFrame):


    def __init__(self, parent):
        form.MainFrame.__init__(self, parent)
        self.__serialPort = serialconnection.SerialConnection()
        self.__serialPort.receivedData = self.rxDataCallback
        self.__serialPort.receivedAnswer = self.rxAnswerCallback
        self.__cmdSent = None
        self.__localSocket = LocalSocket()
        self.__localSocket.connOpenCallback = self.localSocketConnectionOpen
        self.__localSocket.dataReadCallback = self.localSocketDataRead
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
        self.__localSocket.stop()
        self.Destroy()

    def setConnectionStatus(self, status):
        if status:
            wx.CallAfter(pub.sendMessage, "SetStatusText", text="Connected")
        else:
            wx.CallAfter(pub.sendMessage, "SetStatusText", text="Disconnected")

    def localSocketConnectionOpen(self):
        print "Local port conn open"

    def localSocketDataRead(self,data):
        print 'Socket data rx'

    def conn_button_onclick(self, event):
        #self.log_text.AppendText('Conn %s %s '% (self.port_combo.GetValue(), self.m_comboBox2.GetValue()))
        if not self.__serialPort.status:
            status = self.__serialPort.start(self.port_combo.GetValue(), self.m_comboBox2.GetValue())
            self.setConnectionStatus(status)

    def info_buttonOnButtonClick(self, event):
        if self.__serialPort.status:
            cmd = ATcommand(atcmds.ATI_CMD_ID, True, None)
            self.__serialPort.sendCommand(cmd)
        else:
            self.log_text.AppendText("\nSerial connection closed")

    def status_buttonOnButtonClick(self, event):
        if self.__serialPort.status:

            cmd = ATcommand(atcmds.CPIN_CMD_ID, False, None)
            self.__serialPort.sendCommand(cmd)
            cmd = ATcommand(atcmds.CSQ_CMD_ID, True, None)
            self.__serialPort.sendCommand(cmd)
            cmd = ATcommand(atcmds.CGATT_CMD_ID, False, None)
            self.__serialPort.sendCommand(cmd)
        else:
            self.log_text.AppendText("\nSerial connection closed")

    def run_script_buttonOnButtonClick(self, event):
        if self.__serialPort.status:
            self.runScript(self.m_comboBox3.GetValue())

    def clear_buttonOnButtonClick(self,event):
        self.log_text.SetValue("")

    def send_direct_buttonOnButtonClick(self, event):
        if self.__serialPort.status:
            data = self.direct_cmd_text.GetValue()
            self.__serialPort.writeRaw(data+'\r\n')

    def start_localport_buttonOnButtonClick(self, event):
        self.__localSocket.start(LOCAL_PORT)

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

        if answer.ok:
            text = '\n'+answer.cmdId+' '+atcmds.commandsList[answer.cmdId][3] + ':\n'
            if len(answer.params) > 0:
                for t in answer.params:
                    text += t+', '
            else:
                text += ' OK'
        else:
            text = "\nError: "
            for t in answer.params:
                text += t+' '

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
