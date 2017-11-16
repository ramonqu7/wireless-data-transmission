import kivy

kivy.require('1.9.0')
import os
import time
import random
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
from  kivy.uix.filechooser import FileChooserListView
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

Builder.load_string("""

<Test>:
    size_hint: .9, .9
    pos_hint: {'center_x': .5, 'center_y': .5}
    do_default_tab: False
    
    canvas:
        Color: 
            rgb: [0,0,0]
        Rectangle:
            size: self.size
            pos: self.pos
    TabbedPanelItem:
        text: 'Client'
        GridLayout:
            cols:2
            TextInput:
                id:host 
                size_hint:[0.6,None]
                height:40
                hint_text:"<-- Host Address"
            
            TextInput:
                hint_text:'Message (Leave Empty to send test "x"s)'
                size_hint:[1,None]
                height:300
                id:data
            TextInput
                id: log
                size_hint:[0.2,None]
                height:150
                multiline:True
            Button:
                text:"Send Message"  
                size_hint:[0.2,None]
                height:150
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
                id: log1
                multiline:True
                size_hint:[0.2,None]
                height:150
            Label:
                text:"Server is not running"
                id:state
                size_hint:[0.2,None]
                height:150
            BoxLayout:
                Button:
                    text:"Stop"
                    on_press:app.stop_ser()
    TabbedPanelItem:
        text: 'Send File'
        BoxLayout:
            orientation: 'vertical'
            FileChooser:
                path:"E:/personal_robotics/wireless_data_transmission/PyConn/testFile"
                id: fc
                FileChooserIconLayout
                
            BoxLayout:
                orientation:'vertical'
                BoxLayout:
                    size_hint_y: None
                    height: sp(52)
                    Label:
                        color:[0,0,0,1]
                        canvas.before:
                            Color: 
                                rgb:.6,.6,.6
                            Rectangle:
                                pos:self.pos
                                size:self.size
                        id:fileName
                    
                    Button:
                        text: 'Choose File'
                        on_press: app.fileName()
                BoxLayout:
                    size_hint_y: None   
                    TextInput:
                        hint_text:"Host Address"
                        id: hostAddress
                        size_hint:[1,None]
                        height:100
                    Button:
                        text: "Send"
                        size_hint:[1,None]
                        height:100
                        on_press: app.sendFile()
    TabbedPanelItem:
        text: 'Receive File'
        Label:
            id: rec_file_name
        Button:
            text: "Start Server"
            on_press: app.ser_file_start()
                
            

""")


class Test(TabbedPanel):
    pass


class MyConnector(App):

    def build(self):

        self.PORT = 5000
        self.BUFSIZE = 10000
        self.root = Test()
        return self.root

    def cli_send(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.root.ids.host.text, self.PORT))
        if self.root.ids.data.text == "":
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
        self.ser_run = True
        self.root.ids.data_rec.text = ""
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind(('', 5000))
        self.s.listen(1)
        print("listening...")
        self.root.ids.log1.text += "\n Server Starts.. Listening.."
        self.root.ids.state.text = "Server is running"
        while self.ser_run:
            conn, (host, remoteport) = self.s.accept()
            while self.ser_run:
                if not self.ser_run:
                    break
                data = conn.recv(self.BUFSIZE)
                self.root.ids.data_rec.text += "\n" + data.decode("utf-8")
                if not data:
                    break
                del data
            conn.send(b'OK\n')
            conn.close()
            self.root.ids.log1.text += "\n Done with" + str(host) + ' port ' + str(remoteport)
            if not self.ser_run:
                break
        self.root.ids.state.text = "Server is not running"
        self.root.ids.log1.text += "\n Server Closed"
        self.s.close()

    def start_ser(self):

        self.thread = threading.Thread(target=self.ser)
        self.thread.start()

    def stop_ser(self):
        self.ser_run = False


    def fileName(self):
        print(self.root.ids.fc.selection)
        self.root.ids.fileName.text = (self.root.ids.fc.selection[0]).split('\\')[-1]
        self.fileName = self.root.ids.fc.selection[0]

    def FileSend(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.root.ids.hostAddress.text, self.PORT))
        s.send((self.fileName.split('\\')[-1]).encode("utf-8"))
        data = s.recv(self.BUFSIZE)
        if(data.decode("utf-8") == self.fileName.split('\\')[-1]):
            f = open(self.fileName,'rb')
            l = f.read(self.BUFSIZE)
            while(l):
                s.send(l)
                l = f.read(self.BUFSIZE)
        s.close()
    def file_ser(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', 5000))
        s.listen(5)
        print("listening...")
        conn, (host, remoteport) = s.accept()
        tempName = conn.recv(self.BUFSIZE)
        print(tempName.decode("utf-8"))
        #self.root.ids.rec_file_name.text = str(tempName.decode("utf-8"))
        conn.send(tempName)
        start_time = int(round(time.time()*1000))
        print("start:" +str(start_time))
        fileNameTemp = tempName.decode("utf-8")
        print(fileNameTemp)
        with open(fileNameTemp,"wb") as f:
            while True:
                data = conn.recv(self.BUFSIZE)
                if not data:
                    break
                f.write(data)
        finish_time = int(round(time.time()*1000))
        print("finish:"+str(finish_time))
        print('Transfer Finished')
        print("Time: ",finish_time - start_time, "ms")
        size = os.path.getsize(fileNameTemp)
        print("File Size",size)
        print("Rate", size / ((finish_time - start_time) / 1000) * 0.000008,"Mbps")
        f.close()
        conn.close()

    def sendFile(self):
        thread = threading.Thread(target=self.FileSend)
        thread.start()
    def ser_file_start(self):
        self.thread = threading.Thread(target=self.file_ser)
        self.thread.start()

if __name__ == '__main__':
    MyConnector().run()
