from PyQt5.uic import compileUi
compileUi("mainwindow.ui", "mainwindow.py", execute=True)
compileUi("controller_frame.ui", "controller_frame.py", execute=True)

from PyQt5.QtWidgets import QFrame, QApplication, QWidget, QMainWindow
import sys
from mainwindow import Ui_MainWindow
import json
import zmq

class client_GUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(client_GUI, self).__init__()
        self.setupUi(self)
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        
        self.pushButton_save.clicked.connect(self.save_config)
        self.pushButton_load.clicked.connect(self.load_config)
        self.pushButton_connect.clicked.connect(self.connect)
        self.pushButton_set_device.clicked.connect(self.set_device)

        self.is_connected = False

        self.verbose("[WELCOME] This program is developed by Chung-You (Gilbert) Shih @ QITI lab, IQC, UWaterloo.", color="green")
        self.verbose("[WELCOME] For more information, please visit https://github.com/senkolab/pll-evalboard-synthesizer", color="green")
        
        self.dict_of_channel_widgets = dict()
        for key in self.__dict__.keys():
            if key[0:15] == "Channel_Widget_":
                self.dict_of_channel_widgets[key] = self.__dict__[key]

        
    def connect(self):
        try:
            self.socket.connect("tcp://" + self.lineEdit_address.text())
            self.is_connected = True
        except zmq.error.ZMQError as err:
            self.verbose("[ZMQERROR] " + str(err), color="red")
            self.is_connected = False


    def set_device(self):
        if not self.is_connected:
            self.verbose("[ERROR] Haven't connect to any device!", color="red")
            return

        data = []
        for ch_widget in self.dict_of_channel_widgets.values():
            if ch_widget.is_configuring_channel():
                data.append(ch_widget.get_data())
        self.verbose("[MSG] "+"Setting the device...")
        self.socket.send_json(data)
        self.verbose("[REPLY] "+self.socket.recv_string(), color="yellow")

    def save_config(self):
        config = dict()
        for key, ch_widget in self.dict_of_channel_widgets.items():
            config[key] = ch_widget.get_form()
 
        config["address"] = self.lineEdit_address.text()

        with open('config.json', 'w') as outfile:
            json.dump(config, outfile, indent=4)
            self.verbose("[MSG] Save Configuration successfully.")

    def load_config(self):
        try:
            with open('config.json', 'r') as infile:
                config = json.load(infile)
        except IOError:
            self.verbose("[IOError] Cannot load configuration file!", color="red")
            return

        for key, ch_widget in self.dict_of_channel_widgets.items():
            ch_widget.set_form(config[key])
 
        self.lineEdit_address.setText(config["address"])
        self.verbose("[MSG] Load Configuration successfully.")
        

    def verbose(self, string, color="white"):
        self.textBrowser.insertHtml("<p style='color:{0}'>".format(color)+string+'<br></p>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = client_GUI()
    program.show()
    sys.exit(app.exec_())
