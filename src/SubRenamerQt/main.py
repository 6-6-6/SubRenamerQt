#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from NQListWidget import NQListWidget
from NUtils import toOrdinal


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.smallFont = QFont()
        self.smallFont.setPointSize(9)
        self.mediumFont = QFont()
        self.mediumFont.setPointSize(12)

        self.initListPreviewWidget()
        self.initMultiFunctionWidget()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def initListPreviewWidget(self):
        self.ListWidget = QWidget(self.centralwidget)
        self.ListWidget.setObjectName("ListWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.ListWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # list 1
        self.VideoFiles = NQListWidget(self, self.ListWidget, hint="video")
        self.VideoFiles.setObjectName("VideoFiles")
        self.VideoFiles.setFont(self.smallFont)
        self.horizontalLayout.addWidget(self.VideoFiles)
        # list 2
        self.OldSubtitles = NQListWidget(
            self, self.ListWidget, hint="subtitle")
        self.OldSubtitles.setObjectName("OldSubtitles")
        self.OldSubtitles.setFont(self.smallFont)
        self.horizontalLayout.addWidget(self.OldSubtitles)
        # list 3
        self.NewSubtitles = QListWidget(self.ListWidget)
        self.NewSubtitles.setObjectName("NewSubtitles")
        self.NewSubtitles.setFont(self.smallFont)
        self.horizontalLayout.addWidget(self.NewSubtitles)
        # state
        self.setIsPrepared(False)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout.addWidget(self.ListWidget, 1, 0, 1, 1)

    def initMultiFunctionWidget(self):
        self.MultiFuncWidget = QWidget(self.centralwidget)
        self.MultiFuncWidget.setObjectName("MultiFuncWidget")
        self.MultiFuncWidget.setMinimumSize(QSize(0, 30))
        self.MultiFuncWidget.setMaximumSize(QSize(16777215, 30))
        #
        self.SortList1Button = QPushButton(self.MultiFuncWidget)
        self.SortList1Button.setObjectName("SortList1Button")
        self.SortList1Button.setGeometry(QRect(10, 0, 122, 30))
        self.SortList1Button.setMinimumSize(QSize(122, 30))
        self.SortList1Button.setFont(self.mediumFont)
        self.SortList2Button = QPushButton(self.MultiFuncWidget)
        self.SortList2Button.setObjectName("SortList2Button")
        self.SortList2Button.setGeometry(QRect(140, 0, 122, 30))
        self.SortList2Button.setMinimumSize(QSize(122, 30))
        self.SortList2Button.setFont(self.mediumFont)
        self.PreviewButton = QPushButton(self.MultiFuncWidget)
        self.PreviewButton.setObjectName("PreviewButton")
        self.PreviewButton.setGeometry(QRect(270, 0, 122, 30))
        self.PreviewButton.setMinimumSize(QSize(122, 30))
        self.PreviewButton.setFont(self.mediumFont)
        self.RunButton = QPushButton(self.MultiFuncWidget)
        self.RunButton.setObjectName("RunButton")
        self.RunButton.setGeometry(QRect(400, 0, 122, 30))
        self.RunButton.setMinimumSize(QSize(122, 30))
        self.RunButton.setFont(self.mediumFont)
        #
        self.checkBox = QCheckBox(self.MultiFuncWidget)
        self.checkBox.setObjectName("checkBox_2")
        self.checkBox.setGeometry(QRect(530, 0, 491, 30))
        self.checkBox.setMinimumSize(QSize(130, 30))
        self.checkBox.setFont(self.mediumFont)

        self.gridLayout.addWidget(self.MultiFuncWidget, 2, 0, 1, 1)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", "SubRenamerQt", None))

        #__sortingEnabled = self.VideoFiles.isSortingEnabled()
        # self.VideoFiles.setSortingEnabled(False)
        # self.VideoFiles.setSortingEnabled(__sortingEnabled)
        self.SortList1Button.setText(QCoreApplication.translate(
            "MainWindow", "Sort List1", None))
        self.SortList1Button.clicked.connect(self.VideoFiles.sortItems)
        #
        self.SortList2Button.setText(QCoreApplication.translate(
            "MainWindow", "Sort List2", None))
        self.SortList1Button.clicked.connect(self.OldSubtitles.sortItems)
        #
        self.PreviewButton.setText(QCoreApplication.translate(
            "MainWindow", "Preview", None))
        self.PreviewButton.clicked.connect(self.fillNewSubtitles)
        #
        self.RunButton.setText(QCoreApplication.translate(
            "MainWindow", "Run", None))
        self.RunButton.clicked.connect(self.renameSubtitles)
        #
        self.checkBox.setText(QCoreApplication.translate(
            "MainWindow",
            "Move Subtitles to The Directory of Video Files",
            None))
    # retranslateUi

    def setIsPrepared(self, state):
        if state:
            self.isPrepared = True
        else:
            self.newSub = {}
            self.NewSubtitles.clear()
            self.isPrepared = False

    def fillNewSubtitles(self):
        if self.VideoFiles.count() != self.OldSubtitles.count():
            # msgbox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(QCoreApplication.translate(
                "The number of video files does not" +
                " match the number of subtitles."))
            msg.exec_()
            return
        #
        self.setIsPrepared(False)
        #
        for i in range(self.OldSubtitles.count()):
            #
            videoFile = self.VideoFiles.item(i).text()
            subtitleName = self.VideoFiles.realData[videoFile].stem
            #
            oldSubtitle = self.OldSubtitles.item(i).text()
            subtitleSfx = self.OldSubtitles.realData[oldSubtitle].suffix
            #
            if self.checkBox.isChecked():
                dstPfx = self.VideoFiles.realData[videoFile].parent
            else:
                dstPfx = self.OldSubtitles.realData[oldSubtitle].parent
            #
            fname = subtitleName + subtitleSfx
            self.NewSubtitles.addItem(fname)
            self.newSub[fname] = Path(dstPfx / fname)
        self.setIsPrepared(True)

    # @pyqtSlot()

    def renameSubtitles(self):
        # check whether the app is prepared to rename the stuffs
        if not self.isPrepared:
            # msgbox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(QCoreApplication.translate(
                "I have not prepared to rename the subtitles."))
            msg.setDetailedText(QCoreApplication.translate(
                "Please click \"Preview\" first."))
            msg.exec_()
            return
        # catch exceptions while renaming the things
        try:
            for i in range(self.OldSubtitles.count()):
                #
                oldSubtitle = self.OldSubtitles.item(i).text()
                oldSubtitle = self.OldSubtitles.realData[oldSubtitle]
                #
                newSubtitle = self.newSub[self.NewSubtitles.item(i).text()]
                #
                shutil.move(oldSubtitle, newSubtitle)
        except Exception as ex:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(QCoreApplication.translate(
                "An exception is encountered while renaming " +
                f"the {toOrdinal(i+1)} subtitle."))
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


