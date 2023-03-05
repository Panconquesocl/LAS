from PyQt5.QtCore import pyqtSignal, Qt, QDate, QTime
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QHeaderView, QMenu,
                             QActionGroup, QAction, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
import parametros as p
asistencia_window_name, asistencia_base_class = uic.loadUiType(p.RUTA_UI_POPUP_ASISTENCIA)


class PopUpAsistencia(asistencia_window_name, asistencia_base_class):
    senal_enviar_asistencia = pyqtSignal(list)
    senal_cambiar_nombre_chica = pyqtSignal(int, str)

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.setupUi(self)
        self.time_edit.setTime(QTime.currentTime())
        self.autofill_hora = False
        self.check_hora.stateChanged.connect(self.checkbox_changed_hora)
        self.boton_cerrar.clicked.connect(self.cerrar)
        self.init_tables()
        self.boton_agregar_chicas.clicked.connect(self.agregar_chica)
        self.tabla_nombres.itemChanged.connect(self.editar)
        self.editable = False
        self.parent.senal_pedir_chicas.emit()
        self.cargar_nombres(self.parent.chicas)

    def editar(self, item):
        if self.editable == False: return
        fila = item.row()
        nombre = item.text()
        id = self.tabla_nombres.item(fila,0).text()
        self.senal_cambiar_nombre_chica.emit(int(id), nombre)
        self.cargar_nombres(self.parent.chicas)

    def init_tables(self):
        self.tabla_nombres.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.tabla_nombres.setTextElideMode(Qt.ElideRight)
        self.tabla_nombres.setWordWrap(False)
        self.tabla_nombres.horizontalHeader().setStretchLastSection(True)
        self.tabla_nombres.verticalHeader().setVisible(False)
        self.tabla_nombres.setAlternatingRowColors(True)
        self.tabla_nombres.verticalHeader().setDefaultSectionSize(20)
        self.boton_agregar_asistencia.clicked.connect(self.agregar_asistencia)
        
    def agregar_chica(self):
        rowPosition = self.tabla_nombres.rowCount()
        self.tabla_nombres.insertRow(rowPosition)
        self.parent.senal_agregar_chica.emit()
        self.cargar_nombres(self.parent.chicas)
        
    def checkbox_changed_hora(self, state):
        if state == Qt.Checked:
            self.autofill_hora = True
            self.time_edit.setEnabled(True)
        else:
            self.time_edit.setEnabled(False)
            self.autofill_hora = False
    
    def agregar_asistencia(self):
        if self.tabla_nombres.currentItem() == None: 
            self.error_seleccion()
            return 
        fila = self.tabla_nombres.currentItem().row()
        cid = int(self.tabla_nombres.item(fila,0).text())
        print(id)

        #self.add_row()
        #row = index.row()
        #item = self.tabla_nombres.item(row, column)
        #cid = self.tabla_nombres.item(row, 0).text()
        fecha = self.parent.fecha.date().toString("yyyy-MM-dd")
        asistencia = "Si"
        hora = ""
        if self.autofill_hora: hora = self.time_edit.time().toString("hh:mm")
        if hora == "": asistencia = "No"
        self.senal_enviar_asistencia.emit([cid,fecha, asistencia, hora])
        self.parent.buscar()
            

    def cerrar(self):
        self.close()

    def cargar_nombres(self, chicas):
        self.editable = False
        self.tabla_nombres.setRowCount(len(chicas))
        fila = 0
        for chica in chicas:#Fila,Columna,String
            cid = QtWidgets.QTableWidgetItem(str(chica[0]))
            cid.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabla_nombres.setItem(fila,0,cid)#Id
            nombre = QtWidgets.QTableWidgetItem(str(chica[1]))
            nombre.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            #nombre.setFlags(nombre.flags() & Qt.ItemIsSelectable)

            self.tabla_nombres.setItem(fila,1,nombre)#Nombre

            
            #self.tabla_nombres.setItem(fila,2,QtWidgets.QTableWidgetItem("Si"))#Nombre
            fila += 1
        self.editable = True

    def result(self, code, descripcion):
        if code == "Already exists": 
            pop = QMessageBox()
            pop.setWindowTitle("Error")
            pop.setText(p.ALREADY_EXIST + descripcion)
            pop.setIcon(QMessageBox.Warning)
            popup = pop.exec_()

    def error_seleccion(self):
        pop = QMessageBox()
        pop.setWindowTitle("Error")
        pop.setText("Selecciona una chica para agregar a la asistencia")
        pop.setIcon(QMessageBox.Warning)
        popup = pop.exec_()


class PopUpPagos(asistencia_window_name, asistencia_base_class):
    senal_enviar_asistencia = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.date_edit.setDate(QDate.currentDate())
        self.time_edit.setTime(QTime.currentTime())
        self.autofill_fecha = False
        self.autofill_hora = False
        self.check_hora.stateChanged.connect(self.checkbox_changed_hora)
        self.check_fecha.stateChanged.connect(self.checkbox_changed_fecha)
        self.boton_cerrar.clicked.connect(self.cerrar)
        self.boton_guardar.clicked.connect(self.enviar_asistencia)
        self.init_tables()

    def init_tables(self):
        self.tabla_nombres.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.tabla_nombres.setTextElideMode(Qt.ElideRight)
        self.tabla_nombres.setWordWrap(False)
        self.tabla_nombres.horizontalHeader().setStretchLastSection(True)
        self.tabla_nombres.verticalHeader().setVisible(False)
        self.tabla_nombres.setAlternatingRowColors(True)
        self.tabla_nombres.verticalHeader().setDefaultSectionSize(20)
        self.tabla_nombres.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_nombres.doubleClicked.connect(self.on_double_click)
        self.tabla.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.tabla.setTextElideMode(Qt.ElideRight)
        self.tabla.setWordWrap(False)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.verticalHeader().setDefaultSectionSize(20)

    def add_row(self):
        rowPosition = self.tabla.rowCount()
        self.tabla.insertRow(rowPosition)

    def checkbox_changed_hora(self, state):
        if state == Qt.Checked:
            self.autofill_hora = True
            self.time_edit.setEnabled(True)
        else:
            self.time_edit.setEnabled(False)
            self.autofill_hora = False

    def checkbox_changed_fecha(self, state):
        if state == Qt.Checked:
            self.autofill_fecha = True
            self.date_edit.setEnabled(True)
        else:
            self.autofill_fecha = False
            self.date_edit.setEnabled(False)
    
    def on_double_click(self,index):
        self.add_row()
        row = index.row()
        values = []
        for column in range(self.tabla_nombres.columnCount()):
            item = self.tabla_nombres.item(row, column)
            if item:
                values.append(item.text())
            else:
                values.append("")
        cid = QtWidgets.QTableWidgetItem(str(values[0]))
        cid.setFlags(Qt.ItemIsEnabled)
        nombre = QtWidgets.QTableWidgetItem(str(values[1]))
        nombre.setFlags(Qt.ItemIsEnabled)
        self.tabla.setItem(self.tabla.rowCount()-1,0,cid)#Id
        self.tabla.setItem(self.tabla.rowCount()-1,1,nombre)#Nombre
        if self.autofill_fecha: self.tabla.setItem(self.tabla.rowCount()-1,2,QtWidgets.QTableWidgetItem(self.date_edit.date().toString("dd-MM-yyyy")))#Fecha
        if self.autofill_hora: self.tabla.setItem(self.tabla.rowCount()-1,4,QtWidgets.QTableWidgetItem(self.time_edit.time().toString("hh:mm")))#Hora

    def cerrar(self):
        self.close()

    def enviar_asistencia(self):
        filas = self.get_rows()
        if filas:
            for chica in filas:
                chica.pop(1)
            self.senal_enviar_asistencia.emit(filas)
        else:
            texto = """Deben estar todas las casillas llenas para agregar la asistencia"""
            pop = QMessageBox()
            pop.setWindowTitle("Error")
            pop.setText(texto)
            pop.setIcon(QMessageBox.Critical)
            popup = pop.exec_()

    def cargar_nombres(self, chicas):
        self.tabla_nombres.setRowCount(len(chicas))
        fila = 0
        for chica in chicas:#Fila,Columna,String
            self.tabla_nombres.setItem(fila,0,QtWidgets.QTableWidgetItem(str(chica[0])))#Id
            self.tabla_nombres.setItem(fila,1,QtWidgets.QTableWidgetItem(str(chica[1])))#Nombre
            fila += 1

    def result(self, code, descripcion):
        if code == "Already exists": 
            pop = QMessageBox()
            pop.setWindowTitle("Error")
            pop.setText(p.ALREADY_EXIST + descripcion)
            pop.setIcon(QMessageBox.Warning)
            popup = pop.exec_()
        elif code == "Succeded":
            pop = QMessageBox()
            pop.setWindowTitle("Datos Guardados!")
            pop.setText("Los datos han sido guardados con exito!")
            pop.setIconPixmap(QPixmap(p.RUTA_ICONO_VERDE))
            pop.setWindowIcon(QIcon(p.RUTA_ICONO_VERDE))
            popup = pop.exec_()
            self.tabla.setRowCount(0)

    def get_rows(self):
        rows = []
        for i in range(self.tabla.rowCount()):
            row = []
            for j in range(self.tabla.columnCount()):
                item = self.tabla.item(i, j)
                if item is not None:
                    row.append(item.text())
                else:
                    return False
            rows.append(row)
        return rows
