import kivy
kivy.require('1.9.0')

import threading
import sys, time
from socket import *
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder

Builder.load_string("""

<Test>:
    size_hint: .9, .9
    pos_hint: {'center_x': .5, 'center_y': .5}
    do_default_tab: False
    

    TabbedPanelItem:
        text: 'Client'
        GridLayout:
            cols:2
            TextInput:
                id:host
            Label:
                text:"<-- Host Address"
            Label:
                text: 'Message (Leave Empty to send test "x"s)'
            TextInput:
                id:data
            

            TextInput
                id : log
                multiline:True
            Button:
                text:"Send Message"   
                on_press:app.send()
    TabbedPanelItem:
        text: 'Server'
        GridLayout:
            cols:2
            
            Button:
                text:"Start"
                on_press:app.start_ser()
             
            TextInput:
                id:data_rec
                multiline:True
            TextInput
                id : log1
                multiline:True
            Label:
                text:"Server is not running"
                id:state
            

""")


class Test(TabbedPanel):
    pass

class MyConnector(App):



    def build(self):
        self.PORT = 5000
        self.BUFSIZE = 4096
        self.root = Test()
        return self.root

    def cli_send(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.root.ids.host.text, self.PORT))
        if (self.root.ids.data.text == ""):
            s.send(b"This is a Test Messge from the Server side to test the connection. \n PEACE! :)")
            self.root.ids.log.text += "\n Test Message Sent..."
        else:
            s.send(self.root.ids.data.text.encode("utf-8"))
            self.root.ids.log.text += "\n --" + self.root.ids.data.text + "-- Sent..."
        s.close()
    def send(self):
        self.thread = threading.Thread(target=self.cli_send)
        self.thread.start()

    def ser(self):
        self.root.ids.data_rec.text = ""
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', 5000))
        s.listen(1)
        print("listening...")
        self.root.ids.log1.text += "\n Server Starts.. Listening.."
        self.root.ids.state.text = "Server is running"
        while 1:
            conn, (host, remoteport) = s.accept()
            while 1:
                data = conn.recv(self.BUFSIZE)
                self.root.ids.data_rec.text += "\n" + data.decode("utf-8")
                if not data:
                    break
                del data
            conn.send(b'OK\n')
            conn.close()
            self.root.ids.log1.text += "\n Done with" + str(host) + ' port ' + str(remoteport)

    def start_ser(self):

        self.thread = threading.Thread(target=self.ser)
        self.thread.start()





if __name__ == '__main__':
    MyConnector().run()
