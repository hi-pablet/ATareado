#!/usr/bin/python
import serial
import time
import threading
import sys
import pprint
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
                'ATI': ['ATI', '', '%text% OK'],
                'CPIN': ['AT+CPIN', '', '+CPIN:%text%'],
                'CSQ': ['AT+CSQ', '', '+CSQ:%number%'],
                'CGATT': ['AT+CGATT', '', '+CGATT:%number%'],
                'CIPMUX': ['AT+CIPMUX', '', '+CIPMUX'],
                'CIPMODE': ['AT+CIPMODE','"%val1%,%val2%,%val3%"', 'OK'],
                'CSTT' : ['AT+CSTT','"%val1%,%val2%,%val3%"','OK'],
                'CIICR': ['AT+CIICR', '', 'OK']},
                'CIFSR' : ['AT+CIFSR', '', '%text%'],
                'CIPSTART' : ['AT+CIPSTART', '"%val1","%val2","%val3"'], #"[TCP/UDP]", "<ip_dest>", "<port>"
                'CIPSEND': ['AT+CIPSEND', '', '>'],
                'CIPCLOSE': ['AT+CIPCLOSE', '', 'OK'],
                'CIPCCFG': ['AT+CIPCCFG', '', 'OK'],
                }


class SerialConnection(object):

    #Callback
    receivedData = None

    def __init__(self):
        self.__status = False
        self.__readThread = None
        self.__serial = None

    def start(self, port, baudrate):
        result = True

        if self.__status:
            result = False

        if result:
            try:
                self.__status = True
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
        self.__status = False
        if self.__serial is not None:
            self.__serial.close()

    def reader(self):
        try:
            while self.__status:
                # read all that is there or wait for one byte
                #print >> sys.stdout, "wait"
                data = self.__serial.read(self.__serial.in_waiting or 1)
                #print >> sys.stdout, "rx"
                if data:
                    self.receivedData(data)
                    print >> sys.stdout, data
        except serial.SerialException:
            self.__status = False

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

