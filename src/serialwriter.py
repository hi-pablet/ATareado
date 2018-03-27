import codecs
import threading
import time
from Log import logger


class SerialWriter(object):

    sendData = None

    def __init__(self):
        self.__runLoop = False
        self.__msDelay = 1000
        self.__data = 'A'
        self.running = False
        self.__serialThread = None
        self.__tx_decoder = codecs.getincrementalencoder('UTF-8')('replace')

    def start(self, loop, delay, data):
        result = True

        if self.running:
            result = False

        if result:
            try:
                self.running = True

                self.__runLoop = loop
                self.__msDelay = delay/1000.0
                self.__data = self.__tx_decoder.encode(data)

                self.__serialThread = threading.Thread(target=self.__serialWriterLoop, args=())
                self.__serialThread.daemon = True
                self.__serialThread.start()
            except:
                logger.error("Error starting serial loop")
                result = False

        return result

    def stop(self):
        self.running = False

    def __serialWriterLoop(self):
        while self.running:
            self.sendData(self.__data)
            time.sleep(self.__msDelay)

            if not self.__runLoop:
                self.running = False