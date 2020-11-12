#!/usr/bin/python
# -*- coding:utf-8 -*-

import weakref
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class NMiscDialog(object):
    appId = "MiscDialog"
    hints = ['Videos', 'Subtitles']

    def __init__(self, parent, dialog, name='MiscDialog'):
        self.dialog = weakref.ref(dialog)
        self.parent = weakref.ref(parent)
        dialog.setObjectName(name)
        dialog.resize(400, 300)
        #
        self.setupUi()
        self.retranslateUi()
        self.connectButtons()
        QMetaObject.connectSlotsByName(dialog)

    def connectButtons(self):
        vDict = self.VideosWidgetCpnt
        sDict = self.SubtitlesWidgetCpnt
        #
        vDict['save'].clicked.connect(
            lambda: self.parent().videoFiles.setItemFilter(
                vDict['inputBox'].text()))
        vDict['clear'].clicked.connect(
            lambda: self.parent().videoFiles.setItemFilter('.'))
        vDict['filter'].clicked.connect(
            lambda: self.parent().videoFiles.applyItemFilter())
        vDict['sort'].clicked.connect(
            lambda: self.parent().videoFiles.sortItems())
        #
        sDict['save'].clicked.connect(
            lambda: self.parent().oldSubtitles.setItemFilter(
                sDict['inputBox'].text()))
        sDict['clear'].clicked.connect(
            lambda: self.parent().oldSubtitles.setItemFilter('.'))
        sDict['filter'].clicked.connect(
            lambda: self.parent().oldSubtitles.applyItemFilter())
        sDict['sort'].clicked.connect(
            lambda: self.parent().oldSubtitles.sortItems())

    def createWidget(self, hint):
        tmpDict = {}
        tmpName = f'{hint}Widget'
        tmpWidget = QWidget()
        tmpWidget.setObjectName(f"{self.appId}.{tmpName}")
        tmpLayout = QFormLayout(tmpWidget)
        #
        tmpLineEdit = QLineEdit(tmpWidget)
        tmpLayout.setWidget(2, QFormLayout.FieldRole, tmpLineEdit)
        tmpDict['inputBox'] = tmpLineEdit
        #
        buttons = ['save', 'clear', 'filter', 'sort']
        i = 3
        for button in buttons:
            tmpButton = QPushButton(tmpWidget)
            tmpButton.setObjectName(f"{self.appId}.{tmpName}.{button}")
            tmpLayout.setWidget(i, QFormLayout.FieldRole, tmpButton)
            tmpDict[button] = tmpButton
            i += 1
        #
        tmpLabel = QLabel(tmpWidget)
        tmpLabel.setObjectName(f"{self.appId}.{tmpName}.label")
        tmpLayout.setWidget(2, QFormLayout.LabelRole, tmpLabel)
        tmpDict['label'] = tmpLabel
        #
        setattr(self, tmpName, tmpWidget)
        setattr(self, tmpName + 'Cpnt', tmpDict)
        return tmpWidget

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self.dialog())
        self.mainLayout.setObjectName(f'{self.appId}.mainLayout')
        for hint in self.hints:
            self.mainLayout.addWidget(self.createWidget(hint))

    def retranslateUi(self):
        self.dialog().setWindowTitle(QCoreApplication.translate(
            self.appId,
            "Miscellanies",
            None))
        for widget in self.hints:
            tmpDict = getattr(self, f'{widget}WidgetCpnt')
            # save the filter
            tmpDict['save'].setText(QCoreApplication.translate(
                self.appId,
                "Save the Filter",
                None))
            # clear the filter
            tmpDict['clear'].setText(QCoreApplication.translate(
                self.appId,
                "Clear the Filter",
                None))
            # trigger filter
            tmpDict['filter'].setText(QCoreApplication.translate(
                self.appId,
                f"Filter Existing {widget}",
                None))
            # sort the list
            tmpDict['sort'].setText(QCoreApplication.translate(
                self.appId,
                f"Sort {widget}",
                None))
            # translate label
            tmpDict['label'].setText("{0:22}".format(
                QCoreApplication.translate(
                    self.appId,
                    f"Filter for {widget}",
                    None) + ":"))
