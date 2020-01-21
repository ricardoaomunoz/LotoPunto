from thermal_print import ThermalPrinter
import time

class PrintPaper():
    def __init__(self):
        self.txt = "print paper"
        self.printer = ThermalPrinter()
        self.printer.hardware_operation('init')
        


class ReceiptHeader(PrintPaper):

    def __init__(self, transaction_number, header_imagen, header_format):
        self.transaction_number = transaction_number
        self.header_imagen = header_imagen
        self.header_format = header_format
        PrintPaper.__init__(self)

    def print_header(self):
        if self.header_imagen:
            self.printer.set_txt(font='a', height=2, align='center')
            self.printer.insert_imagen(self.header_imagen)
            time.sleep(0.1)

        self.printer.set_txt(font='a', height=2, align='left')
        self.printer.insert_raw_txt("BBI COLOMBIA S.A.S NIT: XXXXXXXXXXXXXXXXXXXXXXXXXXXXX \n Somos agentes retenedores de IVA \n direccion:xxxxx \n INVOICE: {} \n\n\n".format(str(self.transaction_number)))



class ReceiptDescription(PrintPaper):

    def __init__(self, description_type, text, data):
        self.description_type = description_type
        self.text = text
        self.data = data
        PrintPaper.__init__(self)

    def print_description(self):
        self.printer.set_txt(font='a', height=2, align='center')
        for i in self.data:
            self.printer.insert_raw_txt("{}     {}      {}      {}\n".format(i[0], i[1], i[2], i[3]))

        self.printer.set_txt()
        self.printer.insert_raw_txt("\n\n")
        self.printer.insert_qr("www.google.com", 6)
        self.printer.cut_paper()

            
        
    


    
