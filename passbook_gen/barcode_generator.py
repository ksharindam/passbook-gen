# -*- coding: utf-8 -*-
# This file is a part of PassbookGen Program which is GNU GPLv3 licensed
# Copyright (C) 2024 Arindam Chaudhuri <arindamsoft94@gmail.com>
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QIcon
from PyQt5.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
     QPushButton, QSizePolicy, QDialogButtonBox, QWidget, QFileDialog)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog


data = [
# widths    A           B           C
"212222",   " ",        " ",        "00",
"222122",   "!",        "!",        "01",
"222221",   "\"",       "\"",       "02",
"121223",   "#",        "#",        "03",
"121322",   "$",        "$",        "04",
"131222",   "%",        "%",        "05",
"122213",   "&",        "&",        "06",
"122312",   "'",        "'",        "07",
"132212",   "(",        "(",        "08",
"221213",   ")",        ")",        "09",
"221312",   "*",        "*",        "10",
"231212",   "+",        "+",        "11",
"112232",   ",",        ",",        "12",
"122132",   "-",        "-",        "13",
"122231",   ".",        ".",        "14",
"113222",   "/",        "/",        "15",
"113222",   "0",        "0",        "16",
"123221",   "1",        "1",        "17",
"223211",   "2",        "2",        "18",
"221132",   "3",        "3",        "19",
"221231",   "4",        "4",        "20",
"213212",   "5",        "5",        "21",
"223112",   "6",        "6",        "22",
"312131",   "7",        "7",        "23",
"311222",   "8",        "8",        "24",
"321122",   "9",        "9",        "25",
"321221",   ":",        ":",        "26",
"312212",   ";",        ";",        "27",
"322112",   "<",        "<",        "28",
"322211",   "=",        "=",        "29",
"212123",   ">",        ">",        "30",
"212321",   "?",        "?",        "31",
"232121",   "@",        "@",        "32",
"111323",   "A",        "A",        "33",
"131123",   "B",        "B",        "34",
"131321",   "C",        "C",        "35",
"112313",   "D",        "D",        "36",
"132113",   "E",        "E",        "37",
"132311",   "F",        "F",        "38",
"211313",   "G",        "G",        "39",
"231113",   "H",        "H",        "40",
"231311",   "I",        "I",        "41",
"112133",   "J",        "J",        "42",
"112331",   "K",        "K",        "43",
"132131",   "L",        "L",        "44",
"113123",   "M",        "M",        "45",
"113321",   "N",        "N",        "46",
"133121",   "O",        "O",        "47",
"313121",   "P",        "P",        "48",
"211331",   "Q",        "Q",        "49",
"231131",   "R",        "R",        "50",
"213113",   "S",        "S",        "51",
"213311",   "T",        "T",        "52",
"213131",   "U",        "U",        "53",
"311123",   "V",        "V",        "54",
"311321",   "W",        "W",        "55",
"331121",   "X",        "X",        "56",
"312113",   "Y",        "Y",        "57",
"312311",   "Z",        "Z",        "58",
"332111",   "[",        "[",        "59",
"314111",   "\\",       "\\",       "60",
"221411",   "]",        "]",        "61",
"431111",   "^",        "^",        "62",
"111224",   "_",        "_",        "63",
"111422",   "\x00",     "`",        "64",
"121124",   "\x01",     "a",        "65",
"121421",   "\x02",     "b",        "66",
"141122",   "\x03",     "c",        "67",
"141221",   "\x04",     "d",        "68",
"112214",   "\x05",     "e",        "69",
"112412",   "\x06",     "f",        "70",
"122114",   "\x07",     "g",        "71",
"122411",   "\x08",     "h",        "72",
"142112",   "\t",       "i",        "73",
"142211",   "\n",       "j",        "74",
"241211",   "\v",       "k",        "75",
"221114",   "\f",       "l",        "76",
"413111",   "\r",       "m",        "77",
"241112",   "\x0e",     "n",        "78",
"134111",   "\x0f",     "o",        "79",
"111242",   "\x10",     "p",        "80",
"121142",   "\x11",     "q",        "81",
"121241",   "\x12",     "r",        "82",
"114212",   "\x13",     "s",        "83",
"124112",   "\x14",     "t",        "84",
"124211",   "\x15",     "u",        "85",
"411212",   "\x16",     "v",        "86",
"421112",   "\x17",     "w",        "87",
"421211",   "\x18",     "x",        "88",
"212141",   "\x19",     "y",        "89",
"214121",   "\x1a",     "z",        "90",
"412121",   "\x1b",     "{",        "91",
"111143",   "\x1c",     "|",        "92",
"111341",   "\x1d",     "}",        "93",
"131141",   "\x1e",     "~",        "94",
"114113",   "\x1f",     "DEL",      "95",
"114311",   "FNC3",     "FNC3",     "96",
"411113",   "FNC2",     "FNC2",     "97",
"411311",   "ShiftB",   "ShiftA",   "98",
"113141",   "CodeC",    "CodeC",    "99",
"114131",   "CodeB",    "FNC4",     "CodeB",
"311141",   "FNC4",     "CodeA",    "CodeA",
"411131",   "FNC1",     "FNC1",     "FNC1",
"211412",   "StartA",   "StartA",   "StartA",
"211214",   "StartB",   "StartB",   "StartB",
"211232",   "StartC",   "StartC",   "StartC",
"2331112",  "Stop",     "Stop",     "Stop",
]

class Code128():

    def __init__(self):
        self.codeset_type = None
        self.codeset = None
        self.A = {}
        self.B = {}
        self.C = {}
        self.WIDTHS = []

        for i in range(len(data)//4):
            self.A[data[i*4+1]] = i
            self.B[data[i*4+2]] = i
            self.C[data[i*4+3]] = i
            self.WIDTHS.append(data[i*4])

    def set_codeset_type(self, codeset_type):
        codesets = {"A": self.A, "B": self.B, "C": self.C}
        self.codeset = codesets[codeset_type]
        self.codeset_type = codeset_type


    def generate(self, text):
        """ returns a list of alternating bar and space widths """
        text = str(text).encode('latin_1', 'replace').decode('latin_1')
        length = len(text)
        codes = []
        # Start Code
        # C is effective if starts with atleast 4 digits,
        # or whole text consists of only two digits
        if (length==2 and text.isdigit()) or (length>=4 and text[:4].isdigit()):
            self.set_codeset_type("C")
        # start with A if text contains A-only character
        elif need_a(text, 0):
            self.set_codeset_type("A")
        else:
            self.set_codeset_type("B")

        codes.append(self.codeset["Start"+self.codeset_type])

        # Data
        pos = 0
        while pos < length:
            if self.codeset_type=="C" and length-pos>=2 and text[pos:pos+2].isdigit():
                codes.append(int(text[pos:pos+2]))
                pos += 2

            elif self.codeset_type!="C" \
                 and ( (length-pos>=6 and text[pos:pos+6].isdigit()) \
                     or (length-pos==4 and text[pos:pos+4].isdigit() )):
                codes.append(self.codeset["CodeC"])
                self.set_codeset_type("C")

            # switch to A if there is atleast one A-only character. and
            # there is no B-only character before that.
            elif (self.codeset_type!="A" and need_a(text, pos)):
                codes.append(self.codeset["CodeA"])
                self.set_codeset_type("A")
            # if contains B-only character, switch to B
            elif self.codeset_type=="C" or (self.codeset_type=="A" and ord(text[pos])>=96):
                codes.append(self.codeset["CodeB"])
                self.set_codeset_type("B")
            # switching not needed, append character
            else:
                codes.append(self.codeset[text[pos]])
                pos += 1

        # Checksum
        checksum = 0
        for weight, code in enumerate(codes):
            checksum += max(weight, 1) * code
        codes.append(checksum % 103)

        # Stop Code
        codes.append(self.codeset["Stop"])

        # calculate bars
        barcode_widths = []
        for code in codes:
            for width in self.WIDTHS[code]:
                barcode_widths.append(int(width))

        return barcode_widths


# should have atleast one of A-only characters and before that
# must not have any B-only character
def need_a(text, pos):
    for i in range(pos, len(text)):
        val = ord(text[i])
        if val>=96:# B-only character
            return False
        if val<32:# A-only character
            return True
    # all characters fit in B
    return False



class BarcodeGeneratorDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Barcode Generator")
        self.resize(250, 150)
        self.setupUi()
        self.result = None

    def setupUi(self):
        layout = QGridLayout(self)
        label = QLabel("Barcode Type : Code 128", self)
        self.textEdit = QLineEdit(self)
        self.textEdit.setPlaceholderText("Enter A/c No...")
        self.barcodeLabel = QLabel(self)
        self.barcodeLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        pm = QPixmap(250,78)
        pm.fill()
        self.barcodeLabel.setPixmap(pm)
        self.buttonWidget = QWidget(self)
        btnLayout = QHBoxLayout(self.buttonWidget)
        btnLayout.setContentsMargins(0, 0, 0, 0)
        self.saveBtn = QPushButton(QIcon(":/icons/save.png"), "Save", self.buttonWidget)
        self.printBtn = QPushButton(QIcon(":/icons/document-print.png"), "Print", self.buttonWidget)
        self.closeBtn = QPushButton(QIcon(":/icons/quit.png"), "Close", self.buttonWidget)
        btnLayout.addStretch()
        btnLayout.addWidget(self.saveBtn)
        btnLayout.addWidget(self.printBtn)
        btnLayout.addWidget(self.closeBtn)

        layout.addWidget(label, 0,0,1,1)
        layout.addWidget(self.textEdit, 1,0,1,1)
        layout.addWidget(self.barcodeLabel, 2,0,1,1)
        layout.addWidget(self.buttonWidget, 3,0,1,1)

        self.textEdit.textEdited.connect(self.generateBarcode)
        self.saveBtn.clicked.connect(self.saveBarcode)
        self.printBtn.clicked.connect(self.printBarcode)
        self.closeBtn.clicked.connect(self.close)


    def generateBarcode(self):
        bars = Code128().generate(self.textEdit.text())
        self.result = self.drawBarcode(bars, self.textEdit.text())
        scaled_result = self.result.scaledToWidth(250, Qt.SmoothTransformation)
        self.barcodeLabel.setPixmap(QPixmap.fromImage(scaled_result))


    def drawBarcode(self, bars, text):
        barcode_w, barcode_h = 614, 142 # 5.2x1.2cm @300 dpi
        margin = 20
        dpi = 300
        img_w = barcode_w + 2*margin
        img_h = barcode_h + 3*margin
        # calculate unit thickness of bars
        sum_w = 20 # 10 units of quiet zone on each side
        for w in bars:
            sum_w += w
        thickness = barcode_w//sum_w

        img = QImage(img_w, img_h, QImage.Format_RGB32)
        img.fill(Qt.white)
        img.setDotsPerMeterX(int(dpi/0.0254))
        img.setDotsPerMeterY(int(dpi/0.0254))

        painter = QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(Qt.black)

        x = (img_w - (sum_w-20)*thickness)//2 # horizontal center
        bar = True# bar or space
        for w in bars:
            if bar:
                painter.drawRect(x,margin, w*thickness, barcode_h)
            bar = not bar
            x += w*thickness

        # draw border
        painter.setPen(QPen(Qt.black, 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0,0,img_w, img_h)
        # draw text
        font = painter.font()
        font.setPointSize(7)
        painter.setFont(font)
        painter.drawText(QRect(0, margin+barcode_h, img_w, 2*margin), Qt.AlignCenter, text)
        painter.end()
        return img


    def saveBarcode(self):
        if not self.result:
            return
        filename = "barcode-%s.jpg"%self.textEdit.text()
        filename, sel_filter = QFileDialog.getSaveFileName(self, "Save File",
                        filename, "JPEG Image (*.jpg)")
        if not filename:
            return
        if not self.result.save(filename):
            QMessageBox.critical(self, "Failed !", "Failed to save Barcode Image !")


    def printBarcode(self):
        if not self.result:
            return
        printer = QPrinter(QPrinter.HighResolution)
        #printer.setOutputFileName("barcode-%s.pdf"%self.textEdit.text())
        dlg = QPrintDialog(printer, self)
        # disable some options (PrintSelection, PrintCurrentPage are disabled by default)
        dlg.setOption(QPrintDialog.PrintPageRange, False)
        dlg.setOption(QPrintDialog.PrintCollateCopies, False)
        if dlg.exec() == dlg.Accepted:
            img = self.result
            painter = QPainter(printer)
            rect = painter.viewport()# area inside margin
            dpi = printer.physicalDpiY()
            scale = dpi/300 # 300 is rendered dpi
            dst_rect = QRectF(0.3*dpi, 0.2*dpi, img.width()*scale, img.height()*scale)
            painter.drawImage(dst_rect, img)
            painter.end()

