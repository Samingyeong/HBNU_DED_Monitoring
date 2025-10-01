# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'template.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import QRect, QSize, Qt, QMetaObject, QCoreApplication
from PySide2.QtGui import QFont, QIcon, QPixmap
from PySide2.QtWidgets import (
    QWidget, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QGridLayout, QFrame, QPushButton, QSpacerItem,
    QDateTimeEdit, QAbstractSpinBox, QGroupBox, QCheckBox, QLayout,
    QOpenGLWidget
)
from pyqtgraph import PlotWidget

from UI import main_logo_rc
from UI import icon_rc
from UI import setting_rc

class Ui_DED_Monitoring(object):
    def setupUi(self, DED_Monitoring):
        if not DED_Monitoring.objectName():
            DED_Monitoring.setObjectName(u"DED_Monitoring")
        DED_Monitoring.resize(1800, 1000)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DED_Monitoring.sizePolicy().hasHeightForWidth())
        DED_Monitoring.setSizePolicy(sizePolicy)
        DED_Monitoring.setMinimumSize(QSize(1300, 840))
        DED_Monitoring.setMaximumSize(QSize(1800, 1000))
        font = QFont()
        font.setFamily(u"Times New Roman")
        font.setPointSize(12)
        DED_Monitoring.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icon/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        DED_Monitoring.setWindowIcon(icon)
        self.centralwidget = QWidget(DED_Monitoring)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_6 = QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.Main_frame = QFrame(self.centralwidget)
        self.Main_frame.setObjectName(u"Main_frame")
        sizePolicy.setHeightForWidth(self.Main_frame.sizePolicy().hasHeightForWidth())
        self.Main_frame.setSizePolicy(sizePolicy)
        self.Main_frame.setFrameShape(QFrame.NoFrame)
        self.Main_frame.setFrameShadow(QFrame.Plain)
        self.Main_frame.setLineWidth(0)
        self.gridLayout_3 = QGridLayout(self.Main_frame)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.Top = QFrame(self.Main_frame)
        self.Top.setObjectName(u"Top")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Top.sizePolicy().hasHeightForWidth())
        self.Top.setSizePolicy(sizePolicy1)
        self.Top.setMinimumSize(QSize(500, 50))
        self.Top.setMaximumSize(QSize(16777215, 50))
        self.Top.setFrameShape(QFrame.StyledPanel)
        self.Top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.Top)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.Top)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setPixmap(QPixmap(u":/logo/AMS_logo.png"))

        self.horizontalLayout.addWidget(self.label)

        self.openGLWidget = QOpenGLWidget(self.Top)
        self.openGLWidget.setObjectName(u"openGLWidget")

        self.horizontalLayout.addWidget(self.openGLWidget)

        self.horizontalSpacer = QSpacerItem(1297, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.current_time = QDateTimeEdit(self.Top)
        self.current_time.setObjectName(u"current_time")
        font1 = QFont()
        font1.setFamily(u"Times New Roman")
        font1.setPointSize(20)
        self.current_time.setFont(font1)
        self.current_time.setFrame(False)
        self.current_time.setAlignment(Qt.AlignCenter)
        self.current_time.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout.addWidget(self.current_time)

        self.horizontalSpacer_3 = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.setting_btn = QPushButton(self.Top)
        self.setting_btn.setObjectName(u"setting_btn")
        self.setting_btn.setMaximumSize(QSize(40, 40))
        icon1 = QIcon()
        icon1.addFile(u":/setting/setting_button.png", QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile(u":/setting/setting_button_ON.png", QSize(), QIcon.Normal, QIcon.On)
        icon1.addFile(u":/setting/setting_button.png", QSize(), QIcon.Active, QIcon.Off)
        icon1.addFile(u":/setting/setting_button_ON.png", QSize(), QIcon.Active, QIcon.On)
        icon1.addFile(u":/setting/setting_button.png", QSize(), QIcon.Selected, QIcon.Off)
        icon1.addFile(u":/setting/setting_button_ON.png", QSize(), QIcon.Selected, QIcon.On)
        self.setting_btn.setIcon(icon1)
        self.setting_btn.setIconSize(QSize(40, 40))
        self.setting_btn.setCheckable(True)
        self.setting_btn.setAutoRepeat(False)

        self.horizontalLayout.addWidget(self.setting_btn)


        self.gridLayout_3.addWidget(self.Top, 0, 0, 1, 2)

        self.frm_CNC_state = QFrame(self.Main_frame)
        self.frm_CNC_state.setObjectName(u"frm_CNC_state")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frm_CNC_state.sizePolicy().hasHeightForWidth())
        self.frm_CNC_state.setSizePolicy(sizePolicy3)
        self.frm_CNC_state.setMaximumSize(QSize(500, 16777215))
        self.frm_CNC_state.setFrameShape(QFrame.StyledPanel)
        self.frm_CNC_state.setFrameShadow(QFrame.Raised)
        self.frm_CNC_state.setLineWidth(0)
        self.verticalLayout = QVBoxLayout(self.frm_CNC_state)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frm_CNC_state)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.mac_pos_box = QGroupBox(self.frame_3)
        self.mac_pos_box.setObjectName(u"mac_pos_box")
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        font2.setPointSize(15)
        font2.setBold(True)
        font2.setWeight(75)
        self.mac_pos_box.setFont(font2)
        self.gridLayout_5 = QGridLayout(self.mac_pos_box)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.mac_x_label = QLabel(self.mac_pos_box)
        self.mac_x_label.setObjectName(u"mac_x_label")
        font3 = QFont()
        font3.setFamily(u"Times New Roman")
        font3.setPointSize(20)
        font3.setBold(True)
        font3.setWeight(75)
        self.mac_x_label.setFont(font3)
        self.mac_x_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_x_label, 0, 0, 1, 1)

        self.mac_x_val = QLabel(self.mac_pos_box)
        self.mac_x_val.setObjectName(u"mac_x_val")
        self.mac_x_val.setFont(font3)
        self.mac_x_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_x_val, 0, 1, 1, 1)

        self.mac_y_label = QLabel(self.mac_pos_box)
        self.mac_y_label.setObjectName(u"mac_y_label")
        self.mac_y_label.setFont(font3)
        self.mac_y_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_y_label, 1, 0, 1, 1)

        self.mac_y_val = QLabel(self.mac_pos_box)
        self.mac_y_val.setObjectName(u"mac_y_val")
        self.mac_y_val.setFont(font3)
        self.mac_y_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_y_val, 1, 1, 1, 1)

        self.mac_z_label = QLabel(self.mac_pos_box)
        self.mac_z_label.setObjectName(u"mac_z_label")
        self.mac_z_label.setFont(font3)
        self.mac_z_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_z_label, 2, 0, 1, 1)

        self.mac_z_val = QLabel(self.mac_pos_box)
        self.mac_z_val.setObjectName(u"mac_z_val")
        self.mac_z_val.setFont(font3)
        self.mac_z_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_z_val, 2, 1, 1, 1)

        self.mac_a_label = QLabel(self.mac_pos_box)
        self.mac_a_label.setObjectName(u"mac_a_label")
        self.mac_a_label.setFont(font3)
        self.mac_a_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_a_label, 3, 0, 1, 1)

        self.mac_a_val = QLabel(self.mac_pos_box)
        self.mac_a_val.setObjectName(u"mac_a_val")
        self.mac_a_val.setFont(font3)
        self.mac_a_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_a_val, 3, 1, 1, 1)

        self.mac_c_label = QLabel(self.mac_pos_box)
        self.mac_c_label.setObjectName(u"mac_c_label")
        self.mac_c_label.setFont(font3)
        self.mac_c_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_c_label, 4, 0, 1, 1)

        self.mac_c_val = QLabel(self.mac_pos_box)
        self.mac_c_val.setObjectName(u"mac_c_val")
        self.mac_c_val.setFont(font3)
        self.mac_c_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.mac_c_val, 4, 1, 1, 1)


        self.gridLayout.addWidget(self.mac_pos_box, 4, 0, 1, 1)

        self.rem_pos_box = QGroupBox(self.frame_3)
        self.rem_pos_box.setObjectName(u"rem_pos_box")
        self.rem_pos_box.setFont(font2)
        self.gridLayout_4 = QGridLayout(self.rem_pos_box)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.rem_a_val = QLabel(self.rem_pos_box)
        self.rem_a_val.setObjectName(u"rem_a_val")
        self.rem_a_val.setFont(font3)
        self.rem_a_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_a_val, 3, 1, 1, 1)

        self.rem_c_label = QLabel(self.rem_pos_box)
        self.rem_c_label.setObjectName(u"rem_c_label")
        self.rem_c_label.setFont(font3)
        self.rem_c_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_c_label, 4, 0, 1, 1)

        self.rem_y_label = QLabel(self.rem_pos_box)
        self.rem_y_label.setObjectName(u"rem_y_label")
        self.rem_y_label.setFont(font3)
        self.rem_y_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_y_label, 1, 0, 1, 1)

        self.rem_a_label = QLabel(self.rem_pos_box)
        self.rem_a_label.setObjectName(u"rem_a_label")
        self.rem_a_label.setFont(font3)
        self.rem_a_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_a_label, 3, 0, 1, 1)

        self.rem_z_val = QLabel(self.rem_pos_box)
        self.rem_z_val.setObjectName(u"rem_z_val")
        self.rem_z_val.setFont(font3)
        self.rem_z_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_z_val, 2, 1, 1, 1)

        self.rem_c_val = QLabel(self.rem_pos_box)
        self.rem_c_val.setObjectName(u"rem_c_val")
        self.rem_c_val.setFont(font3)
        self.rem_c_val.setScaledContents(True)
        self.rem_c_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_c_val, 4, 1, 1, 1)

        self.rem_z_label = QLabel(self.rem_pos_box)
        self.rem_z_label.setObjectName(u"rem_z_label")
        self.rem_z_label.setFont(font3)
        self.rem_z_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_z_label, 2, 0, 1, 1)

        self.rem_x_val = QLabel(self.rem_pos_box)
        self.rem_x_val.setObjectName(u"rem_x_val")
        self.rem_x_val.setFont(font3)
        self.rem_x_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_x_val, 0, 1, 1, 1)

        self.rem_x_label = QLabel(self.rem_pos_box)
        self.rem_x_label.setObjectName(u"rem_x_label")
        self.rem_x_label.setFont(font3)
        self.rem_x_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_x_label, 0, 0, 1, 1)

        self.rem_y_val = QLabel(self.rem_pos_box)
        self.rem_y_val.setObjectName(u"rem_y_val")
        self.rem_y_val.setFont(font3)
        self.rem_y_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.rem_y_val, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.rem_pos_box, 0, 8, 1, 1)

        self.cur_pos_box = QGroupBox(self.frame_3)
        self.cur_pos_box.setObjectName(u"cur_pos_box")
        self.cur_pos_box.setFont(font2)
        self.gridLayout_2 = QGridLayout(self.cur_pos_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cur_y_label = QLabel(self.cur_pos_box)
        self.cur_y_label.setObjectName(u"cur_y_label")
        self.cur_y_label.setFont(font3)
        self.cur_y_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_y_label, 1, 0, 1, 1)

        self.cur_z_val = QLabel(self.cur_pos_box)
        self.cur_z_val.setObjectName(u"cur_z_val")
        self.cur_z_val.setFont(font3)
        self.cur_z_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_z_val, 2, 1, 1, 1)

        self.cur_x_label = QLabel(self.cur_pos_box)
        self.cur_x_label.setObjectName(u"cur_x_label")
        self.cur_x_label.setFont(font3)
        self.cur_x_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_x_label, 0, 0, 1, 1)

        self.cur_a_label = QLabel(self.cur_pos_box)
        self.cur_a_label.setObjectName(u"cur_a_label")
        self.cur_a_label.setFont(font3)
        self.cur_a_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_a_label, 3, 0, 1, 1)

        self.cur_y_val = QLabel(self.cur_pos_box)
        self.cur_y_val.setObjectName(u"cur_y_val")
        self.cur_y_val.setFont(font3)
        self.cur_y_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_y_val, 1, 1, 1, 1)

        self.cur_c_val = QLabel(self.cur_pos_box)
        self.cur_c_val.setObjectName(u"cur_c_val")
        self.cur_c_val.setFont(font3)
        self.cur_c_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_c_val, 5, 1, 1, 1)

        self.cur_a_val = QLabel(self.cur_pos_box)
        self.cur_a_val.setObjectName(u"cur_a_val")
        self.cur_a_val.setFont(font3)
        self.cur_a_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_a_val, 3, 1, 1, 1)

        self.cur_x_val = QLabel(self.cur_pos_box)
        self.cur_x_val.setObjectName(u"cur_x_val")
        self.cur_x_val.setFont(font3)
        self.cur_x_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_x_val, 0, 1, 1, 1)

        self.cur_z_label = QLabel(self.cur_pos_box)
        self.cur_z_label.setObjectName(u"cur_z_label")
        self.cur_z_label.setFont(font3)
        self.cur_z_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_z_label, 2, 0, 1, 1)

        self.cur_c_label = QLabel(self.cur_pos_box)
        self.cur_c_label.setObjectName(u"cur_c_label")
        self.cur_c_label.setFont(font3)
        self.cur_c_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.cur_c_label, 5, 0, 1, 1)


        self.gridLayout.addWidget(self.cur_pos_box, 0, 0, 1, 1)

        # ---------------- 연결상태 ----------------
        self.groupBox = QGroupBox(self.frame_3)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font2)

        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 50, 151, 180))   # 높이 조금 늘림

        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(20, 0, 0, 0)

        # 왼쪽: 원 표시
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.camera_status_circle = QLabel(self.layoutWidget)
        self.camera_status_circle.setMinimumSize(QSize(20, 20))
        self.camera_status_circle.setMaximumSize(QSize(20, 20))
        self.camera_status_circle.setStyleSheet("border-radius: 10px;\nbackground-color: red;")
        self.verticalLayout_3.addWidget(self.camera_status_circle)

        self.pyrometer_status_circle = QLabel(self.layoutWidget)
        self.pyrometer_status_circle.setMinimumSize(QSize(20, 20))
        self.pyrometer_status_circle.setMaximumSize(QSize(20, 20))
        self.pyrometer_status_circle.setStyleSheet("border-radius: 10px;\nbackground-color: red;")
        self.verticalLayout_3.addWidget(self.pyrometer_status_circle)

        self.laser_status_circle = QLabel(self.layoutWidget)
        self.laser_status_circle.setMinimumSize(QSize(20, 20))
        self.laser_status_circle.setMaximumSize(QSize(20, 20))
        self.laser_status_circle.setStyleSheet("border-radius: 10px;\nbackground-color: red;")
        self.verticalLayout_3.addWidget(self.laser_status_circle)

        self.hik_status_circle_1 = QLabel(self.layoutWidget)
        self.hik_status_circle_1.setMinimumSize(QSize(20, 20))
        self.hik_status_circle_1.setMaximumSize(QSize(20, 20))
        self.hik_status_circle_1.setStyleSheet("border-radius: 10px;\nbackground-color: red;")
        self.verticalLayout_3.addWidget(self.hik_status_circle_1)

        self.hik_status_circle_2 = QLabel(self.layoutWidget)
        self.hik_status_circle_2.setMinimumSize(QSize(20, 20))
        self.hik_status_circle_2.setMaximumSize(QSize(20, 20))
        self.hik_status_circle_2.setStyleSheet("border-radius: 10px;\nbackground-color: red;")
        self.verticalLayout_3.addWidget(self.hik_status_circle_2)

        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        # 오른쪽: 라벨 텍스트
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.label_camera_status = QLabel(self.layoutWidget)
        self.label_camera_status.setFont(font2)
        self.label_camera_status.setText("Camera")
        self.verticalLayout_2.addWidget(self.label_camera_status)

        self.label_pyro_status = QLabel(self.layoutWidget)
        self.label_pyro_status.setFont(font2)
        self.label_pyro_status.setText("Pyrometer")
        self.verticalLayout_2.addWidget(self.label_pyro_status)

        self.label_ipg_status = QLabel(self.layoutWidget)
        self.label_ipg_status.setFont(font2)
        self.label_ipg_status.setText("Laser")
        self.verticalLayout_2.addWidget(self.label_ipg_status)

        self.label_hik1_status = QLabel(self.layoutWidget)
        self.label_hik1_status.setFont(font2)
        self.label_hik1_status.setText("HikRobot-1")
        self.verticalLayout_2.addWidget(self.label_hik1_status)

        self.label_hik2_status = QLabel(self.layoutWidget)
        self.label_hik2_status.setFont(font2)
        self.label_hik2_status.setText("HikRobot-2")
        self.verticalLayout_2.addWidget(self.label_hik2_status)

        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.gridLayout.addWidget(self.groupBox, 4, 8, 1, 1)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frm_CNC_state)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(16777215, 600))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")
        font5 = QFont()
        font5.setFamily(u"Times New Roman")
        font5.setPointSize(16)
        self.label_8.setFont(font5)

        self.gridLayout_8.addWidget(self.label_8, 3, 2, 1, 1)

        self.feed_val = QLabel(self.frame_4)
        self.feed_val.setObjectName(u"feed_val")
        self.feed_val.setFont(font5)
        self.feed_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.feed_val, 0, 1, 1, 1)

        self.override_val = QLabel(self.frame_4)
        self.override_val.setObjectName(u"override_val")
        self.override_val.setFont(font5)
        self.override_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.override_val, 2, 1, 1, 1)

        self.label_12 = QLabel(self.frame_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font5)

        self.gridLayout_8.addWidget(self.label_12, 2, 0, 1, 1)

        self.rapid_override_val = QLabel(self.frame_4)
        self.rapid_override_val.setObjectName(u"rapid_override_val")
        self.rapid_override_val.setFont(font5)
        self.rapid_override_val.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.rapid_override_val, 3, 1, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font5)

        self.gridLayout_8.addWidget(self.label_3, 0, 2, 1, 1)

        self.label_13 = QLabel(self.frame_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font5)

        self.gridLayout_8.addWidget(self.label_13, 6, 0, 1, 1)

        self.feed_label = QLabel(self.frame_4)
        self.feed_label.setObjectName(u"feed_label")
        self.feed_label.setFont(font5)

        self.gridLayout_8.addWidget(self.feed_label, 0, 0, 1, 1)

        self.checkBox = QCheckBox(self.frame_4)
        self.checkBox.setObjectName(u"checkBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy4)
        self.checkBox.setMouseTracking(False)
        self.checkBox.setCheckable(True)

        self.gridLayout_8.addWidget(self.checkBox, 10, 1, 1, 1)

        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font5)

        self.gridLayout_8.addWidget(self.label_4, 2, 2, 1, 1)

        self.operating_time = QLabel(self.frame_4)
        self.operating_time.setObjectName(u"operating_time")
        self.operating_time.setFont(font5)
        self.operating_time.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.operating_time, 6, 1, 1, 2)

        self.label_15 = QLabel(self.frame_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font5)

        self.gridLayout_8.addWidget(self.label_15, 3, 0, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        font6 = QFont()
        font6.setFamily(u"Times New Roman")
        font6.setPointSize(15)
        self.label_10.setFont(font6)

        self.gridLayout_8.addWidget(self.label_10, 10, 0, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font5)

        self.gridLayout_8.addWidget(self.label_6, 7, 0, 1, 1)

        self.total_operating_time = QLabel(self.frame_4)
        self.total_operating_time.setObjectName(u"total_operating_time")
        self.total_operating_time.setFont(font5)
        self.total_operating_time.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.total_operating_time, 7, 1, 1, 2)


        self.verticalLayout.addWidget(self.frame_4)


        self.gridLayout_3.addWidget(self.frm_CNC_state, 1, 0, 1, 1)

        self.frm_monitoring = QFrame(self.Main_frame)
        self.frm_monitoring.setObjectName(u"frm_monitoring")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frm_monitoring.sizePolicy().hasHeightForWidth())
        self.frm_monitoring.setSizePolicy(sizePolicy5)
        self.frm_monitoring.setMaximumSize(QSize(1700, 16777215))
        self.frm_monitoring.setFrameShape(QFrame.StyledPanel)
        self.frm_monitoring.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frm_monitoring)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        # ✅ 왼쪽: Basler + HikRobot (세로 배치)
        self.verticalLayout_images = QVBoxLayout()
        self.verticalLayout_images.setObjectName("verticalLayout_images")

        # Basler 이미지
        self.img_label = QLabel(self.frm_monitoring)
        self.img_label.setObjectName("img_label")
        self.img_label.setMinimumSize(540, 260)
        self.img_label.setMaximumSize(540, 260)
        self.verticalLayout_images.addWidget(self.img_label)

        # HikRobot 이미지
        self.hik_img_label = QLabel(self.frm_monitoring)
        self.hik_img_label.setObjectName("hik_img_label")
        self.hik_img_label.setMinimumSize(540, 260)
        self.hik_img_label.setMaximumSize(540, 260)
        self.hik_img_label.setStyleSheet("background-color: black; border: 1px solid gray;")
        self.hik_img_label.setAlignment(Qt.AlignCenter)
        self.hik_img_label.setText("HikRobot Camera")
        self.verticalLayout_images.addWidget(self.hik_img_label)

        # ✅ 오른쪽: Melt Pool Area
        self.meltpool_area = PlotWidget(self.frm_monitoring)
        self.meltpool_area.setObjectName("meltpool_area")
        self.meltpool_area.setMinimumSize(500, 440)
        self.meltpool_area.setMaximumSize(1000, 16777215)

        # ✅ 좌/우 합치기
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.addLayout(self.verticalLayout_images)
        self.horizontalLayout_4.addWidget(self.meltpool_area)

        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        # ✅ Melt Pool Temp 크기 줄이기
        self.meltpool_temp = PlotWidget(self.frm_monitoring)
        self.meltpool_temp.setObjectName("meltpool_temp")
        self.meltpool_temp.setMinimumSize(0, 150)
        self.meltpool_temp.setMaximumSize(16777215, 150)
        self.verticalLayout_4.addWidget(self.meltpool_temp)

        # ✅ Laser Power는 Melt Pool Temp 아래
        self.laserpower = PlotWidget(self.frm_monitoring)
        self.laserpower.setObjectName("laserpower")
        self.laserpower.setMinimumSize(0, 150)
        self.laserpower.setMaximumSize(16777215, 150)
        self.verticalLayout_4.addWidget(self.laserpower)


        self.gridLayout_3.addWidget(self.frm_monitoring, 1, 1, 1, 1)

        self.Bottom = QFrame(self.Main_frame)
        self.Bottom.setObjectName(u"Bottom")
        sizePolicy1.setHeightForWidth(self.Bottom.sizePolicy().hasHeightForWidth())
        self.Bottom.setSizePolicy(sizePolicy1)
        self.Bottom.setMinimumSize(QSize(500, 50))
        self.Bottom.setMaximumSize(QSize(16777215, 50))
        self.Bottom.setFrameShape(QFrame.StyledPanel)
        self.Bottom.setFrameShadow(QFrame.Raised)
        self.Bottom.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.Bottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.bottom_label = QLabel(self.Bottom)
        self.bottom_label.setObjectName(u"bottom_label")
        font7 = QFont()
        font7.setFamily(u"Times New Roman")
        font7.setPointSize(9)
        self.bottom_label.setFont(font7)

        self.horizontalLayout_2.addWidget(self.bottom_label)

        self.horizontalSpacer_2 = QSpacerItem(1417, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.Save_btn = QPushButton(self.Bottom)
        self.Save_btn.setObjectName(u"Save_btn")
        sizePolicy1.setHeightForWidth(self.Save_btn.sizePolicy().hasHeightForWidth())
        self.Save_btn.setSizePolicy(sizePolicy1)
        self.Save_btn.setMinimumSize(QSize(0, 40))
        self.Save_btn.setMaximumSize(QSize(150, 40))
        self.Save_btn.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.Save_btn)

        self.Exit_btn = QPushButton(self.Bottom)
        self.Exit_btn.setObjectName(u"Exit_btn")
        sizePolicy1.setHeightForWidth(self.Exit_btn.sizePolicy().hasHeightForWidth())
        self.Exit_btn.setSizePolicy(sizePolicy1)
        self.Exit_btn.setMinimumSize(QSize(0, 40))
        self.Exit_btn.setMaximumSize(QSize(150, 40))

        self.horizontalLayout_2.addWidget(self.Exit_btn)


        self.gridLayout_3.addWidget(self.Bottom, 2, 0, 1, 2)


        self.gridLayout_6.addWidget(self.Main_frame, 0, 0, 1, 1)

        DED_Monitoring.setCentralWidget(self.centralwidget)

        self.retranslateUi(DED_Monitoring)

        QMetaObject.connectSlotsByName(DED_Monitoring)
    # setupUi

    def retranslateUi(self, DED_Monitoring):
        DED_Monitoring.setWindowTitle(QCoreApplication.translate("DED_Monitoring", u"MainWindow", None))
        self.label.setText("")
        self.current_time.setDisplayFormat(QCoreApplication.translate("DED_Monitoring", u"yyyy-MM-dd AP h:mm:ss", None))
        self.setting_btn.setText("")
        self.mac_pos_box.setTitle(QCoreApplication.translate("DED_Monitoring", u"\uae30\uacc4\uc88c\ud45c", None))
        self.mac_x_label.setText(QCoreApplication.translate("DED_Monitoring", u"X", None))
        self.mac_x_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.mac_y_label.setText(QCoreApplication.translate("DED_Monitoring", u"Y", None))
        self.mac_y_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.mac_z_label.setText(QCoreApplication.translate("DED_Monitoring", u"Z", None))
        self.mac_z_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.mac_a_label.setText(QCoreApplication.translate("DED_Monitoring", u"A", None))
        self.mac_a_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.mac_c_label.setText(QCoreApplication.translate("DED_Monitoring", u"C", None))
        self.mac_c_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.rem_pos_box.setTitle(QCoreApplication.translate("DED_Monitoring", u"\ub0a8\uc740\uac70\ub9ac", None))
        self.rem_a_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.rem_c_label.setText(QCoreApplication.translate("DED_Monitoring", u"C", None))
        self.rem_y_label.setText(QCoreApplication.translate("DED_Monitoring", u"Y", None))
        self.rem_a_label.setText(QCoreApplication.translate("DED_Monitoring", u"A", None))
        self.rem_z_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.rem_c_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.rem_z_label.setText(QCoreApplication.translate("DED_Monitoring", u"Z", None))
        self.rem_x_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.rem_x_label.setText(QCoreApplication.translate("DED_Monitoring", u"X", None))
        self.rem_y_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.cur_pos_box.setTitle(QCoreApplication.translate("DED_Monitoring", u"\ud604\uc7ac\uc88c\ud45c", None))
        self.cur_y_label.setText(QCoreApplication.translate("DED_Monitoring", u"Y", None))
        self.cur_z_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.cur_x_label.setText(QCoreApplication.translate("DED_Monitoring", u"X", None))
        self.cur_a_label.setText(QCoreApplication.translate("DED_Monitoring", u"A", None))
        self.cur_y_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.cur_c_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.cur_a_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.cur_x_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.00", None))
        self.cur_z_label.setText(QCoreApplication.translate("DED_Monitoring", u"Z", None))
        self.cur_c_label.setText(QCoreApplication.translate("DED_Monitoring", u"C", None))
        self.groupBox.setTitle(QCoreApplication.translate("DED_Monitoring", u"\uc5f0\uacb0\uc0c1\ud0dc", None))
        self.camera_status_circle.setText("")
        self.pyrometer_status_circle.setText("")
        self.laser_status_circle.setText("")
        self.label_camera_status.setText(QCoreApplication.translate("DED_Monitoring", u"Camera", None))
        self.label_pyro_status.setText(QCoreApplication.translate("DED_Monitoring", u"Pyrometer", None))
        self.label_ipg_status.setText(QCoreApplication.translate("DED_Monitoring", u"Laser", None))
        self.label_hik1_status.setText(QCoreApplication.translate("DED_Monitoring", u"HikRobot-1", None))
        self.label_hik2_status.setText(QCoreApplication.translate("DED_Monitoring", u"HikRobot-2", None))
        self.label_8.setText(QCoreApplication.translate("DED_Monitoring", u"%", None))
        self.feed_val.setText(QCoreApplication.translate("DED_Monitoring", u"0.000", None))
        self.override_val.setText(QCoreApplication.translate("DED_Monitoring", u"0", None))
        self.label_12.setText(QCoreApplication.translate("DED_Monitoring", u"Feed Override", None))
        self.rapid_override_val.setText(QCoreApplication.translate("DED_Monitoring", u"0", None))
        self.label_3.setText(QCoreApplication.translate("DED_Monitoring", u"mm/min", None))
        self.label_13.setText(QCoreApplication.translate("DED_Monitoring", u"Operating time", None))
        self.feed_label.setText(QCoreApplication.translate("DED_Monitoring", u"Travel speed", None))
        self.label_4.setText(QCoreApplication.translate("DED_Monitoring", u"%", None))
        self.operating_time.setText(QCoreApplication.translate("DED_Monitoring", u"0.000", None))
        self.label_15.setText(QCoreApplication.translate("DED_Monitoring", u"Rapid Override", None))
        self.label_10.setText(QCoreApplication.translate("DED_Monitoring", u"Emergency", None))
        self.label_6.setText(QCoreApplication.translate("DED_Monitoring", u"Total operating time", None))
        self.total_operating_time.setText(QCoreApplication.translate("DED_Monitoring", u"0.000", None))
        self.img_label.setText("")
        self.bottom_label.setText(QCoreApplication.translate("DED_Monitoring", u"Copyright by KITECH V2.0", None))
        self.Save_btn.setText(QCoreApplication.translate("DED_Monitoring", u"SAVE", None))
        self.Exit_btn.setText(QCoreApplication.translate("DED_Monitoring", u"EXIT", None))
    # retranslateUi

