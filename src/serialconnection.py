#!/usr/bin/python
import serial
import time
import threading
import sys
import pprint
import re
from serial.tools.list_ports import comports

#--------------------------------------
def getPortsList():
    """\
    Show a list of ports and ask the user for a choice. To make selection
    easier on systems with long device names, also allow the input of an
    index.
    """
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        ports.append(port)
    return ports


# Command List [id, command, params, return]
commandsList = {'AT': ['AT', '', 'OK'],
                'ATI': ['ATI', '', '(.*) OK'],
                'CPIN': ['AT+CPIN', '', '+CPIN:(.*)'],
                'CSQ': ['AT+CSQ', '', '+CSQ:(\d+)'],
                'CGATT': ['AT+CGATT', '', '+CGATT:(\d+)'],
                'CIPMUX': ['AT+CIPMUX', '', '+CIPMUX'],
                'CIPMODE': ['AT+CIPMODE','"%val1%,%val2%,%val3%"', 'OK'],
                'CSTT': ['AT+CSTT','"%val1%,%val2%,%val3%"', 'OK'],
                'CIICR': ['AT+CIICR', '', 'OK'],
                'CIFSR': ['AT+CIFSR', '', '(.*)'],
                'CIPSTART': ['AT+CIPSTART', '"%val1","%val2","%val3"', 'OK'], #"[TCP/UDP]", "<ip_dest>", "<port>"
                'CIPSEND': ['AT+CIPSEND', '', '>'],
                'CIPCLOSE': ['AT+CIPCLOSE', '', 'OK'],
                'CIPCCFG': ['AT+CIPCCFG', '', 'OK'] }


class ATcommand(object):

    def __init__(self, cmdId, setMode, params):
        self.cmd = cmdId
        self.setOperation = setMode
        self.params = params
        self.paramString = ''
        self.answer = ''
        self.respError = False


class SerialConnection(object):

    #Callback
    receivedData = None

    def __init__(self):
        self.status = False
        self.__readThread = None
        self.__serial = None
        self.__currCommand = None
        self.__waitingAnswer = False
        # 5 seconds timeout
        self.__TOTimer = Timer(5, self._timeoutHandler)
        self.__cmdMutex = threading.Lock()

    def start(self, port, baudrate):
        result = True

        if self.status:
            result = False

        if result:
            try:
                self.status = True
                self.__serial = serial.serial_for_url(
                port,
                baudrate,
                do_not_open=True)

                if not hasattr(self.__serial, 'cancel_read'):
                    # enable timeout for alive flag polling if cancel_read is not available
                    self.__serial.timeout = 1

                self.__serial.open()

            except serial.SerialException as e:
                sys.stderr.write('could not open port {!r}: {}\n'.format(port, e))
                result = False

            if result:
                # start serial->console thread
                self.__readThread = threading.Thread(target=self.reader, args=())
                self.__readThread.daemon = True
                self.__readThread.start()

        return result

    def stop(self):
        self.status = False
        if self.__serial is not None:
            self.__serial.close()

    def _timeoutHandler(self):
        self.__cmdMutex.aquire()

        if self.__waitingAnswer:
            self.__currCommand.respError = True
            self.__waitingAnswer = False

        self.__cmdMutex.release()

    def sendCommand(self, newCommand):

        self.__cmdMutex.aquire()

        # Check if we are waiting for an answer
        if self.__waitingAnswer:
            self.__cmdMutex.release()
            return False

        self.__cmdMutex.release()

        res = True
        # Known command
        if newCommand.cmd in commandsList:
            self.__waitingAnswer = True
            self.__currCommand = newCommand
            self.writeRaw(commandsList[newCommand.cmd])
            self.__TOTimer.start()
        else:
            res = False

        return res

    def processAnswer(self, data):
        res = True
        searchObj = re.search(commandsList[self.__currCommand.cmd][2], data, re.I)
        if searchObj:
            print "Searched ans : ", searchObj.group()
        return res

    def reader(self):
        try:
            while self.status:
                # read all that is there or wait for one byte
                #print >> sys.stdout, "wait"
                data = self.__serial.read(self.__serial.in_waiting or 1)
                #print >> sys.stdout, "rx"
                if data:
                    self.__cmdMutex.aquire()
                    self.__TOTimer.stop()
                    if self.__waitingAnswer:
                        self.__waitingAnswer = False
                        self.__cmdMutex.release()
                    else:
                        self.__cmdMutex.release()
                        self.receivedData(data)
                        print >> sys.stdout, data
                        
        except serial.SerialException:
            self.status = False

    def writeRaw(self, data):
        print >> sys.stdout, "tx"
        self.__serial.write(data)


def printerCallback(data):
    print >> sys.stdout, data


if __name__ == '__main__':
    ports = getPortsList()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(ports)

    conn = SerialConnection()
    conn.receivedData = printerCallback
    conn.start("/dev/ttyUSB1", 115200)
    time.sleep(1)
    conn.write("ATI\n\r")
    time.sleep(5)

