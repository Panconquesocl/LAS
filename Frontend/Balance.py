from PyQt5.QtCore import pyqtSignal, Qt, QDate
from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5 import QtCore
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QHeaderView, QMenu,
                             QActionGroup, QAction, QMessageBox, QDateEdit, QCalendarWidget)

import parametros as p                             
from Frontend.Calendar import CalenderX

window_name, base_class = uic.loadUiType(p.RUTA_UI_BALANCE)

class VentanaBalance(window_name, base_class):
    senal_volver = pyqtSignal()

    def __init__(self):
        self.fecha_inicio = None
        self.fecha_fin = None
        super().__init__()
        self.setupUi(self)
        self.tabla.setDragDropOverwriteMode(False)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.tabla.setTextElideMode(Qt.ElideRight)
        self.tabla.setWordWrap(False)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.verticalHeader().setDefaultSectionSize(20)

        today = QDate.currentDate()
        monday = today.addDays(-(today.dayOfWeek()-1))
        self.fecha.setDate(monday)
        end = monday.addDays(5)
        self.fecha_2.setDate(end)
        self.fecha_inicio= monday
        self.fecha_fin = end
        calendar = CalenderX()
        self.fecha.setCalendarPopup(True)
        self.fecha.setCalendarWidget(calendar)
        self.boton_volver.clicked.connect(self.volver)

    def volver(self):
        self.senal_volver.emit()
        self.hide()

    def mostrar(self):
        self.show()