from PyQt5.QtCore import pyqtSignal, Qt, QDate, QMutex
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QHeaderView, QMenu,
                             QActionGroup, QAction, QMessageBox)
import parametros as p
from Frontend import PopUps as Pops
from datetime import datetime
from re import sub

window_name, base_class = uic.loadUiType(p.RUTA_UI_PAGO_DIARIO)

def format(num):
        num = f"{int(num):,}"
        return num.replace(",", ".")

def remdot(str):
    return str.replace(".","")

class VentanaPagoDiario(window_name,base_class):
    senal_volver = pyqtSignal()
    senal_pedir_pagos = pyqtSignal(str)
    senal_actualizar_pago = pyqtSignal(list)
     

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.boton_volver.clicked.connect(self.volver)
        #self.boton_buscar.clicked.connect(self.pedir_pagos)
       
        self.chicas = []
        self.datos_cargados = False
        self.fecha.setDate(QDate.currentDate())
        self.init_tabla()
        self.fecha.dateChanged.connect(self.pedir_pagos)

    def start(self):
        self.pedir_pagos()

    def init_tabla(self):
        self.tabla.setDragDropOverwriteMode(False)
        self.tabla.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.tabla.setTextElideMode(Qt.ElideRight)
        self.tabla.setWordWrap(False)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.verticalHeader().setDefaultSectionSize(20)
        self.tabla.itemChanged.connect(self.actualizar_pago)
        self.tabla.setColumnWidth(7,600)
        self.chicas = []
        self.pedir_pagos()
        
    def actualizar_pago(self, item):
        if self.datos_cargados == False: return
        fila = item.row()
        cid = self.tabla.item(fila, 0).text()
        fecha = self.fecha.date().toString("yyyy-MM-dd")
        sueldo = remdot(self.tabla.item(fila, 2).text())
        bonus = remdot(self.tabla.item(fila, 3).text())
        fichas = remdot(self.tabla.item(fila, 4).text())
        extras = remdot(self.tabla.item(fila, 5).text())
        self.senal_actualizar_pago.emit([cid, fecha, sueldo, bonus, fichas, extras])
        self.pedir_pagos()



    def volver(self):
        self.hide()
        self.senal_volver.emit()

    def pedir_pagos(self):
        fecha = self.fecha.date().toString("yyyy-MM-dd")
        self.senal_pedir_pagos.emit(fecha)

    def cargar_datos(self, pagos):
        self.datos_cargados = False
        self.tabla.setRowCount(len(pagos))
        fila = 0
        
        for chica in pagos:
            cid = QtWidgets.QTableWidgetItem(str(chica[0]))
            cid.setFlags(Qt.ItemIsEnabled)
            nombre = QtWidgets.QTableWidgetItem(str(chica[1]))
            nombre.setFlags(Qt.ItemIsEnabled)
            total = QtWidgets.QTableWidgetItem(format(str(chica[2]+ chica[3]+ chica[4] + chica[5])))
            total.setFlags(Qt.ItemIsEnabled)
            sueldo = QtWidgets.QTableWidgetItem(format(chica[2]))
            sueldo.setFlags(Qt.ItemIsEnabled)
            bonus = QtWidgets.QTableWidgetItem(format(chica[3]))
            bonus.setFlags(Qt.ItemIsEnabled)
            self.tabla.setItem(fila,0,cid)#Fila,Columna,String
            self.tabla.setItem(fila,1,nombre)
            self.tabla.setItem(fila,2,sueldo)
            self.tabla.setItem(fila,3,QtWidgets.QTableWidgetItem(bonus))

            self.tabla.setItem(fila,4,QtWidgets.QTableWidgetItem(format(chica[4])))

            self.tabla.setItem(fila,5,QtWidgets.QTableWidgetItem(format(chica[5])))
            self.tabla.setItem(fila,6,total)
            info = QtWidgets.QTableWidgetItem(chica[6])
            info.setFlags(Qt.ItemIsEnabled)
            self.tabla.setItem(fila,7,info)

            fila += 1
        self.datos_cargados = True

    def set_chicas(self, chicas):
        self.chicas = chicas
if __name__ == "__main__":
    app = QApplication([])
    PagoDiario = VentanaPagoDiario()
    PagoDiario.show()
    app.exec()