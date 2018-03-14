#!/usr/bin/python
import serial
import time
import threading
import sys
from pprint import pprint
import re
from serial.tools.list_ports import comports
from Queue import Queue

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


AT_CMD_ID = 'AT'
ATI_CMD_ID = 'ATI'
CPIN_CMD_ID = 'CPIN'
CSQ_CMD_ID = 'CSQ'
CGATT_CMD_ID = 'CGATT'
CIPMUX_CMD_ID = 'CIPMUX'
CIPMODE_CMD_ID = 'CIPMODE'
CSTT_CMD_ID = 'CSTT'
CIICR_CMD_ID = 'CIICR'
CIFSR_CMD_ID = 'CIFSR'
CIPSTART_CMD_ID = 'CIPSTART'
CIPSEND_CMD_ID = 'CIPSEND'
CIPCLOSE_CMD_ID = 'CIPCLOSE'
CIPCCFG_CMD_ID = 'CIPCCFG'

# Command List [id, command, params, return]
commandsList = {AT_CMD_ID:     ['AT', '', 'OK'],
                ATI_CMD_ID:    ['ATI', '', '(.*)OK'],
                CPIN_CMD_ID:   ['AT+CPIN', '', '+CPIN:(.*)'],
                CSQ_CMD_ID:    ['AT+CSQ', '', '+CSQ:(\d+)'],
                CGATT_CMD_ID:  ['AT+CGATT', '', '+CGATT:(\d+)'],
                CIPMUX_CMD_ID: ['AT+CIPMUX', '', '+CIPMUX'],
                CIPMODE_CMD_ID:['AT+CIPMODE', '"%val1%,%val2%,%val3%"', 'OK'],
                CSTT_CMD_ID:   ['AT+CSTT', '"%val1%,%val2%,%val3%"', 'OK'],
                CIICR_CMD_ID:  ['AT+CIICR', '', 'OK'],
                CIFSR_CMD_ID:  ['AT+CIFSR', '', '(.*)'],
                CIPSTART_CMD_ID: ['AT+CIPSTART', '"%val1","%val2","%val3"', 'OK'],  # "[TCP/UDP]", "<ip_dest>", "<port>"
                CIPSEND_CMD_ID:['AT+CIPSEND', '', '>'],
                CIPCLOSE_CMD_ID: ['AT+CIPCLOSE', '', 'OK'],
                CIPCCFG_CMD_ID:['AT+CIPCCFG', '', 'OK']}


class ATcommand(object):

    def __init__(self, cmdId, setMode, params):
        self.cmd = cmdId
        self.setOperation = setMode
        self.params = params
        try:
            self.paramString = commandsList[self.cmd][1]
            self.answer = ''
            self.respError = False
            if self.paramString.find('%val1%') != -1 and 0 in params:
                self.paramString = self.paramString.replace('%val1%', params[0])
            if self.paramString.find('%val2%') != -1 and 1 in params:
                self.paramString = self.paramString.replace('%val2%', params[1])
            if self.paramString.find('%val3%') != -1 and 2 in params:
                self.paramString = self.paramString.replace('%val3%', params[2])
        except:
            print "Exception creating command"

    def getSetString(self):
        return commandsList[self.cmd][0] + self.paramString + "\r\n"

    def getQueryString(self):
        return commandsList[self.cmd][0] + "=?\r\n"

    def parseResponse(self, response):
        #print "[%s] search %s " % (response, commandsList[self.cmd][2])
        searchObj = re.search(commandsList[self.cmd][2], (response.replace('\n', '')).replace('\r', ''), re.S | re.M)
        if searchObj:
            pprint(searchObj.groups())
            #print "Searched ans : ", searchObj.group(1)
            res = (True, searchObj.groups())
        else:
            res = (False, response)

        return res


class SerialConnection(object):

    #Callback
    receivedData = None
    receivedAnswer = None

    def __init__(self):
        self.status = False
        self.__readThread = None
        self.__readThread = threading.Thread(target=self._reader, args=())
        self.__readThread.daemon = True

        self.__writeThread = None
        self.__writeThread = threading.Thread(target=self._writer, args=())
        self.__writeThread.daemon = True

        self.__cmdQueue = Queue()
        self.__cmdProcesssedEvent = threading.Event()

        self.__serial = None
        self.__currCommand = None
        self.__waitingAnswer = False
        # 5 seconds timeout
        self.__TOTimer = None
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
                if self.__serial.in_waiting > 0:
                    self.__serial.timeout = 1
                    self.__serial.read(self.__serial.in_waiting)
                    self.__serial.timeout = 0

            except serial.SerialException as e:
                sys.stderr.write('could not open port {!r}: {}\n'.format(port, e))
                result = False

            if result:
                # start thread
                self.__readThread.start()
                self.__writeThread.start()

        return result

    def stop(self):
        self.status = False
        # Exit write thread
        self.__cmdQueue.put(None)

        if self.__serial is not None:
            self.__serial.cancel_read()
            self.__serial.close()

    def _timeoutHandler(self):
        try:
            print "Command response timeout, command %s" % self.__currCommand.cmd
            self.__cmdMutex.acquire()
            if self.__waitingAnswer:
                self.__currCommand.respError = True
                self.__waitingAnswer = False
                self.receivedAnswer((False, "Timeout"))

            self.__cmdMutex.release()
        except:
            print "Timeout handler exception"

        self.__cmdProcesssedEvent.set()

    def sendCommand(self, newCommand):

        self.__cmdQueue.put(newCommand)


    def _writer(self):
        while self.status:
            try:
                print >> sys.stdout, "Get cmd"
                newCmd = self.__cmdQueue.get(True)

                print >> sys.stdout, "new cmd %s" % newCmd.cmd

                if newCmd is None:
                    raise Exception("Exit thread")

                self.__cmdMutex.acquire()

                # Check if we are waiting for an answer
                if self.__waitingAnswer:
                    self.__cmdMutex.release()

                self.__cmdMutex.release()

                self.__waitingAnswer = True
                self.__currCommand = newCmd
                if self.__currCommand.setOperation:
                    self.writeRaw(self.__currCommand.getSetString())
                else:
                    self.writeRaw(self.__currCommand.getQueryString())

                # Start timeout
                print >> sys.stdout, "Start timeout timer"
                self.__TOTimer = threading.Timer(5, self._timeoutHandler)
                self.__TOTimer.start()

                self.__cmdProcesssedEvent.wait()
                print >> sys.stdout, "Wait next cmd"

            except Exception as e:
                print >> sys.stdout, "Exception write thread %s" % e

    def _reader(self):
        try:
            answerString = ''
            while self.status:
                # read all that is there or wait for one byte
                print >> sys.stdout, "wait"
                readBytes = self.__serial.read(self.__serial.in_waiting or 1)
                print >> sys.stdout, "rx"

                if readBytes and self.status:
                    print >> sys.stdout, readBytes
                    self.__cmdMutex.acquire()
                    #self.__waitingAnswer = False  #DELETEME

                    if self.__waitingAnswer:
                        answerString += readBytes
                        answer = self.__currCommand.parseResponse(answerString)

                        # Expected answer
                        if answer[0]:
                            self.__TOTimer.cancel()
                            self.__waitingAnswer = False
                            answerString = ''
                            print "Answer: "
                            #print(', '.join(map(str, answer)))
                            self.__cmdProcesssedEvent.set()
                            self.receivedAnswer(answer)
                        self.__cmdMutex.release()

                    else:
                        self.__cmdMutex.release()
                        self.receivedData(readBytes)
                        print >> sys.stdout, readBytes
                        
        except serial.SerialException:
            self.status = False

    def writeRaw(self, data):
        if self.status:
            print >> sys.stdout, "tx", data
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

