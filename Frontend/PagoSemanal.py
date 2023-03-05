from PyQt5.QtCore import pyqtSignal, Qt, QDate
from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5 import QtCore
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QHeaderView, QMenu,
                             QActionGroup, QAction, QMessageBox, QDateEdit, QCalendarWidget)

import parametros as p                             
from Frontend.Calendar import CalenderX
from datetime import datetime

window_name, base_class = uic.loadUiType(p.RUTA_UI_PAGO_SEMANAL)

def format(num):
        num = f"{int(str(num)):,}"
        return num.replace(",", ".")
        
class VentanaPagoSemanal(window_name, base_class):
    senal_volver = pyqtSignal()
    senal_pedir_pagos = pyqtSignal(str,str)

    def __init__(self):
        super().__init__()
        self.init_ui()

        today = QDate.currentDate()
        monday = today.addDays(-(today.dayOfWeek()-1))
        self.fecha_inicio.setDate(monday)
        end = monday.addDays(5)
        self.fecha_fin.setDate(end)
        #self.boton_volver.clicked.connect(self.volver)
    def start(self):
        self.pedir_pagos()
        
    def rellenar(self):
        for i in range(self.tabla.rowCount()):
            for j in range(self.tabla.columnCount()):
                item = QTableWidgetItem("0")
                self.tabla.setItem(i, j, item)

        
    def formatear(self):
        for i in range(self.tabla.rowCount()):
            
            l = int(self.tabla.item(i, 1).text())
            ma = int(self.tabla.item(i, 2).text())
            mi = int(self.tabla.item(i, 3).text())
            ju = int(self.tabla.item(i, 4).text())
            vi = int(self.tabla.item(i, 5).text())
            sa = int(self.tabla.item(i, 6).text())
            self.tabla.setItem(i, 7, QtWidgets.QTableWidgetItem(format(l + ma + mi + ju + vi + sa))) 
            self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(format(l)))
            self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(format(ma)))
            self.tabla.setItem(i, 3, QtWidgets.QTableWidgetItem(format(mi)))
            self.tabla.setItem(i, 4, QtWidgets.QTableWidgetItem(format(ju)))
            self.tabla.setItem(i, 5, QtWidgets.QTableWidgetItem(format(vi)))
            self.tabla.setItem(i, 6, QtWidgets.QTableWidgetItem(format(sa)))
            


    def actualizar_fecha(self):
        today = self.fecha_inicio.date()
        monday = today.addDays(-(today.dayOfWeek()-1))
        fin = monday.addDays(5)
        self.fecha_inicio.setDate(monday)
        self.fecha_fin.setDate(fin)
        self.pedir_pagos()

    def pedir_pagos(self):
        fecha1 = self.fecha_inicio.date().toString("yyyy-MM-dd")
        fecha2 = self.fecha_fin.date().toString("yyyy-MM-dd")
        self.senal_pedir_pagos.emit(fecha1,fecha2)

    def cargar_datos(self,dicto):
        self.tabla.setRowCount(len(dicto))
        self.rellenar()

        today = self.fecha_inicio.date()
        monday = today.toString("yyyy-MM-dd")
        tuesday = today.addDays(1).toString("yyyy-MM-dd")
        wednesday = today.addDays(2).toString("yyyy-MM-dd")
        thursday = today.addDays(3).toString("yyyy-MM-dd")
        friday = today.addDays(4).toString("yyyy-MM-dd")
        saturday = today.addDays(5).toString("yyyy-MM-dd")
        dias = {monday:1,tuesday:2,wednesday:3,thursday:4,friday:5,saturday:6}
        
        fila = 0
        for id in dicto: #Defineuna fila (persona)
            #total_semana = 0
            chica = dicto[id]
            columna_nombre = 0
            self.tabla.setItem(fila ,columna_nombre,QtWidgets.QTableWidgetItem(str(chica[0][0])))
            for a in range(len(chica)): #Define las columnas
                total_dia = int(chica[a][2]) + int(chica[a][3]) + int(chica[a][4]) + int(chica[a][5])
                #total_semana += total_dia
                self.tabla.setItem(fila,dias[chica[a][1]],QtWidgets.QTableWidgetItem(str(total_dia)))
            fila +=1
            


        self.formatear()
           
    def init_ui(self):
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
        self.fecha_inicio.dateChanged.connect(self.actualizar_fecha)
        self.pedir_pagos()
        #self.boton_buscar.clicked.connect(self.pedir_pagos)

    def volver(self):
        self.senal_volver.emit()
        self.hide()
