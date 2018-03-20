import sys
import inspect
import threading
from Singleton import singleton
import mutex
import Queue


class LogType(object):
    Debug = 0
    Info = 1
    Error = 2
    description = ["Debug", " Info", "Error"]


class LogMessage(object):
    def __init__(self):
        self.type = LogType.Info
        self.text = ""
        self.caller = ""


class CLog:
    __metaclass__ = singleton

    def __init__(self):
        self.__running = False
        self.__logThread = None
        self.__logMutex = mutex.mutex()
        self.__logsQueue = Queue.Queue()
        self.logLevel = LogType.Debug

    def start(self, log_level):
        result = True

        if log_level == 0:
            self.logLevel = LogType.Debug
        elif log_level == 1:
            self.logLevel = LogType.Info
        elif log_level == 2:
            self.logLevel = LogType.Error

        if self.__running:
            result = False

        if result:
            try:
                self.__running = True
                self.__logThread = threading.Thread(target=self.log_thread, args=())
                self.__logThread.start()
            except StandardError:
                result = False
        return result

    def stop(self):
        self.__running = False
        self.post(LogType.Debug, "Close Log")

    def log_thread(self):
        print "Start Log"
        while self.__running:
            try:
                msg = self.__logsQueue.get()

                print_msg = False

                if msg is not None:
                    if msg.type >= self.logLevel:
                        print_msg = True

                if msg.type == LogType.Error:
                    out_file = sys.stderr
                else:
                    out_file = sys.stdout

                if print_msg:
                    print >> out_file, "[%20s][%s] %s" % (msg.caller, LogType.description[msg.type], msg.text)

            except StandardError, v:
                print "Error reading msg from log queue %s" % v.message

    def post(self, log_type, text):
        msg = LogMessage()
        msg.type = log_type
        msg.text = text
        msg.caller = inspect.stack()[1][3]

        self.__logsQueue.put(msg)

    def debug(self, text):
        msg = LogMessage()
        msg.type = LogType.Debug
        msg.text = text
        msg.caller = inspect.stack()[1][3]

        self.__logsQueue.put(msg)

    def info(self, text):
        msg = LogMessage()
        msg.type = LogType.Info
        msg.text = text
        msg.caller = inspect.stack()[1][3]

        self.__logsQueue.put(msg)

    def error(self, text):
        msg = LogMessage()
        msg.type = LogType.Error
        msg.text = text
        msg.caller = inspect.stack()[1][3]

        self.__logsQueue.put(msg)


# Global object
logger = CLog()
