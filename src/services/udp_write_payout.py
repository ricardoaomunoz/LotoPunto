import socket 
import thread
import time


readPort = 8080
writePort = 8081
localIP = "127.0.0.1"
bufferSize = 1024




class UDPPORT():
    def __init__(self):
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def WriteUDPport(self, message):
        msg = str.encode(message)
        self.UDPServerSocket.sendto(msg, (localIP, int(writePort)))    