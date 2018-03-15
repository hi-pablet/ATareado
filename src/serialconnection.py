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
        self.input_encoding = 'UTF-8'
        self.output_encoding = 'UTF-8'
        self.__rx_decoder = codecs.getincrementaldecoder('UTF-8')('replace')
        self.__tx_decoder = codecs.getincrementalencoder('UTF-8')('replace')

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
            answer = None
            self.__cmdMutex.acquire()
            if self.__waitingAnswer:
                self.__waitingAnswer = False
                answer = ATresponse(False, self.__currCommand.cmd, ["Timeout"])
            self.__cmdMutex.release()

            if answer is not None:
                self.receivedAnswer(answer)
        except:
            print "Timeout handler exception"

        self.__cmdProcesssedEvent.set()

    def sendCommand(self, newCommand):

        self.__cmdQueue.put(newCommand)


    def _writer(self):
        self.__cmdProcesssedEvent.clear()
        while self.status:
            try:
                print >> sys.stdout, "[W]queue Get"
                newCmd = self.__cmdQueue.get(True)

                if newCmd is None:
                    #Exit from queue block
                    raise Exception("Exit thread")

                print >> sys.stdout, "[W]new cmd %s" % newCmd.cmd

                self.__cmdMutex.acquire()

                # Check if we are waiting for an answer
                self.__waitingAnswer = True

                self.__currCommand = newCmd
                self.writeRaw(self.__currCommand.getString())

                self.__cmdMutex.release()

                # Start timeout
                print >> sys.stdout, "[W]Start timeout timer"
                self.__TOTimer = threading.Timer(5, self._timeoutHandler)
                self.__TOTimer.start()

                print >> sys.stdout, "[W]Wait event"
                self.__cmdProcesssedEvent.wait()
                self.__cmdProcesssedEvent.clear()
                print >> sys.stdout, "[W]event rx"

            except Exception as e:
                print >> sys.stdout, "[W]Exception write thread %s" % e

    def _reader(self):
        try:
            answerString = ''
            while self.status:
                # read all that is there or wait for one byte
                print >> sys.stdout, "[R]wait"
                readBytes = self.__serial.read(self.__serial.in_waiting or 1)
                print >> sys.stdout, "[R]rx"

                if readBytes and self.status:
                    text = self.__rx_decoder.decode(readBytes)
                    print >> sys.stdout, text
                    self.__cmdMutex.acquire()
                    #self.__waitingAnswer = False  #DELETEME

                    if self.__waitingAnswer:
                        answerString += text
                        answer = self.__currCommand.parseResponse(answerString)

                        # Expected answer
                        if answer is not None:
                            self.__TOTimer.cancel()
                            self.__waitingAnswer = False
                            answerString = ''
                            #print "[R]Answer: "
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
            self.__serial.write(self.__tx_decoder.encode(data))


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

