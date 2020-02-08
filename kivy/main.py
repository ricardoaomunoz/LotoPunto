from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty



class MyGrid(BoxLayout):
    qr_label = ObjectProperty(None)

    def btn(self):
        print("botton press")
        self.qr_label.text = "Botton press"

class TestApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    TestApp().run()