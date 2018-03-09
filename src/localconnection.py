import socket
import threading
from time import sleep

RX_BUFFER_SIZE = 128

class LocalPort(object):
# This class receives connection requests from the drivers and handles the
# communication with them to get the driver_id and return the new ip and port
# of the engine to connect to

    # Callback
    newDataRead = None

    def __init__(self, port):
        self.__status = False
        self.listenPort = port
        self.connOpen = False
        self.__listenSocket = None
        self.__connSocket = None
        self.__listenThread = None

    def start(self):
        result = True

        if self.__status:
            result = False

        if result:
            try:
                self.__status = True
                self.__listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Bind the socket to the port
                server_address = ("", self.listenPort)  # to connect from outside the machine
                self.__listenSocket.bind(server_address)
                #Log.logger.info('Starting request port on port %s' % server_address[1])
            except socket.error, v:
                #Log.logger.error('Error starting Request Port on %s port %s. %s' % (server_address[0], server_address[1], v.strerror))
                result = False
        if result:
            __listenThread = threading.Thread(target=self.listen_thread, args=())
            __listenThread.start()
        return result

    def stop(self):
        self.__status = False
        if self.__listenSocket is not None:
            self.__listenSocket.shutdown(socket.SHUT_RDWR)
        self.__listenSocket.close()

    def listen_thread(self):

        if not self.__status:
            return

        try:
            # Listen for incoming connections
            self.__listenSocket.listen(1)
        except socket.error, v:
            #Log.logger.error('Socket error listening', v.strerror)

        while self.__status:

            try:
                #Log.logger.info('waiting for driver connection')
                # Wait for a connection
                self.__connSocket, client_address = self.__listenSocket.accept()
                self.connOpen = True
                self.receive_data()
                #Log.logger.post(Log.LogType.Debug, 'New Connection from ' + client_address[0])

            except socket.error:
                Log.logger.error('Exception accepting new connection')
                self.connOpen = False

    def receive_data(self):

        rx_complete = False
        rx_error = False
        while self.__status:
            try:
                rx_bytes = bytearray(self.__connSocket.recv(RX_BUFFER_SIZE))

                self.newDataRead(rx_bytes)
            except socket.error:
                rx_error = True
                break

        return rx_error

    def writeData(self, tx_data):
        #Build message

        #print "Sending message %s length %d payload [%d]" % (message, len(message), len(payload))
        if self.__status:
            try:
                self.__connSocket.sendall(tx_data)
            except socket.error:
                #Log.logger.error("Error sending mesage")