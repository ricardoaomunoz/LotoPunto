from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from src.services.camera_service import PicameraControl



class MyGrid(BoxLayout):
    qr_label = ObjectProperty(None)

    def btn(self):
        print("botton press")
        self.qr_label.text = "Botton press"
        cam = PicameraControl()
        read_from_qr = cam.read_code()
        if read_from_qr[0]:
            text = "Read successful: " + str(read_from_qr[1])
            
        else:
            text = "Fail Reading: " + str(read_from_qr[1])
        self.qr_label.text = text

class TestApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    TestApp().run()