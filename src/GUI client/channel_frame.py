# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'channel_frame.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(500, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Frame.sizePolicy().hasHeightForWidth())
        Frame.setSizePolicy(sizePolicy)
        Frame.setMinimumSize(QtCore.QSize(449, 0))
        self.doubleSpinBox_freq = QtWidgets.QDoubleSpinBox(Frame)
        self.doubleSpinBox_freq.setGeometry(QtCore.QRect(128, 60, 101, 26))
        self.doubleSpinBox_freq.setObjectName("doubleSpinBox_freq")
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setGeometry(QtCore.QRect(246, 67, 26, 17))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(Frame)
        self.label_5.setGeometry(QtCore.QRect(30, 60, 81, 17))
        self.label_5.setObjectName("label_5")
        self.lineEdit_ch_name = QtWidgets.QLineEdit(Frame)
        self.lineEdit_ch_name.setGeometry(QtCore.QRect(128, 19, 311, 25))
        self.lineEdit_ch_name.setObjectName("lineEdit_ch_name")
        self.label_7 = QtWidgets.QLabel(Frame)
        self.label_7.setGeometry(QtCore.QRect(30, 19, 81, 17))
        self.label_7.setObjectName("label_7")
        self.spinBox_atten = QtWidgets.QSpinBox(Frame)
        self.spinBox_atten.setGeometry(QtCore.QRect(128, 102, 101, 26))
        self.spinBox_atten.setObjectName("spinBox_atten")
        self.label_6 = QtWidgets.QLabel(Frame)
        self.label_6.setGeometry(QtCore.QRect(30, 102, 81, 17))
        self.label_6.setObjectName("label_6")
        self.label_4 = QtWidgets.QLabel(Frame)
        self.label_4.setGeometry(QtCore.QRect(246, 103, 16, 17))
        self.label_4.setObjectName("label_4")
        self.checkBox_amp_control = QtWidgets.QCheckBox(Frame)
        self.checkBox_amp_control.setGeometry(QtCore.QRect(320, 100, 126, 23))
        self.checkBox_amp_control.setObjectName("checkBox_amp_control")
        self.checkBox_configure_channel = QtWidgets.QCheckBox(Frame)
        self.checkBox_configure_channel.setGeometry(QtCore.QRect(320, 60, 151, 23))
        self.checkBox_configure_channel.setObjectName("checkBox_configure_channel")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_3.setText(_translate("Frame", "MHz"))
        self.label_5.setText(_translate("Frame", "Frequency"))
        self.label_7.setText(_translate("Frame", "Ch Name"))
        self.label_6.setText(_translate("Frame", "Attenuation"))
        self.label_4.setText(_translate("Frame", "db"))
        self.checkBox_amp_control.setText(_translate("Frame", "Amplitute Control"))
        self.checkBox_configure_channel.setText(_translate("Frame", "Configure Channel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

