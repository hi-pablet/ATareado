
class SerialConnection(object):

    def __init__(self):
        self.__currState = 0

    def processRxData(self, data):
        if self.__currState 
