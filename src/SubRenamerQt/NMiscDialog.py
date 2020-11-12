#!/usr/bin/python
# -*- coding:utf-8 -*-

import weakref
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class NMiscDialog(object):
    appId = "MiscDialog"
    def __init__(self, parent, dialog, name='MiscDialog'):
        self.dialog = weakref.ref(dialog)
        self.parent = weakref.ref(parent)
        dialog.setObjectName(name)
        dialog.resize(400, 300)
        #
        self.setupUi()
        self.retranslateUi()
        QMetaObject.connectSlotsByName(dialog)

    def createWidget(self, hint):
        tmpDict = {}
        tmpName = f'{hint}Widget'
        tmpWidget = QWidget()
        tmpWidget.setObjectName(f"{self.appId}.{tmpName}")
        tmpLayout = QFormLayout(tmpWidget)
        #
        tmpLineEdit = QLineEdit(tmpWidget)
        tmpLayout.setWidget(2, QFormLayout.FieldRole, tmpLineEdit)
        tmpDict['InputBox'] = tmpLineEdit
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
        self.mainLayout.addWidget(self.createWidget('Videos'))
        self.mainLayout.addWidget(self.createWidget('Subtitles'))


    def retranslateUi(self):
        self.dialog().setWindowTitle(QCoreApplication.translate(
            self.appId,
            "Miscellanies",
            None))
        for widget in ['Videos', 'Subtitles']:
            tmpDict = getattr(self, f'{widget}WidgetCpnt')
            tmpDict['save'].setText(QCoreApplication.translate(
                self.appId,
                "Save the Filter",
                None))
            tmpDict['clear'].setText(QCoreApplication.translate(
                self.appId,
                "Clear the Filter",
                None))
            tmpDict['filter'].setText(QCoreApplication.translate(
                self.appId,
                "Filter Existing {widget}",
                None))
            tmpDict['sort'].setText(QCoreApplication.translate(
                self.appId,
                f"Sort {widget}",
                None))
            tmpDict['label'].setText("{0:22}".format(
                QCoreApplication.translate(
                    self.appId,
                    f"Filter for {widget}",
                    None) + ":"))
