from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
import sys
import os
sys.path.append(os.path.abspath("../"))
import redis
import json
import socket 
# from src.services.camera_service import PicameraControl
# from src.services.receipt_content import ReceiptHeader

readPort = 8080
writePort = 8081
localIP = "127.0.0.1"
bufferSize = 1024


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def write_udp(message):
    msg = str.encode(message)
    print(f"send udp msg: {msg}")
    UDPServerSocket.sendto(msg, (localIP, int(writePort)))
    

class MyGrid(FloatLayout):
    qr_read_label = ObjectProperty(None)
    transaction_number_label = ObjectProperty(None)
    set_qr_label = ObjectProperty(None)
    credit = ObjectProperty(None)
    payout_value = ObjectProperty(None)
    payout_label = ObjectProperty(None)
    error_message = ObjectProperty(None)
    alert_message = ObjectProperty(None)
    warning_message = ObjectProperty(None)
    q1 = ObjectProperty(None)
    q2 = ObjectProperty(None)
    q3 = ObjectProperty(None)
    q4 = ObjectProperty(None)
    q5 = ObjectProperty(None)
    q6 = ObjectProperty(None)
    r1 = ObjectProperty(None)
    r2 = ObjectProperty(None)
    r3 = ObjectProperty(None)
    r4 = ObjectProperty(None)
    r5 = ObjectProperty(None)
    r6 = ObjectProperty(None)

    r = redis.Redis(host='localhost', port=6379, db=0)
    p_cred = r.pubsub()
    p_valu = r.pubsub()
    p_mess = r.pubsub()

    msg_err = ""
    msg_ale = ""
    msg_war = ""


    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        def credit_msg(message):
            data = message['data']
            data = json.loads(data)
            credit = data['credit']
            self.credit.text = '$ ' + str(credit)

        def value_msg(message):
            data = message['data']
            data = json.loads(data)
            for i in range(1,7):
                if "channel"+str(i) in data:
                    if i == 1:
                        self.r1.text = data["channel"+str(i)][0]["route"]
                        self.q1.text = str(data["channel"+str(i)][0]["quantity"])
                    elif i == 2:
                        self.r2.text = data["channel"+str(i)][0]["route"]
                        self.q2.text = str(data["channel"+str(i)][0]["quantity"])
                    elif i == 3:
                        self.r3.text = data["channel"+str(i)][0]["route"]
                        self.q3.text = str(data["channel"+str(i)][0]["quantity"])
                    elif i == 4:
                        self.r4.text = data["channel"+str(i)][0]["route"]
                        self.q4.text = str(data["channel"+str(i)][0]["quantity"])
                    elif i == 5:
                        self.r5.text = data["channel"+str(i)][0]["route"]
                        self.q5.text = str(data["channel"+str(i)][0]["quantity"])
                    elif i == 6:
                        self.r6.text = data["channel"+str(i)][0]["route"]
                        self.q6.text = str(data["channel"+str(i)][0]["quantity"])
        def msgs(message):
            print(f"getting msg {message}")
            ch = message['channel']
            data = message['data']
            data = data.decode()
            ch = ch.decode()
            if ch == "message-error":
                self.msg_err = self.msg_err + data
                self.error_message.text = self.msg_err
            elif ch == "message-alert":
                self.msg_ale = self.msg_ale + data
                self.alert_message.text = self.msg_ale
            elif ch == "message-warning":
                self.msg_war = self.msg_war + data
                self.warning_message.text = self.msg_war
            

        self.p_cred.subscribe(**{'money-insert': credit_msg})
        self.p_valu.subscribe(**{'value-level': value_msg})
        self.p_mess.psubscribe(**{'message-*': msgs})

        self.p_cred.run_in_thread(sleep_time=0.001)
        self.p_valu.run_in_thread(sleep_time=0.001)
        self.p_mess.run_in_thread(sleep_time=0.001)


    def print_receipt(self):
        transaction_number = self.transaction_number_label.text
        set_qr = self.set_qr_label.text
        if transaction_number == "":
            transaction_number = "1234567890"
        if set_qr == "":
            set_qr = "www.lotopunto.com"
        print(f"Transaction number: {transaction_number}.")
        print(f"Convert this: {set_qr}.")
        print(f"Transaction number: {type(transaction_number)}.")
        print(f"Convert this: {type(set_qr)}.")
        # person = ReceiptHeader(transaction_number, None, 1, "demo")
        # person.print_header()
        # lista = (["QTY", "PRICE", "DESCRIPTION", "TOTAL"],["01", "160,99", "SKIRT", 500.00],["02", "10.33", "COAT", 300.01],["03", "100,99", "SKIRT", 200.00], ["04", "20.01", "SKIRT", 20.02])
        # person.print_description(lista, set_qr)
        # person.print_bottom("Factura de venta N W:B345 \n Autorizacion de Numercion de Facturacion DIAN sistema POS: 12643677863877364 26/09/2019 - Vigencia 24 meses \n ")
        

    def read_qr(self):
        print(f"Text read: {self.qr_read_label.text}")
        # cam = PicameraControl()
        # cam.close()
        # read_from_qr = cam.read_code()
        # if read_from_qr[0]:
        #     text = "Read successful: " + str(read_from_qr[1])
        # else:
        #     text = "Fail Reading: " + str(read_from_qr[1])
        # self.qr_read_label.text = text

    def  make_payout(self):
        value = self.payout_value.text
        print(f"Make payout..{value}")
        if value == '':
            self.payout_label.text = "Insert Value to payout"
        else:
            try:
                value = int(value)
            except Exception as err:
                self.payout_label.text = "Invalid Value"
                raise
            value = int(value/1000)
            if value > 255:
                self.payout_label.text = "Invalid Value"
            else:
                msg = 'p'+chr(value)
                write_udp(msg)

        


class TestApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    TestApp().run()
