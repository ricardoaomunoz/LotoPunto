
import serial
import sys
from escpos.printer import Usb

class ThermalPrinter():

  def __init__(self):
    self.p = Usb(0x0fe6, 0x811e, 98, 0x82, 0x02)

  def insert_imagen(self, img_surce):
    self.p.image(img_surce)

  def insert_qr(self, content, size):
    self.p.qr(content, size=size) #size 1 - 16 default 3
    

  def insert_barcode(self, code, bc, height, width):
    self.p.barcode(code, bc, height=height, width=width)

  def insert_text(self, txt):
    self.p.text(txt)

  def insert_raw_txt(self, txt):
    self.p._raw(txt)

  # harware action, may be: INIT, SELECT, RESET
  def hardware_operation(self, hw):
    self.p.hw(hw)


  #string for the following control sequences:
  # LF for Line Feed
  # FF for Form Feed
  # CR for Carriage Return
  # HT for Horizontal Tab
  # VT for Vertical Tab
  #pos = horizontal tab position 1 - 16
  def feed_control(self, ctl, pos):
    self.p.control()

    self.p.charcode()
#   #def insert_textln(self, txt):
# align = CENTER LEFT RIGHT  default left
# font_type = A or B         default A
# textt_type = B(bold), U(underline), U2(underline, version2), BU(for bold and underlined, NORMAL(normal text) defaul tnormal
# width = width multiplier decimal 1 - 8 defaul 1
# heigh =  height multiplier decimal 1 - 8 defaul 1
# density = density 0 - 8
  # def set_txt(self, align, font, text_type, density, height, width):
  def set_txt(self, *args, **Kwargs):
    print(Kwargs)
    self.p.set(Kwargs)
    
    
  def cut_paper(self):
    self.p.cut()

  # def print_n_feed(self, n):
  #   self.p.
    # def __init__(self, port, baudrate=9600, timeout=5):
    #     self.printer_serial = serial.Serial(port=port, baudrate=baudrate,
    #                                         timeout=timeout, writeTimeout=timeout)

    # def read_serial(self):
    #     reading = self.printer_serial.read()
    #     return reading

    # def write_serial(self, *data):
    #     for args in data:
    #         self.printer_serial.write(args)
    #     # return writing

    # def close_port(self):
    #     self.printer_serial.close()

    # # Print data in the print buffer and feeds one line, this commands sets the print
    # # position to the beginning of the line
    # # LF
    # def print_data_buffer(self):
    #     if automatic_line:  # CR same as LF when automatic line feed is enabled
    #         self.write_serial(13)
    #     else:
    #         self.write_serial(10)

    # # Transmits the selected printer status specified by n in real-time
    # def real_time_status_transmission(self, n):
    #     # n=1 printer status, n=2 offline status
    #     # n=3 error status, n=4 paper roll sensor status
    #     self.write_serial(16, 4, n)

    # # def real_time_request(self):

    # # Set the character spacing for the right side of the character
    # # to [n x 0.125 mm - n x 0.0049"]
    # # default n = 0
    # # ESC SP n
    # def set_right_side_character_spacing(self, n):
    #     self.write_serial(27, 32, n)

    # # ESC ! n
    # def select_print_mode(self, n):  # 3
    #     self.write_serial(27, 33, n)

    # # Set the distance from the beginning of the line to the
    # # position at wich subsequent characters are to be printed
    # # the distance from the beginning of the line to the position at
    # # wich subsequencent characters are to be printed
    # # [(nL + nH x 256) x 0.125 mm]
    # # ESC $ nL nH
    # def set_absolute_print_position(self, nL, nH):
    #     self.write_serial(27, 36, nL, nH)

    # # Turns underline mode on or off, based on the fllowing values
    # # 0,48 = OFF, 1, 49 = ON 1 dot, 2,50 = ON 2 dots
    # def turn_underline_mode(self, n):
    #     self.write_serial(27, 45, n)

    # def setBarcodeHeight(self, val=50):
    #     if val < 1:
    #         val = 1
    #     self.barcodeHeight = val
    #     self.write_serial(29, 104, val)

    # def begin(self):
    #     # Select default line spacing 3.75mm (30 x 0.125mm)
    #     self.write_serial(27, 50)

    # def reset(self):
    #     self.write_serial(27, 64)

    # # print and feed paper n x 0.125mm
    # # ESC J n
    # def print_and_feed(self, n):
    #     self.write_serial(27, 74, n)

    # # select character font
    # # n = 0,48 Font A (12 x 24), n=1,49 font B (9x17)
    # # ESC M n
    # def character_font(self, n):
    #     self.write_serial(27, 77, n)

    # # select international character n = table pag 26 manual
    # # ESC R n
    # def internationa_character_set(self, n):
    #     self.write_serial(27, 82, n)

    # # Aling all the data in one line to the specified position
    # # n = 0,48 LEFT, n = 1,49 Centering, n = 2,50 RIGHT
    # # ESC a n
    # def justification(self, n):
    #     self.write_serial(27, 97, n)

    # # Selects page n from the character code table
    # def character_code(self, n):
    #     self.write_serial(27, 116, n)

    # # Turns upside-down printing mode on or OFF
    # # when the lsb of n is 0 OFF
    # # ESC { n
    # def upside_down_printing(self, n):
    #     self.write_serial(27, 23, n)

    # # def test(self):
    # #     self.write("Hello world!")
    # #     self.feed(2)

    # def testPage(self):
    #     self.write_serial(18, 84)
    #     # self.timeoutSet(
    #     #     self.dotPrintTime * 24 * 26 +
    #     #     self.dotFeedTime * (6 * 26 + 30))
