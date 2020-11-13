#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .NMiscDialog import NMiscDialog
from .NQListWidget import NQListWidget
from .NUtils import toOrdinal


class Ui_MainWindow(object):

    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1400, 600)
        self.mainWindow = mainWindow
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.smallFont = QFont()
        self.smallFont.setPointSize(9)
        self.mediumFont = QFont()
        self.mediumFont.setPointSize(11)

        self.initListPreviewWidget()
        self.initMultiFunctionWidget()

        self.mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def initListPreviewWidget(self):
        self.listPreviewWidget = QWidget(self.centralwidget)
        self.listPreviewWidget.setObjectName("listPreviewWidget")
        self.listPreviewLayout = QHBoxLayout(self.listPreviewWidget)
        self.listPreviewLayout.setObjectName("listPreviewLayout")
        # list 1
        self.videoFiles = NQListWidget(
            self, self.listPreviewWidget, hint="video")
        self.videoFiles.setObjectName("videoFiles")
        self.videoFiles.setFont(self.smallFont)
        self.listPreviewLayout.addWidget(self.videoFiles)
        # list 2
        self.oldSubtitles = NQListWidget(
            self, self.listPreviewWidget, hint="subtitle")
        self.oldSubtitles.setObjectName("oldSubtitles")
        self.oldSubtitles.setFont(self.smallFont)
        self.listPreviewLayout.addWidget(self.oldSubtitles)
        # list 3
        self.newSubtitles = QListWidget(self.listPreviewWidget)
        self.newSubtitles.setObjectName("newSubtitles")
        self.newSubtitles.setFont(self.smallFont)
        self.listPreviewLayout.addWidget(self.newSubtitles)
        # state
        self.setIsPrepared(False)

        self.gridLayout.addWidget(self.listPreviewWidget, 1, 0, 1, 1)

    def initMultiFunctionWidget(self):
        # initialize widget
        self.multiFuncWidget = QWidget(self.centralwidget)
        self.multiFuncWidget.setObjectName("multiFuncWidget")
        self.multiFuncWidget.setMinimumSize(QSize(0, 40))
        self.multiFuncWidget.setMaximumSize(QSize(16777215, 40))
        ## set a layout
        self.mFWidgetLayout = QHBoxLayout(self.multiFuncWidget)
        self.mFWidgetLayout.setObjectName("mFWidgetLayout")

        # initialize buttons
        buttons = ['PreviewButton',
                   'RunButton',
                   'MiscsButton']
        for button in buttons:
            tmpButton = QPushButton(self.multiFuncWidget)
            tmpButton.setObjectName(button)
            tmpButton.setMinimumSize(QSize(122, 30))
            tmpButton.setMaximumSize(QSize(122, 30))
            tmpButton.setFont(self.mediumFont)
            setattr(self, button, tmpButton)
            self.mFWidgetLayout.addWidget(tmpButton)
        #
        boxes = ['ToVideosBox', 'OnTopBox']
        for box in boxes:
            tmpBox = QCheckBox(self.multiFuncWidget)
            tmpBox.setObjectName(box)
            tmpBox.setMinimumSize(QSize(130, 30))
            tmpBox.setMaximumSize(QSize(450, 30))
            tmpBox.setFont(self.mediumFont)
            setattr(self, box, tmpBox)
            self.mFWidgetLayout.addWidget(tmpBox)

        getattr(self, boxes[-1]).setMaximumSize(QSize(8192, 30))
        self.gridLayout.addWidget(self.multiFuncWidget, 2, 0, 1, 1)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "mainWindow", "SubRenamerQt", None))

        # translate PreviewButton
        self.PreviewButton.setText(QCoreApplication.translate(
            "mainWindow", "Preview", None))
        self.PreviewButton.clicked.connect(self.fillNewSubtitles)
        # translate RunButton
        self.RunButton.setText(QCoreApplication.translate(
            "mainWindow", "Run", None))
        self.RunButton.clicked.connect(self.renameSubtitles)
        # translate MiscsButton
        self.MiscsButton.setText(QCoreApplication.translate(
            "mainWindow", "Misc", None))
        self.MiscsButton.clicked.connect(self.createMiscDialog)
        #
        self.ToVideosBox.setText(QCoreApplication.translate(
            "mainWindow",
            "Move Subtitles to The Directory of Video Files",
            None))
        #
        self.OnTopBox.setText(QCoreApplication.translate(
            "mainWindow",
            "Always on Top",
            None))
        self.OnTopBox.stateChanged.connect(self.setOnTop)
        self.OnTopBox.setCheckState(Qt.Checked)
    # retranslateUi

    def createMiscDialog(self):
        self.setIsPrepared(False)
        dlg = QDialog(self.centralwidget)
        dlgUi = NMiscDialog(self, dlg)
        dlg.exec_()

    def setIsPrepared(self, state):
        if state:
            self.isPrepared = True
        else:
            self.newSub = {}
            self.newSubtitles.clear()
            self.isPrepared = False

    def setOnTop(self, state):
        flags = self.mainWindow.windowFlags()
        if Qt.Checked == state:
            self.mainWindow.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.mainWindow.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.mainWindow.show()

    def fillNewSubtitles(self):
        if self.videoFiles.count() != self.oldSubtitles.count():
            # msgbox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(QCoreApplication.translate(
                "ErrorMsgBox",
                "The number of video files does not" +
                " match the number of subtitles.",
                None))
            msg.exec_()
            return
        #
        self.setIsPrepared(False)
        #
        for i in range(self.oldSubtitles.count()):
            #
            videoFile = self.videoFiles.item(i).text()
            subtitleName = self.videoFiles.realData[videoFile].stem
            #
            oldSubtitle = self.oldSubtitles.item(i).text()
            subtitleSfx = self.oldSubtitles.realData[oldSubtitle].suffix
            #
            if self.ToVideosBox.isChecked():
                dstPfx = self.videoFiles.realData[videoFile].parent
            else:
                dstPfx = self.oldSubtitles.realData[oldSubtitle].parent
            #
            fname = subtitleName + subtitleSfx
            self.newSubtitles.addItem(fname)
            self.newSub[fname] = Path(dstPfx / fname)
        self.setIsPrepared(True)

    def renameSubtitles(self):
        # check whether the app is prepared to rename the stuffs
        if not self.isPrepared:
            # msgbox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(QCoreApplication.translate(
                "ErrorMsgBox",
                "I have not prepared to rename the subtitles.",
                None))
            msg.setDetailedText(QCoreApplication.translate(
                "ErrorMsgBox",
                "Please click \"Preview\" first.",
                None))
            msg.exec_()
            return
        # catch exceptions while renaming the things
        try:
            for i in range(self.oldSubtitles.count()):
                #
                oldSubtitle = self.oldSubtitles.item(i).text()
                oldSubtitle = self.oldSubtitles.realData[oldSubtitle]
                #
                newSubtitle = self.newSub[self.newSubtitles.item(i).text()]
                #
                shutil.move(oldSubtitle, newSubtitle)
        except Exception as ex:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(QCoreApplication.translate(
                "ErrorMsgBox",
                "An exception is encountered while renaming " +
                f"the {toOrdinal(i+1)} subtitle.",
                None))
            msg.setDetailedText(f"{ex}")
            msg.exec_()
        self.setIsPrepared(False)


def main():
    app = QApplication([])

    w = QMainWindow()
    a = Ui_MainWindow()
    a.setupUi(w)
    w.show()

    app.exec_()
