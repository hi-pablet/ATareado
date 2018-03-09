#!/usr/bin/python

import wx
import atframe
import serialconnection
from serial.tools.list_ports import comports

class ATareado(object):

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

    def __init__(self):
        self.__serialconn =  SerialConnection()
        self.__mainForm = atframe.ATFrame(None)
        self.__mainForm.connectCallback = self.connectCallback

    def start(self):
        serialPorts = serialconnection.getPortsList()
        self.__mainForm.setAvailablePorts(serialPorts)
        self.__mainForm.Show()

    def connectCallback(self, port, baudrate):

        status = self.__serialconn.start(port, baudrate)
        self.__mainForm.setConnectionStatus(status)

if __name__ == "__main__":
    app = wx.App(False)

    atareado = ATareado()
    atareado.start()

    app.MainLoop()
