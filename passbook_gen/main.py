#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is a part of PassbookGen Program which is GNU GPLv3 licensed
# Copyright (C) 2024 Arindam Chaudhuri <arindamsoft94@gmail.com>

import sys, os, platform
from datetime import datetime

from PyQt5.QtCore import ( QTimer, Qt, QPoint, QRectF, QSettings,
    QStandardPaths, QDir, QRegExp)
from PyQt5.QtGui import (QPixmap, QImage, QPainter, QPen, QFontMetrics, QFont, QIcon, QFontDatabase,
    QTransform, QColor, QIntValidator, QRegExpValidator
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout, QStyleFactory,
    QSizePolicy, QFrame, QGroupBox, QWidget, QScrollArea,
    QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox
)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

sys.path.append(os.path.dirname(__file__)) # to enable python 2 like relative import

from __init__ import __version__, COPYRIGHT_YEAR, AUTHOR_NAME, AUTHOR_EMAIL
from barcode_generator import BarcodeGeneratorDialog
import resources_rc



class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Passbook Page Generator")
        self.setWindowIcon(QIcon(":/icons/passbook-gen.png"))

        self.setupUi()
        # ---------- Load Settings --------------
        self.settings = QSettings("passbook-gen", "passbook-gen", self)
        win_w = int(self.settings.value("WindowWidth", 960))
        win_h = int(self.settings.value("WindowHeight", 640))
        win_maximized = self.settings.value("WindowMaximized", "false") == "true"
        curr_dir = self.settings.value("WorkingDir", "")
        branch_name = self.settings.value("BranchName", "KHIRAGRAM")
        branch_addr = self.settings.value("BranchAddress", "VILLandP.O KHIRAGRAM, DIST BURDWAN-713143(Ph:7070656531)")
        ifsc = self.settings.value("IFSC", "PUNB0124420")
        micr = self.settings.value("MICR", "713024404")

        village = self.settings.value("Village", "KSHIRGRAM")
        pin_code = self.settings.value("PinCode", "713143")
        city = self.settings.value("City", "BURDWAN, WEST BENGAL")
        account_no = self.settings.value("AccountNo", "12442017000")

        # set initial values
        if not curr_dir or not os.path.isdir(curr_dir):
            curr_dir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        QDir.setCurrent(curr_dir)
        self.issueDateEdit.setToday()
        self.branchNameEdit.setText(branch_name)
        self.branchAddressEdit.setText(branch_addr)
        self.branchAddressEdit.home(False)# show text left aligned
        self.ifscEdit.setText(ifsc)
        self.micrEdit.setText(micr)

        self.villageEdit.setText(village)
        self.pinCodeEdit.setText(pin_code)
        self.cityEdit.setText(city)
        self.accountNoEdit.setText(account_no)
        # --------- Connect Signals ------------
        self.generateBarcodeBtn.clicked.connect(self.generateBarcode)
        self.saveBtn.clicked.connect(self.savePassbookPage)
        self.printBtn.clicked.connect(self.printPassbookPage)
        self.closeBtn.clicked.connect(self.close)

        for comboBox in (self.salutationCombo, self.accountTypeCombo):
            comboBox.currentIndexChanged.connect(self.updatePassbookPage)

        for textEdit in (self.branchNameEdit, self.branchAddressEdit, self.ifscEdit,
            self.micrEdit, self.customerNameEdit, self.careOfEdit, self.villageEdit,
            self.pinCodeEdit, self.cityEdit, self.aadhaarNoEdit,
            self.accountNoEdit, self.cifEdit, self.openDateEdit, self.issueDateEdit):
                textEdit.textChanged.connect(self.updatePassbookPage)

        self.updatePassbookPage()

        self.resize(win_w, win_h)
        if win_maximized:
            self.showMaximized()
        else:
            self.show()


    def setupUi(self):
        """ create widgets and layouts """
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        #self.statusbar = QStatusBar(self)
        #self.setStatusBar(self.statusbar)

        self.frame = QFrame(self.centralwidget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.frame.setMaximumWidth(300)

        self.groupBox = QGroupBox("Branch Details :", self.frame)
        self.branchNameEdit = QLineEdit(self.groupBox)
        self.ifscEdit = QLineEdit(self.groupBox)
        self.micrEdit = QLineEdit(self.groupBox)
        self.branchAddressEdit = QLineEdit(self.groupBox)

        self.groupBox_1 = QGroupBox("Customer Details :", self.frame)
        self.salutationCombo = QComboBox(self.groupBox_1)
        self.salutationCombo.addItems(["MR", "MRS", "SHRI", "SMT", "MASTR", "KUM"])
        self.customerNameEdit = QLineEdit(self.groupBox_1)
        self.customerNameEdit.setPlaceholderText("Customer Name")
        self.customerNameEdit.setFocus()
        self.careOfEdit = QLineEdit(self.groupBox_1)
        self.villageEdit = QLineEdit(self.groupBox_1)
        self.pinCodeEdit = QLineEdit(self.groupBox_1)
        self.pinCodeEdit.setValidator(QIntValidator(0,999999))
        self.cityEdit = QLineEdit(self.groupBox_1)
        self.aadhaarNoEdit = QLineEdit(self.groupBox_1)
        self.aadhaarNoEdit.setPlaceholderText("Last 4 Digit")
        self.aadhaarNoEdit.setValidator(QIntValidator(0,9999))

        self.groupBox_2 = QGroupBox("Account Details :", self.frame)
        self.accountTypeCombo = QComboBox(self.groupBox_1)
        self.accountTypeCombo.addItems(["SBBDA", "SBGEN"])
        self.accountNoEdit = QLineEdit(self.groupBox_1)
        self.accountNoEdit.setValidator(QRegExpValidator(QRegExp("\d{1,16}"), self))
        self.cifEdit = QLineEdit(self.groupBox_1)
        self.cifEdit.setPlaceholderText("Customer ID")
        self.openDateEdit = DateEdit(self.groupBox_2)
        self.openDateEdit.setPlaceholderText("Account Opening Date")
        self.issueDateEdit = DateEdit(self.groupBox_2)
        self.issueDateEdit.setPlaceholderText("Passbook Issue Date")


        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout = QHBoxLayout(self.scrollAreaWidgetContents)
        layout.setContentsMargins(0, 0, 0, 0)
        self.passbookPage = PassbookPage(self.scrollArea)
        self.passbookPage.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.passbookPage)

        self.buttonWidget = QWidget(self.centralwidget)
        btnLayout = QHBoxLayout(self.buttonWidget)
        btnLayout.setContentsMargins(0, 0, 0, 0)
        self.generateBarcodeBtn = QPushButton(QIcon(":/icons/barcode.png"), "Generate Barcode", self.buttonWidget)
        self.saveBtn = QPushButton(QIcon(":/icons/save.png"), "Save", self.buttonWidget)
        self.printBtn = QPushButton(QIcon(":/icons/document-print.png"), "Print", self.buttonWidget)
        self.closeBtn = QPushButton(QIcon(":/icons/quit.png"), "Close", self.buttonWidget)
        btnLayout.addWidget(self.generateBarcodeBtn)
        btnLayout.addStretch()
        btnLayout.addWidget(self.saveBtn)
        btnLayout.addWidget(self.printBtn)
        btnLayout.addWidget(self.closeBtn)

        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.addRow("Branch :", self.branchNameEdit)
        self.formLayout.addRow("Address :", self.branchAddressEdit)
        self.formLayout.addRow("IFSC :", self.ifscEdit)
        self.formLayout.addRow("MICR :", self.micrEdit)

        self.formLayout_1 = QFormLayout(self.groupBox_1)
        self.formLayout_1.addRow(self.salutationCombo, self.customerNameEdit)
        self.formLayout_1.addRow("C/O :", self.careOfEdit)
        self.formLayout_1.addRow("Village :", self.villageEdit)
        self.formLayout_1.addRow("PIN :", self.pinCodeEdit)
        self.formLayout_1.addRow("City :", self.cityEdit)
        self.formLayout_1.addRow("Aadhaar :", self.aadhaarNoEdit)

        self.formLayout_2 = QFormLayout(self.groupBox_2)
        self.formLayout_2.addRow("A/c Type :", self.accountTypeCombo)
        self.formLayout_2.addRow("A/c No. :", self.accountNoEdit)
        self.formLayout_2.addRow("CIF ID. :", self.cifEdit)
        self.formLayout_2.addRow("A/c Opened :", self.openDateEdit)
        self.formLayout_2.addRow("Issue Date :", self.issueDateEdit)

        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout.addWidget(self.groupBox_1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.verticalLayout.addStretch()

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.buttonWidget, 1, 0, 1, 2)


    def updatePassbookPage(self):
        # branch info
        self.passbookPage.branch_name = self.branchNameEdit.text()
        self.passbookPage.branch_addr = self.branchAddressEdit.text()
        self.passbookPage.ifsc = self.ifscEdit.text()
        self.passbookPage.micr = self.micrEdit.text()
        # customer info
        self.passbookPage.salutation = self.salutationCombo.currentText()
        self.passbookPage.customer_name = self.customerNameEdit.text()
        self.passbookPage.care_of = self.careOfEdit.text()
        self.passbookPage.village = self.villageEdit.text()
        self.passbookPage.pin_code = self.pinCodeEdit.text()
        self.passbookPage.city = self.cityEdit.text()
        self.passbookPage.aadhaar_no = self.aadhaarNoEdit.text()
        # account info
        self.passbookPage.account_type = self.accountTypeCombo.currentText()
        self.passbookPage.account_no = self.accountNoEdit.text()
        self.passbookPage.cif = self.cifEdit.text()
        self.passbookPage.open_date = self.openDateEdit.text()
        self.passbookPage.issue_date = self.issueDateEdit.text()
        # update passbook page
        self.passbookPage.redraw()


    def savePassbookPage(self):
        if not self.passbookPage.customer_name:
            return
        filename = "%s-passbook.jpg"%self.passbookPage.customer_name
        filename, sel_filter = QFileDialog.getSaveFileName(self, "Save File",
                        filename, "JPEG Image (*.jpg)")
        if not filename:
            return
        if self.passbookPage.result.save(filename):
            QDir.setCurrent(os.path.dirname(filename))
        else:
            QMessageBox.critical(self, "Failed !", "Failed to save Image !")


    def printPassbookPage(self):
        printer = QPrinter(QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)
        # disable some options (PrintSelection, PrintCurrentPage are disabled by default)
        dlg.setOption(QPrintDialog.PrintPageRange, False)
        dlg.setOption(QPrintDialog.PrintCollateCopies, False)
        if dlg.exec() == dlg.Accepted:
            img = self.passbookPage.result
            painter = QPainter(printer)
            rect = painter.viewport()# area inside margin
            scale = rect.width()/img.width() # fit to width
            dst_rect = QRectF(0, 0.5*printer.physicalDpiY(), img.width()*scale, img.height()*scale)
            painter.drawImage(dst_rect, img)
            painter.end()

    def generateBarcode(self):
        dlg = BarcodeGeneratorDialog(self)
        dlg.exec()


    def closeEvent(self, ev):
        """ Save all settings on window close """
        self.settings = QSettings("passbook-gen", "passbook-gen", self)
        self.settings.setValue("WorkingDir", QDir.currentPath())
        if not self.isMaximized():
            self.settings.setValue("WindowWidth", self.width())
            self.settings.setValue("WindowHeight", self.height())
        self.settings.setValue("WindowMaximized", self.isMaximized())
        self.settings.setValue("BranchName", self.branchNameEdit.text())
        self.settings.setValue("BranchAddress", self.branchAddressEdit.text())
        self.settings.setValue("IFSC", self.ifscEdit.text())
        self.settings.setValue("MICR", self.micrEdit.text())

        self.settings.setValue("Village", self.villageEdit.text())
        self.settings.setValue("PinCode", self.pinCodeEdit.text())
        self.settings.setValue("City", self.cityEdit.text())
        if len(self.accountNoEdit.text())==16:
            self.settings.setValue("AccountNo", self.accountNoEdit.text()[:11])
        QMainWindow.closeEvent(self, ev)



class PassbookPage(QLabel):

    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.passbook_bg = QImage(os.path.dirname(__file__) + "/passbook-page.jpg")
        self.result = None # generate passbook page
        # page format
        self.setPageSize(595,842) # calculates page_w and  page_h
        # branch info
        self.branch_name = ""
        self.branch_addr = ""
        self.ifsc = ""
        self.micr = ""
        # customer info
        self.salutation = ""
        self.customer_name = ""
        self.customer_addr = ""
        self.care_of = ""
        self.village = ""
        self.city = ""
        self.pin_code = ""
        self.aadhaar_no = ""
        # account info
        self.account_type = ""
        self.account_no = ""
        self.cif = ""
        self.open_date = ""
        self.issue_date = ""


    def setPageSize(self, w, h):
        self.page_size = w, h
        dpi = max(self.physicalDpiX(), self.physicalDpiY())
        self.page_w = int(w*dpi/72)
        self.page_h = int(h*dpi/72)


    def redraw(self):
        self.result = self.passbook_bg.copy()
        self.result.setDotsPerMeterX(11810)
        self.result.setDotsPerMeterY(11810)
        painter = QPainter(self.result)
        self.drawOnPainter(painter, self.result.width(), self.result.height())
        painter.end()
        self.setPixmap(QPixmap.fromImage(self.result.scaledToWidth(826)))


    def drawOnPainter(self, painter, page_w, page_h):
        scale_x = 0.8
        painter.setTransform(QTransform.fromScale(scale_x,1.0))# to make fonts narrower

        painter.setPen(QColor(145,145,145))
        if platform.system()=="Windows":
            font = QFont("Consolas", 10)
            line_height = int(0.9*QFontMetrics(font, painter.device()).height())
        else: # linux
            font = QFont("DejaVu Sans Mono", 9)
            line_height = QFontMetrics(font, painter.device()).height()
        painter.setFont(font)



        scale = page_w/21.0 # cm to px conversion factor

        left = int(1.9*scale/scale_x) # for most line lines
        left1 = int(3.0*scale/scale_x) # for account type header
        left2 = int(0.5*scale/scale_x) # for comments
        line_top = int(0.8*scale)

        s = "Each depositor is insured by DICGC upto a maximum Rs.5.00lac"
        painter.drawText(QPoint(left2, line_top), s)
        line_top += line_height

        s = "subject to change from time to time.(T&C applicable)"
        painter.drawText(QPoint(left2, line_top), s)
        line_top += line_height

        line_top = int(3.2*scale)

        painter.drawText(QPoint(left, line_top), "BO :  " + self.branch_name)
        line_top += line_height

        painter.drawText(QPoint(left2, line_top), self.branch_addr)
        line_top += line_height

        line_top = int(5.0*scale)

        if self.account_type=="SBBDA":
            painter.drawText(QPoint(left1, line_top), "SAVINGS FUND BASIC DEP A/C")
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "MICR Code: %s  IFSC Code: %s" %(self.micr, self.ifsc))
        line_top += line_height

        s = "*Toll Free-18001802222/18001032222, Tolled-01202490000,Email-care@pnb.co.in*"
        painter.drawText(QPoint(left2, line_top), s)
        line_top += line_height

        s = "*Principal Nodal Officer: Phn- 0124-4126244*"
        painter.drawText(QPoint(left, line_top), s)
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "CKYC:")
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "CIF Id: %s M/O Oper.: SELF"%self.cif)
        line_top += line_height

        if self.aadhaar_no:
            painter.drawText(QPoint(left, line_top), "A/C No: %s INR Aadhaar:XX%s"%(self.account_no, self.aadhaar_no))
        else:
            painter.drawText(QPoint(left, line_top), "A/C No: %s INR"%self.account_no)
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "%s %s"%(self.salutation, self.customer_name))
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "Account Open Date : %s"%(self.open_date))
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "C/O: %s"%self.care_of)
        line_top += line_height

        painter.drawText(QPoint(left, line_top), self.village)
        line_top += line_height
        line_top += line_height

        painter.drawText(QPoint(left, line_top), self.city)
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "WEST BENGAL      INDIA    Pin: %s"%self.pin_code)
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "Nomination not Registered")
        line_top += line_height

        painter.drawText(QPoint(left, line_top), "Date of Issue : %s"%self.issue_date)
        line_top += line_height



class DateEdit(QLineEdit):
    """ automatically puts date-separator between numbers """
    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self.sep = "-" # date separator
        # validator for "DD/MM/YYYY" (allows entering DDMMYYYY then converts to DD/MM/YYYY)
        self.setValidator(QRegExpValidator(QRegExp("\d{2}[0-9%s]\d{2}[0-9%s]\d{4}"%(self.sep,self.sep)), self))

    def keyPressEvent(self, ev):
        # automatically insert / where required
        QLineEdit.keyPressEvent(self, ev)
        text = self.text()
        if len(text) in (3,6) and text[-1]!=self.sep:
            self.setText(text[:-1] + self.sep + text[-1])

    def setToday(self):
        """ set today's date """
        self.setText(datetime.today().strftime(self.sep.join(["%d","%m","%Y"])))


def main():
    app = QApplication(sys.argv)
    #app.setOrganizationName("Arindamsoft")
    app.setApplicationName("PassbookGen")
    # use fusion style on Windows platform
    if platform.system()=="Windows" and "Fusion" in QStyleFactory.keys():
        app.setStyle(QStyleFactory.create("Fusion"))
    # add font (not used because adding fonts creates ugly rendering)
    #id = QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/DejaVuSansMono.ttf")
    #family = QFontDatabase.applicationFontFamilies(id)[0]
    # load window
    win = Window()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
