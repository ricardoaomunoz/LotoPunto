
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

    #Print data in the print buffer and feeds one line, this commands sets the print
    #position to the beginning of the line 
    # LF
    def print_data_buffer(self):
      if automatic_line: #CR same as LF when automatic line feed is enabled
        self.write_serial(13)
      else:
        self.write_serial(10)

    # Transmits the selected printer status specified by n in real-time
    def real_time_status_transmission(self, n):
      #n=1 printer status, n=2 offline status
      #n=3 error status, n=4 paper roll sensor status
      self.write_serial(16, 4 , n)

    #def real_time_request(self):

    #Set the character spacing for the right side of the character
    #to [n x 0.125 mm - n x 0.0049"]
    #default n = 0
    #ESC SP n
    def set_right_side_character_spacing(self, n):
      self.write_serial(27, 32 , n)

    #ESC ! n
    def select_print_mode(self, n):
      self.write_serial(27, 33, n)

    #Set the distance from the beginning of the line to the 
    #position at wich subsequent characters are to be printed
    #the distance from the beginning of the line to the position at
    #wich subsequencent characters are to be printed
    #[(nL + nH x 256) x 0.125 mm]
    # ESC $ nL nH
    def set_absolute_print_position(self, nL, nH):
      self.write_serial(27, 36 , nL, nH)

    def setBarcodeHeight(self, val=50):
      if val < 1: val = 1
      self.barcodeHeight = val
      self.write_serial(29, 104, val)

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
