#!/usr/bin/python
# -*- coding:utf-8 -*-


import weakref
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pathlib import Path
from .NUtils import removeNonTargetFiles


class NQListWidget(QListWidget):

    def __init__(self, parent, *args, hint='video', **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.parent = weakref.ref(parent)
        # accept manually reorder items
        self.setDragDropMode(self.InternalMove)
        self.setSelectionMode(self.ExtendedSelection)
        self.hint = hint
        # mapping displayed data and real data
        self.realData = {}
        self.addedItems = set()

    def addItem(self, item):
        self.parent().setIsPrepared(False)
        if item not in self.addedItems:
            super().addItem(item)
            self.addedItems.add(item)

    def addItems(self, items):
        list(map(self.addItem, items))

    def applyItemFilter(self):
        pass

    def clear(self):
        self.parent().setIsPrepared(False)
        self.realData = {}
        self.addedItems = set()
        super().clear()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if not url.isLocalFile():
                    return
            event.accept()
        elif event.source() == self:
            # trigger internalMove mode in dropEvent()
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.source() == self:
            # set action to move explictly
            event.setDropAction(Qt.MoveAction)
            super().dropEvent(event)
        else:
            # clear items
            self.clear()
            # get list of file and strings to-be-displayed
            urls = event.mimeData().urls()
            fileList = [Path(_.toLocalFile()) for _ in urls]
            fileList = removeNonTargetFiles(fileList, hint=self.hint)
            fileKeys = [_.name for _ in fileList]
            # update dict
            self.realData.update(dict(zip(fileKeys, fileList)))
            # add keys to items
            self.addItems(fileKeys)
            #
            self.sortItems()

    # delete selected items while pressing 'delete'
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delSelectedItem()

    def delSelectedItem(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def setItemFilter(self, itemFilter):
        pass

    # override sortItems()
    def sortItems(self):
        self.parent().setIsPrepared(False)
        super().sortItems()
