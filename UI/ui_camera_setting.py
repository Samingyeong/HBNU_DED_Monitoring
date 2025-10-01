# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingUVGCpW.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Cam_set(object):
    def setupUi(self, Cam_set):
        if not Cam_set.objectName():
            Cam_set.setObjectName(u"Cam_set")
        Cam_set.resize(640, 480)
        self.gridLayout = QGridLayout(Cam_set)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(Cam_set)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.tabWidget = QTabWidget(Cam_set)
        self.tabWidget.setObjectName(u"tabWidget")
        self.Camera_setting = QWidget()
        self.Camera_setting.setObjectName(u"Camera_setting")
        self.gridLayout_4 = QGridLayout(self.Camera_setting)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.Default_parameters = QGroupBox(self.Camera_setting)
        self.Default_parameters.setObjectName(u"Default_parameters")
        self.gridLayout_2 = QGridLayout(self.Default_parameters)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_gain = QLabel(self.Default_parameters)
        self.label_gain.setObjectName(u"label_gain")

        self.gridLayout_2.addWidget(self.label_gain, 1, 0, 1, 1)

        self.label_exposure_7 = QLabel(self.Default_parameters)
        self.label_exposure_7.setObjectName(u"label_exposure_7")
        self.label_exposure_7.setMaximumSize(QSize(50, 16777215))
        self.label_exposure_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_exposure_7, 11, 2, 1, 1)

        self.label_exposure_6 = QLabel(self.Default_parameters)
        self.label_exposure_6.setObjectName(u"label_exposure_6")
        self.label_exposure_6.setMaximumSize(QSize(50, 16777215))
        self.label_exposure_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_exposure_6, 10, 2, 1, 1)

        self.fps = QSpinBox(self.Default_parameters)
        self.fps.setObjectName(u"fps")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fps.sizePolicy().hasHeightForWidth())
        self.fps.setSizePolicy(sizePolicy)
        self.fps.setMinimumSize(QSize(50, 30))
        self.fps.setAlignment(Qt.AlignCenter)
        self.fps.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.fps.setMinimum(1)
        self.fps.setMaximum(200)
        self.fps.setValue(30)

        self.gridLayout_2.addWidget(self.fps, 11, 1, 1, 1)

        self.threshold = QSpinBox(self.Default_parameters)
        self.threshold.setObjectName(u"threshold")
        sizePolicy.setHeightForWidth(self.threshold.sizePolicy().hasHeightForWidth())
        self.threshold.setSizePolicy(sizePolicy)
        self.threshold.setMinimumSize(QSize(50, 30))
        self.threshold.setAlignment(Qt.AlignCenter)
        self.threshold.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.threshold.setMaximum(255)
        self.threshold.setValue(250)

        self.gridLayout_2.addWidget(self.threshold, 10, 1, 1, 1)

        self.label_exposure = QLabel(self.Default_parameters)
        self.label_exposure.setObjectName(u"label_exposure")

        self.gridLayout_2.addWidget(self.label_exposure, 0, 0, 1, 1)

        self.label_exposure_5 = QLabel(self.Default_parameters)
        self.label_exposure_5.setObjectName(u"label_exposure_5")
        self.label_exposure_5.setMaximumSize(QSize(50, 16777215))
        self.label_exposure_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_exposure_5, 8, 2, 1, 1)

        self.label_3 = QLabel(self.Default_parameters)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 8, 0, 1, 1)

        self.image_width = QSpinBox(self.Default_parameters)
        self.image_width.setObjectName(u"image_width")
        sizePolicy.setHeightForWidth(self.image_width.sizePolicy().hasHeightForWidth())
        self.image_width.setSizePolicy(sizePolicy)
        self.image_width.setMinimumSize(QSize(50, 30))
        self.image_width.setAlignment(Qt.AlignCenter)
        self.image_width.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.image_width.setMinimum(100)
        self.image_width.setMaximum(10000)
        self.image_width.setValue(1920)

        self.gridLayout_2.addWidget(self.image_width, 0, 1, 1, 1)

        self.label_5 = QLabel(self.Default_parameters)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 11, 0, 1, 1)

        self.image_height = QSpinBox(self.Default_parameters)
        self.image_height.setObjectName(u"image_height")
        sizePolicy.setHeightForWidth(self.image_height.sizePolicy().hasHeightForWidth())
        self.image_height.setSizePolicy(sizePolicy)
        self.image_height.setMinimumSize(QSize(50, 30))
        self.image_height.setAlignment(Qt.AlignCenter)
        self.image_height.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.image_height.setMinimum(100)
        self.image_height.setMaximum(10000)
        self.image_height.setValue(1200)

        self.gridLayout_2.addWidget(self.image_height, 1, 1, 1, 1)

        self.pixel_size = QDoubleSpinBox(self.Default_parameters)
        self.pixel_size.setObjectName(u"pixel_size")
        sizePolicy.setHeightForWidth(self.pixel_size.sizePolicy().hasHeightForWidth())
        self.pixel_size.setSizePolicy(sizePolicy)
        self.pixel_size.setMinimumSize(QSize(50, 30))
        self.pixel_size.setAlignment(Qt.AlignCenter)
        self.pixel_size.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pixel_size.setDecimals(6)
        self.pixel_size.setMaximum(100.000000000000000)
        self.pixel_size.setSingleStep(0.100000000000000)
        self.pixel_size.setValue(0.008350000000000)

        self.gridLayout_2.addWidget(self.pixel_size, 8, 1, 1, 1)

        self.label_exposure_3 = QLabel(self.Default_parameters)
        self.label_exposure_3.setObjectName(u"label_exposure_3")
        self.label_exposure_3.setMaximumSize(QSize(50, 16777215))
        self.label_exposure_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_exposure_3, 0, 2, 1, 1)

        self.label_4 = QLabel(self.Default_parameters)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 10, 0, 1, 1)

        self.label_exposure_4 = QLabel(self.Default_parameters)
        self.label_exposure_4.setObjectName(u"label_exposure_4")
        self.label_exposure_4.setMaximumSize(QSize(50, 16777215))
        self.label_exposure_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_exposure_4, 1, 2, 1, 1)


        self.gridLayout_4.addWidget(self.Default_parameters, 0, 0, 1, 1)

        self.camera_parameters = QGroupBox(self.Camera_setting)
        self.camera_parameters.setObjectName(u"camera_parameters")
        self.gridLayout_3 = QGridLayout(self.camera_parameters)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gamma = QDoubleSpinBox(self.camera_parameters)
        self.gamma.setObjectName(u"gamma")
        sizePolicy.setHeightForWidth(self.gamma.sizePolicy().hasHeightForWidth())
        self.gamma.setSizePolicy(sizePolicy)
        self.gamma.setMinimumSize(QSize(50, 30))
        self.gamma.setAlignment(Qt.AlignCenter)
        self.gamma.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.gamma.setMaximum(4.000000000000000)
        self.gamma.setSingleStep(0.100000000000000)
        self.gamma.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.gamma, 8, 1, 1, 1)

        self.label_exposure_2 = QLabel(self.camera_parameters)
        self.label_exposure_2.setObjectName(u"label_exposure_2")

        self.gridLayout_3.addWidget(self.label_exposure_2, 0, 0, 1, 1)

        self.exposure_time = QSpinBox(self.camera_parameters)
        self.exposure_time.setObjectName(u"exposure_time")
        sizePolicy.setHeightForWidth(self.exposure_time.sizePolicy().hasHeightForWidth())
        self.exposure_time.setSizePolicy(sizePolicy)
        self.exposure_time.setMinimumSize(QSize(50, 30))
        self.exposure_time.setAlignment(Qt.AlignCenter)
        self.exposure_time.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.exposure_time.setMinimum(19)
        self.exposure_time.setMaximum(9999999)
        self.exposure_time.setValue(500)

        self.gridLayout_3.addWidget(self.exposure_time, 0, 1, 1, 1)

        self.digital_shift = QSpinBox(self.camera_parameters)
        self.digital_shift.setObjectName(u"digital_shift")
        sizePolicy.setHeightForWidth(self.digital_shift.sizePolicy().hasHeightForWidth())
        self.digital_shift.setSizePolicy(sizePolicy)
        self.digital_shift.setMinimumSize(QSize(50, 30))
        self.digital_shift.setAlignment(Qt.AlignCenter)
        self.digital_shift.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.digital_shift.setMaximum(4)

        self.gridLayout_3.addWidget(self.digital_shift, 11, 1, 1, 1)

        self.gain = QDoubleSpinBox(self.camera_parameters)
        self.gain.setObjectName(u"gain")
        sizePolicy.setHeightForWidth(self.gain.sizePolicy().hasHeightForWidth())
        self.gain.setSizePolicy(sizePolicy)
        self.gain.setMinimumSize(QSize(50, 30))
        self.gain.setAlignment(Qt.AlignCenter)
        self.gain.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.gain.setMaximum(48.000000000000000)
        self.gain.setSingleStep(0.100000000000000)

        self.gridLayout_3.addWidget(self.gain, 1, 1, 1, 1)

        self.label_gain_2 = QLabel(self.camera_parameters)
        self.label_gain_2.setObjectName(u"label_gain_2")

        self.gridLayout_3.addWidget(self.label_gain_2, 1, 0, 1, 1)

        self.black_level = QDoubleSpinBox(self.camera_parameters)
        self.black_level.setObjectName(u"black_level")
        sizePolicy.setHeightForWidth(self.black_level.sizePolicy().hasHeightForWidth())
        self.black_level.setSizePolicy(sizePolicy)
        self.black_level.setMinimumSize(QSize(50, 30))
        self.black_level.setAlignment(Qt.AlignCenter)
        self.black_level.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.black_level.setMaximum(1023.750000000000000)
        self.black_level.setSingleStep(0.100000000000000)

        self.gridLayout_3.addWidget(self.black_level, 10, 1, 1, 1)

        self.label_8 = QLabel(self.camera_parameters)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 8, 0, 1, 1)

        self.label_7 = QLabel(self.camera_parameters)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 10, 0, 1, 1)

        self.label_6 = QLabel(self.camera_parameters)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 11, 0, 1, 1)


        self.gridLayout_4.addWidget(self.camera_parameters, 0, 1, 1, 1)

        self.tabWidget.addTab(self.Camera_setting, "")
        self.Pyrometer_setting = QWidget()
        self.Pyrometer_setting.setObjectName(u"Pyrometer_setting")
        self.gridLayout_13 = QGridLayout(self.Pyrometer_setting)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.Default_parameters_4 = QGroupBox(self.Pyrometer_setting)
        self.Default_parameters_4.setObjectName(u"Default_parameters_4")
        self.gridLayout_8 = QGridLayout(self.Default_parameters_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_gain_5 = QLabel(self.Default_parameters_4)
        self.label_gain_5.setObjectName(u"label_gain_5")

        self.gridLayout_8.addWidget(self.label_gain_5, 1, 0, 1, 1)

        self.laser_ip = QLineEdit(self.Default_parameters_4)
        self.laser_ip.setObjectName(u"laser_ip")
        self.laser_ip.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.laser_ip, 0, 3, 1, 2)

        self.label_exposure_22 = QLabel(self.Default_parameters_4)
        self.label_exposure_22.setObjectName(u"label_exposure_22")

        self.gridLayout_8.addWidget(self.label_exposure_22, 0, 0, 1, 1)

        self.laser_port = QSpinBox(self.Default_parameters_4)
        self.laser_port.setObjectName(u"laser_port")
        self.laser_port.setAlignment(Qt.AlignCenter)
        self.laser_port.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.laser_port.setMaximum(500000)
        self.laser_port.setValue(5100)

        self.gridLayout_8.addWidget(self.laser_port, 1, 3, 1, 2)


        self.gridLayout_13.addWidget(self.Default_parameters_4, 0, 1, 1, 1)

        self.Default_parameters_8 = QGroupBox(self.Pyrometer_setting)
        self.Default_parameters_8.setObjectName(u"Default_parameters_8")
        self.gridLayout_14 = QGridLayout(self.Default_parameters_8)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_gain_9 = QLabel(self.Default_parameters_8)
        self.label_gain_9.setObjectName(u"label_gain_9")

        self.gridLayout_14.addWidget(self.label_gain_9, 2, 0, 1, 1)

        self.cnc_ip = QLineEdit(self.Default_parameters_8)
        self.cnc_ip.setObjectName(u"cnc_ip")
        self.cnc_ip.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.cnc_ip, 0, 3, 1, 2)

        self.label_exposure_23 = QLabel(self.Default_parameters_8)
        self.label_exposure_23.setObjectName(u"label_exposure_23")

        self.gridLayout_14.addWidget(self.label_exposure_23, 0, 0, 1, 1)

        self.cnc_port = QSpinBox(self.Default_parameters_8)
        self.cnc_port.setObjectName(u"cnc_port")
        self.cnc_port.setAlignment(Qt.AlignCenter)
        self.cnc_port.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.cnc_port.setMaximum(500000)
        self.cnc_port.setValue(10001)

        self.gridLayout_14.addWidget(self.cnc_port, 2, 3, 1, 2)


        self.gridLayout_13.addWidget(self.Default_parameters_8, 1, 1, 1, 1)

        self.Default_parameters_6 = QGroupBox(self.Pyrometer_setting)
        self.Default_parameters_6.setObjectName(u"Default_parameters_6")
        self.gridLayout_11 = QGridLayout(self.Default_parameters_6)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_gain_7 = QLabel(self.Default_parameters_6)
        self.label_gain_7.setObjectName(u"label_gain_7")

        self.gridLayout_11.addWidget(self.label_gain_7, 1, 0, 1, 1)

        self.label_exposure_34 = QLabel(self.Default_parameters_6)
        self.label_exposure_34.setObjectName(u"label_exposure_34")

        self.gridLayout_11.addWidget(self.label_exposure_34, 0, 0, 1, 1)

        self.pyro_com = QComboBox(self.Default_parameters_6)
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.addItem("")
        self.pyro_com.setObjectName(u"pyro_com")

        self.gridLayout_11.addWidget(self.pyro_com, 0, 1, 1, 2)

        self.label_22 = QLabel(self.Default_parameters_6)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_11.addWidget(self.label_22, 11, 0, 1, 1)

        self.label_21 = QLabel(self.Default_parameters_6)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_11.addWidget(self.label_21, 8, 0, 1, 1)

        self.label_23 = QLabel(self.Default_parameters_6)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_11.addWidget(self.label_23, 10, 0, 1, 1)

        self.label_27 = QLabel(self.Default_parameters_6)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_11.addWidget(self.label_27, 12, 0, 1, 1)

        self.pyro_timeout = QSpinBox(self.Default_parameters_6)
        self.pyro_timeout.setObjectName(u"pyro_timeout")
        sizePolicy.setHeightForWidth(self.pyro_timeout.sizePolicy().hasHeightForWidth())
        self.pyro_timeout.setSizePolicy(sizePolicy)
        self.pyro_timeout.setMinimumSize(QSize(50, 30))
        self.pyro_timeout.setAlignment(Qt.AlignCenter)
        self.pyro_timeout.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pyro_timeout.setMinimum(1)
        self.pyro_timeout.setMaximum(10)
        self.pyro_timeout.setValue(5)
        self.pyro_timeout.setDisplayIntegerBase(10)

        self.gridLayout_11.addWidget(self.pyro_timeout, 12, 2, 1, 1)

        self.pyro_baudrate = QComboBox(self.Default_parameters_6)
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.addItem("")
        self.pyro_baudrate.setObjectName(u"pyro_baudrate")

        self.gridLayout_11.addWidget(self.pyro_baudrate, 1, 1, 1, 2)

        self.pyro_parity = QComboBox(self.Default_parameters_6)
        self.pyro_parity.addItem("")
        self.pyro_parity.addItem("")
        self.pyro_parity.addItem("")
        self.pyro_parity.addItem("")
        self.pyro_parity.addItem("")
        self.pyro_parity.setObjectName(u"pyro_parity")

        self.gridLayout_11.addWidget(self.pyro_parity, 8, 1, 1, 2)

        self.pyro_bytesize = QComboBox(self.Default_parameters_6)
        self.pyro_bytesize.addItem("")
        self.pyro_bytesize.addItem("")
        self.pyro_bytesize.addItem("")
        self.pyro_bytesize.setObjectName(u"pyro_bytesize")

        self.gridLayout_11.addWidget(self.pyro_bytesize, 11, 1, 1, 2)

        self.pyro_stopbit = QComboBox(self.Default_parameters_6)
        self.pyro_stopbit.addItem("")
        self.pyro_stopbit.addItem("")
        self.pyro_stopbit.setObjectName(u"pyro_stopbit")

        self.gridLayout_11.addWidget(self.pyro_stopbit, 10, 1, 1, 2)


        self.gridLayout_13.addWidget(self.Default_parameters_6, 0, 2, 2, 1)

        self.tabWidget.addTab(self.Pyrometer_setting, "")

        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)


        self.retranslateUi(Cam_set)
        self.buttonBox.accepted.connect(Cam_set.accept)
        self.buttonBox.rejected.connect(Cam_set.reject)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Cam_set)
    # setupUi

    def retranslateUi(self, Cam_set):
        Cam_set.setWindowTitle(QCoreApplication.translate("Cam_set", u"Dialog", None))
        self.Default_parameters.setTitle(QCoreApplication.translate("Cam_set", u"Communication", None))
        self.label_gain.setText(QCoreApplication.translate("Cam_set", u"Image Height", None))
        self.label_exposure_7.setText(QCoreApplication.translate("Cam_set", u"fps", None))
        self.label_exposure_6.setText(QCoreApplication.translate("Cam_set", u"0-255", None))
        self.label_exposure.setText(QCoreApplication.translate("Cam_set", u"Image Width", None))
        self.label_exposure_5.setText(QCoreApplication.translate("Cam_set", u"mm/pix", None))
        self.label_3.setText(QCoreApplication.translate("Cam_set", u"Pixel Size", None))
        self.label_5.setText(QCoreApplication.translate("Cam_set", u"frame per sec.", None))
        self.label_exposure_3.setText(QCoreApplication.translate("Cam_set", u"pixel", None))
        self.label_4.setText(QCoreApplication.translate("Cam_set", u"Threshold", None))
        self.label_exposure_4.setText(QCoreApplication.translate("Cam_set", u"pixel", None))
        self.camera_parameters.setTitle(QCoreApplication.translate("Cam_set", u"Camera parameters", None))
        self.label_exposure_2.setText(QCoreApplication.translate("Cam_set", u"Exposure Time [us]", None))
        self.label_gain_2.setText(QCoreApplication.translate("Cam_set", u"Gain [dB]", None))
        self.label_8.setText(QCoreApplication.translate("Cam_set", u"Gamma", None))
        self.label_7.setText(QCoreApplication.translate("Cam_set", u"Balck Level [DN]", None))
        self.label_6.setText(QCoreApplication.translate("Cam_set", u"Digital Shift", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Camera_setting), QCoreApplication.translate("Cam_set", u"Camera", None))
        self.Default_parameters_4.setTitle(QCoreApplication.translate("Cam_set", u"Laser", None))
        self.label_gain_5.setText(QCoreApplication.translate("Cam_set", u"Port", None))
        self.laser_ip.setText(QCoreApplication.translate("Cam_set", u"192.168.0.1", None))
        self.label_exposure_22.setText(QCoreApplication.translate("Cam_set", u"IP", None))
        self.Default_parameters_8.setTitle(QCoreApplication.translate("Cam_set", u"CNC", None))
        self.label_gain_9.setText(QCoreApplication.translate("Cam_set", u"Port", None))
        self.cnc_ip.setText(QCoreApplication.translate("Cam_set", u"192.168.0.1", None))
        self.label_exposure_23.setText(QCoreApplication.translate("Cam_set", u"IP", None))
        self.Default_parameters_6.setTitle(QCoreApplication.translate("Cam_set", u"Pyrometer", None))
        self.label_gain_7.setText(QCoreApplication.translate("Cam_set", u"Baud Rate", None))
        self.label_exposure_34.setText(QCoreApplication.translate("Cam_set", u"Port", None))
        self.pyro_com.setItemText(0, QCoreApplication.translate("Cam_set", u"COM1", None))
        self.pyro_com.setItemText(1, QCoreApplication.translate("Cam_set", u"COM2", None))
        self.pyro_com.setItemText(2, QCoreApplication.translate("Cam_set", u"COM3", None))
        self.pyro_com.setItemText(3, QCoreApplication.translate("Cam_set", u"COM4", None))
        self.pyro_com.setItemText(4, QCoreApplication.translate("Cam_set", u"COM5", None))
        self.pyro_com.setItemText(5, QCoreApplication.translate("Cam_set", u"COM6", None))
        self.pyro_com.setItemText(6, QCoreApplication.translate("Cam_set", u"COM7", None))
        self.pyro_com.setItemText(7, QCoreApplication.translate("Cam_set", u"COM8", None))
        self.pyro_com.setItemText(8, QCoreApplication.translate("Cam_set", u"COM9", None))
        self.pyro_com.setItemText(9, QCoreApplication.translate("Cam_set", u"COM10", None))
        self.pyro_com.setItemText(10, QCoreApplication.translate("Cam_set", u"COM11", None))
        self.pyro_com.setItemText(11, QCoreApplication.translate("Cam_set", u"COM12", None))
        self.pyro_com.setItemText(12, QCoreApplication.translate("Cam_set", u"COM13", None))
        self.pyro_com.setItemText(13, QCoreApplication.translate("Cam_set", u"COM14", None))
        self.pyro_com.setItemText(14, QCoreApplication.translate("Cam_set", u"COM15", None))

        self.pyro_com.setCurrentText(QCoreApplication.translate("Cam_set", u"COM12", None))
        self.label_22.setText(QCoreApplication.translate("Cam_set", u"Byte Size", None))
        self.label_21.setText(QCoreApplication.translate("Cam_set", u"Parity", None))
        self.label_23.setText(QCoreApplication.translate("Cam_set", u"Stop Bit", None))
        self.label_27.setText(QCoreApplication.translate("Cam_set", u"Time Out", None))
        self.pyro_baudrate.setItemText(0, QCoreApplication.translate("Cam_set", u"1200", None))
        self.pyro_baudrate.setItemText(1, QCoreApplication.translate("Cam_set", u"2400", None))
        self.pyro_baudrate.setItemText(2, QCoreApplication.translate("Cam_set", u"4800", None))
        self.pyro_baudrate.setItemText(3, QCoreApplication.translate("Cam_set", u"9600", None))
        self.pyro_baudrate.setItemText(4, QCoreApplication.translate("Cam_set", u"19200", None))
        self.pyro_baudrate.setItemText(5, QCoreApplication.translate("Cam_set", u"38400", None))
        self.pyro_baudrate.setItemText(6, QCoreApplication.translate("Cam_set", u"57600", None))
        self.pyro_baudrate.setItemText(7, QCoreApplication.translate("Cam_set", u"115200", None))
        self.pyro_baudrate.setItemText(8, QCoreApplication.translate("Cam_set", u"460800", None))

        self.pyro_baudrate.setCurrentText(QCoreApplication.translate("Cam_set", u"115200", None))
        self.pyro_parity.setItemText(0, QCoreApplication.translate("Cam_set", u"None", None))
        self.pyro_parity.setItemText(1, QCoreApplication.translate("Cam_set", u"Odd", None))
        self.pyro_parity.setItemText(2, QCoreApplication.translate("Cam_set", u"Even", None))
        self.pyro_parity.setItemText(3, QCoreApplication.translate("Cam_set", u"Mark", None))
        self.pyro_parity.setItemText(4, QCoreApplication.translate("Cam_set", u"Space", None))

        self.pyro_parity.setCurrentText(QCoreApplication.translate("Cam_set", u"Even", None))
        self.pyro_bytesize.setItemText(0, QCoreApplication.translate("Cam_set", u"8", None))
        self.pyro_bytesize.setItemText(1, QCoreApplication.translate("Cam_set", u"16", None))
        self.pyro_bytesize.setItemText(2, QCoreApplication.translate("Cam_set", u"32", None))

        self.pyro_stopbit.setItemText(0, QCoreApplication.translate("Cam_set", u"0", None))
        self.pyro_stopbit.setItemText(1, QCoreApplication.translate("Cam_set", u"1", None))

        self.pyro_stopbit.setCurrentText(QCoreApplication.translate("Cam_set", u"1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Pyrometer_setting), QCoreApplication.translate("Cam_set", u"Communication", None))
    # retranslateUi

