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
        self.dict_of_channel_widgets={
            "EOM1": self.Channel_Widget_EOM_1,
            "EOM2": self.Channel_Widget_EOM_2,
            "EOM3": self.Channel_Widget_EOM_3,
            "AOM1": self.Channel_Widget_AOM_1,
            "AOM2": self.Channel_Widget_AOM_2,

        }
    def connect(self):
        self.socket.connect("tcp://" + self.lineEdit_address.text())

    def set_device(self):
        data = []
        for ch_widget in self.dict_of_channel_widgets.values():
            if ch_widget.is_configuring_channel():
                data.append(ch_widget.get_data())
        print(data)
        self.socket.send_json(data)
        self.verbose("[REPLY] "+self.socket.recv_string())

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
            self.verbose("[IOError] Cannot load configuration file!")
            return

        for key, ch_widget in self.dict_of_channel_widgets.items():
            ch_widget.set_form(config[key])
 
        self.lineEdit_address.setText(config["address"])
        self.verbose("[MSG] Load Configuration successfully.")
        

    def verbose(self, string):
        self.textBrowser.insertPlainText(string+'\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = client_GUI()
    program.show()
    sys.exit(app.exec_())