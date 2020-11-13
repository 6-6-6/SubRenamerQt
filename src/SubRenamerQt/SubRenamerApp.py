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

    buttons = {'PreviewButton': ['Preview', 'fillNewSubtitles'],
               'RunButton': ['Run', 'renameSubtitles'],
               'MiscsButton': ['Misc', 'createMiscDialog']}

    boxes = {'ToVideosBox': ['Move Subtitles to The Directory of Video Files', None],
             'OnTopBox': ['Always on Top', 'setOnTop']}

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
        ## set a layout
        self.mFWidgetLayout = QHBoxLayout(self.multiFuncWidget)
        self.mFWidgetLayout.setObjectName("mFWidgetLayout")

        for button in self.buttons:
            tmpButton = QPushButton(self.multiFuncWidget)
            tmpButton.setObjectName(button)
            setattr(self, button, tmpButton)
            self.mFWidgetLayout.addWidget(tmpButton)
        #
        for box in self.boxes:
            tmpBox = QCheckBox(self.multiFuncWidget)
            tmpBox.setObjectName(box)
            setattr(self, box, tmpBox)
            self.mFWidgetLayout.addWidget(tmpBox)

        self.gridLayout.addWidget(self.multiFuncWidget, 2, 0, 1, 1)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "mainWindow", "SubRenamerQt", None))
        # measure length of the button
        met = QFontMetrics(self.mediumFont)
        buttonWidth = 0
        translatedText = []

        # translate texts, and get button width
        for buttonName in self.buttons:
            text = QCoreApplication.translate(
                "mainWindow",
                self.buttons[buttonName][0],
                None)
            translatedText.append(text)
            text += '        '
            if buttonWidth < met.horizontalAdvance(text):
                buttonWidth = met.horizontalAdvance(text)
        # set text
        for buttonName in self.buttons:
            button = getattr(self, buttonName)
            func = getattr(self, self.buttons[buttonName][1])
            button.setText(translatedText.pop(0))
            button.clicked.connect(func)
            button.setFont(self.mediumFont)
            buttonHeight = button.sizeHint().height()
            button.setMinimumSize(QSize(buttonWidth, buttonHeight))
            button.setMaximumSize(QSize(buttonWidth, buttonHeight))

        #
        for boxName in self.boxes:
            text = QCoreApplication.translate(
                "mainWindow",
                self.boxes[boxName][0],
                None)
            box = getattr(self, boxName)
            box.setText(text)
            box.setFont(self.mediumFont)
            boxWidth = box.sizeHint().width()
            box.setMinimumSize(QSize(boxWidth, buttonHeight))
            box.setMaximumSize(QSize(boxWidth, buttonHeight))
            if self.boxes[boxName][1]:
                func = getattr(self, self.boxes[boxName][1])
                box.stateChanged.connect(func)
        # make the app stay on top by default
        self.OnTopBox.setCheckState(Qt.Checked)
        # set the length of the last widget to 65536
        self.OnTopBox.setMaximumSize(QSize(65535, buttonHeight))
        # set height of the parent
        mFWHeight = self.multiFuncWidget.sizeHint().height()
        self.multiFuncWidget.setMinimumSize(QSize(0, mFWHeight))
        self.multiFuncWidget.setMaximumSize(QSize(16777215, mFWHeight))
    # retranslateUi

    def createMiscDialog(self):
        self.setIsPrepared(False)
        dlg = QDialog(self.centralwidget)
        dlgUi = NMiscDialog(self, dlg)
        dlg.exec_()

    def createMessageBox(self, level, msg, detailedMsg=None):
        msgBox = QMessageBox(self.centralwidget)
        msgBox.setIcon(level)
        msgBox.setText(QCoreApplication.translate(
            "ErrorMsgBox",
            msg,
            None))
        if detailedMsg:
            msgBox.setDetailedText(QCoreApplication.translate(
                "ErrorMsgBox",
                detailedMsg,
                None))
        msgBox.exec_()

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
        self.setIsPrepared(False)
        if self.videoFiles.count() != self.oldSubtitles.count():
            self.createMessageBox(
                QMessageBox.Information,
                "The number of video files does not" +
                " match the number of subtitles.",
                None)
            return
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
            self.createMessageBox(
                QMessageBox.Information,
                "I have not prepared to rename the subtitles.",
                'Please click "Preview" first.')
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
            self.createMessageBox(
                QMessageBox.Warning,
                "An exception is encountered while renaming " +
                f"the {toOrdinal(i+1)} subtitle.",
                f"{ex}")
        self.setIsPrepared(False)


def main():
    app = QApplication([])

    w = QMainWindow()
    a = Ui_MainWindow()
    a.setupUi(w)
    w.show()

    app.exec_()
