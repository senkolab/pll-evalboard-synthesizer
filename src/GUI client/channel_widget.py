from __future__ import division
from channel_frame import Ui_Frame
import sys

from PyQt5.QtWidgets import QFrame, QApplication, QWidget

class Channel_Widget(QFrame, Ui_Frame):
    def __init__(self, central_widget):
        super(Channel_Widget, self).__init__()
        self.setupUi(central_widget)

    def get_data(self):
        data = dict()
        data["name"] = str(self.lineEdit_ch_name.text())
        data["freq"] = int(self.doubleSpinBox_freq.value()*10e6)
        if self.checkBox_amp_control.isChecked():
            data["atten"] = int(self.spinBox_atten.value())
        
    def is_configuring_channel(self):
        if self.checkBox_configure_channel.isChecked():
            return True
        else:
            return False
    
    def get_form(self):
        data = dict()
        data["name"] = str(self.lineEdit_ch_name.text())
        data["freq"] = int(self.doubleSpinBox_freq.value()*10e6)
        data["atten"] = int(self.spinBox_atten.value())
        data["amp_control"] = self.checkBox_amp_control.isChecked()
        data["configure_channel"] = self.checkBox_configure_channel.isChecked()

        return data
    
    def set_form(self, data):
        self.lineEdit_ch_name.setText(data["name"])
        self.doubleSpinBox_freq.setValue(data["freq"]/10e6)
        self.spinBox_atten.setValue(data["atten"])
        self.checkBox_amp_control.setChecked(data["amp_control"])
        self.checkBox_configure_channel.setChecked(data["configure_channel"])




    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    qf = QFrame()
    program = Channel_Widget(qf)
    qf.show()
    sys.exit(app.exec_())