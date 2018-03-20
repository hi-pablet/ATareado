#!/usr/bin/python
import sys
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import form
import serialconnection
import threading
import atcmds
from atcmds import ATcommand
from serial.tools.list_ports import comports
from localsocket import LocalSocket
import scriptsreader
import Log
from Log import logger


SCRIPTS_PATH = './scripts/'
LOCAL_PORT = 5001


class ATareado(form.MainFrame):


    def __init__(self, parent):
        form.MainFrame.__init__(self, parent)
        self.__serialPort = serialconnection.SerialConnection()
        self.__serialPort.receivedData = self.rxDataCallback
        self.__serialPort.receivedAnswer = self.rxAnswerCallback
        self.__serialPort.rawData = self.rawDataCallback

        self.__localSocket = LocalSocket()
        self.__localSocket.connOpenCallback = self.localSocketConnectionOpen
        self.__localSocket.dataReadCallback = self.localSocketDataRead
        self.__localSocket.connClosedCallback = self.localSocketConnectionClosed
        self.__socketRedirection = False

        #self.__guiMutex = threading.Lock()

        pub.subscribe(self.AppendLogText, "AppendLogText")
        pub.subscribe(self.SetStatusText, "SetStatusText")
        pub.subscribe(self.AppendAtTrafficText, "AppendAtTrafficText")
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
        try:
            self.__serialPort.stop()
            self.__localSocket.stop()
            logger.stop()
        except:
            print "Error stoping ports"
        self.Destroy()

    def setConnectionStatus(self, status):
        #self.__guiMutex.acquire()
        if status:
            wx.CallAfter(pub.sendMessage, "SetStatusText", text="Connected")
        else:
            wx.CallAfter(pub.sendMessage, "SetStatusText", text="Disconnected")
        #self.__guiMutex.release()

    ''' =============================
            Controls event handling
        =============================
    '''
    def conn_button_onclick(self, event):
        #self.log_text.AppendText('Conn %s %s '% (self.port_combo.GetValue(), self.m_comboBox2.GetValue()))
        if not self.__serialPort.status:
            connected = True
            baudrate = self.m_comboBox2.GetValue()

            if int(baudrate) > 115200:
                # TODO: handle response
                self.__serialPort.receivedAnswer = self.rxAnswerReconectCallback
                if self.__serialPort.start(self.port_combo.GetValue(), 115200):
                    cmd = ATcommand(atcmds.AT_CMD_ID, True, None)
                    self.__serialPort.sendCommand(cmd)
                    cmd = ATcommand(atcmds.ATE0_CMD_ID, True, None)
                    self.__serialPort.sendCommand(cmd)
                    cmd = ATcommand(atcmds.IPR_CMD_ID, True, [baudrate])
                    self.__serialPort.sendCommand(cmd)
                else:
                    connected = False
            else:
                self.__serialPort.receivedAnswer = self.rxAnswerCallback
                if self.__serialPort.start(self.port_combo.GetValue(), baudrate):
                    self.setConnectionStatus(True)
                    cmd = ATcommand(atcmds.AT_CMD_ID, True, None)
                    self.__serialPort.sendCommand(cmd)
                    cmd = ATcommand(atcmds.ATE0_CMD_ID, True, None)
                    self.__serialPort.sendCommand(cmd)
                else:
                    connected = False

            if not connected:
                self.log_text.AppendText('Error: Could not connect to serial port!')


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
            self.__serialPort.writeDirect(data+'\r\n')

    def start_localport_buttonOnButtonClick(self, event):
        portTxt = self.localport_text.GetValue()
        try:
            port = int(portTxt)
            self.__localSocket.start(port)
        except:
            logger.error("Error, invalid port "+portTxt)

    def close_remote_conn_buttonOnButtonClick(self, event):
        self.__socketRedirection = False
        self.__serialPort.writeRaw("+++")
        self.__serialPort.rawMode = False
        cmd = ATcommand(atcmds.CIPSHUT_CMD_ID, True, None)
        self.__serialPort.sendCommand(cmd)

    ''' =============================
            Callbacks handlers
        =============================
    '''
    def localSocketConnectionOpen(self):
        self.__socketRedirection = True
        self.__serialPort.rawMode = True
        logger.info("Local socket, connection open")

        wx.CallAfter(pub.sendMessage, "AppendLogText", text='Local socket connected')

    def localSocketConnectionClosed(self):
        self.__socketRedirection = False
        self.__serialPort.writeRaw("+++")
        self.__serialPort.rawMode = False

    def localSocketDataRead(self, data):
        #print "socket rd "+data
        self.__serialPort.writeRaw(data)

    def runScript(self, name):
        if name in scriptsreader.scriptsList:
            script = scriptsreader.scriptsList[name]
            for cmd in script:
                self.__serialPort.sendCommand(cmd)


    def rxDataCallback(self, data):
        if self.__socketRedirection:
            #print "socket wr " + data
            self.__localSocket.writeData(data)
        else:
            try:
                wx.CallAfter(pub.sendMessage, "AppendLogText", text='\n'+data)
            except Exception as e:
                logger.error("Exception writing to log_text" + e)

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

    def rxAnswerReconectCallback(self, answer):
        if answer.cmdId == atcmds.IPR_CMD_ID:
            connected = True
            if answer.ok:
                self.__serialPort.receivedAnswer = self.rxAnswerCallback
                self.__serialPort.stop()
                if self.__serialPort.start(self.port_combo.GetValue(), self.m_comboBox2.GetValue()):
                    cmd = ATcommand(atcmds.AT_CMD_ID, True, None)
                    self.__serialPort.sendCommand(cmd)
                else:
                    connected = False
            else:
                connected = False

            if not connected:
                wx.CallAfter(pub.sendMessage, "AppendLogText", text='Error: Could not connect to serial port!')
                self.setConnectionStatus(False)
            else:
                self.setConnectionStatus(True)
        else:
            self.rxAnswerCallback(answer)

    def rawDataCallback(self, data):
        wx.CallAfter(pub.sendMessage, "AppendAtTrafficText", text=data)

    def AppendAtTrafficText(self, text):
        self.atcmd_text.AppendText(text)

    def AppendLogText(self, text):
        self.log_text.AppendText(text)

    def SetStatusText(self, text):
        self.m_staticText1.SetLabel(text)


if __name__ == "__main__":
    app = wx.App(False)

    atareado = ATareado(None)
    atareado.initialize()
    atareado.Show()

    if not logger.start(Log.LogType.Debug):
        logger.stop()
        print >> sys.stderr, "Error starting Log"

    app.MainLoop()
