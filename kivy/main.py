from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import sys
import os
sys.path.append(os.path.abspath("../"))
from src.services.camera_service import PicameraControl
from src.services.receipt_content import ReceiptHeader



class MyGrid(BoxLayout):
    qr_label = ObjectProperty(None)

    def btn(self):
        print("botton press")
        self.qr_label.text = "Botton press"
        cam = PicameraControl()
        cam.close()
        read_from_qr = cam.read_code()
        if read_from_qr[0]:
            text = "Read successful: " + str(read_from_qr[1])
            
        else:
            text = "Fail Reading: " + str(read_from_qr[1])
        self.qr_label.text = text
    def print(self):
        person = ReceiptHeader(9878654524313, None, 1, "demo")
        person.print_header()
        lista = (["QTY", "PRICE", "DESCRIPTION", "TOTAL"],["01", "160,99", "SKIRT", 500.00],["02", "10.33", "COAT", 300.01],["03", "100,99", "SKIRT", 200.00], ["04", "20.01", "SKIRT", 20.02])
        person.print_description(lista, "ejemplo_QR")
        person.print_bottom("Factura de venta N W:B345 \n Autorizacion de Numercion de Facturacion DIAN sistema POS: 12643677863877364 26/09/2019 - Vigencia 24 meses \n ")



class TestApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    TestApp().run()