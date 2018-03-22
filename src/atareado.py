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
import time
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

        self.__answerHandler = {atcmds.CIPSTART_CMD_ID:  self._answerCIPSTARTHandler,
                                atcmds.IPR_CMD_ID:       self._answerIPRHandler}

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
            # Set auto baudrate detection as default
            if self.__serialPort.status:
                self.__serialPort.writeDirect("AT+IPR=0\r\n")
            self.__localSocket.stop()
            logger.stop()
            self.__serialPort.stop()
        except:
            print "Error stoping ports"
        self.Destroy()

    def setConnectionStatus(self, status):
        if status:
            wx.CallAfter(pub.sendMessage, "SetStatusText", text="Connected")
        else:
            wx.CallAfter(pub.sendMessage, "SetStatusText", text="Disconnected")

    ''' =============================
            Controls event handling
        =============================
    '''
    def conn_button_onclick(self, event):
        #self.log_text.AppendText('Conn %s %s '% (self.port_combo.GetValue(), self.m_comboBox2.GetValue()))
        if not self.__serialPort.status:
            connected = True
            baudrate = self.m_comboBox2.GetValue()

            iprCmd = None

            if int(baudrate) > 115200:
                iprCmd = ATcommand(atcmds.IPR_CMD_ID, True, [baudrate])
                baudrate = "115200"

            if self.__serialPort.start(self.port_combo.GetValue(), baudrate):
                self.setConnectionStatus(True)
                cmd = ATcommand(atcmds.AT_CMD_ID, True, None)
                self.__serialPort.sendCommand(cmd)
                cmd = ATcommand(atcmds.ATE0_CMD_ID, True, None)
                self.__serialPort.sendCommand(cmd)
                if iprCmd is not None:
                    self.__serialPort.sendCommand(iprCmd)
            else:
                connected = False

            if not connected:
                self.log_text.AppendText('Error: Could not connect to serial port!')
            else:
                self.conn_button.SetLabelText('Disconnect')
        else:
            self.__serialPort.writeDirect("AT+IPR=0\r\n")
            self.__serialPort.stop()
            self.conn_button.SetLabelText('Connect')


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

    # Stop current script
    def stop_buttonOnButtonClick(self, event):
        self.__serialPort.clearCommandsQueue()

    def clear_buttonOnButtonClick(self, event):
        self.log_text.SetValue("")

    def send_direct_buttonOnButtonClick(self, event):
        if self.__serialPort.status:
            data = self.direct_cmd_text.GetValue()
            self.__serialPort.writeDirect(data+'\r\n')

    def start_localport_buttonOnButtonClick(self, event):
        if not self.__localSocket.status:
            portTxt = self.localport_text.GetValue()
            try:
                port = int(portTxt)
                self.__localSocket.start(port, 'UDP')
                self.start_localport_button.SetLabelText('Stop Listening')
            except:
                logger.error("Error, invalid port "+portTxt)
        else:
            self.__localSocket.stop()
            self.start_localport_button.SetLabelText('Start Listening')

        self.start_localport_button.Refresh()


    def close_remote_conn_buttonOnButtonClick(self, event):
        if self.__serialPort.status:
            self.__socketRedirection = False
            self.__serialPort.writeDirect("+++")
            self.__serialPort.rawMode = False
            time.sleep(2)
            cmd = ATcommand(atcmds.CIPSHUT_CMD_ID, True, None)
            self.__serialPort.sendCommand(cmd)

    def connect_remote_buttonOnButtonClick(self, event):
        # Get addr
        if self.__serialPort.status:
            params = ["UDP", self.remoteaddress_text.GetValue(), self.remoteport_text.GetValue()]
            cmd = ATcommand(atcmds.CIPSTART_CMD_ID, True, params)
            self.__serialPort.sendCommand(cmd)

    ''' =============================
            Callbacks handlers
        =============================
    '''
    def localSocketConnectionOpen(self):
        self.__socketRedirection = True
        logger.info("Local socket, connection open")
        wx.CallAfter(pub.sendMessage, "AppendLogText", text='Local socket connected')

    def localSocketConnectionClosed(self):
        self.__socketRedirection = False

    def localSocketDataRead(self, data):
        #print "socket rd "+data
        #print "*"
        if self.__serialPort.status:
            self.__serialPort.writeDirect(data)

    def runScript(self, name):
        if name in scriptsreader.scriptsList:
            script = scriptsreader.scriptsList[name]
            for cmd in script:
                self.__serialPort.sendCommand(cmd)


    def rxDataCallback(self, data):
        if self.__socketRedirection:
            #print "socket wr " + data
            #print "."
            self.__localSocket.writeData(data)
        else:
            try:
                wx.CallAfter(pub.sendMessage, "AppendLogText", text=data)
            except Exception as e:
                logger.error("Exception writing to log_text" + e)

    # Command answer handler
    def rxAnswerCallback(self, answer):

        if answer.cmdId in self.__answerHandler:
            self.__answerHandler[answer.cmdId](answer)

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

    def _answerCIPSTARTHandler(self, answer):
        if answer.ok:
            self.__serialPort.rawMode = True
            wx.CallAfter(pub.sendMessage, "AppendLogText", text='\nRemote connection open')
            logger.info('Remote connection open')

    def _answerIPRHandler(self, answer):
        if answer.ok:
            if self.__serialPort.reconnect(self.port_combo.GetValue(), self.m_comboBox2.GetValue()):
                connected = True
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

    if not logger.start(Log.LogType.Info):
        logger.stop()
        print >> sys.stderr, "Error starting Log"

    app.MainLoop()
