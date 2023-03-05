from PyQt5.QtCore import pyqtSignal, Qt, QDate, QTime, QPoint
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QHeaderView, QMenu,
                             QActionGroup, QAction, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
import parametros as p
from Frontend import PopUps as Pops
from datetime import datetime

window_name, base_class = uic.loadUiType(p.RUTA_UI_ASISTENCIA)

class VentanaAsistencia(window_name,base_class):
    senal_cambiar_nombre_chica = pyqtSignal(int, str)
    senal_pedir_chicas = pyqtSignal()
    senal_volver = pyqtSignal()
    senal_buscar = pyqtSignal(str)
    senal_enviar_asistencia = pyqtSignal(list)
    senal_borrar_asistencia = pyqtSignal(list)
    senal_actualizar = pyqtSignal(list)
    senal_agregar_chica = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.chicas = []
        self.setupUi(self)
        self.init_ui()
        self.datos_cargados = False
        #self.boton_volver.clicked.connect(self.volver)
        #self.boton_buscar.clicked.connect(self.buscar)
        self.boton_agregar_asistencia.clicked.connect(self.popup)
        self.boton_borrar.clicked.connect(self.borrar_fila)
        self.pop = Pops.PopUpAsistencia(self)
        self.pop.senal_enviar_asistencia.connect(self.enviar_asistencia)
        self.fecha.dateChanged.connect(self.buscar)
        self.tabla.itemChanged.connect(self.update)
        #self.boton_agregar_chicas.clicked.connect(.)"""rellenar"""
    def start(self):
        self.buscar()
    def update(self, item):
        if self.datos_cargados:
            self.datos_cargados = False
            fila = item.row()
            #print(item)
            cid = self.tabla.item(fila, 0).text()
            fecha = self.tabla.item(fila, 2).text()
            asistencia= self.tabla.item(fila, 3).text()
            hora = self.tabla.item(fila, 4).text()
            dt = datetime.strptime(fecha,"%d-%m-%Y")
            fecha = dt.strftime("%Y-%m-%d")
            self.senal_actualizar.emit([cid,fecha,asistencia,hora]) 
            self.buscar()
            self.datos_cargados = True

    def init_ui(self):
        self.tabla.setDragDropOverwriteMode(False)
        self.tabla.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.tabla.setTextElideMode(Qt.ElideRight)
        self.tabla.setWordWrap(False)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.verticalHeader().setDefaultSectionSize(20)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.itemClicked.connect(self.click_row)
        self.senal_pedir_chicas.emit()
        self.fecha.setDate(QDate.currentDate())
        self.buscar()
        print(self.chicas)

    def switch(self,a):
        self.save.setEnabled(True)
        print(a)

    def borrar_fila(self):
        self.datos_cargados = False
        selected = self.tabla.selectedItems()
        selected_row = []
        row = selected[0].row()
        for i in range(self.tabla.columnCount()):
            selected_row.append(self.tabla.item(row, i).text())
        print("Selected Row:", selected_row)
        dt = datetime.strptime(selected_row[2],"%d-%m-%Y")
        fecha = dt.strftime("%Y-%m-%d")
        selected_row[2] = fecha
        print(selected_row)
        self.tabla.clearSelection()
        self.boton_borrar.setEnabled(False)
        self.senal_borrar_asistencia.emit(selected_row)
        self.buscar()
        
    def click_row(self):
        self.boton_borrar.setEnabled(True)

    def pop_result(self,codigo, descripcion):
        self.pop.result(codigo, descripcion)

    def volver(self):
        self.hide()
        self.senal_volver.emit()
    
    def center(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        center_point = QPoint(screen_geometry.center().x() - self.width()/2,
                      screen_geometry.center().y() - self.height()/2)
        self.move(center_point)
        

    def buscar(self):
        fecha = self.fecha.date().toString("yyyy-MM-dd")
        self.senal_buscar.emit(fecha)

    def enviar_asistencia(self, asistencia):
        self.senal_enviar_asistencia.emit(asistencia)

    def popup(self):
        self.pop = Pops.PopUpAsistencia(self)
        self.pop.senal_enviar_asistencia.connect(self.enviar_asistencia)
        self.pop.cargar_nombres(self.chicas)
        self.pop.senal_cambiar_nombre_chica.connect(self.cambiar_nombre_chica)
        result = self.pop.exec_()
        self.buscar()

    def set_chicas(self, chicas):
        self.chicas = chicas

    def cargar_datos(self, chicas):
        self.datos_cargados = False
        self.tabla.setRowCount(len(chicas))
        fila = 0
        for chica in chicas:#Fila,Columna,String
            cid = QtWidgets.QTableWidgetItem(str(chica[0]))
            cid.setFlags(Qt.ItemIsEditable)
            nombre = QtWidgets.QTableWidgetItem(str(chica[1]))
            nombre.setFlags(Qt.ItemIsEnabled)
            dt = datetime.strptime(chica[2],"%Y-%m-%d")
            fecha = dt.strftime("%d-%m-%Y")
            fecha = QtWidgets.QTableWidgetItem(fecha)
            fecha.setFlags(Qt.ItemIsEnabled)
            self.tabla.setItem(fila,0,QtWidgets.QTableWidgetItem(cid))#Id
            self.tabla.setItem(fila,1,QtWidgets.QTableWidgetItem(nombre))#Nombre
            self.tabla.setItem(fila,2,QtWidgets.QTableWidgetItem(fecha))#Nombre
            self.tabla.setItem(fila,3,QtWidgets.QTableWidgetItem(str(chica[3])))#Nombre
            self.tabla.setItem(fila,4,QtWidgets.QTableWidgetItem(str(chica[4])))#Nombre
            fila += 1
        self.datos_cargados = True
        
    def cambiar_nombre_chica(self, id, nombre):
        self.senal_cambiar_nombre_chica.emit(id, nombre)


if __name__ == "__main__":
    app = QApplication([])
    PagoDiario = VentanaAsistencia()
    PagoDiario.show()
    app.exec()