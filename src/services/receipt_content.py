#from thermal_print import ThermalPrinter
from escpos.printer import Usb
import time

class PrintPaper():
    # def __init__(self, left_margin, font, font_size,):
    def __init__(self):
        self.txt = "print paper"
        self.printer = Usb(0x0fe6, 0x811e, 98, 0x82, 0x02) #Setup the printer

        # self.printer.hw('restart')

        # self.printer.set(font='a', height=2, align='center')




class ReceiptHeader(PrintPaper):

    def __init__(self, transaction_number, header_imagen, header_format, type):
        self.transaction_number = transaction_number
        self.header_imagen = header_imagen
        self.header_format = header_format
        PrintPaper.__init__(self)
        self.printer.hw('init')

    def print_header(self):
        if self.header_imagen:
            self.printer.set(font='a', height=1, align='left')
            # self.printer.image()
            self.printer.text("\n")
            # self.printer.image(self.header_imagen, impl="bitImageColumn")
            # self.printer.image()
            self.printer.image(self.header_imagen, high_density_horizontal=True, high_density_vertical=True, impl="graphics")
            self.printer.text("\n")
            time.sleep(0.5)

        self.printer.set(font='a', height=1, align='center')
        self.printer._raw("BBI COLOMBIA S.A.S NIT: XXXXXXXXXXXXXXXXXXXXXXXXXXXXX \n Somos agentes retenedores de IVA \n direccion:xxxxx \n INVOICE: {} \n\n\n".format(str(self.transaction_number)))
        self.printer._raw("------------------------------------------------\n")
    def print_description(self, data):
        
        total = 0
        tax = 6
        # self.printer.set(font='a', height=2, align='center')
        for i in data:
            print(type(i[3]))
            if type(i[3]) == int or type(i[3]) == float:
                total = total + i[3]
            print("i", i)
            self.printer._raw("{:7}     {:7}      {:7}      {:7}\n".format(i[0], i[1], i[2], i[3]))
        self.printer._raw("------------------------------------------------\n")
        self.printer.set(font='a', height=1, align='right')
        self.printer._raw("{:>7}: {:>9}\n".format("TOTAL", total))
        self.printer._raw("{:>7}: {:>9}%\n".format("TAX", tax))
        amount = (total + ((tax/100)*total))
        self.printer._raw("{:>7}: {:>9}\n".format("AMOUNT", amount))



        self.printer.set()
        self.printer._raw("\n\n")
        self.printer.qr("www.lotopunto.com", size=6)
        rsume_time= time.time() + 0.3
        while (time.time() - rsume_time) < 0: pass

    def print_bottom(self, data):
        self.printer._raw("------------------------------------------------\n")
        self.printer.set(font='a', height=1, align='left')
        self.printer._raw("{}".format(data))

        self.printer.cut()

class ReceiptDescription(PrintPaper):

    def __init__(self, description_type, text, data):
        self.description_type = description_type
        self.text = text
        self.data = data
        PrintPaper.__init__(self)

    def print_description(self):
        # self.printer.set(font='a', height=2, align='center')
        for i in self.data:
            print("i", i)
            self.printer._raw("{}     {}      {}      {}\n".format(i[0], i[1], i[2], i[3]))

        self.printer.set()
        self.printer._raw("\n\n")
        self.printer.qr("www.google.com", size=6)
        self.printer.qr("www.google.com", size=8)
        self.printer.qr("www.google.com", size=10)
        self.printer.qr("www.google.com", size=12)
        self.printer.qr("www.google.com", size=14)
        self.printer.cut()







