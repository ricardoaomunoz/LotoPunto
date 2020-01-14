
import serial
import sys


class ThermalPrinter():

    def __init__(self, port, baudrate=9600, timeout=5):
        self.printer_serial = serial.Serial(port = port, baudrate = baudrate,
        timeout=timeout, writeTimeout=timeout)

    def read_serial(self):
        reading = self.printer_serial.read()
        return reading

    def write_serial(self, data):
        writing = self.printer_serial.write(data)
        return writing

    def close_port(self):
        self.printer_serial.close()   

    def begin(self, heatTime=defaultHeatTime):
		self.writeBytes(
		  27,       # Esco91012# Configure tab stops on recent printers
		self.writeBytes(27, 68)         # Set tab stops
		self.writeBytes( 4,  8, 12, 16) # every 4 columns,
		self.writeBytes(20, 24, 28,  0) # 0 is end-of-list.

    def test(self):
		self.write("Hello world!")
		self.feed(2)

	def testPage(self):
		self.writeBytes(18, 84)
		self.timeoutSet(
		  self.dotPrintTime * 24 * 26 +
		  self.dotFeedTime * (6 * 26 + 30))
