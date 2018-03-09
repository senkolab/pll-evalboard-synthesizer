from PyQt5.QtWidgets import QFrame, QApplication, QWidget, QMainWindow
import sys
from mainwindow import Ui_MainWindow
import json

class client_GUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(client_GUI, self).__init__()
        self.setupUi(self)
        self.pushButton_save.clicked.connect(self.save_config)
        self.pushButton_load.clicked.connect(self.load_config)

    def save_config(self):
        config = dict()
        config["EOM1"] = self.Channel_Widget_EOM_1.get_form()
        config["EOM2"] = self.Channel_Widget_EOM_2.get_form()
        config["EOM3"] = self.Channel_Widget_EOM_3.get_form()
        config["AOM1"] = self.Channel_Widget_AOM_1.get_form()
        config["AOM2"] = self.Channel_Widget_AOM_2.get_form()
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

        self.Channel_Widget_EOM_1.set_form(config["EOM1"])
        self.Channel_Widget_EOM_2.set_form(config["EOM2"])
        self.Channel_Widget_EOM_3.set_form(config["EOM3"])
        self.Channel_Widget_AOM_1.set_form(config["AOM1"])
        self.Channel_Widget_AOM_2.set_form(config["AOM2"])
        self.lineEdit_address.setText(config["address"])
        self.verbose("[MSG] Load Configuration successfully.")
        

    def verbose(self, string):
        self.textBrowser.insertPlainText(string+'\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = client_GUI()
    program.show()
    sys.exit(app.exec_())
