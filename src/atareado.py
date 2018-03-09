#!/usr/bin/python

import wx
import atframe
import serialconnection
from serial.tools.list_ports import comports
import form

class ATareado(form.MainFrame):

    # Command List [id, command, params, return]
    commandsList = {'AT': ['AT', '', 'OK'],
                    'ATI': ['ATI', '', '%text% OK'],
                    'CPIN': ['AT+CPIN', '', '+CPIN:%text%'],
                    'CSQ': ['AT+CSQ', '', '+CSQ:%number%'],
                    'CGATT': ['AT+CGATT', '', '+CGATT:%number%'],
                    'CIPMUX': ['AT+CIPMUX', '+CIPMUX'],
                    'CIPMODE': ['AT+CIPMODE','"%val1%,%val2%,%val3%"', 'OK'] }
    '''
    # Start task and set APN
    AT + CSTT = "orangeworld", "orange", "orange"
    OK

    # Bring up wireless connection
    AT + CIICR
    OK

    # Get local IP address
    AT + CIFSR
    10.78
    .245
    .128

    # Start up the connection
    AT + CIPSTART = "[TCP/UDP]", "<ip_dest>", "<port>"
    OK
    CONNECT
    OK

    # Send data CTRL+Z (0x1a) to send
    AT + CIPSEND
    > [data]
    SEND
    OK

    # Close UDP connection
    AT + CIPCLOSE

    # Config
    AT + CIPCCFG
    '''

    def __init__(self, parent):
        form.MainFrame.__init__(self, parent)
        self.__serialconn = serialconnection.SerialConnection()

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

#    def connectCallback(self, port, baudrate):
#        status = self.__serialconn.start(port, baudrate)
#        self.__mainForm.setConnectionStatus(status)

if __name__ == "__main__":
    app = wx.App(False)

    atareado = ATareado(None)
    atareado.start()
    atareado.Show()

    app.MainLoop()
