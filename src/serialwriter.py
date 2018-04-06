import codecs
import threading
import time
from Log import logger


class SerialWriter(object):

    sendData = None

    def __init__(self):
        self.__runLoop = False
        self.__delay = 1
        self.__data = '0123456789'
        self.__repetitions = 10
        self.__nrOfPacketsPerIteration = 1
        self.running = False
        self.__serialThread = None
        self.__tx_decoder = codecs.getincrementalencoder('ASCII')('replace')

    def start(self, throughput, duration):
        result = True

        if self.running:
            result = False

        if result:
            #try:
            self.running = True

            nrPacketsPerSec = throughput/80
            if nrPacketsPerSec >= 1000:
                self.__nrOfPacketsPerIteration = nrPacketsPerSec/1000
                self.__delay = 0.001
            else:
                self.__nrOfPacketsPerIteration = 1
                self.__delay = 1.0/nrPacketsPerSec

            self.__repetitions = duration/self.__delay

            self.__data = self.__tx_decoder.encode(self.__data)

            logger.info("Start serial write, repetitions %s, %s" % (self.__repetitions, self.__nrOfPacketsPerIteration))
            self.__serialThread = threading.Thread(target=self.__serialWriterLoop, args=())
            self.__serialThread.daemon = True
            self.__serialThread.start()
        #except:
            #logger.error("Error starting serial loop")
            #result = False

        return result

    def stop(self):
        self.running = False

    def __serialWriterLoop(self):
        while self.running:
            for x in range(0, self.__nrOfPacketsPerIteration):
                self.sendData(self.__data)
            time.sleep(self.__delay)

            self.__repetitions -= 1

            if self.__repetitions == 0:
                self.running = False