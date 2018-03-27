#!/usr/bin/python
import codecs
import serial
import time
import threading
import sys
from serial.tools.list_ports import comports
from Queue import Queue
from atcmds import commandsList
from atcmds import ATcommand
from atcmds import ATresponse
from Log import logger

codecs.register(lambda c: hexlify_codec.getregentry() if c == 'hexlify' else None)


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


class SerialConnection(object):

    #Callback
    receivedData = None
    receivedAnswer = None
    rawData = None

    def __init__(self):
        self.status = False
        self.rawMode = False
        self.__readThread = None

        self.__writeThread = None

        self.__cmdQueue = Queue()
        self.__cmdProcesssedEvent = threading.Event()

        self.__serial = None
        self.__currCommand = None
        self.__waitingAnswer = False
        # 5 seconds timeout
        self.__TOTimer = None
        self.__cmdMutex = threading.Lock()
        #self.input_encoding = 'UTF-8'
        #self.output_encoding = 'UTF-8'
        self.__rx_decoder = codecs.getincrementaldecoder('UTF-8')('replace')
        self.__tx_decoder = codecs.getincrementalencoder('UTF-8')('replace')

    def start(self, port, baudrate):
        result = True

        if self.status:
            result = False

        if result:
            try:
                self.status = True
                self.__serial = serial.Serial()
                self.__serial.port = port
                self.__serial.baudrate = baudrate

                if not hasattr(self.__serial, 'cancel_read'):
                    # enable timeout for alive flag polling if cancel_read is not available
                    self.__serial.timeout = 1

                self.__serial.open()
                if self.__serial.in_waiting > 0:
                    self.__serial.timeout = 1
                    self.__serial.read(self.__serial.in_waiting)
                    self.__serial.timeout = 0

            except serial.SerialException as e:
                logger.error('could not open port {!r}: {}\n'.format(port, e))
                self.status = False
                result = False

            if result:
                self.__readThread = threading.Thread(target=self._reader, args=())
                self.__readThread.daemon = True
                self.__writeThread = threading.Thread(target=self._writer, args=())
                self.__writeThread.daemon = True

                # start thread
                self.__readThread.start()
                self.__writeThread.start()

        return result

    def stop(self):
        if self.status:
            self.status = False
            # Exit write thread
            self.__cmdQueue.put(None)
            if self.__writeThread.isAlive():
                self.__writeThread.join()
            logger.debug("Write thread stopped")

            if self.__serial is not None:
                self.__serial.cancel_read()
                self.__serial.close()

            if self.__readThread.isAlive():
                self.__readThread.join()
            logger.debug("Read thread stopped")

    def reconnect(self, port, baudrate):
        res = True
        try:
            if self.status:
                self.__serial.close()
                self.status = False

            self.__serial.port = port
            self.__serial.baudrate = baudrate
            self.__serial.open()
            self.status = True
        except:
            res = False
            logger.error("Error reconnecting")
        return res

    def _timeoutHandler(self):
        try:
            logger.debug( "Command response timeout, command %s" % self.__currCommand.cmd)
            answer = None
            self.__cmdMutex.acquire()
            if self.__waitingAnswer:
                self.__waitingAnswer = False
                answer = ATresponse(False, self.__currCommand.cmd, ["Timeout"])
            self.__cmdMutex.release()

            if answer is not None:
                self.receivedAnswer(answer)
        except:
            logger.error("Timeout handler exception")

        self.__cmdProcesssedEvent.set()

    def sendCommand(self, newCommand):
        if self.status:
            self.__cmdQueue.put(newCommand)

    def clearCommandsQueue(self):
        # empty cmdQueue
        while not self.__cmdQueue.empty():
            self.__cmdQueue.get(False, 1)

    def _writer(self):
        self.__cmdProcesssedEvent.clear()
        while self.status:
            try:
                logger.debug("[W]queue Get")
                newCmd = self.__cmdQueue.get(True)

                if newCmd is None:
                    #Exit from queue block
                    raise Exception("Exit thread")

                logger.debug("[W]new cmd " + newCmd.cmd)

                #self.__cmdMutex.acquire()

                # Check if we are waiting for an answer
                self.__waitingAnswer = True

                self.__currCommand = newCmd
                #self.__cmdMutex.release()


                self.writeDirect(self.__currCommand.getString())


                # Start timeout
                logger.debug("[W]Start timeout timer")
                self.__TOTimer = threading.Timer(5, self._timeoutHandler)
                self.__TOTimer.start()

                logger.debug("[W]Wait event")
                self.__cmdProcesssedEvent.wait()
                self.__cmdProcesssedEvent.clear()
                logger.debug("[W]event rx")

            except Exception:
                logger.error("[W]Exception write thread ")
        logger.debug("exit wr")

    def _reader(self):
        try:
            answerString = ''
            while self.status:
                # read all that is there or wait for one byte
                logger.debug("[R]wait")
                readBytes = self.__serial.read(self.__serial.in_waiting or 1)
                logger.debug("[R]rx ")

                if readBytes and self.status:
                    # Check if we are forwarding
                    if not self.rawMode:
                        text = self.__rx_decoder.decode(readBytes)
                        self.rawData(text)

                        self.__cmdMutex.acquire()

                        if self.__waitingAnswer:
                            answerString += text
                            answer = self.__currCommand.checkResponse(answerString)

                            # Expected answer
                            if answer is not None:
                                self.__TOTimer.cancel()
                                self.__waitingAnswer = False
                                answerString = ''

                                self.__cmdMutex.release()
                                logger.debug('[' + text + ']')
                                logger.debug("[R]Answer ok")

                                self.receivedAnswer(answer)
                                self.__cmdProcesssedEvent.set()
                            else:
                                self.__cmdMutex.release()
                                logger.debug('[' + text + ']')

                        else:
                            self.__cmdMutex.release()
                            self.receivedData(text)
                            logger.debug('<'+text+'>')
                    else:
                        logger.debug('{' + text + '}')
                        self.receivedData(readBytes)
                        
        except serial.SerialException:
            self.status = False
        logger.debug("exit rd")

    def writeDirect(self, data):
        try:
            if self.status:
                if self.rawMode:
                    self.__serial.write(data)
                else:
                    logger.debug("tx " + data)
                    self.rawData(data)
                    self.__serial.write(self.__tx_decoder.encode(data))

        except Exception, v:
            logger.error("Exception writeDirect")

    def writeRaw(self, data):
        if self.status:
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

