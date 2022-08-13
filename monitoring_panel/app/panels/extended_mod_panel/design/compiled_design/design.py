# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'design.ui'
##
# Created by: Qt User Interface Compiler version 6.2.4
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
                               QRadioButton, QSizePolicy, QTextBrowser, QTextEdit,
                               QToolButton, QWidget)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.setEnabled(True)
        Dialog.resize(570, 370)
        Dialog.setMinimumSize(QSize(570, 370))
        Dialog.setMaximumSize(QSize(570, 370))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        Dialog.setFont(font)
        Dialog.setCursor(QCursor(Qt.PointingHandCursor))
        Dialog.setMouseTracking(False)
        Dialog.setFocusPolicy(Qt.WheelFocus)
        icon = QIcon()
        icon.addFile(r"D:\pprojects\poe_beast_bot_v3\monitoring_panel\app\panels\extended_mod_panel\design\raw_design\Bestiary_Brimmed_Hat_inventory_icon.webp",
                     QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWindowOpacity(1.000000000000000)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet(u"QDialog {\n"
                             "	background-image: url(\":/images/bestiary_background.png\");\n"
                             "}\n"
                             "\n"
                             "QWidget {\n"
                             "	color: white;\n"
                             "	background-color: rgba(100, 100, 100, .8);\n"
                             "}\n"
                             "\n"
                             "QTextBrowser {\n"
                             "	color: white;\n"
                             "	border-style: inset;\n"
                             "	border-width: 1px;\n"
                             "	border-color: white;\n"
                             "	border-color: rgb(100, 100, 100);\n"
                             "	background-color: rgba(40, 40, 40, .8);\n"
                             "}\n"
                             "\n"
                             "QRadioButton {\n"
                             "	color: white;\n"
                             "	font-family: Rubik;\n"
                             "	font-size: 8pt;\n"
                             "	font-weight: 500;\n"
                             "	border-style: inset;\n"
                             "	border-width: 1px;\n"
                             "	border-color: white;\n"
                             "	border-color:  rgb(100, 100, 100);\n"
                             "	border-left:  rgb(100, 100, 100);\n"
                             "	background-color: rgba(40, 40, 40, .8);\n"
                             "}\n"
                             "\n"
                             "QToolButton:hover {\n"
                             "	color: white;\n"
                             "	border-style: inset;\n"
                             "	border-width: 1px;\n"
                             "	border-color: white;\n"
                             "	border-color: rgb(220, 220, 220);\n"
                             "	background-color: rgba(20, 20, 20, .8);\n"
                             "}\n"
                             "\n"
                             "QToolButton:pressed {\n"
                             "	color: white;\n"
                             "	border-style: inset;\n"
                             "	border-width: 1px;\n"
                             "	borde"
                             "r-color: white;\n"
                             "	border-color:  rgb(100, 100, 100);\n"
                             "	background-color: rgba(50, 50, 50, .8);\n"
                             "}\n"
                             "\n"
                             "QToolButton {\n"
                             "	color: white;\n"
                             "	font-family: Rubik;\n"
                             "	font-size: 8pt;\n"
                             "	font-weight: 600;\n"
                             "	border-style: inset;\n"
                             "	border-width : 1px;\n"
                             "	border-color:  rgb(100, 100, 100);\n"
                             "	background-color: rgba(40, 40, 40, .8);\n"
                             "}\n"
                             "\n"
                             "QComboBox {\n"
                             "	color: white;\n"
                             "	font-size: 8pt;\n"
                             "	font-weight: 600;\n"
                             "	border-color:  rgb(100, 100, 100);\n"
                             "	background-color: rgba(40, 40, 40, .8);\n"
                             "}\n"
                             "\n"
                             "")
        Dialog.setInputMethodHints(Qt.ImhNone)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 140, 251, 211))
        self.textBrowser_2 = QTextBrowser(Dialog)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setGeometry(QRect(300, 20, 251, 41))
        self.textBrowser_2.setFrameShadow(QFrame.Sunken)
        self.textBrowser_2.setLineWidth(1)
        self.textBrowser_2.setAutoFormatting(QTextEdit.AutoNone)
        self.textBrowser_3 = QTextBrowser(Dialog)
        self.textBrowser_3.setObjectName(u"textBrowser_3")
        self.textBrowser_3.setGeometry(QRect(20, 100, 251, 31))
        self.textBrowser_4 = QTextBrowser(Dialog)
        self.textBrowser_4.setObjectName(u"textBrowser_4")
        self.textBrowser_4.setGeometry(QRect(20, 20, 251, 31))
        self.textBrowser_4.setStyleSheet(u"")
        self.toolButton_8 = QToolButton(Dialog)
        self.toolButton_8.setObjectName(u"toolButton_8")
        self.toolButton_8.setGeometry(QRect(300, 160, 121, 31))
        self.toolButton_9 = QToolButton(Dialog)
        self.toolButton_9.setObjectName(u"toolButton_9")
        self.toolButton_9.setGeometry(QRect(370, 200, 121, 31))
        self.toolButton_10 = QToolButton(Dialog)
        self.toolButton_10.setObjectName(u"toolButton_10")
        self.toolButton_10.setGeometry(QRect(430, 160, 121, 31))
        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(20, 60, 251, 22))
        self.comboBox.setStyleSheet(u"")
        self.comboBox.setEditable(False)
        self.radioButton = QRadioButton(Dialog)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(480, 120, 71, 31))
        self.toolButton_3 = QToolButton(Dialog)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setGeometry(QRect(300, 70, 121, 31))
        self.toolButton_4 = QToolButton(Dialog)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setGeometry(QRect(430, 70, 121, 31))
        self.textBrowser_6 = QTextBrowser(Dialog)
        self.textBrowser_6.setObjectName(u"textBrowser_6")
        self.textBrowser_6.setGeometry(QRect(300, 120, 181, 31))
        self.textBrowser_6.setStyleSheet(u"border-right: rgb(180, 180, 180);")
        self.textBrowser_6.setFrameShadow(QFrame.Sunken)
        self.textBrowser_6.setLineWidth(1)
        self.textBrowser_6.setAutoFormatting(QTextEdit.AutoNone)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate(
            "Dialog", u"Monitoring Panel", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                            "p, li { white-space: pre-wrap; }\n"
                                                            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:10px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Rubik'; font-size:8pt; font-weight:600;\"><br /></p></body></html>", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                              "p, li { white-space: pre-wrap; }\n"
                                                              "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Rubik'; font-size:8pt; font-weight:600;\">Worker control events</span></p>\n"
                                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Rubik'; font-size:6pt; font-weight:600;\">only single requests method</span></p></body></html>", None))
        self.textBrowser_3.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                              "p, li { white-space: pre-wrap; }\n"
                                                              "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Rubik'; font-size:8pt; font-weight:600;\">Worker machines info</span></p></body></html>", None))
        self.textBrowser_4.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                              "p, li { white-space: pre-wrap; }\n"
                                                              "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Rubik'; font-size:8pt; font-weight:600;\">Select machine</span></p></body></html>", None))
        self.toolButton_8.setText(
            QCoreApplication.translate("Dialog", u"portal", None))
        self.toolButton_9.setText(
            QCoreApplication.translate("Dialog", u"to own ho", None))
        self.toolButton_10.setText(
            QCoreApplication.translate("Dialog", u"door", None))
        self.radioButton.setText(
            QCoreApplication.translate("Dialog", u"TO ALL", None))
        self.toolButton_3.setText(
            QCoreApplication.translate("Dialog", u"pause", None))
        self.toolButton_4.setText(
            QCoreApplication.translate("Dialog", u"resume", None))
        self.textBrowser_6.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                              "p, li { white-space: pre-wrap; }\n"
                                                              "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Party machine actions</span></p></body></html>", None))
    # retranslateUi
